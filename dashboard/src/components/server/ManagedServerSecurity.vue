<template>
	<div class="space-y-6" v-if="serverDoc">
		<section
			class="overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-white shadow-sm"
		>
			<div class="grid gap-6 px-6 py-6 lg:grid-cols-[minmax(0,1.35fr)_420px] lg:px-8">
				<div class="space-y-4">
					<div class="inline-flex w-fit items-center rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.24em] text-indigo-100">
						Server Security
					</div>
					<div class="space-y-3">
						<h2 class="max-w-3xl text-2xl font-semibold tracking-tight text-white">
							Access paths, firewall policy, and trust posture for the managed runtime
						</h2>
						<p class="max-w-3xl text-sm leading-6 text-slate-200">
							This page keeps the server security story visible: known access path,
							private network posture, recorded TLS identity, and the firewall
							controls that protect the runtime.
						</p>
					</div>
					<div class="flex flex-wrap gap-3">
						<Button :route="`/servers/${server}/operations`">
							Open Recovery Actions
						</Button>
						<Button :route="`/servers/${server}/health`" variant="outline" theme="gray">
							Back to Health
						</Button>
					</div>
				</div>

				<div class="grid gap-3 sm:grid-cols-2">
					<div
						v-for="card in heroCards"
						:key="card.label"
						class="rounded-2xl border border-white/10 bg-white/10 p-4 backdrop-blur-sm"
					>
						<div class="text-xs uppercase tracking-[0.2em] text-slate-300">
							{{ card.label }}
						</div>
						<div class="mt-2 text-xl font-semibold text-white">
							{{ card.value }}
						</div>
						<div class="mt-2 text-sm leading-6 text-slate-200">
							{{ card.help }}
						</div>
					</div>
				</div>
			</div>
		</section>

		<section class="grid gap-4 xl:grid-cols-[minmax(0,1.35fr)_360px]">
			<div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
				<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
					<div>
						<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
							Security Summary
						</p>
						<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
							Current security posture
						</h3>
						<p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
							These signals summarize whether the managed server has the basic
							network and trust controls we expect before treating it as production-ready.
						</p>
					</div>
					<Badge :label="securityStatus" />
				</div>

				<div class="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
					<div
						v-for="card in summaryCards"
						:key="card.label"
						class="rounded-2xl border border-slate-200 bg-slate-50/70 px-4 py-4"
					>
						<div class="text-xs uppercase tracking-[0.2em] text-slate-500">
							{{ card.label }}
						</div>
						<div class="mt-2 text-lg font-semibold text-slate-900">
							{{ card.value }}
						</div>
						<div class="mt-2 text-sm leading-6 text-slate-600">
							{{ card.help }}
						</div>
					</div>
				</div>
			</div>

			<div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
				<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
					Security Notes
				</p>
				<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
					What to confirm
				</h3>
				<div class="mt-4 space-y-3">
					<div
						v-for="item in securityNotes"
						:key="item.label"
						class="rounded-2xl border border-slate-200 px-4 py-4"
					>
						<div class="flex items-center justify-between gap-3">
							<div class="font-medium text-slate-900">{{ item.label }}</div>
							<Badge :label="item.status" />
						</div>
						<div class="mt-2 text-sm leading-6 text-slate-600">{{ item.detail }}</div>
					</div>
				</div>
			</div>
		</section>

		<section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
			<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
				Recorded Access
			</p>
			<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
				Known runtime identity
			</h3>
			<dl class="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
				<div class="rounded-2xl border border-slate-200 px-4 py-4">
					<dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Public IP</dt>
					<dd class="mt-2 text-base font-semibold text-slate-900">
						{{ serverDoc.ip || "Not recorded" }}
					</dd>
				</div>
				<div class="rounded-2xl border border-slate-200 px-4 py-4">
					<dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Private IP</dt>
					<dd class="mt-2 text-base font-semibold text-slate-900">
						{{ serverDoc.private_ip || "Not recorded" }}
					</dd>
				</div>
				<div class="rounded-2xl border border-slate-200 px-4 py-4">
					<dt class="text-xs uppercase tracking-[0.2em] text-slate-500">Hostname</dt>
					<dd class="mt-2 text-base font-semibold text-slate-900">
						{{ serverDoc.hostname || "Not recorded" }}
					</dd>
				</div>
				<div class="rounded-2xl border border-slate-200 px-4 py-4">
					<dt class="text-xs uppercase tracking-[0.2em] text-slate-500">TLS Domain</dt>
					<dd class="mt-2 text-base font-semibold text-slate-900">
						{{ serverDoc.domain || serverDoc.name || "Not recorded" }}
					</dd>
				</div>
			</dl>
		</section>

		<section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
			<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
				Security Controls
			</p>
			<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
				Control surface
			</h3>
			<div class="mt-5 grid gap-3 md:grid-cols-2">
				<div
					v-for="control in controls"
					:key="control.label"
					class="rounded-2xl border border-slate-200 px-4 py-4"
				>
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-slate-900">{{ control.label }}</div>
						<Badge :label="control.status" />
					</div>
					<div class="mt-2 text-sm leading-6 text-slate-600">{{ control.detail }}</div>
				</div>
			</div>
		</section>

		<section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
						Firewall Policy
					</p>
					<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
						Network control surface
					</h3>
					<p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
						Use the firewall document as the main network policy surface for the
						managed server.
					</p>
				</div>
				<Badge :label="firewallStatus" />
			</div>
			<div class="mt-5">
				<ServerFirewall :id="server" />
			</div>
		</section>
	</div>
