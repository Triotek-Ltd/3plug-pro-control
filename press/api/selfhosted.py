import json
import socket
import time
from contextlib import suppress
from urllib.parse import urlparse

import frappe
from dns.resolver import Resolver
from frappe.query_builder.functions import Count
from frappe.utils import cint
from frappe.utils import get_url
from frappe.utils import strip

from press.api.server import plans
from press.runner import Ansible
from press.utils import get_current_team
from press.utils.dns import NAMESERVERS


@frappe.whitelist()
def new(server):
	server_details = frappe._dict(server)

	team = get_current_team(get_doc=True)
	validate_team(team)

	proxy_server = get_proxy_server_for_cluster()

	return create_self_hosted_server(server_details, team, proxy_server)


def create_self_hosted_server(server_details, team, proxy_server):
	server_url = strip(server_details.get("server_url", ""))
	onboarding_email = strip(server_details.get("onboarding_email", ""))
	managed_domains = _normalize_managed_domains(server_details.get("managed_domains"))
	app_public_ip = _resolve_public_ip(
		server_details.get("app_public_ip", "") or server_details.get("server_public_ip", ""),
		server_url=server_url,
		managed_domains=managed_domains,
	)
	app_private_ip = strip(
		server_details.get("app_private_ip", "") or server_details.get("server_private_ip", "")
	)
	db_public_ip = strip(server_details.get("db_public_ip", "") or app_public_ip)
	db_private_ip = strip(server_details.get("db_private_ip", "") or app_private_ip)
	ssh_user = strip(server_details.get("ssh_user", "") or "root")
	ssh_port = cint(server_details.get("ssh_port") or 22)

	try:
		self_hosted_server = frappe.new_doc(
			"Self Hosted Server",
			**{
				"ip": app_public_ip,
				"private_ip": app_private_ip,
				"mariadb_ip": db_public_ip,
				"mariadb_private_ip": db_private_ip,
				"title": server_details.title,
				"proxy_server": proxy_server,
				"proxy_created": True,
				# Keep the legacy split-runtime model underneath for now so setup,
				# jobs, and bench onboarding continue to work while the product UX
				# is narrowed to a single managed Linux server.
				"different_database_server": True,
				"team": team.name,
				"plan": server_details.plan["name"],
				"database_plan": server_details.plan["name"],
				"new_server": True,
				"ssh_user": ssh_user,
				"ssh_port": ssh_port,
				"server_url": server_url,
				"onboarding_email": onboarding_email,
				"managed_domains": managed_domains,
			},
		).insert()
	except frappe.DuplicateEntryError as e:
		# Exception return  tupple like ('Self Hosted Server', 'SHS-00018.cloud.pressonprem.com')
		return e.args[1]

	return self_hosted_server.name


def validate_team(team):
	if not team:
		frappe.throw("You must be part of a team to create a new server")

	if not team.enabled:
		frappe.throw("You cannot create a new server because your account is disabled")

	if not team.self_hosted_servers_enabled:
		frappe.throw(
			"You cannot create a new server because Hybrid Cloud is disabled for your account. Please contact support to enable it."
		)


def get_proxy_server_for_cluster(cluster=None):
	cluster = cluster if cluster else get_hybrid_cluster()

	return frappe.get_all("Proxy Server", {"cluster": cluster}, pluck="name")[0]


def get_hybrid_cluster():
	return frappe.db.get_value("Cluster", {"hybrid": 1}, "name")


@frappe.whitelist()
def sshkey():
	return frappe.db.get_value("SSH Key", {"enabled": 1, "default": 1}, "public_key")


@frappe.whitelist()
def verify(server):
	server_doc = frappe.get_doc("Self Hosted Server", server)

	app_server_verified = verify_server("app", server_doc)
	db_server_verified = verify_server("db", server_doc)

	if app_server_verified and db_server_verified:
		server_doc.check_minimum_specs()

		server_doc.status = "Pending"
		server_doc.save()

		server_doc.reload()
		server_doc.create_database_server()

		server_doc.reload()
		server_doc.create_application_server()
		return True

	return False


