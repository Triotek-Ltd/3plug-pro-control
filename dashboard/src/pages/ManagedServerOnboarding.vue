<template>
	<div class="mx-auto max-w-6xl px-5 py-8" v-if="state">
		<section class="overflow-hidden rounded-2xl border bg-gradient-to-br from-slate-950 via-slate-900 to-cyan-950 p-6 text-white">
			<div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
				<div>
					<p class="text-sm uppercase tracking-[0.18em] text-cyan-200">Server Onboarding</p>
					<h1 class="mt-2 text-3xl font-semibold tracking-tight">
						{{ state.onboarding_profile?.title || state.self_hosted_server }}
					</h1>
					<p class="mt-3 max-w-3xl text-sm leading-6 text-slate-200">
						3plug is onboarding the managed Linux server automatically. This
						view tracks verification, runtime creation, setup, and readiness as
						background work instead of relying on manual shell steps.
					</p>
				</div>
				<div class="flex flex-wrap items-center gap-2">
					<Badge :label="onboardingBadge" />
					<Button
						variant="outline"
						@click="$resources.onboardingState.reload()"
						:loading="$resources.onboardingState.loading"
					>
						Refresh
					</Button>
					<Button
						v-if="canRetry"
						variant="outline"
						@click="$resources.rerunOnboarding.submit()"
						:loading="$resources.rerunOnboarding.loading"
					>
						Rerun Onboarding
					</Button>
					<Button
						v-if="state.server"
						variant="solid"
						:route="`/servers/${state.server}`"
					>
						Open Server Management
					</Button>
				</div>
			</div>
			<div class="mt-6 grid gap-3 sm:grid-cols-3">
				<div
					v-for="card in heroCards"
					:key="card.label"
					class="rounded-xl border border-white/10 bg-white/5 px-4 py-4 backdrop-blur"
				>
					<div class="text-xs uppercase tracking-wide text-cyan-200">{{ card.label }}</div>
					<div class="mt-2 text-lg font-semibold text-white">{{ card.value }}</div>
					<div class="mt-1 text-xs text-slate-300">{{ card.help }}</div>
				</div>
			</div>
			<div
				v-if="state.onboarding_error"
				class="mt-5 rounded-lg border border-red-200 bg-red-50 px-4 py-3"
			>
				<p class="text-sm font-medium text-red-800">Onboarding failed</p>
				<pre class="mt-2 overflow-auto whitespace-pre-wrap text-xs text-red-700">{{ state.onboarding_error }}</pre>
			</div>
		</section>

		<div class="mt-6 grid gap-6 xl:grid-cols-[minmax(0,1.35fr)_24rem]">
			<div class="space-y-6">
				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Pipeline</h2>
					<div class="mt-5 grid gap-3 md:grid-cols-2">
						<div
							v-for="step in onboardingSteps"
							:key="step.label"
							class="rounded-xl border px-4 py-4"
						>
							<div class="flex items-center justify-between gap-3">
								<div>
									<div class="text-xs uppercase tracking-wide text-gray-500">{{ step.index }}</div>
									<div class="mt-1 font-medium text-gray-900">{{ step.label }}</div>
								</div>
								<Badge :label="step.status" />
							</div>
							<div class="mt-2 text-sm text-gray-600">{{ step.detail }}</div>
						</div>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Machine Facts</h2>
					<div class="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
						<div v-for="card in machineFactCards" :key="card.label">
							<div class="text-sm text-gray-500">{{ card.label }}</div>
							<div class="mt-1 text-sm font-medium text-gray-900">{{ card.value }}</div>
						</div>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Runtime Readiness</h2>
					<div class="mt-5 grid gap-3 md:grid-cols-2">
						<div
							v-for="check in readinessChecks"
							:key="check.label"
							class="rounded-lg border px-4 py-3"
						>
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">{{ check.label }}</div>
								<Badge :label="check.status" />
							</div>
							<div class="mt-2 text-sm text-gray-600">{{ check.detail }}</div>
						</div>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Storage Layout</h2>
					<pre class="mt-4 overflow-auto rounded-lg bg-gray-950 p-4 text-xs leading-6 text-gray-100">{{
						state.machine_facts?.storage_layout || 'Storage facts will appear after verification.'
					}}</pre>
				</section>
			</div>

			<div class="space-y-6">
				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Onboarding Profile</h2>
					<div class="mt-4 space-y-3 text-sm text-gray-700">
						<div>
							<span class="text-gray-500">Primary Domain:</span>
							{{ state.onboarding_profile?.primary_domain || 'Not recorded' }}
						</div>
						<div>
							<span class="text-gray-500">Primary Contact:</span>
							{{ state.onboarding_profile?.onboarding_email || 'Not recorded' }}
						</div>
						<div>
							<span class="text-gray-500">Sudo / SSH User:</span>
							{{ state.onboarding_profile?.ssh_user || 'Not recorded' }}
							<span class="text-gray-500">
								{{ state.onboarding_profile?.ssh_port ? `:${state.onboarding_profile.ssh_port}` : '' }}
							</span>
						</div>
						<div>
							<span class="text-gray-500">Managed Domains:</span>
							{{ managedDomains }}
						</div>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Quick Actions</h2>
					<div class="mt-4 grid gap-3">
						<Button
							variant="solid"
							v-if="state.server"
							:route="`/servers/${state.server}`"
						>
							Open Server Management
						</Button>
						<Button
							variant="outline"
							@click="$resources.onboardingState.reload()"
							:loading="$resources.onboardingState.loading"
						>
							Refresh Onboarding State
						</Button>
						<Button
							v-if="canRetry"
							variant="outline"
							@click="$resources.rerunOnboarding.submit()"
							:loading="$resources.rerunOnboarding.loading"
						>
							Rerun Onboarding
						</Button>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Execution Trail</h2>
					<div class="mt-4 space-y-3">
						<div class="rounded-lg border px-4 py-3">
							<div class="text-sm text-gray-500">Recent Plays</div>
							<div class="mt-1 text-lg font-semibold text-gray-900">{{ state.recent_plays?.length || 0 }}</div>
						</div>
						<div class="rounded-lg border px-4 py-3">
							<div class="text-sm text-gray-500">Recent Jobs</div>
							<div class="mt-1 text-lg font-semibold text-gray-900">{{ state.recent_jobs?.length || 0 }}</div>
						</div>
						<div class="rounded-lg border px-4 py-3">
							<div class="text-sm text-gray-500">Started</div>
							<div class="mt-1 text-sm font-medium text-gray-900">{{ startedLabel }}</div>
						</div>
						<div class="rounded-lg border px-4 py-3">
							<div class="text-sm text-gray-500">Completed</div>
							<div class="mt-1 text-sm font-medium text-gray-900">{{ completedLabel }}</div>
						</div>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Next Handoff</h2>
					<p class="mt-3 text-sm text-gray-600">
						When onboarding completes, 3plug will take you into server management
						first. Bench discovery and site operations come after the managed
						server runtime is ready.
					</p>
				</section>
			</div>
		</div>
	</div>
