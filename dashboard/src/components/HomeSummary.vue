<template>
	<div class="space-y-6">
		<section class="rounded-2xl border bg-white p-6">
			<div class="flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
				<div class="max-w-3xl">
					<p class="text-sm uppercase tracking-wide text-gray-500">
						3plug Command Center
					</p>
					<h2 class="mt-1 text-2xl font-semibold text-gray-900">
						Operate the server, benches, sites, and recovery flow from one place
					</h2>
					<p class="mt-2 text-sm text-gray-600">
						This is the operator-facing control surface for the managed Linux
						server, its benches, its sites, and the jobs and forensic trails
						behind every action.
					</p>
				</div>
				<div class="grid gap-2 sm:grid-cols-2 xl:w-[28rem]">
					<Button variant="solid" :route="primaryAction.route">
						{{ primaryAction.label }}
					</Button>
					<Button :route="'/servers'">Review server health</Button>
					<Button :route="'/jobs'">Open jobs</Button>
					<Button :route="'/forensics/signals'">Review incidents</Button>
				</div>
			</div>
		</section>

		<section class="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
			<div
				v-for="card in summaryCards"
				:key="card.label"
				class="rounded-2xl border bg-white p-5"
			>
				<p class="text-sm text-gray-500">{{ card.label }}</p>
				<p class="mt-3 text-3xl font-semibold text-gray-900">
					{{ card.value }}
				</p>
				<p class="mt-2 text-sm text-gray-600">{{ card.helper }}</p>
			</div>
		</section>

		<div class="grid gap-6 xl:grid-cols-[1.2fr_minmax(0,1fr)]">
			<div class="space-y-6">
				<section class="rounded-2xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">
								What needs attention next
							</h3>
							<p class="mt-1 text-sm text-gray-600">
								Keep the real server to bench to site workflow moving forward.
							</p>
						</div>
						<Button :route="primaryAction.route" variant="ghost">
							{{ primaryAction.label }}
						</Button>
					</div>
					<div class="mt-4 grid gap-3 md:grid-cols-2">
						<div
							v-for="item in actionBoard"
							:key="item.label"
							class="rounded-xl border px-4 py-4"
						>
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">{{ item.label }}</div>
								<Badge :label="item.status" />
							</div>
							<p class="mt-2 text-sm text-gray-600">{{ item.detail }}</p>
							<Button v-if="item.route" class="mt-3" size="sm" :route="item.route">
								{{ item.action }}
							</Button>
						</div>
					</div>
				</section>

				<section class="rounded-2xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Operational inventory</h3>
							<p class="mt-1 text-sm text-gray-600">
								The current managed runtime footprint across servers, benches, and
								sites.
							</p>
						</div>
					</div>
					<div class="mt-4 grid gap-4 lg:grid-cols-3">
						<div class="rounded-xl border p-4">
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">Servers</div>
								<Button size="sm" variant="ghost" :route="'/servers'">Open</Button>
							</div>
							<div v-if="servers.length" class="mt-3 space-y-2">
								<router-link
									v-for="server in servers.slice(0, 3)"
									:key="server.name"
									:to="`/servers/${server.name}`"
									class="block rounded-lg border px-3 py-3 transition hover:bg-gray-50"
								>
									<div class="flex items-center justify-between gap-2">
										<span class="font-medium text-gray-900">
											{{ server.title || server.name }}
										</span>
										<Badge :label="server.status || 'Unknown'" />
									</div>
									<div class="mt-1 text-xs text-gray-500">
										{{ server.ip || server.name }}
									</div>
								</router-link>
							</div>
							<p v-else class="mt-3 text-sm text-gray-500">
								No managed servers yet.
							</p>
						</div>

						<div class="rounded-xl border p-4">
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">Benches</div>
								<Button size="sm" variant="ghost" :route="'/benches'">Open</Button>
							</div>
							<div v-if="benches.length" class="mt-3 space-y-2">
								<router-link
									v-for="bench in benches.slice(0, 3)"
									:key="bench.name"
									:to="`/benches/${bench.name}`"
									class="block rounded-lg border px-3 py-3 transition hover:bg-gray-50"
								>
									<div class="flex items-center justify-between gap-2">
										<span class="font-medium text-gray-900">{{ bench.name }}</span>
										<Badge :label="bench.status || 'Unknown'" />
									</div>
									<div class="mt-1 text-xs text-gray-500">
										{{ bench.server || 'No server recorded' }}
									</div>
								</router-link>
							</div>
							<p v-else class="mt-3 text-sm text-gray-500">No benches yet.</p>
						</div>

						<div class="rounded-xl border p-4">
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">Sites</div>
								<Button size="sm" variant="ghost" :route="'/sites'">Open</Button>
							</div>
							<div v-if="sites.length" class="mt-3 space-y-2">
								<router-link
									v-for="site in sites.slice(0, 3)"
									:key="site.name"
									:to="`/sites/${site.name}`"
									class="block rounded-lg border px-3 py-3 transition hover:bg-gray-50"
								>
									<div class="flex items-center justify-between gap-2">
										<span class="font-medium text-gray-900">
											{{ site.host_name || site.name }}
										</span>
										<Badge :label="site.status || 'Unknown'" />
									</div>
									<div class="mt-1 text-xs text-gray-500">
										{{ site.bench || site.name }}
									</div>
								</router-link>
							</div>
							<p v-else class="mt-3 text-sm text-gray-500">No managed sites yet.</p>
						</div>
					</div>
				</section>
			</div>

			<div class="space-y-6">
				<section class="rounded-2xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Operator scripts</h3>
							<p class="mt-1 text-sm text-gray-600">
								Direct paths into the actions we expect operators to use most.
							</p>
						</div>
					</div>
					<div class="mt-4 grid gap-3">
						<router-link
							v-for="script in operatorScripts"
							:key="script.label"
							:to="script.route"
							class="block rounded-xl border px-4 py-4 transition hover:bg-gray-50"
						>
							<div class="font-medium text-gray-900">{{ script.label }}</div>
							<div class="mt-1 text-sm text-gray-600">{{ script.detail }}</div>
						</router-link>
					</div>
				</section>

				<section class="rounded-2xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Execution</h3>
							<p class="mt-1 text-sm text-gray-600">
								Tracked jobs remain the primary execution trail for this product.
							</p>
						</div>
						<Button variant="ghost" :route="'/jobs'">Open jobs</Button>
					</div>
					<div class="mt-4 grid gap-3 sm:grid-cols-3">
						<div class="rounded-xl bg-gray-50 px-3 py-3">
							<p class="text-xs uppercase tracking-wide text-gray-500">Server Jobs</p>
							<p class="mt-2 text-xl font-semibold text-gray-900">
								{{ jobScopeSummary.server_jobs || 0 }}
							</p>
						</div>
						<div class="rounded-xl bg-gray-50 px-3 py-3">
							<p class="text-xs uppercase tracking-wide text-gray-500">Bench Jobs</p>
							<p class="mt-2 text-xl font-semibold text-gray-900">
								{{ jobScopeSummary.bench_jobs || 0 }}
							</p>
						</div>
						<div class="rounded-xl bg-gray-50 px-3 py-3">
							<p class="text-xs uppercase tracking-wide text-gray-500">Site Jobs</p>
							<p class="mt-2 text-xl font-semibold text-gray-900">
								{{ jobScopeSummary.site_jobs || 0 }}
							</p>
						</div>
					</div>
					<div v-if="recentJobs.length" class="mt-4 space-y-3">
						<component
							v-for="job in recentJobs.slice(0, 5)"
							:key="job.name"
							:is="jobRoute(job) ? 'router-link' : 'div'"
							:to="jobRoute(job)"
							class="block rounded-xl border px-4 py-3 transition hover:bg-gray-50"
						>
							<div class="flex items-center justify-between gap-3">
								<div>
									<p class="font-medium text-gray-900">{{ job.job_type }}</p>
									<p class="mt-1 text-sm text-gray-600">
										{{ job.site || job.bench || job.server || 'No target recorded' }}
									</p>
								</div>
								<Badge :label="job.status || 'Unknown'" />
							</div>
							<p class="mt-2 text-xs text-gray-500">
								{{ formatTimestamp(job.creation) }}
							</p>
						</component>
					</div>
					<p v-else class="mt-4 text-sm text-gray-500">No recent jobs yet.</p>
				</section>

				<section class="rounded-2xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Incident signals</h3>
							<p class="mt-1 text-sm text-gray-600">
								Repeated failures stay visible here so operators can investigate
								without hunting across screens.
							</p>
						</div>
						<Button variant="ghost" :route="'/forensics/signals'">View all</Button>
					</div>
					<div v-if="recentSignals.length" class="mt-4 space-y-3">
						<router-link
							v-for="signal in recentSignals.slice(0, 5)"
							:key="signal.signal_key"
							:to="{ name: 'Forensic Event Detail', params: { name: signal.latest_event } }"
							class="block rounded-xl border px-4 py-3 transition hover:bg-gray-50"
						>
							<div class="flex items-center justify-between gap-3">
								<div>
									<p class="font-medium text-gray-900">
										{{ signal.target_label }}
									</p>
									<p class="mt-1 text-sm text-gray-600">{{ signal.event_type }}</p>
								</div>
								<div class="text-right">
									<Badge :label="signal.signal_state || 'Open'" />
									<p class="mt-1 text-xs text-gray-500">{{ signal.count }} hits</p>
								</div>
							</div>
						</router-link>
					</div>
					<p v-else class="mt-4 text-sm text-gray-500">
						No repeated signals in the current window.
					</p>
				</section>
			</div>
		</div>
	</div>
