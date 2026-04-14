<template>
	<div class="space-y-5" v-if="serverDoc">
		<section class="rounded-md border bg-white p-5">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">Operations</p>
					<h2 class="mt-1 text-xl font-semibold text-gray-900">
						Runtime actions and recovery
					</h2>
					<p class="mt-2 max-w-3xl text-sm text-gray-600">
						Run the operational actions that keep the managed server usable:
						restarts, cleanup, certificates, and other actions already exposed
						by the underlying server records.
					</p>
				</div>
				<Badge :label="operationsStatus" />
			</div>
		</section>

		<section class="rounded-md border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Operations Summary</h3>
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
			<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
				<div>
					<h3 class="text-lg font-semibold text-gray-900">Action Flow</h3>
					<p class="mt-1 text-sm text-gray-600">
						Use the existing action engine while we keep narrowing the server
						model to the one-managed-server product shape.
					</p>
				</div>
				<div class="flex flex-wrap gap-2">
					<Button :route="`/servers/${server}/jobs`" variant="outline">
						Open Jobs
					</Button>
					<Button :route="`/servers/${server}/plays`" variant="outline">
						Open Plays
					</Button>
				</div>
			</div>
			<div class="mt-4">
				<ServerActions :server="server" />
			</div>
		</section>
	</div>
</template>

<script>
import { Badge, Button } from "frappe-ui";
import ServerActions from "./ServerActions.vue";
import { getDocResource } from "../../utils/resource";

export default {
	name: "ManagedServerOperations",
	components: {
		Badge,
		Button,
		ServerActions,
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
		operationsStatus() {
			if (this.serverDoc?.status === "Active") {
				return "Ready";
			}
			if (this.serverDoc?.status) {
				return this.serverDoc.status;
			}
			return "Unknown";
		},
		summaryCards() {
			const actions = this.serverDoc?.actions || [];
			return [
				{
					label: "Server Status",
					value: this.serverDoc?.status || "Unknown",
					help: "The current state of the managed server record.",
				},
				{
					label: "Available Actions",
					value: `${actions.length}`,
					help: "Actions directly exposed on the main server record.",
				},
				{
					label: "Bench Source",
					value: this.serverDoc?.is_self_hosted ? "Managed" : "Cloud",
					help: "This operations surface is optimized for the managed Linux server flow.",
				},
				{
					label: "Runbook",
					value: "Jobs + Plays",
					help: "Use execution traces to confirm what changed after an action runs.",
				},
			];
		},
	},
	created() {
		this.$server = getDocResource({
			doctype: "Server",
			name: this.server,
		});
	},
};
</script>