</template>

<script>
import { Badge, Button } from 'frappe-ui';

export default {
	name: 'ManagedServerOnboarding',
	components: { Badge, Button },
	props: ['name'],
	data() {
		return {
			state: null,
		};
	},
	resources: {
		onboardingState() {
			return {
				url: 'press.api.selfhosted.get_managed_server_onboarding_state',
				auto: true,
				makeParams: () => ({
					self_hosted_server: this.name,
				}),
				onSuccess: (data) => {
					this.state = data || null;
				},
			};
		},
		rerunOnboarding() {
			return {
				url: 'press.api.selfhosted.rerun_managed_server_onboarding',
				auto: false,
				makeParams: () => ({
					self_hosted_server: this.name,
				}),
				onSuccess: (data) => {
					this.state = data || null;
				},
			};
		},
	},
		computed: {
		heroCards() {
			return [
				{
					label: 'Current Stage',
					value: this.onboardingBadge,
					help: 'The live onboarding stage reported by workers and backend state.',
				},
				{
					label: 'Managed Runtime',
					value: this.state?.server || 'Creating...',
					help: 'The server management record appears here once runtime creation succeeds.',
				},
				{
					label: 'Latest Checkpoint',
					value: this.completedLabel === 'Not completed' ? this.startedLabel : this.completedLabel,
					help: this.completedLabel === 'Not completed' ? 'When onboarding last entered the queue.' : 'When onboarding last completed successfully.',
				},
			];
		},
		onboardingBadge() {
			return this.state?.onboarding_stage || this.state?.status || 'Pending';
		},
		canRetry() {
			return ['Failed', 'Broken', 'Unreachable'].includes(
				this.state?.onboarding_stage || this.state?.status,
			);
		},
		managedDomains() {
			const domains = this.state?.onboarding_profile?.managed_domains || [];
			return domains.length ? domains.join(', ') : 'Not recorded';
		},
		machineFactCards() {
			const facts = this.state?.machine_facts || {};
			return [
				{ label: 'Hostname', value: facts.hostname || 'Awaiting verification' },
				{ label: 'Distribution', value: facts.distribution || 'Awaiting verification' },
				{ label: 'Processor', value: facts.processor || 'Awaiting verification' },
				{ label: 'Runtime User', value: facts.runtime_user || 'Awaiting setup' },
				{ label: 'Public IP', value: facts.public_ip || 'Awaiting verification' },
				{ label: 'Private IP', value: facts.private_ip || 'Awaiting verification' },
				{ label: 'Memory', value: facts.ram || 'Awaiting verification' },
				{ label: 'Storage', value: facts.total_storage || 'Awaiting verification' },
			];
		},
		readinessChecks() {
			return [
				...(this.state?.readiness_checks || []),
				...(this.state?.production_checks?.checks || []),
			];
		},
		onboardingSteps() {
			const stage = this.state?.onboarding_stage || '';
			const failed = stage === 'Failed';
			const completed = stage === 'Completed';
			const current = (target) => !failed && !completed && stage === target;
			const done = (targets) => completed || targets.includes(stage);

			return [
				{
					index: '01',
					label: 'Queued',
					status: done(['Queued', 'Verifying Access', 'Validating Machine Capacity', 'Creating Database Runtime', 'Creating Application Runtime', 'Applying Runtime Setup']) ? 'Done' : failed ? 'Failed' : 'Pending',
					detail: 'The onboarding job has been accepted and queued for workers.',
				},
				{
					index: '02',
					label: 'Verification',
					status: done(['Verifying Access', 'Validating Machine Capacity', 'Creating Database Runtime', 'Creating Application Runtime', 'Applying Runtime Setup']) ? 'Done' : current('Verifying Access') ? 'Running' : failed ? 'Failed' : 'Pending',
					detail: '3plug verifies reachability, SSH access, private IPs, CPU, memory, and storage facts.',
				},
				{
					index: '03',
					label: 'Runtime Records',
					status: done(['Creating Database Runtime', 'Creating Application Runtime', 'Applying Runtime Setup']) ? 'Done' : current('Creating Database Runtime') || current('Creating Application Runtime') ? 'Running' : failed ? 'Failed' : 'Pending',
					detail: 'Managed application and database runtime records are created from the verified machine.',
				},
				{
					index: '04',
					label: 'Runtime Setup',
					status: completed ? 'Done' : current('Applying Runtime Setup') ? 'Running' : failed ? 'Failed' : 'Pending',
					detail: 'The runtime setup scripts apply the managed production stack and collect the first health snapshot.',
				},
			];
		},
		startedLabel() {
			return this.state?.onboarding_started_at
				? new Date(this.state.onboarding_started_at).toLocaleString()
				: 'Not started';
		},
		completedLabel() {
			return this.state?.onboarding_completed_at
				? new Date(this.state.onboarding_completed_at).toLocaleString()
				: 'Not completed';
		},
	},
	mounted() {
		this.pollInterval = setInterval(() => {
			if (!this.$resources.onboardingState.loading) {
				this.$resources.onboardingState.reload();
			}
		}, 5000);
	},
	beforeUnmount() {
		clearInterval(this.pollInterval);
	},
};
</script>
