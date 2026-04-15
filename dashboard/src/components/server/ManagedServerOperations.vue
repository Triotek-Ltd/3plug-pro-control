<template>
	<div class="space-y-6" v-if="serverDoc">
		<section
			class="overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-950 via-slate-900 to-cyan-950 text-white shadow-sm"
		>
			<div class="grid gap-6 px-6 py-6 lg:grid-cols-[minmax(0,1.35fr)_420px] lg:px-8">
				<div class="space-y-4">
					<div class="inline-flex w-fit items-center rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.24em] text-cyan-100">
						Server Operations
					</div>
					<div class="space-y-3">
						<h2 class="max-w-3xl text-2xl font-semibold tracking-tight text-white">
							Runtime actions, targeted recovery, and guided operator response
						</h2>
						<p class="max-w-3xl text-sm leading-6 text-slate-200">
							Use this page to rerun production checks, recover failing services,
							and move from diagnosis to action without leaving the managed server
							flow.
						</p>
					</div>
					<div class="flex flex-wrap gap-3">
						<Button
							:loading="$resources.runProductionChecks.loading"
							@click="$resources.runProductionChecks.submit()"
						>
							Run Production Checks
						</Button>
						<Button
							:loading="$resources.restartAll.loading"
							@click="$resources.restartAll.submit()"
							variant="outline"
							theme="gray"
						>
							Restart Production Services
						</Button>
						<Button :route="`/servers/${server}/health`" variant="ghost">
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

		<section class="grid gap-4 xl:grid-cols-[minmax(0,1.45fr)_360px]">
			<div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
				<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
					<div>
						<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
							Recovery Actions
						</p>
						<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
							Recommended runtime actions
						</h3>
						<p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
							These actions follow the latest runtime checks and the common
							recovery paths we expect operators to take first.
						</p>
					</div>
					<Badge :label="operationsStatus" />
				</div>

				<div class="mt-5 grid gap-3 md:grid-cols-2">
					<div
						v-for="action in recommendedActions"
						:key="action.label"
						class="rounded-2xl border border-slate-200 px-4 py-4"
					>
						<div class="flex items-center justify-between gap-3">
							<div class="font-medium text-slate-900">{{ action.label }}</div>
							<Badge :label="action.priority" />
						</div>
						<div class="mt-2 text-sm leading-6 text-slate-600">{{ action.detail }}</div>
						<Button
							class="mt-4"
							variant="outline"
							:loading="loadingFor(action.scope)"
							@click="runRuntimeAction(action.scope)"
						>
							{{ action.buttonLabel }}
						</Button>
					</div>
				</div>
			</div>

			<div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
				<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
					Runbook
				</p>
				<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
					Operator flow
				</h3>
				<div class="mt-4 space-y-3">
					<div
						v-for="step in runbookSteps"
						:key="step.label"
						class="rounded-2xl border border-slate-200 px-4 py-4"
					>
						<div class="flex items-center gap-3">
							<div class="flex h-8 w-8 items-center justify-center rounded-full bg-slate-900 text-sm font-semibold text-white">
								{{ step.index }}
							</div>
							<div class="font-medium text-slate-900">{{ step.label }}</div>
						</div>
						<div class="mt-3 text-sm leading-6 text-slate-600">{{ step.detail }}</div>
					</div>
				</div>
			</div>
		</section>

		<section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
			<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
				Operations Summary
			</p>
			<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
				Current response context
			</h3>
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
		</section>

		<section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
						Advanced Actions
					</p>
					<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
						Full action engine
					</h3>
					<p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
						Use the full action engine when you need deeper runtime actions that
						are already exposed by the server records.
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
			<div class="mt-5">
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
	data() {
		return {
			state: {},
		};
	},
	resources: {
		managedServerState() {
			return {
				url: 'press.api.selfhosted.get_bench_onboarding_state',
				auto: true,
				makeParams: () => ({
					server: this.server,
				}),
				onSuccess: (data) => {
					this.state = data || {};
				},
			};
		},
		runProductionChecks() {
			return {
				url: 'press.api.selfhosted.run_managed_server_production_checks',
				auto: false,
				makeParams: () => ({
					server: this.server,
				}),
				onSuccess: (data) => {
					this.state = data || {};
				},
			};
		},
		restartAll() {
			return this.makeRuntimeActionResource('all');
		},
		restartNginx() {
			return this.makeRuntimeActionResource('nginx');
		},
		restartRedis() {
			return this.makeRuntimeActionResource('redis');
		},
		restartWorkers() {
			return this.makeRuntimeActionResource('workers');
		},
	},
	methods: {
		makeRuntimeActionResource(operationScope) {
			return {
				url: 'press.api.selfhosted.restart_managed_server_runtime',
				auto: false,
				makeParams: () => ({
					server: this.server,
					operation_scope: operationScope,
				}),
				onSuccess: (data) => {
					this.state = data || {};
				},
			};
		},
		runRuntimeAction(scope) {
			const resources = {
				all: this.$resources.restartAll,
				nginx: this.$resources.restartNginx,
				redis: this.$resources.restartRedis,
				workers: this.$resources.restartWorkers,
			};
			resources[scope]?.submit();
		},
		loadingFor(scope) {
			const resources = {
				all: this.$resources.restartAll,
				nginx: this.$resources.restartNginx,
				redis: this.$resources.restartRedis,
				workers: this.$resources.restartWorkers,
			};
			return Boolean(resources[scope]?.loading);
		},
	},
	computed: {
		serverDoc() {
			return this.$server?.doc || null;
		},
		productionChecks() {
			return this.state.production_checks?.checks || [];
		},
		failedChecks() {
			return this.productionChecks.filter((check) => check.status === 'Failed');
		},
		operationsStatus() {
			if (this.failedChecks.length) {
				return "Needs Attention";
			}
			if (this.serverDoc?.status === "Active") {
				return "Ready";
			}
			if (this.serverDoc?.status) {
				return this.serverDoc.status;
			}
			return "Unknown";
		},
		heroCards() {
			const actions = this.serverDoc?.actions || [];
			return [
				{
					label: "Operations State",
					value: this.operationsStatus,
					help: "Whether the runtime currently needs recovery or is ready for normal managed work.",
				},
				{
					label: "Failed Checks",
					value: `${this.failedChecks.length}`,
					help: "Checks currently indicating that production services need operator attention.",
				},
				{
					label: "Action Surface",
					value: `${actions.length + 4}`,
					help: "Server record actions plus the targeted runtime recovery controls added to this page.",
				},
				{
					label: "Runbook",
					value: "Checks -> Fix -> Verify",
					help: "Use the same response loop every time to make job and play logs easier to trust.",
				},
			];
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
					value: `${actions.length + 4}`,
					help: "Runtime recovery actions plus the underlying server action engine.",
				},
				{
					label: "Latest Runtime User",
					value:
						this.state.production_checks?.runtime_user?.value ||
						this.state.machine_facts?.runtime_user ||
						"Unknown",
					help: "The current runtime owner that should line up with the live process state.",
				},
				{
					label: "Latest Check Snapshot",
					value:
						this.state.production_checks?.checked_at ||
						this.state.production_checks_updated_at ||
						"Never",
					help: "The latest check snapshot that informs the recommendations above.",
				},
			];
		},
		recommendedActions() {
			const failedLabels = new Set(this.failedChecks.map((check) => check.label));

			return [
				{
					label: 'Restart NGINX',
					scope: 'nginx',
					priority: failedLabels.has('NGINX') ? 'Recommended' : 'Available',
					buttonLabel: 'Restart NGINX',
					detail: failedLabels.has('NGINX')
						? 'NGINX failed the latest production check and should be restarted first.'
						: 'Use this when the web entrypoint or proxy layer needs a targeted reset.',
				},
				{
					label: 'Restart Redis',
					scope: 'redis',
					priority: failedLabels.has('Redis') ? 'Recommended' : 'Available',
					buttonLabel: 'Restart Redis',
					detail: failedLabels.has('Redis')
						? 'Redis failed the latest production check and should be recovered directly.'
						: 'Use this when queue or cache traffic is stale or runtime tasks are stuck.',
				},
				{
					label: 'Restart Workers',
					scope: 'workers',
					priority:
						failedLabels.has('Workers') || failedLabels.has('Scheduler')
							? 'Recommended'
							: 'Available',
					buttonLabel: 'Restart Workers',
					detail:
						failedLabels.has('Workers') || failedLabels.has('Scheduler')
							? 'Worker or scheduler processes failed the latest production check.'
							: 'Use this when background execution, scheduling, or queue processing is not moving.',
				},
				{
					label: 'Restart Production Services',
					scope: 'all',
					priority: failedLabels.size > 1 ? 'High Priority' : 'Available',
					buttonLabel: 'Restart All',
					detail: failedLabels.size > 1
						? 'Multiple checks failed together. A full runtime restart is the fastest coordinated recovery move.'
						: 'Use this when you intentionally want to reset the whole production stack.',
				},
			];
		},
		runbookSteps() {
			return [
				{
					index: 1,
					label: 'Inspect the current checks',
					detail: 'Start with the latest health snapshot so you know whether the issue is web, queue, workers, or a broader runtime problem.',
				},
				{
					index: 2,
					label: 'Apply the narrowest safe action',
					detail: 'Prefer targeted restarts for NGINX, Redis, or workers before using a full production restart.',
				},
				{
					index: 3,
					label: 'Review jobs and plays',
					detail: 'Open the related execution trail to see whether the issue came from a recent deploy, patch run, or operator action.',
				},
				{
					index: 4,
					label: 'Rerun checks and confirm recovery',
					detail: 'Always rerun production checks after a fix so the runtime returns to a clearly verified state.',
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