def verify_server(server_type, server_doc):
	ping = Ansible(
		playbook="ping.yml",
		server=frappe._dict(
			{
				"doctype": "Self Hosted Server",
				"name": server_doc.name,
				"ssh_user": server_doc.ssh_user,
				"ssh_port": server_doc.ssh_port,
				"ip": server_doc.ip if server_type == "app" else server_doc.mariadb_ip,
			}
		),
	)
	result = ping.run()

	if result.status == "Success":
		server_doc.validate_private_ip(result.name, server_type=server_type)

		server_doc.fetch_system_specifications(result.name, server_type=server_type)
		server_doc.reload()

		return True

	return False


@frappe.whitelist()
def setup(server):
	server_doc = frappe.get_doc("Self Hosted Server", server)
	server_doc.start_setup = True
	server_doc.save()
	server_doc.setup_server()
	time.sleep(1)


@frappe.whitelist()
def get_plans():
	return plans("Self Hosted Server")


@frappe.whitelist()
def check_dns(domain, ip):
	try:
		resolver = Resolver(configure=False)
		resolver.nameservers = NAMESERVERS
		domain_ip = resolver.query(domain.strip(), "A")[0].to_text()
		if domain_ip == ip:
			return True
	except Exception:
		return False
	return False


@frappe.whitelist()
def options_for_new():
	return {
		"plans": get_plans(),
		"ssh_key": sshkey(),
		"default_ssh_user": "root",
		"default_ssh_port": 22,
	}


def _resolve_public_ip(explicit_ip, server_url: str, managed_domains: str):
	explicit_ip = strip(explicit_ip or "")
	if explicit_ip:
		return explicit_ip

	for host in _candidate_hosts(server_url, managed_domains):
		try:
			_, _, addresses = socket.gethostbyname_ex(host)
		except OSError:
			continue

		for address in addresses:
			address = strip(address or "")
			if address and not address.startswith("127."):
				return address

	frappe.throw(
		"3plug could not determine the server public IP from the primary domain. "
		"Point the domain to the server first, then start onboarding again."
	)


def _candidate_hosts(server_url: str, managed_domains: str):
	hosts = []
	for value in [server_url, *(managed_domains.splitlines() if managed_domains else [])]:
		host = _normalize_host(value)
		if host and host not in hosts:
			hosts.append(host)

	with suppress(Exception):
		current_host = _normalize_host(urlparse(get_url()).hostname or get_url())
		if current_host and current_host not in hosts:
			hosts.append(current_host)

	return hosts


def _normalize_host(value):
	raw_value = strip(value or "")
	if not raw_value:
		return ""

	parsed = urlparse(raw_value if "://" in raw_value else f"https://{raw_value}")
	return strip(parsed.hostname or raw_value).strip("/")


@frappe.whitelist()
def create_and_verify_selfhosted(server):
	self_hosted_server_name = new(server)
	self_hosted_server = frappe.get_doc("Self Hosted Server", self_hosted_server_name)
	self_hosted_server.start_onboarding()
	return {
		"self_hosted_server": self_hosted_server_name,
		"onboarding_stage": self_hosted_server.onboarding_stage,
	}


def _get_self_hosted_server(self_hosted_server: str | None = None, server: str | None = None):
	if self_hosted_server:
		return frappe.get_doc("Self Hosted Server", self_hosted_server)
	if server:
		return _get_self_hosted_server_for_managed_server(server)
	frappe.throw("A self-hosted server reference is required")


def _get_self_hosted_server_for_managed_server(server: str):
	frappe.get_doc("Server", server)
	self_hosted_server_name = frappe.db.get_value("Self Hosted Server", {"server": server}, "name")
	if not self_hosted_server_name:
		frappe.throw("No linked self-hosted server record was found for this managed server")
	return frappe.get_doc("Self Hosted Server", self_hosted_server_name)


