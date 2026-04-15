# Copyright (c) 2023, Frappe and contributors
# For license information, please see license.txt

from __future__ import annotations

import json
from contextlib import suppress
from collections import Counter

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import now_datetime

from press.runner import Ansible
from press.utils import log_error

# from tldextract import extract as sdext


class SelfHostedServer(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from press.press.doctype.self_hosted_site_apps.self_hosted_site_apps import (
			SelfHostedSiteApps,
		)
		from press.press.doctype.site_analytics_app.site_analytics_app import SiteAnalyticsApp

		agent_password: DF.Password | None
		apps: DF.Table[SiteAnalyticsApp]
		architecture: DF.Data | None
		bench_directory: DF.Data | None
		cluster: DF.Link | None
		database_plan: DF.Link | None
		database_server: DF.Link | None
		database_service: DF.Literal["AWS - RDS"]
		database_setup: DF.Check
		db_ram: DF.Data | None
		db_total_storage: DF.Data | None
		db_vcpus: DF.Data | None
		dedicated_proxy: DF.Check
		different_database_server: DF.Check
		distribution: DF.Data | None
		domain: DF.Data | None
		existing_bench_present: DF.Check
		frappe_version: DF.Data | None
		hostname: DF.Data | None
		instance_type: DF.Data | None
		ip: DF.Data
		is_managed_database: DF.Check
		mariadb_ip: DF.Data | None
		mariadb_private_ip: DF.Data | None
		mariadb_root_password: DF.Password
		mariadb_root_user: DF.Data | None
		new_server: DF.Check
		onboarding_email: DF.Data | None
		onboarding_completed_at: DF.Datetime | None
		onboarding_error: DF.SmallText | None
		onboarding_stage: DF.Data | None
		onboarding_started_at: DF.Datetime | None
		plan: DF.Link | None
		private_ip: DF.Data | None
		processor: DF.Data | None
		production_checks: DF.LongText | None
		production_checks_updated_at: DF.Datetime | None
		proxy_created: DF.Check
		proxy_private_ip: DF.Data | None
		proxy_public_ip: DF.Data | None
		proxy_server: DF.Link | None
		ram: DF.Data | None
		release_group: DF.Link | None
		server: DF.Link | None
		server_created: DF.Check
		server_url: DF.Data | None
		sites: DF.Table[SelfHostedSiteApps]
		ssh_port: DF.Int
		ssh_user: DF.Data | None
		status: DF.Literal["Active", "Pending", "Broken", "Archived", "Unreachable"]
		storage_layout: DF.SmallText | None
		swap_total: DF.Data | None
		team: DF.Link
		title: DF.Data | None
		total_storage: DF.Data | None
		managed_domains: DF.SmallText | None
		runtime_user: DF.Data | None
		vcpus: DF.Data | None
		vendor: DF.Data | None
	# end: auto-generated types

	def before_insert(self):
		self.validate_is_duplicate()

	def autoname(self):
		series = make_autoname("SHS-.#####")
		self.name = f"{series}.{self.hybrid_domain}"

		self.hostname = series
		self.domain = self.hybrid_domain

	def validate(self):
		self.set_proxy_details()
		self.set_mariadb_config()
		self.set_database_plan()

		if not self.agent_password:
			self.agent_password = frappe.generate_hash(length=32)

	def validate_is_duplicate(self):
		filters = {
			"ip": self.ip,
			"private_ip": self.private_ip,
			"mariadb_ip": self.mariadb_ip,
			"mariadb_private_ip": self.mariadb_private_ip,
			"status": ("not in", ["Archived", "Broken"]),
		}
		duplicate_server = frappe.db.get_value("Self Hosted Server", filters, pluck="name")

		if duplicate_server:
			raise frappe.DuplicateEntryError(self.doctype, duplicate_server)

	def set_proxy_details(self):
		if self.proxy_created or self.proxy_server:
			self.proxy_public_ip, self.proxy_private_ip = frappe.db.get_value(
				"Proxy Server", self.proxy_server, ["ip", "private_ip"]
			)

	def set_mariadb_config(self):
		if not self.mariadb_ip:
			self.mariadb_ip = self.ip
		if not self.mariadb_private_ip:
			self.mariadb_private_ip = self.private_ip
		if not self.mariadb_root_user:
			self.mariadb_root_user = "root"
		if not self.mariadb_root_password:
			self.mariadb_root_password = frappe.generate_hash(length=32)

	@frappe.whitelist()
	def fetch_apps_and_sites(self):
		# Reset the current import snapshot so repeated discovery reflects the
		# server's latest bench state instead of appending duplicate rows.
		self.set("apps", [])
		self.set("sites", [])
		self.save()

		frappe.enqueue_doc(self.doctype, self.name, "_get_apps", queue="long", timeout=1200)
		frappe.enqueue_doc(self.doctype, self.name, "_get_sites", queue="long", timeout=1200)

	@frappe.whitelist()
	def ping_ansible(self):
		try:
			ansible = Ansible(
				playbook="ping.yml",
				server=self,
				user=self.ssh_user or "root",
				port=self.ssh_port or 22,
			)
			play = ansible.run()
			if play.status == "Success" and self.status == "Unreachable":
				self.status = "Pending"
				self.save()
			self.reload()
		except Exception:
			log_error("Server Ping Exception", server=self.as_dict())

	def _get_sites(self):
		"""
		Get Sites from Existing Bench in the server
		"""
		try:
			ansible = Ansible(
				playbook="get_sites.yml",
				server=self,
				user=self.ssh_user or "root",
				port=self.ssh_port or 22,
				variables={"bench_path": self.bench_directory},
			)
			play = ansible.run()
			if play.status == "Success":
				self.append_to_sites()
		except Exception:
			log_error("Self Hosted Sites Issue", server=self.as_dict())

	def _get_apps(self):
		"""
		Get Apps from Existing Bench in the server
		"""
		try:
			ansible = Ansible(
				playbook="get_apps.yml",
				server=self,
				user=self.ssh_user or "root",
				port=self.ssh_port or "22",
				variables={"bench_path": self.bench_directory},
			)
			play = ansible.run()
			if play.status == "Success":
				self.append_to_apps()
		except Exception:
			log_error("Self Hosted Apps Issue", server=self.as_dict())

	def map_branch_to_version(self, branch):
		versions = {
			"version-13": "Version 13",
			"version-14": "Version 14",
			"develop": "Nightly",
		}
		return versions[branch]

	def append_to_sites(self):
		"""
		Append Sites and the app used by each site from existing bench to Sites Child table
		"""
		ansible_play = frappe.get_last_doc("Ansible Play", {"server": self.name})
		ansible_task_op = frappe.get_value(
			"Ansible Task",
			{"play": ansible_play.name, "task": "Get Sites from Current Bench"},
			"output",
		)
		sites = json.loads(ansible_task_op)
		try:
			for k, v in sites.items():
				self.append("sites", {"site_name": k, "apps": ",".join(map(str, v))})
			self.save()
			self.append_site_configs(ansible_play.name)
			self.status = "Active"
		except Exception:
			self.status = "Broken"
			log_error("Append to Sites Failed", server=self.as_dict())
		self.save()

	def append_to_apps(self):
		"""
		Append apps from existing bench to `apps` child table
		Appends app name, app version and app branch
		"""
		ansible_play = frappe.get_last_doc("Ansible Play", {"server": self.name})
		ansible_task_op = frappe.get_value(
			"Ansible Task",
			{"play": ansible_play.name, "task": "Get Versions from Current Bench"},
			"output",
		).replace("'", '"')
		task_output = json.loads(ansible_task_op)
		temp_task_result = task_output  # Removing risk of mutating the same loop variable
		for i, app in enumerate(temp_task_result):  # Rearrange JSON if frappe isn't first app
			if app["app"] == "frappe" and i > 0:
				task_output[i], task_output[0] = task_output[0], task_output[i]
		try:
			for app in task_output:
				self.append(
					"apps",
					{"app_name": app["app"], "version": app["version"], "branch": app["branch"]},
				)
				if app["app"] == "frappe":
					self.frappe_version = self.map_branch_to_version(app["branch"])
			self.status = "Active"

		except Exception:
			self.status = "Broken"
			log_error("Appending Apps Error", server=self.as_dict())
		self.save()

	@frappe.whitelist()
	def create_new_rg(self):
		"""
		Create **a** Release Group for the apps in the Existing bench
		"""
		ansible_play = frappe.get_last_doc(
			"Ansible Play",
			{"server": self.server, "play": "Get Bench data from Self Hosted Server"},
		)
		ansible_task_op = frappe.get_value(
			"Ansible Task",
			{"play": ansible_play.name, "task": "Get Apps for Release Group"},
			"output",
		).replace("'", '"')
		task_result = json.loads(ansible_task_op)
		temp_task_result = task_result  # Removing risk of mutating the same loop variable
		for i, app in enumerate(temp_task_result):  # Rearrange JSON if frappe isn't first app
			if app["app"] == "frappe" and i > 0:
				task_result[i], task_result[0] = task_result[0], task_result[i]
		release_group = frappe.new_doc("Release Group")
		release_group.title = f"{self.server}-bench"
		branches = []
		try:
			for app in task_result:
				branches.append(app["branch"])
				if not frappe.db.exists("App Source", {"app": app["app"], "branch": app["branch"]}):  # noqa: SIM102
					if not frappe.db.exists("App", {"_newname": app["app"]}):
						app_doc = frappe.get_doc(
							{
								"doctype": "App",
								"_newname": app["app"],
								"title": app["app"].title(),
								"name": app["app"],
							}
						)
						app_doc.insert()
						app_source_doc = frappe.get_doc(
							{
								"doctype": "App Source",
								"app": app["app"],
								"repository_url": app["remote"],
								"team": "Administrator",
								"branch": app["branch"],
							}
						)
						app_source_doc.append("versions", {"version": self.frappe_version})
						app_source_doc.insert()
						frappe.db.commit()
						release_group.append("apps", {"app": app["app"], "source": app_source_doc.name})
				release_group.append(
					"apps",
					{
						"app": app["app"],
						"source": frappe.get_value(
							"App Source",
							{
								"app": app["app"],
								"branch": app["branch"],
							},
							"name",
						),
					},
				)
				release_group.append("servers", {"server": self.server})
		except Exception:
			self.status = "Broken"
			self.save()
			log_error("Creating RG failed", server=self.as_dict())
		release_group.team = self.team
		release_group.version = self.map_branch_to_version(max(branches))
		rg = release_group.insert()
		self.release_group = rg.name
		self.status = "Active"
		self.save()

	def set_database_plan(self):
		if self.database_plan:
			return

		if not self.different_database_server and not frappe.db.exists("Server Plan", "Unlimited"):
			self._create_server_plan("Unlimited")
			self.database_plan = "Unlimited"

	def _create_server_plan(self, plan_name):
		plan = frappe.new_doc("Server Plan")
		plan.name = plan_name
		plan.title = plan_name
		plan.price_inr = 0
		plan.price_usd = 0
		plan.save()

	@frappe.whitelist()
	def create_database_server(self):
		try:
			if not self.mariadb_ip:
				frappe.throw("Public IP for MariaDB not found")

			db_server = frappe.new_doc(
				"Database Server",
				**{
					"hostname": self.get_hostname("Database Server"),
					"title": f"{self.title} Database",
					"is_self_hosted": True,
					"domain": self.hybrid_domain,
					"self_hosted_server_domain": self.hybrid_domain,
					"ip": self.mariadb_ip,
					"private_ip": self.mariadb_private_ip,
					"team": self.team,
					"ssh_user": self.ssh_user,
					"ssh_port": self.ssh_port,
					"mariadb_root_password": self.get_password("mariadb_root_password"),
					"cluster": self.cluster,
					"agent_password": self.get_password("agent_password"),
					"is_server_setup": not self.new_server,
					"plan": self.database_plan,
				},
			).insert()

			db_server.create_subscription(self.database_plan)
			self.database_setup = True
			self.database_server = db_server.name
			self.status = "Active"
			self.save()

			if not frappe.flags.in_test:
				db_server.create_dns_record()

			frappe.db.commit()

			frappe.msgprint(f"Database server record {db_server.name} created")
		except Exception:
			frappe.throw("Adding Server to Database Server Doctype failed")
			self.status = "Broken"
			self.save()
			log_error("Inserting a new DB server failed")

	def append_site_configs(self, play_name):
		"""
		Append site_config.json to `sites` Child Table
		"""
		try:
			ansible_task_op = frappe.get_value(
				"Ansible Task",
				{"play": play_name, "task": "Get Site Configs from Existing Sites"},
				"output",
			)
			task_result = json.loads(
				ansible_task_op.replace("'", '"').replace('"{', "{").replace('}"', "}").replace("\\n", "")
			)
			self.status = "Pending"
			for site in task_result:
				for _site in self.sites:
					if _site.site_name == site["site"]:
						_site.site_config = str(site["config"]).replace(
							"'", '"'
						)  # JSON Breaks since dict uses only single quotes
					self.save()
			self.status = "Active"
		except Exception as e:
			self.status = "Broken"
			frappe.throw("Fetching sites configs from Existing Bench failed", exc=e)
		self.save()

	@frappe.whitelist()
	def create_application_server(self):
		"""
		Add a new record to the Server doctype
		"""

		try:
			server = frappe.new_doc(
				"Server",
				**{
					"hostname": self.get_hostname("Server"),
					"title": f"{self.title} Application",
					"is_self_hosted": True,
					"domain": self.hybrid_domain,
					"self_hosted_server_domain": self.hybrid_domain,
					"team": self.team,
					"ip": self.ip,
					"private_ip": self.private_ip,
					"ssh_user": self.ssh_user,
					"ssh_port": self.ssh_port,
					"proxy_server": self.proxy_server,
					"database_server": self.database_server,
					"cluster": self.cluster,
					"agent_password": self.get_password("agent_password"),
					"self_hosted_mariadb_root_password": self.get_password("mariadb_root_password"),
					"ram": self.ram,
					"new_worker_allocation": True,
					"plan": self.plan,
				},
			).insert()

			self.server = server.name
			self.status = "Active"
			self.server_created = True

			if not frappe.flags.in_test:
				server.create_dns_record()

			frappe.db.commit()

		except Exception as e:
			self.status = "Broken"
			frappe.throw("Server Creation Error", exc=e)

		self.save()

		frappe.msgprint(f"Server record {server.name} created")
		return server

	@frappe.whitelist()
	def create_new_sites(self):
		"""
		Create new FC sites from sites in Current Bench
		"""
		try:
			for _site in self.sites:
				if len(_site.site_name) < 5:
					sdomain = _site.site_name + "-new"
				else:
					sdomain = _site.site_name
				sdomain = sdomain.replace(".", "-")
				domain = self.domain
				if not frappe.db.exists("Site", f"{sdomain}.{domain}"):
					new_site = frappe.new_doc("Site")
					new_site.subdomain = sdomain
					new_site.domain = domain
					try:
						new_site.bench = frappe.get_last_doc(
							"Bench", {"group": self.release_group, "server": self.name}
						).name
					except Exception as e:
						frappe.throw("Site Creation Failed", exc=e)
					new_site.team = self.team
					new_site.server = self.name
					for app in _site.apps.split(","):
						new_site.append("apps", {"app": app})
					config = json.loads(_site.site_config)
					for key, value in config.items():
						new_site.append("configuration", {"key": key, "value": value})
					new_site.database_name = config["db_name"]
					_new_site = new_site.insert()
					_site.site = _new_site.name
					self.save()
					self.reload()
		except Exception:
			log_error("New Site Creation Error", server=self.as_dict())

	@frappe.whitelist()
	def restore_files(self):
		frappe.enqueue_doc(self.doctype, self.name, "_restore_files", queue="long", timeout=2400)

	def _restore_files(self):
		"""
		Copy required folder of Existing Bench to new sites
		"""
		self.status = "Pending"
		self.save()
		ex_sites = []
		nw_sites = []
		benches = []
		for _site in self.sites:
			ex_sites.append(_site.site_name)
			nw_sites.append(_site.site)
			bench = frappe.db.get_value("Site", _site.site, "bench")
			benches.append(bench)
		try:
			ansible = Ansible(
				playbook="self_hosted_restore.yml",
				server=self,
				user=self.ssh_user or "root",
				port=self.ssh_port or 22,
				variables={
					"bench_path": self.bench_directory,
					"ex_sites": ex_sites,
					"new_benches": benches,
					"new_sites": nw_sites,
				},
			)
			play = ansible.run()
			if play.status == "Success":
				self.status = "Active"
		except Exception:
			self.status = "Broken"
			log_error("Self Hosted Restore error", server=self.name)
		self.save()

	def get_hostname(self, server_type):
		symbolic_name = get_symbolic_name(server_type)
		series = f"{symbolic_name}-{self.cluster}.#####"

		index = make_autoname(series)[-5:]

		return f"{symbolic_name}-{index}-{self.cluster}".lower()

	@property
	def hybrid_domain(self):
		return frappe.db.get_single_value("Press Settings", "hybrid_domain")

	@frappe.whitelist()
	def create_proxy_server(self):
		"""
		Add a new record to the Proxy Server doctype
		"""
		try:
			proxy_server = frappe.new_doc(
				"Proxy Server",
				**{
					"hostname": self.get_hostname("Proxy Server"),
					"title": self.title,
					"is_self_hosted": True,
					"domain": self.hybrid_domain,
					"self_hosted_server_domain": self.hybrid_domain,
					"team": self.team,
					"ip": self.proxy_public_ip,
					"private_ip": self.proxy_private_ip,
					"is_primary": True,
					"cluster": self.cluster,
					"ssh_user": self.ssh_user,
					"ssh_port": self.ssh_port,
				},
			).insert()

			self.agent_password = proxy_server.get_password("agent_password")
			self.proxy_server = proxy_server.name
			self.status = "Active"
			self.proxy_created = True
		except Exception as e:
			self.status = "Broken"
			frappe.throw("Self Hosted Proxy Server Creation Error", exc=e)
		self.save()

		frappe.msgprint(f"Proxy server record {proxy_server.name} created")

	@frappe.whitelist()
	def create_tls_certs(self, domain):
		try:
			tls_cert = frappe.db.get_value("TLS Certificate", {"domain": f"{domain}"})

			if not tls_cert:
				tls_cert = frappe.new_doc(
					"TLS Certificate",
					**{
						"domain": domain,
						"team": self.team,
						"wildcard": False,
					},
				).insert()
				tls_cert = tls_cert.name

			return tls_cert
		except Exception:
			log_error("TLS Certificate(SelfHosted) Creation Error")

	def setup_nginx(self, server):
		try:
			ansible = Ansible(
				playbook="self_hosted_nginx.yml",
				server=server,
				user=server.ssh_user or "root",
				port=server.ssh_port or 22,
				variables={
					"domain": self.name,
					"press_domain": frappe.db.get_single_value("Press Settings", "domain"),  # for ssl renewal
				},
			)
			play = ansible.run()
			if play.status == "Success":
				return True
		except Exception:
			log_error("Nginx setup failed for self hosted server", server=self.as_dict())
			return False

	@frappe.whitelist()
	def update_tls(self):
		from press.press.doctype.tls_certificate.tls_certificate import (
			update_server_tls_certifcate,
		)

		try:
			cert = frappe.get_last_doc("TLS Certificate", {"domain": self.server, "status": "Active"})
		except frappe.DoesNotExistError:
			cert = frappe.get_last_doc("TLS Certificate", {"domain": self.name, "status": "Active"})

		update_server_tls_certifcate(self, cert)

	def process_tls_cert_update(self):
		self.update_tls()

	def setup_server(self):
		if not self.runtime_user:
			# The self-hosted setup playbook creates and runs the managed runtime
			# under the dedicated `frappe` user.
			self.runtime_user = "frappe"
			self.save()

		self._setup_db_server()

		if self.different_database_server:
			self._setup_app_server()

		self.run_production_checks()

	@frappe.whitelist()
	def start_onboarding(self):
		if self.onboarding_stage in {
			"Queued",
			"Verifying Access",
			"Validating Machine Capacity",
			"Creating Database Runtime",
			"Creating Application Runtime",
			"Applying Runtime Setup",
		}:
			frappe.throw("Server onboarding is already running for this managed server")
		self.onboarding_stage = "Queued"
		self.onboarding_error = None
		self.onboarding_started_at = now_datetime()
		self.onboarding_completed_at = None
		self.status = "Pending"
		self.save()
		frappe.enqueue_doc(
			self.doctype,
			self.name,
			"_run_onboarding_pipeline",
			queue="long",
			timeout=3600,
			enqueue_after_commit=True,
		)

	def _run_onboarding_pipeline(self):
		try:
			self.reload()
			self._set_onboarding_state("Verifying Access")

			app_server_verified = self._verify_target("app")
			db_server_verified = self._verify_target("db")
			if not (app_server_verified and db_server_verified):
				frappe.throw("Managed server verification failed")

			self._set_onboarding_state("Validating Machine Capacity")
			self.check_minimum_specs()
			self.status = "Pending"
			self.save()

			if not self.database_server:
				self._set_onboarding_state("Creating Database Runtime")
				self.create_database_server()

			if not self.server:
				self._set_onboarding_state("Creating Application Runtime")
				self.create_application_server()

			self._set_onboarding_state("Applying Runtime Setup")
			self.setup_server()

			self._set_onboarding_state("Completed", completed=True)
			self.status = "Active"
			self.save()
		except Exception:
			self.reload()
			self.status = "Broken"
			self.onboarding_stage = "Failed"
			self.onboarding_error = frappe.get_traceback(with_context=False)
			self.save()
			log_error("Self Hosted Server Onboarding Failed", server=self.as_dict())
			raise

	def _set_onboarding_state(self, stage: str, completed: bool = False):
		self.onboarding_stage = stage
		self.onboarding_error = None
		if completed:
			self.onboarding_completed_at = now_datetime()
		self.save()

	def _verify_target(self, server_type: str):
		ping = Ansible(
			playbook="ping.yml",
			server=frappe._dict(
				{
					"doctype": "Self Hosted Server",
					"name": self.name,
					"ssh_user": self.ssh_user,
					"ssh_port": self.ssh_port,
					"ip": self.ip if server_type == "app" else self.mariadb_ip,
				}
			),
		)
		result = ping.run()

		if result.status == "Success":
			private_ip = self.private_ip if server_type == "app" else self.mariadb_private_ip
			if private_ip:
				self.validate_private_ip(result.name, server_type=server_type)
			else:
				self.fetch_private_ip(result.name, server_type=server_type)
			self.fetch_system_specifications(result.name, server_type=server_type)
			self.reload()
			return True

		return False

	def _setup_db_server(self):
		db_server = frappe.get_doc("Database Server", self.database_server)
		db_server.setup_server()

	def _setup_app_server(self):
		app_server = frappe.get_doc("Server", self.server)
		app_server.setup_server()

	@property
	def subscription(self):
		name = frappe.db.get_value(
			"Subscription", {"document_type": self.doctype, "document_name": self.name}
		)
		return frappe.get_doc("Subscription", name) if name else None

	def can_charge_for_subscription(self, subscription=None):
		return (
			self.status not in ["Archived", "Unreachable", "Pending"]
			and self.team
			and self.team != "Administrator"
		)

	def _get_play_id(self):
		try:
			play_id = frappe.get_last_doc("Ansible Play", {"server": self.server, "play": "Ping Server"}).name
		except frappe.DoesNotExistError:
			play_id = frappe.get_last_doc("Ansible Play", {"server": self.name, "play": "Ping Server"}).name

		return play_id

	def _get_play(self, play_id):
		play = frappe.get_doc("Ansible Task", {"status": "Success", "play": play_id, "task": "Gather Facts"})

		return json.loads(play.result)

	@frappe.whitelist()
	def fetch_system_ram(self, play_id=None, server_type="app"):
		"""
		Fetch the RAM from the Ping Ansible Play
		"""
		if not play_id:
			play_id = self._get_play_id()

		try:
			result = result = self._get_play(play_id)

			if server_type == "app":
				self.ram = result["ansible_facts"]["memtotal_mb"]
			else:
				self.db_ram = result["ansible_facts"]["memtotal_mb"]

			self.save()
		except Exception:
			log_error("Fetching RAM failed", server=self.as_dict())

	def validate_private_ip(self, play_id=None, server_type="app"):
		if not play_id:
			play_id = self._get_play_id()

		all_ipv4_addresses = []
		result = self._get_play(play_id)

		try:
			all_ipv4_addresses = result["ansible_facts"]["all_ipv4_addresses"]
		except Exception:
			log_error("Fetching Private IP failed", server=self.as_dict())
			return

		private_ip = self.private_ip
		public_ip = self.ip
		if server_type == "db":
			private_ip = self.mariadb_private_ip
			public_ip = self.mariadb_ip

		if private_ip not in all_ipv4_addresses:
			frappe.throw(f"Private IP {private_ip} is not associated with server having IP {public_ip} ")

	@frappe.whitelist()
	def fetch_private_ip(self, play_id=None, server_type="app"):
		"""
		Fetch the Private IP from the Ping Ansible Play
		"""
		if not play_id:
			play_id = self._get_play_id()

		try:
			result = self._get_play(play_id)

			if server_type == "app":
				self.private_ip = fetch_private_ip_based_on_vendor(result)
			else:
				self.mariadb_private_ip = fetch_private_ip_based_on_vendor(result)

			self.save()
		except Exception:
			log_error("Fetching Private IP failed", server=self.as_dict())

	@frappe.whitelist()
	def fetch_system_specifications(self, play_id=None, server_type="app"):
		"""
		Fetch the RAM from the Ping Ansible Play
		"""
		if not play_id:
			play_id = self._get_play_id()

		try:
			result = self._get_play(play_id)
			if server_type == "app":
				self.vendor = result["ansible_facts"]["system_vendor"]
				self.ram = result["ansible_facts"]["memtotal_mb"]
				self.vcpus = result["ansible_facts"]["processor_vcpus"]
				self.swap_total = result["ansible_facts"]["swaptotal_mb"]
				self.architecture = result["ansible_facts"]["architecture"]
				self.instance_type = result["ansible_facts"]["product_name"]
				self.processor = result["ansible_facts"]["processor"][2]
				self.distribution = result["ansible_facts"]["lsb"]["description"]
				self.total_storage = self._get_total_storage(result)
				self.storage_layout = self._get_storage_layout(result)

			else:
				self.db_ram = result["ansible_facts"]["memtotal_mb"]
				self.db_vcpus = result["ansible_facts"]["processor_vcpus"]
				self.db_total_storage = self._get_total_storage(result)

			self.save()
		except Exception:
			log_error("Fetching System Details Failed", server=self.as_dict())

	def _get_total_storage(self, result):
		match self.vendor:
			case "DigitalOcean":
				total_storage = result["ansible_facts"]["devices"]["vda"]["size"]
			case "Amazon EC2":
				total_storage = result["ansible_facts"]["devices"]["nvme0n1"]["size"]
			case _:
				total_storage = result["ansible_facts"]["devices"]["sda"]["size"]

		return total_storage

	def _get_storage_layout(self, result):
		ansible_facts = result.get("ansible_facts", {})
		devices = ansible_facts.get("devices") or {}
		mounts = ansible_facts.get("mounts") or []
		lines = []

		if devices:
			lines.append("Devices")
			for name in sorted(devices):
				device = devices.get(name) or {}
				size = device.get("size") or "unknown-size"
				model = device.get("model") or device.get("vendor") or "unknown-model"
				lines.append(f"- {name} ({size}, {model})")
				for partition_name in sorted((device.get("partitions") or {}).keys()):
					partition = device["partitions"][partition_name]
					partition_size = partition.get("size") or "unknown-size"
					lines.append(f"  - {partition_name} ({partition_size})")

		if mounts:
			if lines:
				lines.append("")
			lines.append("Mounts")
			for mount in mounts:
				device = mount.get("device") or "unknown-device"
				path = mount.get("mount") or "unknown-mount"
				fstype = mount.get("fstype") or "unknown-fs"
				size_total = mount.get("size_total")
				size_label = self._format_bytes(size_total) if size_total else "unknown-size"
				lines.append(f"- {path} -> {device} [{fstype}] ({size_label})")

		return "\n".join(lines[:24])

	@frappe.whitelist()
	def run_production_checks(self):
		try:
			ansible = Ansible(
				playbook="self_hosted_runtime_checks.yml",
				server=self,
				user=self.ssh_user or "root",
				port=self.ssh_port or 22,
				variables={"bench_directory": self.bench_directory or "/home/frappe"},
			)
			play = ansible.run()
			checks = self._build_production_checks(play.name, play.status)
			self.production_checks = json.dumps(checks, indent=2)
			self.production_checks_updated_at = now_datetime()

			detected_runtime_user = checks.get("runtime_user", {}).get("value")
			if detected_runtime_user:
				self.runtime_user = detected_runtime_user

			device_layout = checks.get("storage_devices", {}).get("detail")
			if device_layout:
				self.storage_layout = device_layout

			self.save()
			return checks
		except Exception:
			log_error("Self Hosted Production Checks Failed", server=self.as_dict())
			return {
				"status": "Failure",
				"checks": [],
				"last_error": "Production checks could not be collected from the managed server.",
			}

	@frappe.whitelist()
	def restart_production_services(self):
		return self._restart_runtime("all")

	@frappe.whitelist()
	def restart_nginx(self):
		return self._restart_runtime("nginx")

	@frappe.whitelist()
	def restart_redis(self):
		return self._restart_runtime("redis")

	@frappe.whitelist()
	def restart_workers(self):
		return self._restart_runtime("workers")

	def _restart_runtime(self, operation_scope: str):
		try:
			ansible = Ansible(
				playbook="self_hosted_runtime_operation.yml",
				server=self,
				user=self.ssh_user or "root",
				port=self.ssh_port or 22,
				variables={"operation_scope": operation_scope},
			)
			play = ansible.run()
			self.run_production_checks()
			return {
				"status": play.status,
				"operation_scope": operation_scope,
			}
		except Exception:
			log_error(
				"Self Hosted Runtime Operation Failed",
				server=self.as_dict(),
				operation_scope=operation_scope,
			)
			return {
				"status": "Failure",
				"operation_scope": operation_scope,
			}

	def _build_production_checks(self, play_name: str, play_status: str):
		service_facts = self._get_task_result_dict(play_name, "Gather Runtime Service Facts")
		supervisor_status = self._get_task_output(play_name, "Capture Bench Supervisor Status")
		supervisor_service = self._get_task_output(play_name, "Capture Supervisor Service State")
		nginx_service = self._get_task_output(play_name, "Capture NGINX Service State")
		redis_services = self._get_task_output(play_name, "Capture Redis Service States")
		runtime_processes = self._get_task_output(play_name, "Capture Runtime Processes")
		runtime_users = self._get_task_output(play_name, "Capture Runtime Users")
		disk_usage = self._get_task_output(play_name, "Capture Disk Usage")
		block_devices = self._get_task_output(play_name, "Capture Block Devices")
		bench_owner = self._get_task_output(play_name, "Capture Bench Owner")

		services = (service_facts.get("ansible_facts") or {}).get("services") or {}
		supervisor_programs = self._parse_supervisor_programs(supervisor_status)
		redis_units = [
			line.strip()
			for line in redis_services.splitlines()
			if line.strip() and ".service" in line
		]
		detected_users = [user.strip() for user in runtime_users.split(",") if user.strip()]
		if not detected_users and bench_owner.strip():
			detected_users = [bench_owner.strip()]
		runtime_user = self._pick_runtime_user(detected_users)
		storage_detail = (
			self._format_block_devices_output(block_devices, disk_usage)
			or self.storage_layout
			or "No storage devices captured yet."
		)

		check_rows = [
			self._make_check(
				"NGINX",
				self._is_active_service(services, "nginx.service", nginx_service),
				nginx_service or self._service_summary(services, "nginx.service"),
				success_detail="NGINX is active and ready to serve traffic.",
				failure_detail="NGINX is missing or not active on the managed server.",
			),
			self._make_check(
				"Supervisor",
				self._is_supervisor_ready(supervisor_service, supervisor_status),
				supervisor_service or "Supervisor service state not captured.",
				success_detail="Supervisor is available for bench process control.",
				failure_detail="Supervisor is not active, so worker and scheduler recovery will be limited.",
			),
			self._make_check(
				"Redis",
				self._is_redis_ready(redis_units, supervisor_programs),
				redis_services or supervisor_status or "Redis service state not captured.",
				success_detail="Redis services were detected in a running or active state.",
				failure_detail="Redis services were not detected as healthy.",
			),
			self._make_check(
				"Workers",
				self._are_supervisor_programs_ready(supervisor_programs, ("worker",)),
				supervisor_status or "Worker state not captured.",
				success_detail="Worker processes are running under supervisor.",
				failure_detail="One or more worker processes are missing or not running.",
			),
			self._make_check(
				"Scheduler",
				self._are_supervisor_programs_ready(supervisor_programs, ("schedule",)),
				supervisor_status or "Scheduler state not captured.",
				success_detail="Scheduler process is running under supervisor.",
				failure_detail="Scheduler process is missing or not running.",
			),
			self._make_check(
				"Web",
				self._are_supervisor_programs_ready(supervisor_programs, ("web", "socketio")),
				supervisor_status or "Web process state not captured.",
				success_detail="Web-facing supervisor programs are running.",
				failure_detail="Web-facing supervisor programs are missing or not running.",
			),
			{
				"label": "Runtime User",
				"status": "Ready" if runtime_user else "Pending",
				"detail": runtime_user or "Runtime process owner has not been detected yet.",
			},
			{
				"label": "Storage Devices",
				"status": "Ready" if storage_detail else "Pending",
				"detail": storage_detail,
			},
		]

		return {
			"status": "Success" if play_status == "Success" else "Failure",
			"play": play_name,
			"checked_at": str(now_datetime()),
			"checks": check_rows,
			"runtime_user": {
				"label": "Runtime User",
				"value": runtime_user,
				"detail": ", ".join(detected_users) if detected_users else bench_owner.strip(),
			},
			"storage_devices": {
				"label": "Storage Devices",
				"detail": storage_detail,
			},
			"runtime_processes": runtime_processes.strip(),
		}

	def _get_task_output(self, play_name: str, task_name: str) -> str:
		task = frappe.db.get_value(
			"Ansible Task",
			{"play": play_name, "task": task_name},
			["output", "result"],
			as_dict=True,
		)
		if not task:
			return ""
		return (task.output or "").strip()

	def _get_task_result_dict(self, play_name: str, task_name: str) -> dict:
		task = frappe.db.get_value(
			"Ansible Task",
			{"play": play_name, "task": task_name},
			["result"],
			as_dict=True,
		)
		if not task or not task.result:
			return {}
		with suppress(Exception):
			return json.loads(task.result)
		return {}

	def _is_active_service(self, services: dict, service_name: str, systemctl_state: str):
		service = services.get(service_name) or {}
		active_states = {"running", "started", "active"}
		return (
			service.get("state") in active_states
			or service.get("status") in active_states
			or systemctl_state.strip() == "active"
		)

	def _service_summary(self, services: dict, service_name: str):
		service = services.get(service_name) or {}
		state = service.get("state") or "missing"
		status = service.get("status") or "missing"
		return f"{service_name}: state={state}, status={status}"

	def _parse_supervisor_programs(self, output: str):
		programs = {}
		for line in output.splitlines():
			parts = line.split()
			if len(parts) < 2:
				continue
			programs[parts[0]] = parts[1]
		return programs

	def _are_supervisor_programs_ready(self, programs: dict, patterns: tuple[str, ...]):
		matching = {
			name: status
			for name, status in programs.items()
			if any(pattern in name.lower() for pattern in patterns)
		}
		if not matching:
			return False
		return all(status.upper() == "RUNNING" for status in matching.values())

	def _is_supervisor_ready(self, supervisor_service: str, supervisor_status: str):
		return supervisor_service.strip() == "active" or "RUNNING" in supervisor_status

	def _is_redis_ready(self, redis_units: list[str], supervisor_programs: dict):
		has_active_systemd_redis = any(" active " in f" {line} " or " running " in f" {line} " for line in redis_units)
		redis_supervisor_programs = {
			name: status for name, status in supervisor_programs.items() if "redis" in name.lower()
		}
		has_running_supervisor_redis = any(
			status.upper() == "RUNNING" for status in redis_supervisor_programs.values()
		)
		return has_active_systemd_redis or has_running_supervisor_redis

	def _pick_runtime_user(self, users: list[str]):
		if not users:
			return None
		counts = Counter(users)
		return counts.most_common(1)[0][0]

	def _format_block_devices_output(self, block_devices: str, disk_usage: str):
		block_devices = (block_devices or "").strip()
		disk_usage = (disk_usage or "").strip()
		lines = []

		if block_devices.startswith("{"):
			with suppress(Exception):
				parsed = json.loads(block_devices)
				devices = parsed.get("blockdevices") or []
				lines.append("Devices")
				for device in devices:
					name = device.get("name") or "unknown"
					type_ = device.get("type") or "unknown"
					size = device.get("size") or "unknown-size"
					model = device.get("model") or "unknown-model"
					mountpoint = device.get("mountpoint") or "-"
					lines.append(f"- {name} [{type_}] {size} mount={mountpoint} model={model}")
					for child in device.get("children") or []:
						child_name = child.get("name") or "unknown"
						child_type = child.get("type") or "unknown"
						child_size = child.get("size") or "unknown-size"
						child_mount = child.get("mountpoint") or "-"
						child_fs = child.get("fstype") or "unknown-fs"
						lines.append(
							f"  - {child_name} [{child_type}] {child_size} fs={child_fs} mount={child_mount}"
						)

		if disk_usage:
			if lines:
				lines.append("")
			lines.append("Mount Usage")
			lines.extend(f"- {line}" for line in disk_usage.splitlines()[:12])

		return "\n".join(lines).strip()

	def _make_check(
		self,
		label: str,
		passed: bool,
		raw_detail: str,
		*,
		success_detail: str,
		failure_detail: str,
	):
		status = "Ready" if passed else "Failed"
		detail = success_detail if passed else failure_detail
		if raw_detail:
			detail = f"{detail} {raw_detail}".strip()
		return {"label": label, "status": status, "detail": detail}

	def _format_bytes(self, value):
		try:
			size = float(value)
		except (TypeError, ValueError):
			return str(value)

		for unit in ("B", "KB", "MB", "GB", "TB"):
			if size < 1024 or unit == "TB":
				return f"{size:.1f} {unit}"
			size /= 1024

	def check_minimum_specs(self):
		"""
		Check if the server meets the minimum requirements
		ie: RAM >= 4GB,vCPUs >= 2,Storage >= 40GB
		"""

		if round(int(self.ram), -3) < 4000:  # Round to nearest thousand
			frappe.throw(f"Minimum RAM requirement not met, Minimum is 4GB and available is {self.ram} MB")
		if int(self.vcpus) < 2:
			frappe.throw(
				f"Minimum vCPU requirement not met, Minimum is 2 Cores and available is {self.vcpus}"
			)

		self._validate_disk()

		return True

	def _validate_disk(self):
		disk_size = self.total_storage.split()[0]
		disk_storage_unit = self.total_storage.split()[1]

		if disk_storage_unit.upper() == "TB":
			return True

		if disk_storage_unit.upper() in ["GB", "MB"] and round(int(float(disk_size)), -1) < 40:
			frappe.throw(
				f"Minimum Storage requirement not met, Minimum is 50GB and available is {self.total_storage}"
			)
		return None


def fetch_private_ip_based_on_vendor(play_result: dict):
	vendor = play_result["ansible_facts"]["system_vendor"]
	match vendor:
		case "DigitalOcean":
			return play_result["ansible_facts"]["all_ipv4_addresses"][1]
		case "Hetzner":
			return play_result["ansible_facts"]["all_ipv4_addresses"][1]
		case "Amazon EC2":
			return play_result["ansible_facts"]["default_ipv4"]["address"]
		case "Microsoft Corporation":
			return play_result["ansible_facts"]["all_ipv4_addresses"][0]
		case "Google":
			return play_result["ansible_facts"]["default_ipv4"]["address"]
		case _:
			return play_result["ansible_facts"]["default_ipv4"]["address"]


def get_symbolic_name(server_type):
	return {
		"Proxy Server": "hybrid-n",
		"Server": "hybrid-f",
		"Database Server": "hybrid-m",
	}.get(server_type, "hybrid-f")
