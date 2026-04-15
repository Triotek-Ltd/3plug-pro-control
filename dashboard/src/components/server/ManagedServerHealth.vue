<template>
	<div class="space-y-6" v-if="serverDoc">
		<section
			class="overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950 text-white shadow-sm"
		>
			<div class="grid gap-6 px-6 py-6 lg:grid-cols-[minmax(0,1.4fr)_420px] lg:px-8">
				<div class="space-y-4">
					<div class="inline-flex w-fit items-center rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium uppercase tracking-[0.24em] text-emerald-100">
						Server Health
					</div>
					<div class="space-y-3">
						<h2 class="max-w-3xl text-2xl font-semibold tracking-tight text-white">
							Production readiness, service health, and live runtime verification
						</h2>
						<p class="max-w-3xl text-sm leading-6 text-slate-200">
							This is the live health view for the managed server. Use it to confirm
							that the runtime is reachable, production services are healthy, and
							the latest checks support the next server or bench action.
						</p>
					</div>
					<div class="flex flex-wrap gap-3">
						<Button
							:loading="$resources.runProductionChecks.loading"
							@click="$resources.runProductionChecks.submit()"
						>
							Run Production Checks
						</Button>
						<Button :route="`/servers/${server}/operations`" variant="outline" theme="gray">
							Open Recovery Actions
						</Button>
						<Button :route="`/servers/${server}/bench-onboarding`" variant="ghost">
							Continue Bench Onboarding
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

		<section class="grid gap-4 xl:grid-cols-[minmax(0,1.4fr)_360px]">
			<div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
				<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
					<div>
						<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
							Health Summary
						</p>
						<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
							Current production state
						</h3>
						<p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
							The summary below turns the latest runtime inspection into operator
							signals you can act on quickly.
						</p>
					</div>
					<Badge :label="productionStatus.label" />
				</div>

				<div class="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
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
					Quick Decisions
				</p>
				<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
					What to do next
				</h3>
				<div class="mt-4 space-y-3">
					<div
						v-for="item in decisionCards"
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
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
						Operational Checks
					</p>
					<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
						Service and runtime inspection
					</h3>
					<p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
						These checks come from runtime inspection of services, process ownership,
						and recorded storage state on the managed server.
					</p>
				</div>
				<Button :route="`/servers/${server}/security`" variant="outline">
					Open Security Posture
				</Button>
			</div>

			<div class="mt-5 grid gap-3 md:grid-cols-2">
				<div
					v-for="check in healthChecks"
					:key="check.label"
					class="rounded-2xl border border-slate-200 px-4 py-4"
				>
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-slate-900">{{ check.label }}</div>
						<Badge :label="check.status" />
					</div>
					<div class="mt-2 text-sm leading-6 text-slate-600">{{ check.detail }}</div>
				</div>
			</div>
		</section>

		<section class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
						Recent Execution
					</p>
					<h3 class="mt-2 text-xl font-semibold tracking-tight text-slate-900">
						Jobs and plays tied to this server
					</h3>
					<p class="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
						Use the latest execution trail to confirm whether the runtime is stable
						or whether a recent action introduced the current issue.
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

			<div class="mt-5 grid gap-4 lg:grid-cols-2">
				<div class="rounded-2xl border border-slate-200 px-4 py-4">
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-slate-900">Recent Jobs</div>
						<Badge :label="`${recentJobs.length}`" />
					</div>
					<div v-if="recentJobs.length" class="mt-4 space-y-2">
						<RouterLink
							v-for="job in recentJobs.slice(0, 5)"
							:key="job.name"
							:to="{ name: 'Server Job', params: { id: job.name } }"
							class="block rounded-2xl border border-slate-200 px-3 py-3 text-sm transition hover:border-slate-400"
						>
							<div class="flex items-center justify-between gap-2">
								<span class="font-medium text-slate-900">{{ job.job_type }}</span>
								<Badge :label="job.status || 'Unknown'" />
							</div>
							<div class="mt-2 text-xs uppercase tracking-[0.18em] text-slate-500">
								Resource
							</div>
							<div class="mt-1 text-sm text-slate-600">
								{{ job.site || job.bench || job.server || 'No target recorded' }}
							</div>
						</RouterLink>
					</div>
					<p v-else class="mt-4 text-sm text-slate-500">No related jobs recorded yet.</p>
				</div>

				<div class="rounded-2xl border border-slate-200 px-4 py-4">
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-slate-900">Recent Plays</div>
						<Badge :label="`${recentPlays.length}`" />
					</div>
					<div v-if="recentPlays.length" class="mt-4 space-y-2">
						<RouterLink
							v-for="play in recentPlays.slice(0, 5)"
							:key="play.name"
							:to="{ name: 'Server Play', params: { id: play.name } }"
							class="block rounded-2xl border border-slate-200 px-3 py-3 text-sm transition hover:border-slate-400"
						>
							<div class="flex items-center justify-between gap-2">
								<span class="font-medium text-slate-900">{{ play.play }}</span>
								<Badge :label="play.status || 'Unknown'" />
							</div>
							<div class="mt-2 text-xs uppercase tracking-[0.18em] text-slate-500">
								Server
							</div>
							<div class="mt-1 text-sm text-slate-600">{{ play.server }}</div>
						</RouterLink>
					</div>
					<p v-else class="mt-4 text-sm text-slate-500">No related plays recorded yet.</p>
				</div>
			</div>
		</section>
	</div>
</template>

<script>
import { Badge, Button } from 'frappe-ui';
import { getDocResource } from '../../utils/resource';

