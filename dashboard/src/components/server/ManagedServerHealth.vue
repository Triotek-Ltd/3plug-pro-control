<template>
	<div class="space-y-5" v-if="serverDoc">
		<section class="rounded-md border bg-white p-5">
			<div class="flex items-start justify-between gap-4">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">Health</p>
					<h2 class="mt-1 text-xl font-semibold text-gray-900">
						Server health and production readiness
					</h2>
					<p class="mt-2 max-w-3xl text-sm text-gray-600">
						Track whether the managed Linux server is reachable, whether the bench
						onboarding chain is healthy, and whether recent jobs or plays suggest
						a broken production path.
					</p>
				</div>
				<Badge :label="productionStatus.label" />
			</div>
		</section>

		<section class="rounded-md border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Status Summary</h3>
			<div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
				<div v-for="card in summaryCards" :key="card.label" class="rounded-md border px-4 py-3">
					<div class="text-sm text-gray-500">{{ card.label }}</div>
					<div class="mt-1 text-lg font-semibold text-gray-900">{{ card.value }}</div>
					<div class="mt-1 text-xs text-gray-500">{{ card.help }}</div>
				</div>
			</div>
		</section>

		<section class="rounded-md border bg-white p-5">
			<div class="flex items-center justify-between gap-4">
				<div>
					<h3 class="text-lg font-semibold text-gray-900">Operational Checks</h3>
					<p class="mt-1 text-sm text-gray-600">
						These checks reflect the current managed-server onboarding and execution spine.
					</p>
				</div>
				<Button :route="`/servers/${server}/bench-onboarding`" variant="outline">
					Open Bench Onboarding
				</Button>
			</div>
			<div class="mt-4 grid gap-3 md:grid-cols-2">
				<div v-for="check in healthChecks" :key="check.label" class="rounded-md border px-4 py-3">
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-gray-900">{{ check.label }}</div>
						<Badge :label="check.status" />
					</div>
					<div class="mt-1 text-sm text-gray-600">{{ check.detail }}</div>
				</div>
			</div>
		</section>

		<section class="rounded-md border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Recent Execution</h3>
			<div class="mt-4 grid gap-4 lg:grid-cols-2">
				<div class="rounded-md border px-4 py-3">
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-gray-900">Recent Jobs</div>
						<Badge :label="`${recentJobs.length}`" />
					</div>
					<div v-if="recentJobs.length" class="mt-3 space-y-2">
						<RouterLink
							v-for="job in recentJobs.slice(0, 5)"
							:key="job.name"
							:to="{ name: 'Server Job', params: { id: job.name } }"
							class="block rounded-md border px-3 py-2 text-sm transition hover:border-gray-400"
						>
							<div class="flex items-center justify-between gap-2">
								<span class="font-medium text-gray-900">{{ job.job_type }}</span>
								<Badge :label="job.status || 'Unknown'" />
							</div>
							<div class="mt-1 text-xs text-gray-500">
								{{ job.site || job.bench || job.server || 'No target recorded' }}
							</div>
						</RouterLink>
					</div>
					<p v-else class="mt-3 text-sm text-gray-500">No related jobs recorded yet.</p>
				</div>

				<div class="rounded-md border px-4 py-3">
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-gray-900">Recent Plays</div>
						<Badge :label="`${recentPlays.length}`" />
					</div>
					<div v-if="recentPlays.length" class="mt-3 space-y-2">
						<RouterLink
							v-for="play in recentPlays.slice(0, 5)"
							:key="play.name"
							:to="{ name: 'Server Play', params: { id: play.name } }"
							class="block rounded-md border px-3 py-2 text-sm transition hover:border-gray-400"
						>
							<div class="flex items-center justify-between gap-2">
								<span class="font-medium text-gray-900">{{ play.play }}</span>
								<Badge :label="play.status || 'Unknown'" />
							</div>
							<div class="mt-1 text-xs text-gray-500">{{ play.server }}</div>
						</RouterLink>
					</div>
					<p v-else class="mt-3 text-sm text-gray-500">No related plays recorded yet.</p>
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
		productionStatus() {
			if (this.failedExecutionCount > 0) {
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
		summaryCards() {
			return [
				{
					label: 'Server Status',
					value: this.serverDoc?.status || 'Unknown',
					help: 'The current managed server record status.',
				},
				{
					label: 'Production State',
					value: this.productionStatus.label,
					help: 'Whether the server is ready for normal managed operations.',
				},
				{
					label: 'Recent Failures',
					value: `${this.failedExecutionCount}`,
					help: 'Failed jobs and plays visible from the managed server flow.',
				},
				{
					label: 'Managed Sites',
					value: this.hasManagedSites ? 'Ready' : 'Pending',
					help: 'Whether discovered sites have been turned into managed site records.',
				},
			];
		},
		healthChecks() {
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
