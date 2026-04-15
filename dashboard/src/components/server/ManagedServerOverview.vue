<template>
	<div class="space-y-5" v-if="serverDoc">
		<section class="overflow-hidden rounded-2xl border bg-gradient-to-br from-slate-950 via-slate-900 to-sky-950 p-6 text-white">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm uppercase tracking-[0.18em] text-sky-200">Managed Server</p>
					<h2 class="mt-2 text-3xl font-semibold tracking-tight">
						{{ serverDoc.title || serverDoc.name }}
					</h2>
					<p class="mt-3 max-w-3xl text-sm leading-6 text-slate-200">
						This is the Linux server 3plug manages for this deployment. Bench
						onboarding, site import, jobs, and forensic traces all anchor here.
					</p>
				</div>
				<div class="space-y-2 text-sm text-slate-200">
					<div class="flex items-center gap-2">
						<span>Status</span>
						<Badge :label="state.status || serverDoc.status || 'Unknown'" />
					</div>
					<div>
						Linked self-hosted record:
						<span class="font-medium text-white">
							{{ state.self_hosted_server || 'Not linked' }}
						</span>
					</div>
				</div>
			</div>
			<div class="mt-6 grid gap-3 sm:grid-cols-3">
				<div
					v-for="card in heroCards"
					:key="card.label"
					class="rounded-xl border border-white/10 bg-white/5 px-4 py-4 backdrop-blur"
				>
					<div class="text-xs uppercase tracking-wide text-sky-200">{{ card.label }}</div>
					<div class="mt-2 text-lg font-semibold text-white">{{ card.value }}</div>
					<div class="mt-1 text-xs text-slate-300">{{ card.help }}</div>
				</div>
			</div>
			<div class="mt-6 flex flex-wrap gap-3">
				<Button :route="`/servers/${server}/health`" variant="solid">
					Open Health
				</Button>
				<Button :route="`/servers/${server}/operations`" variant="outline">
					Open Operations
				</Button>
				<Button :route="`/servers/${server}/bench-onboarding`" variant="outline">
					Continue Bench Onboarding
				</Button>
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
					<h3 class="text-lg font-semibold text-gray-900">Onboarding Profile</h3>
					<dl class="mt-4 grid gap-4 md:grid-cols-2">
						<div>
							<dt class="text-sm text-gray-500">Primary Domain</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">
								{{ state.onboarding_profile?.primary_domain || 'Not recorded' }}
							</dd>
						</div>
						<div>
							<dt class="text-sm text-gray-500">Primary Contact Email</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">
								{{ state.onboarding_profile?.onboarding_email || 'Not recorded' }}
							</dd>
						</div>
						<div>
							<dt class="text-sm text-gray-500">Sudo / SSH User</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">
								{{ state.onboarding_profile?.ssh_user || 'Not recorded' }}
								<span class="text-gray-500">
									{{ state.onboarding_profile?.ssh_port ? `:${state.onboarding_profile.ssh_port}` : '' }}
								</span>
							</dd>
						</div>
						<div>
							<dt class="text-sm text-gray-500">Managed Domains</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">
								{{ managedDomainsLabel }}
							</dd>
						</div>
					</dl>
				</section>

				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Machine Facts</h3>
					<dl class="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
						<div v-for="fact in machineFactCards" :key="fact.label">
							<dt class="text-sm text-gray-500">{{ fact.label }}</dt>
							<dd class="mt-1 text-sm font-medium text-gray-900">{{ fact.value }}</dd>
						</div>
					</dl>
				</section>

				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Production Readiness</h3>
					<div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
						<div
							v-for="check in readinessChecks"
							:key="check.label"
							class="rounded-md border px-4 py-3"
						>
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">{{ check.label }}</div>
								<Badge :label="check.status" />
							</div>
							<div class="mt-1 text-sm text-gray-600">{{ check.detail }}</div>
						</div>
					</div>
				</section>

				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Storage Layout</h3>
					<pre
						class="mt-4 overflow-auto rounded-md bg-gray-950 p-4 text-xs leading-6 text-gray-100"
					>{{ storageLayoutText }}</pre>
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
					<h3 class="text-lg font-semibold text-gray-900">Quick Actions</h3>
					<div class="mt-4 grid gap-3">
						<Button :route="`/servers/${server}/health`" variant="solid">
							Review Production Health
						</Button>
						<Button :route="`/servers/${server}/security`" variant="outline">
							Inspect Security
						</Button>
						<Button :route="`/servers/${server}/operations`" variant="outline">
							Run Operations
						</Button>
						<Button :route="`/servers/${server}/bench-onboarding`" variant="outline">
							Continue Bench Onboarding
						</Button>
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
		heroCards() {
			return [
				{
					label: 'Runtime State',
					value: this.state.status || this.serverDoc?.status || 'Unknown',
					help: 'The current state of the managed runtime and onboarding record.',
				},
				{
					label: 'Managed Bench',
					value: this.state.release_group || 'Pending',
					help: this.state.release_group
						? 'The managed bench already anchored to this server.'
						: 'Bench onboarding has not been completed yet.',
				},
				{
					label: 'Runtime User',
					value: this.state.machine_facts?.runtime_user || 'Awaiting setup',
					help: 'The detected owner of the managed production processes.',
				},
			];
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
					status: this.serverDoc ? 'Ready' : this.state.onboarding_stage || 'Pending',
					helper:
						this.serverDoc?.name ||
						this.state.onboarding_stage ||
						'No managed server record yet.',
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
			if (!this.state.server || this.state.onboarding_stage !== 'Completed') {
				return 'Finish Server Onboarding';
			}
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
			if (!this.state.server || this.state.onboarding_stage !== 'Completed') {
				return 'Let the onboarding pipeline finish verification, runtime creation, and setup before bench management starts.';
			}
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
		managedDomainsLabel() {
			const domains = this.state.onboarding_profile?.managed_domains || [];
			if (!domains.length) return 'Not recorded';
			return domains.join(', ');
		},
		machineFactCards() {
			const facts = this.state.machine_facts || {};
			return [
				{ label: 'Public IP', value: facts.public_ip || serverValue(this.serverDoc, 'ip') },
				{ label: 'Private IP', value: facts.private_ip || serverValue(this.serverDoc, 'private_ip') },
				{ label: 'Hostname', value: facts.hostname || serverValue(this.serverDoc, 'hostname') },
				{ label: 'Distribution', value: facts.distribution || 'Awaiting verification' },
				{ label: 'Architecture', value: facts.architecture || 'Awaiting verification' },
				{ label: 'Processor', value: facts.processor || 'Awaiting verification' },
				{ label: 'Runtime User', value: facts.runtime_user || 'Awaiting setup' },
				{ label: 'vCPU', value: facts.vcpus || 'Awaiting verification' },
				{ label: 'Memory', value: facts.ram || 'Awaiting verification' },
				{ label: 'Storage', value: facts.total_storage || 'Awaiting verification' },
				{ label: 'Swap', value: facts.swap_total || 'Awaiting verification' },
				{ label: 'Database IP', value: facts.database_public_ip || 'Same as server' },
				{
					label: 'Runtime Plan',
					value:
						this.serverDoc?.current_plan?.plan_title ||
						this.serverDoc?.plan ||
						'Not recorded',
				},
			];
		},
		readinessChecks() {
			return [
				...(this.state.readiness_checks || []),
				...(this.state.production_checks?.checks || []),
			];
		},
		storageLayoutText() {
			return this.state.machine_facts?.storage_layout || 'Storage layout has not been captured yet.';
		},
	},
	created() {
		this.$server = getDocResource({
			doctype: 'Server',
			name: this.server,
		});
	},
};

function serverValue(doc, key) {
	return doc?.[key] || 'Not recorded';
}
</script>