def _serialize_self_hosted_bench_state(self_hosted_server):
	play_servers = [value for value in [self_hosted_server.name, self_hosted_server.server] if value]
	recent_plays = frappe.get_all(
		"Ansible Play",
		filters={"server": ("in", play_servers)},
		fields=["name", "play", "status", "creation", "server"],
		order_by="creation desc",
		limit=8,
	)
	bench_names = []
	if self_hosted_server.release_group:
		bench_names = frappe.get_all(
			"Bench",
			{"group": self_hosted_server.release_group},
			pluck="name",
			limit=10,
		)
	site_docnames = [row.site for row in self_hosted_server.sites or [] if row.site]
	recent_jobs = _get_recent_onboarding_jobs(
		server=self_hosted_server.server,
		bench_names=bench_names,
		site_names=site_docnames,
	)
	job_scope_summary = _get_onboarding_job_scope_summary(
		server=self_hosted_server.server,
		bench_names=bench_names,
		site_names=site_docnames,
	)
	operation_status = _get_onboarding_operation_status(
		self_hosted_server=self_hosted_server,
		recent_plays=recent_plays,
		recent_jobs=recent_jobs,
	)
	return {
		"self_hosted_server": self_hosted_server.name,
		"server": self_hosted_server.server,
		"status": self_hosted_server.status,
		"onboarding_stage": self_hosted_server.onboarding_stage,
		"onboarding_error": self_hosted_server.onboarding_error,
		"onboarding_started_at": self_hosted_server.onboarding_started_at,
		"onboarding_completed_at": self_hosted_server.onboarding_completed_at,
		"onboarding_profile": _serialize_onboarding_profile(self_hosted_server),
		"machine_facts": _serialize_machine_facts(self_hosted_server),
		"readiness_checks": _serialize_readiness_checks(self_hosted_server),
		"production_checks": _serialize_production_checks(self_hosted_server),
		"production_checks_updated_at": self_hosted_server.production_checks_updated_at,
		"existing_bench_present": bool(self_hosted_server.existing_bench_present),
		"bench_directory": self_hosted_server.bench_directory,
		"release_group": self_hosted_server.release_group,
		"app_count": len(self_hosted_server.apps or []),
		"site_count": len(self_hosted_server.sites or []),
		"apps": [
			{
				"app_name": row.app_name,
				"branch": row.branch,
				"version": row.version,
			}
			for row in self_hosted_server.apps or []
		],
		"sites": [
			{
				"site_name": row.site_name,
				"apps": row.apps,
				"site": row.site,
			}
			for row in self_hosted_server.sites or []
		],
		"can_discover": bool(
			self_hosted_server.existing_bench_present and self_hosted_server.bench_directory
		),
		"can_create_release_group": bool(
			self_hosted_server.existing_bench_present
			and self_hosted_server.bench_directory
			and self_hosted_server.apps
			and not self_hosted_server.release_group
		),
		"can_create_sites": bool(self_hosted_server.release_group and self_hosted_server.sites),
		"can_restore_files": bool(
			self_hosted_server.release_group
			and self_hosted_server.bench_directory
			and any(row.site for row in self_hosted_server.sites or [])
		),
		"job_scope_summary": job_scope_summary,
		"recent_jobs": recent_jobs,
		"operation_status": operation_status,
		"recent_plays": recent_plays,
	}


def _serialize_onboarding_profile(self_hosted_server):
	managed_domains = [
		domain.strip()
		for domain in (self_hosted_server.managed_domains or "").splitlines()
		if domain.strip()
	]
	return {
		"title": self_hosted_server.title,
		"primary_domain": self_hosted_server.server_url,
		"managed_domains": managed_domains,
		"onboarding_email": self_hosted_server.onboarding_email,
		"ssh_user": self_hosted_server.ssh_user,
		"ssh_port": self_hosted_server.ssh_port,
	}


