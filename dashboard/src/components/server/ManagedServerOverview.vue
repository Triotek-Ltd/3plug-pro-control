<template>
	<div class="space-y-5" v-if="serverDoc">
		<section class="rounded-md border bg-white p-5">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">Managed Server</p>
					<h2 class="mt-1 text-xl font-semibold text-gray-900">
						{{ serverDoc.title || serverDoc.name }}
					</h2>
					<p class="mt-2 max-w-3xl text-sm text-gray-600">
						This is the Linux server 3plug manages for this deployment. Bench
						onboarding, site import, jobs, and forensic traces all anchor here.
					</p>
				</div>
				<div class="space-y-2 text-sm text-gray-600">
					<div class="flex items-center gap-2">
						<span>Status</span>
						<Badge :label="state.status || serverDoc.status || 'Unknown'" />
					</div>
					<div>
						Linked self-hosted record:
						<span class="font-medium text-gray-900">
							{{ state.self_hosted_server || 'Not linked' }}
						</span>
					</div>
				</div>
			</div>
		</section>

		<div class="grid gap-5 xl:grid-cols-[minmax(0,1.2fr)_22rem]">
			<div class="space-y-5">
				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Server Summary</h3>
					<div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
						<div v-for="card in summaryCards" :key="card.label" class="rounded-md border px-4 py-3">
							<div class="text-sm text-gray-500">{{ card.label }}</div>
							<div class="mt-1 text-lg font-semibold text-gray-900">{{ card.value }}</div>
							<div v-if="card.help" class="mt-1 text-xs text-gray-500">{{ card.help }}</div>
						</div>
					</div>
				</section>

				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Connectivity</h3>
					<dl class="mt-4 grid gap-4 md:grid-cols-2">
						<div>
							<dt class="text-sm text-gray-500">Public IP</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">{{ serverDoc.ip || 'Not recorded' }}</dd>
						</div>
						<div>
							<dt class="text-sm text-gray-500">Private IP</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">
								{{ serverDoc.private_ip || 'Not recorded' }}
							</dd>
						</div>
						<div>
							<dt class="text-sm text-gray-500">Hostname</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">{{ serverDoc.hostname || 'Not recorded' }}</dd>
						</div>
						<div>
							<dt class="text-sm text-gray-500">Runtime Plan</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">
								{{ serverDoc.current_plan?.plan_title || serverDoc.plan || 'Not recorded' }}
							</dd>
						</div>
					</dl>
				</section>

				<section class="rounded-md border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Onboarding Status</h3>
							<p class="mt-1 text-sm text-gray-600">
								Keep the server to bench to site path visible from the server feature itself.
							</p>
						</div>
						<Button :route="`/servers/${server}/bench-onboarding`" variant="solid">
							Open Bench Onboarding
						</Button>
					</div>
					<div class="mt-4 grid gap-3 md:grid-cols-2">
						<div v-for="stage in onboardingStages" :key="stage.label" class="rounded-md border px-4 py-3">
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">{{ stage.label }}</div>
								<Badge :label="stage.status" />
							</div>
							<div class="mt-1 text-sm text-gray-600">{{ stage.helper }}</div>
						</div>
					</div>
				</section>
			</div>

			<div class="space-y-5">
				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Next Action</h3>
					<div class="mt-4 rounded-md bg-gray-50 px-4 py-3 text-sm text-gray-700">
						<div class="font-medium text-gray-900">{{ nextActionLabel }}</div>
						<div class="mt-1">{{ nextActionDescription }}</div>
					</div>
				</section>

				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Recent Execution</h3>
					<div class="mt-4 space-y-3">
						<div class="rounded-md border px-4 py-3">
							<div class="text-sm text-gray-500">Recent Jobs</div>
							<div class="mt-1 text-lg font-semibold text-gray-900">
								{{ state.recent_jobs?.length || 0 }}
							</div>
						</div>
						<div class="rounded-md border px-4 py-3">
							<div class="text-sm text-gray-500">Recent Plays</div>
							<div class="mt-1 text-lg font-semibold text-gray-900">
								{{ state.recent_plays?.length || 0 }}
							</div>
						</div>
						<div class="rounded-md border px-4 py-3">
							<div class="text-sm text-gray-500">Job Scope</div>
							<div class="mt-1 text-sm text-gray-700">
								Server {{ state.job_scope_summary?.server_jobs || 0 }} |
								Benches {{ state.job_scope_summary?.bench_jobs || 0 }} |
								Sites {{ state.job_scope_summary?.site_jobs || 0 }}
							</div>
						</div>
					</div>
				</section>
			</div>
		</div>
	</div>
</template>

<script>
import { Badge, Button } from 'frappe-ui';
import { getDocResource } from '../../utils/resource';

export default {
	name: 'ManagedServerOverview',
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
		summaryCards() {
			return [
				{
					label: 'Managed Benches',
					value: this.state.release_group ? '1' : '0',
					help: this.state.release_group || 'Create a managed bench from the discovered runtime.',
				},
				{
					label: 'Discovered Apps',
					value: `${this.state.app_count || 0}`,
					help: 'Apps found from the real bench on this Linux server.',
				},
				{
					label: 'Discovered Sites',
					value: `${this.state.site_count || 0}`,
					help: 'Sites captured from the bench before managed import.',
				},
				{
					label: 'Bench Path',
					value: this.state.bench_directory || 'Not set',
					help: 'The real bench directory 3plug inspects during onboarding.',
				},
			];
		},
		onboardingStages() {
			const hasImportedSites = Boolean(this.state.sites?.some((site) => site.site));
			return [
				{
					label: 'Server Registered',
					status: this.serverDoc ? 'Ready' : 'Pending',
					helper: this.serverDoc?.name || 'No managed server record yet.',
				},
				{
					label: 'Bench Source',
					status: this.state.existing_bench_present ? 'Configured' : 'Pending',
					helper: this.state.bench_directory || 'Add the real bench path on the managed server.',
				},
				{
					label: 'Managed Bench',
					status: this.state.release_group ? 'Created' : 'Pending',
					helper: this.state.release_group || 'Create the managed bench record next.',
				},
				{
					label: 'Managed Sites',
					status: hasImportedSites ? 'Created' : 'Pending',
					helper: hasImportedSites ? 'Site records are linked and ready for operations.' : 'Create site records from the discovered bench sites.',
				},
			];
		},
		nextActionLabel() {
			if (!this.state.existing_bench_present || !this.state.bench_directory) {
				return 'Configure Bench Source';
			}
			if (!this.state.app_count && !this.state.site_count) {
				return 'Run Discovery';
			}
			if (!this.state.release_group) {
				return 'Create Managed Bench';
			}
			if (!this.state.sites?.some((site) => site.site)) {
				return 'Create Managed Sites';
			}
			return 'Managed Flow Active';
		},
		nextActionDescription() {
			if (!this.state.existing_bench_present || !this.state.bench_directory) {
				return 'Save the real bench path so 3plug can inspect this Linux server.';
			}
			if (!this.state.app_count && !this.state.site_count) {
				return 'Run discovery to capture the actual apps and sites from the existing bench.';
			}
			if (!this.state.release_group) {
				return 'Turn the discovered runtime into a managed bench record.';
			}
			if (!this.state.sites?.some((site) => site.site)) {
				return 'Create the managed site records so the core server, bench, and site spine is complete.';
			}
			return 'The core managed server flow is active. Continue with normal bench and site operations.';
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
