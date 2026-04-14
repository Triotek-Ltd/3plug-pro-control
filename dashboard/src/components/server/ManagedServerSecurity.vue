<template>
	<div class="space-y-5" v-if="serverDoc">
		<section class="rounded-md border bg-white p-5">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">Security</p>
					<h2 class="mt-1 text-xl font-semibold text-gray-900">
						Access, firewall, and trust posture
					</h2>
					<p class="mt-2 max-w-3xl text-sm text-gray-600">
						Keep the managed server secure enough for normal 3plug operations:
						known access path, recorded network identity, and firewall rules that
						match the production runtime.
					</p>
				</div>
				<Badge :label="securityStatus" />
			</div>
		</section>

		<section class="rounded-md border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Security Summary</h3>
			<div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
				<div
					v-for="card in summaryCards"
					:key="card.label"
					class="rounded-md border px-4 py-3"
				>
					<div class="text-sm text-gray-500">{{ card.label }}</div>
					<div class="mt-1 text-lg font-semibold text-gray-900">
						{{ card.value }}
					</div>
					<div class="mt-1 text-xs text-gray-500">{{ card.help }}</div>
				</div>
			</div>
		</section>

		<section class="rounded-md border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Recorded Access</h3>
			<dl class="mt-4 grid gap-4 md:grid-cols-2">
				<div>
					<dt class="text-sm text-gray-500">Public IP</dt>
					<dd class="mt-1 text-sm font-medium text-gray-900">
						{{ serverDoc.ip || "Not recorded" }}
					</dd>
				</div>
				<div>
					<dt class="text-sm text-gray-500">Private IP</dt>
					<dd class="mt-1 text-sm font-medium text-gray-900">
						{{ serverDoc.private_ip || "Not recorded" }}
					</dd>
				</div>
				<div>
					<dt class="text-sm text-gray-500">Hostname</dt>
					<dd class="mt-1 text-sm font-medium text-gray-900">
						{{ serverDoc.hostname || "Not recorded" }}
					</dd>
				</div>
				<div>
					<dt class="text-sm text-gray-500">TLS Domain</dt>
					<dd class="mt-1 text-sm font-medium text-gray-900">
						{{ serverDoc.domain || serverDoc.name || "Not recorded" }}
					</dd>
				</div>
			</dl>
		</section>

		<section class="rounded-md border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Security Controls</h3>
			<div class="mt-4 grid gap-3 md:grid-cols-2">
				<div
					v-for="control in controls"
					:key="control.label"
					class="rounded-md border px-4 py-3"
				>
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-gray-900">{{ control.label }}</div>
						<Badge :label="control.status" />
					</div>
					<div class="mt-1 text-sm text-gray-600">{{ control.detail }}</div>
				</div>
			</div>
		</section>

		<section class="rounded-md border bg-white p-5">
			<div class="flex items-center justify-between gap-4">
				<div>
					<h3 class="text-lg font-semibold text-gray-900">Firewall Rules</h3>
					<p class="mt-1 text-sm text-gray-600">
						Use the existing server firewall document as the main network
						control surface for this managed server.
					</p>
				</div>
				<Badge :label="firewallStatus" />
			</div>
			<div class="mt-4">
				<ServerFirewall :id="server" />
			</div>
		</section>
	</div>
</template>

<script>
import { Badge } from "frappe-ui";
import ServerFirewall from "./ServerFirewall.vue";
import { getDocResource } from "../../utils/resource";

export default {
	name: "ManagedServerSecurity",
	components: {
		Badge,
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
						: "Add or confirm the hostname/domain used for secure production access.",
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