</template>

<script>
import { Badge, Button } from "frappe-ui";
import ServerFirewall from "./ServerFirewall.vue";
import { getDocResource } from "../../utils/resource";

export default {
	name: "ManagedServerSecurity",
	components: {
		Badge,
		Button,
		ServerFirewall,
	},
	props: {
		server: {
			type: String,
			required: true,
		},
	},
	computed: {
		serverDoc() {
			return this.$server?.doc || null;
		},
		hasPrivateNetwork() {
			return Boolean(this.serverDoc?.private_ip);
		},
		hasTlsIdentity() {
			return Boolean(this.serverDoc?.domain || this.serverDoc?.name);
		},
		firewallStatus() {
			if (!this.$firewall?.doc) {
				return "Not Loaded";
			}
			return this.$firewall.doc.enabled ? "Enabled" : "Disabled";
		},
		securityStatus() {
			if (!this.serverDoc?.ip) {
				return "Needs Setup";
			}
			if (!this.$firewall?.doc?.enabled) {
				return "Review";
			}
			return "Configured";
		},
		heroCards() {
			return [
				{
					label: "Security State",
					value: this.securityStatus,
					help: "The current read on whether the managed server has the basic access and control posture we expect.",
				},
				{
					label: "Firewall",
					value: this.firewallStatus,
					help: "Whether the server firewall document is currently active for this runtime.",
				},
				{
					label: "Public Access",
					value: this.serverDoc?.ip || "Missing",
					help: "The recorded public address used for managed server access and operator reachability.",
				},
				{
					label: "TLS Identity",
					value: this.hasTlsIdentity ? "Recorded" : "Missing",
					help: "The hostname or domain used to anchor trust, certificates, and production access.",
				},
			];
		},
		summaryCards() {
			return [
				{
					label: "Firewall",
					value: this.firewallStatus,
					help: "Whether the managed server firewall is currently enabled.",
				},
				{
					label: "Public Access Path",
					value: this.serverDoc?.ip || "Missing",
					help: "The recorded public address for managed access.",
				},
				{
					label: "Private Network",
					value: this.hasPrivateNetwork ? "Configured" : "Missing",
					help: "Private network information used by the managed runtime.",
				},
				{
					label: "TLS Identity",
					value: this.hasTlsIdentity ? "Recorded" : "Missing",
					help: "Domain or hostname used for certificate and trust flows.",
				},
			];
		},
		securityNotes() {
			return [
				{
					label: 'Confirm access path',
					status: this.serverDoc?.ip ? 'Recorded' : 'Needed',
					detail: this.serverDoc?.ip
						? 'A public endpoint is recorded, so operators know the expected managed access path.'
						: 'Record the public access address before treating the server as ready for normal operations.',
				},
				{
					label: 'Confirm private addressing',
					status: this.hasPrivateNetwork ? 'Recorded' : 'Recommended',
					detail: this.hasPrivateNetwork
						? 'A private network address is recorded for internal or runtime-only connectivity.'
						: 'Add a private IP when the runtime depends on private network paths.',
				},
				{
					label: 'Confirm trust identity',
					status: this.hasTlsIdentity ? 'Recorded' : 'Needed',
					detail: this.hasTlsIdentity
						? 'A hostname or domain is available for certificate and trust workflows.'
						: 'Record the hostname or domain used for secure production access.',
				},
			];
		},
		controls() {
			return [
				{
					label: "SSH Access Path",
					status: this.serverDoc?.ip ? "Recorded" : "Pending",
					detail: this.serverDoc?.ip
						? "The server has a recorded public endpoint for managed access."
						: "Record the managed server public IP so operators know the access path.",
				},
				{
					label: "Private Addressing",
					status: this.hasPrivateNetwork ? "Recorded" : "Pending",
					detail: this.hasPrivateNetwork
						? "A private IP is recorded for internal runtime or network operations."
						: "Private addressing is not recorded yet.",
				},
				{
					label: "TLS Naming",
					status: this.hasTlsIdentity ? "Ready" : "Pending",
					detail: this.hasTlsIdentity
						? "The server has a hostname or domain that can anchor trust and certificate flows."
						: "Add or confirm the hostname or domain used for secure production access.",
				},
				{
					label: "Firewall Policy",
					status: this.firewallStatus,
					detail:
						this.firewallStatus === "Enabled"
							? "Firewall controls are active. Review rules below when opening or tightening access."
							: "Enable and review firewall rules before treating the production path as secure.",
				},
			];
		},
	},
	created() {
		this.$server = getDocResource({
			doctype: "Server",
			name: this.server,
		});
		this.$firewall = getDocResource({
			doctype: "Server Firewall",
			name: this.server,
		});
	},
};
</script>