export default {
	name: 'ManagedServerHealth',
	components: {
		Badge,
		Button,
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
	},
	computed: {
		serverDoc() {
			return this.$server?.doc || null;
		},
		recentJobs() {
			return this.state.recent_jobs || [];
		},
		recentPlays() {
			return this.state.recent_plays || [];
		},
		hasManagedSites() {
			return Boolean(this.state.sites?.some((site) => site.site));
		},
		failedExecutionCount() {
			return [...this.recentJobs, ...this.recentPlays].filter((entry) =>
				['Failed', 'Failure', 'Error', 'Broken'].includes(entry.status),
			).length;
		},
		failedProductionChecks() {
			return this.healthChecks.filter((check) => ['Failed', 'Investigate'].includes(check.status));
		},
		healthyCheckCount() {
			return this.healthChecks.filter((check) => ['Ready', 'Clear', 'Configured'].includes(check.status)).length;
		},
		lastCheckedLabel() {
			const value =
				this.state.production_checks?.checked_at || this.state.production_checks_updated_at;
			if (!value) {
				return 'Never';
			}
			return new Date(value).toLocaleString();
		},
		productionStatus() {
			if (this.failedProductionChecks.length > 0 || this.failedExecutionCount > 0) {
				return { label: 'Needs Attention' };
			}
			if (this.serverDoc?.status !== 'Active' || this.state.status === 'Unreachable') {
				return { label: 'Degraded' };
			}
			if (this.state.release_group && this.hasManagedSites) {
				return { label: 'Production Ready' };
			}
			return { label: 'Onboarding In Progress' };
		},
		heroCards() {
			return [
				{
					label: 'Production State',
					value: this.productionStatus.label,
					help: 'The best current reading of whether the server can support normal managed work.',
				},
				{
					label: 'Healthy Checks',
					value: `${this.healthyCheckCount}/${this.healthChecks.length || 0}`,
					help: 'Checks currently passing in the latest production inspection snapshot.',
				},
				{
					label: 'Runtime User',
					value:
						this.state.production_checks?.runtime_user?.value ||
						this.state.machine_facts?.runtime_user ||
						'Unknown',
					help: 'The detected owner of the runtime processes and production paths.',
				},
				{
					label: 'Last Verified',
					value: this.lastCheckedLabel,
					help: 'The last time 3plug recorded a fresh production verification snapshot.',
				},
			];
		},
		summaryCards() {
			return [
				{
					label: 'Server Status',
					value: this.serverDoc?.status || 'Unknown',
					help: 'The current managed server record status.',
				},
				{
					label: 'Execution Failures',
					value: `${this.failedExecutionCount}`,
					help: 'Recent jobs or plays that need review before you trust the runtime.',
				},
				{
					label: 'Managed Bench',
					value: this.state.release_group || 'Pending',
					help: 'The bench currently associated with this managed server path.',
				},
				{
					label: 'Managed Sites',
					value: this.hasManagedSites ? `${this.state.sites.length}` : '0',
					help: 'Managed site records currently attached to the bench on this server.',
				},
				{
					label: 'Checks Updated',
					value: this.lastCheckedLabel,
					help: 'The timestamp of the latest health inspection on the managed runtime.',
				},
				{
					label: 'Access Path',
					value: this.serverDoc?.ip || 'Missing',
					help: 'The current public access path recorded for the managed runtime.',
				},
			];
		},
		decisionCards() {
			return [
				{
					label: 'Stabilize Runtime',
					status: this.failedProductionChecks.length ? 'Do This Now' : 'Clear',
					detail: this.failedProductionChecks.length
						? 'One or more production checks failed. Move into Operations and use the targeted restart or recovery actions.'
						: 'No failed production checks are currently blocking normal server work.',
				},
				{
					label: 'Finish Onboarding',
					status: this.state.release_group && this.hasManagedSites ? 'Complete' : 'Pending',
					detail: this.state.release_group && this.hasManagedSites
						? 'The server already has a managed bench and site records in place.'
						: 'Continue bench onboarding and site creation before treating the server as fully in service.',
				},
				{
					label: 'Review Security',
					status: this.serverDoc?.domain || this.serverDoc?.private_ip ? 'Recommended' : 'Needed',
					detail: 'Confirm firewall, access, and recorded network identity before opening the runtime to wider use.',
				},
			];
		},
		healthChecks() {
			if (this.state.production_checks?.checks?.length) {
				return this.state.production_checks.checks;
			}
			return [
				{
					label: 'Reachability',
					status: this.state.status === 'Unreachable' ? 'Failed' : this.serverDoc?.status || 'Unknown',
					detail:
						this.state.status === 'Unreachable'
							? 'The managed Linux server is not currently reachable through the known path.'
							: 'The server record is reachable enough for the managed flow to continue.',
				},
				{
					label: 'Bench Source',
					status: this.state.existing_bench_present && this.state.bench_directory ? 'Configured' : 'Pending',
					detail: this.state.bench_directory || 'Bench path not recorded yet.',
				},
				{
					label: 'Managed Bench',
					status: this.state.release_group ? 'Ready' : 'Pending',
					detail:
						this.state.release_group || 'No managed bench has been created from the discovered runtime yet.',
				},
				{
					label: 'Managed Sites',
					status: this.hasManagedSites ? 'Ready' : 'Pending',
					detail: this.hasManagedSites
						? 'Managed site records exist for this server path.'
						: 'Managed site records have not been created yet.',
				},
				{
					label: 'Execution Trace',
					status: this.failedExecutionCount > 0 ? 'Investigate' : 'Clear',
					detail:
						this.failedExecutionCount > 0
							? 'Recent jobs or plays include failures that should be reviewed before calling production healthy.'
							: 'No recent failures were found in the visible server jobs and plays.',
				},
			];
		},
	},
	created() {
		this.$server = getDocResource({
			doctype: 'Server',
			name: this.server,
		});
	},
};
</script>