def _serialize_machine_facts(self_hosted_server):
	return {
		"hostname": self_hosted_server.hostname,
		"distribution": self_hosted_server.distribution,
		"architecture": self_hosted_server.architecture,
		"processor": self_hosted_server.processor,
		"vendor": self_hosted_server.vendor,
		"vcpus": self_hosted_server.vcpus,
		"ram": self_hosted_server.ram,
		"total_storage": self_hosted_server.total_storage,
		"swap_total": self_hosted_server.swap_total,
		"db_vcpus": self_hosted_server.db_vcpus,
		"db_ram": self_hosted_server.db_ram,
		"db_total_storage": self_hosted_server.db_total_storage,
		"storage_layout": self_hosted_server.storage_layout,
		"runtime_user": self_hosted_server.runtime_user,
		"public_ip": self_hosted_server.ip,
		"private_ip": self_hosted_server.private_ip,
		"database_public_ip": self_hosted_server.mariadb_ip,
		"database_private_ip": self_hosted_server.mariadb_private_ip,
	}


def _normalize_managed_domains(value):
	if not value:
		return ""

	if isinstance(value, (list, tuple)):
		items = value
	else:
		raw_text = str(value).replace(",", "\n")
		items = raw_text.splitlines()

	normalized = []
	for item in items:
		domain = strip(item or "")
		if domain and domain not in normalized:
			normalized.append(domain)
	return "\n".join(normalized)


def _serialize_readiness_checks(self_hosted_server):
	checks = [
		{
			"label": "Access Profile",
			"status": "Ready"
			if self_hosted_server.ssh_user and self_hosted_server.server_url and self_hosted_server.onboarding_email
			else "Pending",
			"detail": self_hosted_server.ssh_user
			and f"{self_hosted_server.ssh_user}@{self_hosted_server.ip or 'server'}"
			or "Server access details still need to be completed.",
		},
		{
			"label": "Machine Facts",
			"status": "Ready"
			if self_hosted_server.ram and self_hosted_server.vcpus and self_hosted_server.total_storage
			else "Pending",
			"detail": self_hosted_server.total_storage
			or "CPU, memory, and storage facts will appear after verification.",
		},
		{
			"label": "Runtime User",
			"status": "Ready" if self_hosted_server.runtime_user else "Pending",
			"detail": self_hosted_server.runtime_user
			or "The managed runtime user will be confirmed after setup starts.",
		},
		{
			"label": "Storage Layout",
			"status": "Ready" if self_hosted_server.storage_layout else "Pending",
			"detail": "Disk partitions and mounts captured."
			if self_hosted_server.storage_layout
			else "Storage layout will appear after verification.",
		},
		{
			"label": "Managed Server Records",
			"status": "Ready"
			if self_hosted_server.server_created and self_hosted_server.database_setup and self_hosted_server.server
			else "Pending",
			"detail": self_hosted_server.server
			or "Managed server records are not fully created yet.",
		},
	]
	return checks


def _serialize_production_checks(self_hosted_server):
	if not self_hosted_server.production_checks:
		return {"checks": []}

	try:
		return json.loads(self_hosted_server.production_checks)
	except Exception:
		return {"checks": []}


def _get_recent_onboarding_jobs(server: str | None, bench_names: list[str], site_names: list[str]):
	if not (server or bench_names or site_names):
		return []

	AgentJob = frappe.qb.DocType("Agent Job")
	query = (
		frappe.qb.from_(AgentJob)
		.select(
			AgentJob.name,
			AgentJob.job_type,
			AgentJob.status,
			AgentJob.server,
			AgentJob.bench,
			AgentJob.site,
			AgentJob.creation,
			AgentJob.duration,
			AgentJob.end,
		)
		.orderby(AgentJob.creation, order=frappe.qb.desc)
		.limit(8)
	)
	filters = []
	if server:
		filters.append(AgentJob.server == server)
	if bench_names:
		filters.append(AgentJob.bench.isin(bench_names))
	if site_names:
		filters.append(AgentJob.site.isin(site_names))
	for condition in filters[1:]:
		filters[0] = filters[0] | condition
	return query.where(filters[0]).run(as_dict=True)