</template>

<script>
import { Badge, Button } from 'frappe-ui';
import { getForensicJobRoute } from '../utils/forensics';

export default {
	name: 'HomeSummary',
	components: {
		Badge,
		Button,
	},
	resources: {
		home() {
			if (!this.$team.doc?.name) return;
			return {
				url: 'press.api.client.run_doc_method',
				cache: ['home_data', this.$team.doc.name],
				makeParams() {
					return {
						dt: 'Team',
						dn: this.$team.doc.name,
						method: 'get_home_data',
					};
				},
				auto: true,
			};
		},
	},
	computed: {
		data() {
			return this.$resources.home.data?.message || {};
		},
		summary() {
			return this.data.summary || {};
		},
		servers() {
			return this.data.servers || [];
		},
		benches() {
			return this.data.benches || [];
		},
		sites() {
			return this.data.sites || [];
		},
		onboarding() {
			return this.data.onboarding || {};
		},
		jobScopeSummary() {
			return this.data.job_scope_summary || {};
		},
		recentJobs() {
			return this.data.recent_jobs || [];
		},
		recentSignals() {
			return this.data.recent_signals || [];
		},
		primaryAction() {
			if (!this.onboarding.exists) {
				return {
					label: 'Register managed server',
					route: '/servers/register-managed',
				};
			}
			if (!this.onboarding.release_group) {
				return {
					label: 'Open bench onboarding',
					route: `/servers/${this.onboarding.server}/bench-onboarding`,
				};
			}
			if ((this.onboarding.managed_site_count || 0) === 0) {
				return {
					label: 'Create managed sites',
					route: `/servers/${this.onboarding.server}/bench-onboarding`,
				};
			}
			return {
				label: 'Review server operations',
				route: '/servers',
			};
		},
		summaryCards() {
			return [
				{
					label: 'Managed Servers',
					value: this.summary.server_count || 0,
					helper: `${this.summary.active_server_count || 0} active`,
				},
				{
					label: 'Benches',
					value: this.summary.bench_count || 0,
					helper: `${this.summary.active_bench_count || 0} active`,
				},
				{
					label: 'Sites',
					value: this.summary.site_count || 0,
					helper: `${this.summary.active_site_count || 0} healthy now`,
				},
				{
					label: 'Active Jobs',
					value: this.summary.active_job_count || 0,
					helper: 'Visible execution in flight',
				},
				{
					label: 'Open Signals',
					value: this.summary.open_signal_count || 0,
					helper: 'Incidents or repeated failures to review',
				},
			];
		},
		actionBoard() {
			return [
				{
					label: 'Managed server',
					status: this.onboarding.exists ? 'Registered' : 'Missing',
					detail: this.onboarding.exists
						? `Primary server: ${this.onboarding.server}`
						: 'Register the managed Linux server so the rest of the product has an anchor.',
					action: this.onboarding.exists ? 'Open servers' : 'Register server',
					route: this.onboarding.exists ? '/servers' : '/servers/register-managed',
				},
				{
					label: 'Bench onboarding',
					status: this.onboarding.release_group ? 'Ready' : 'Pending',
					detail: this.onboarding.release_group
						? `Managed bench: ${this.onboarding.release_group}`
						: this.onboarding.bench_directory || 'Point 3plug at the real bench path and complete onboarding.',
					action: 'Open onboarding',
					route: this.onboarding.server
						? `/servers/${this.onboarding.server}/bench-onboarding`
						: '/servers/register-managed',
				},
				{
					label: 'Managed sites',
					status: (this.onboarding.managed_site_count || 0) > 0 ? 'Ready' : 'Pending',
					detail:
						(this.onboarding.managed_site_count || 0) > 0
							? `${this.onboarding.managed_site_count} managed site records created`
							: `${this.onboarding.discovered_site_count || 0} discovered sites are waiting to be managed.`,
					action: 'Open sites',
					route: '/sites',
				},
				{
					label: 'Incident review',
					status: (this.summary.open_signal_count || 0) > 0 ? 'Attention' : 'Clear',
					detail:
						(this.summary.open_signal_count || 0) > 0
							? 'Repeated failures are visible and should be reviewed.'
							: 'No open repeated-failure signals are currently visible.',
					action: 'Review signals',
					route: '/forensics/signals',
				},
			];
		},
		operatorScripts() {
			return [
				{
					label: 'Run server health review',
					detail: 'Open the managed server health and security path first.',
					route: '/servers',
				},
				{
					label: 'Continue bench onboarding',
					detail: 'Keep the real server to bench to site flow moving.',
					route: this.onboarding.server
						? `/servers/${this.onboarding.server}/bench-onboarding`
						: '/servers/register-managed',
				},
				{
					label: 'Inspect job execution',
					detail: 'Use tracked jobs as the main execution trail.',
					route: '/jobs',
				},
				{
					label: 'Investigate incident signals',
					detail: 'Open grouped failures and forensic evidence.',
					route: '/forensics/signals',
				},
			];
		},
	},
	methods: {
		jobRoute(job) {
			return getForensicJobRoute(job);
		},
		formatTimestamp(value) {
			if (!value) return 'Not recorded';
			return this.$format.date(value, 'lll');
		},
	},
};
</script>