def _get_onboarding_job_scope_summary(server: str | None, bench_names: list[str], site_names: list[str]):
	AgentJob = frappe.qb.DocType("Agent Job")
	summary = {"server_jobs": 0, "bench_jobs": 0, "site_jobs": 0}
	if server:
		summary["server_jobs"] = (
			frappe.qb.from_(AgentJob).select(Count("*")).where(AgentJob.server == server)
		).run()[0][0]
	if bench_names:
		summary["bench_jobs"] = (
			frappe.qb.from_(AgentJob).select(Count("*")).where(AgentJob.bench.isin(bench_names))
		).run()[0][0]
	if site_names:
		summary["site_jobs"] = (
			frappe.qb.from_(AgentJob).select(Count("*")).where(AgentJob.site.isin(site_names))
		).run()[0][0]
	return summary


def _normalize_execution_status(value: str | None):
	status = (value or "").lower()
	if status in {"success", "completed"}:
		return "Success"
	if status in {"running", "pending"}:
		return "Running"
	if status in {"failure", "failed", "error"}:
		return "Failed"
	return "Idle"


def _latest_matching_execution(rows: list[dict], patterns: tuple[str, ...], field: str):
	for row in rows:
		label = (row.get(field) or "").lower()
		if any(pattern in label for pattern in patterns):
			return row
	return None


def _get_onboarding_operation_status(self_hosted_server, recent_plays: list[dict], recent_jobs: list[dict]):
	discovery_play = _latest_matching_execution(
		recent_plays,
		("get apps", "get sites", "current bench"),
		"play",
	)
	restore_play = _latest_matching_execution(
		recent_plays,
		("restore", "site files"),
		"play",
	)
	managed_bench_job = _latest_matching_execution(
		recent_jobs,
		("release group", "bench"),
		"job_type",
	)
	managed_site_job = _latest_matching_execution(
		recent_jobs,
		("site",),
		"job_type",
	)
	return {
		"discovery": {
			"label": "Bench Discovery",
			"status": _normalize_execution_status(discovery_play.get("status") if discovery_play else None),
			"detail": discovery_play.get("play") if discovery_play else "No discovery run recorded yet.",
			"reference": discovery_play.get("name") if discovery_play else None,
			"kind": "play",
		},
		"managed_bench": {
			"label": "Managed Bench Creation",
			"status": "Success"
			if self_hosted_server.release_group
			else _normalize_execution_status(managed_bench_job.get("status") if managed_bench_job else None),
			"detail": self_hosted_server.release_group
			if self_hosted_server.release_group
			else managed_bench_job.get("job_type") if managed_bench_job else "Managed bench not created yet.",
			"reference": managed_bench_job.get("name") if managed_bench_job else None,
			"kind": "job",
		},
		"managed_sites": {
			"label": "Managed Site Import",
			"status": "Success"
			if any(row.site for row in self_hosted_server.sites or [])
			else _normalize_execution_status(managed_site_job.get("status") if managed_site_job else None),
			"detail": managed_site_job.get("job_type")
			if managed_site_job
			else "Managed site import has not been recorded yet.",
			"reference": managed_site_job.get("name") if managed_site_job else None,
			"kind": "job",
		},
		"restore": {
			"label": "Site File Restore",
			"status": _normalize_execution_status(restore_play.get("status") if restore_play else None),
			"detail": restore_play.get("play") if restore_play else "Site file restore has not started yet.",
			"reference": restore_play.get("name") if restore_play else None,
			"kind": "play",
		},
	}


@frappe.whitelist()
def get_bench_onboarding_state(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	return _serialize_self_hosted_bench_state(self_hosted_server)


@frappe.whitelist()
def get_managed_server_onboarding_state(self_hosted_server: str):
	doc = _get_self_hosted_server(self_hosted_server=self_hosted_server)
	return _serialize_self_hosted_bench_state(doc)


@frappe.whitelist()
def rerun_managed_server_onboarding(self_hosted_server: str):
	doc = _get_self_hosted_server(self_hosted_server=self_hosted_server)
	doc.start_onboarding()
	doc.reload()
	return _serialize_self_hosted_bench_state(doc)


@frappe.whitelist()
def run_managed_server_production_checks(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	self_hosted_server.run_production_checks()
	self_hosted_server.reload()
	return _serialize_self_hosted_bench_state(self_hosted_server)


@frappe.whitelist()
def restart_managed_server_runtime(server: str, operation_scope: str = "all"):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	operation_scope = strip(operation_scope or "") or "all"
	if operation_scope == "all":
		self_hosted_server.restart_production_services()
	elif operation_scope == "nginx":
		self_hosted_server.restart_nginx()
	elif operation_scope == "redis":
		self_hosted_server.restart_redis()
	elif operation_scope == "workers":
		self_hosted_server.restart_workers()
	else:
		frappe.throw("Unsupported runtime operation requested")
	self_hosted_server.reload()
	return _serialize_self_hosted_bench_state(self_hosted_server)


@frappe.whitelist()
def update_existing_bench_configuration(
	server: str, existing_bench_present: int | str = 0, bench_directory: str | None = None
):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	self_hosted_server.existing_bench_present = cint(existing_bench_present)
	self_hosted_server.bench_directory = strip(bench_directory or "") or None
	if self_hosted_server.existing_bench_present and not self_hosted_server.bench_directory:
		frappe.throw("Bench directory is required when importing an existing bench")
	self_hosted_server.save()
	return _serialize_self_hosted_bench_state(self_hosted_server)


@frappe.whitelist()
def discover_existing_bench(server: str, bench_directory: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	self_hosted_server.existing_bench_present = 1
	self_hosted_server.bench_directory = strip(bench_directory or "")
	if not self_hosted_server.bench_directory:
		frappe.throw("Bench directory is required to inspect an existing bench")
	self_hosted_server.save()
	self_hosted_server.fetch_apps_and_sites()
	self_hosted_server.reload()
	state = _serialize_self_hosted_bench_state(self_hosted_server)
	state["message"] = "Bench discovery has started. Refresh shortly to inspect discovered apps and sites."
	return state


@frappe.whitelist()
def create_release_group_from_existing_bench(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	if not self_hosted_server.existing_bench_present:
		frappe.throw("Enable existing-bench import before creating a managed bench")
	if not self_hosted_server.bench_directory:
		frappe.throw("Bench directory is required before creating a managed bench")
	if not self_hosted_server.apps:
		frappe.throw("Discover the existing bench apps before creating a managed bench")
	if self_hosted_server.release_group:
		return _serialize_self_hosted_bench_state(self_hosted_server)
	self_hosted_server.create_new_rg()
	self_hosted_server.reload()
	state = _serialize_self_hosted_bench_state(self_hosted_server)
	state["message"] = "Managed bench created from the discovered existing bench"
	return state


@frappe.whitelist()
def create_sites_from_existing_bench(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	if not self_hosted_server.release_group:
		frappe.throw("Create the managed bench before importing sites from it")
	if not self_hosted_server.sites:
		frappe.throw("Discover the existing bench sites before importing them")
	self_hosted_server.create_new_sites()
	self_hosted_server.reload()
	state = _serialize_self_hosted_bench_state(self_hosted_server)
	state["message"] = "Managed site records created from the discovered bench sites"
	return state


@frappe.whitelist()
def restore_site_files_from_existing_bench(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	if not self_hosted_server.release_group:
		frappe.throw("Create the managed bench before restoring site files")
	if not self_hosted_server.bench_directory:
		frappe.throw("Bench directory is required before restoring site files")
	if not any(row.site for row in self_hosted_server.sites or []):
		frappe.throw("Create the managed site records before restoring site files")
	self_hosted_server.restore_files()
	self_hosted_server.reload()
	state = _serialize_self_hosted_bench_state(self_hosted_server)
	state["message"] = "Site file restoration has started. Track the related plays for progress."
	return state
