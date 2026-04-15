<template>
	<div class="mx-auto max-w-4xl space-y-6">
		<section class="rounded-2xl border bg-white p-8">
			<p class="text-sm uppercase tracking-wide text-gray-500">
				First-Run Onboarding
			</p>
			<h1 class="mt-2 text-3xl font-semibold text-gray-900">
				Start by onboarding the managed server
			</h1>
			<p class="mt-3 max-w-3xl text-sm leading-6 text-gray-600">
				3plug Control is built around one managed Linux server. Benches, sites,
				jobs, and forensics all hang from that server, so the first task should
				be to register it and verify that production is ready.
			</p>
			<div class="mt-6 flex flex-wrap gap-3">
				<Button variant="solid" :route="{ name: 'Register Managed Server' }">
					Onboard managed server
				</Button>
				<Button :route="{ name: 'SettingsProfile' }">Review account settings</Button>
			</div>
		</section>

		<section class="grid gap-6 lg:grid-cols-[1.3fr_minmax(0,1fr)]">
			<div class="rounded-2xl border bg-white p-6">
				<h2 class="text-lg font-semibold text-gray-900">Recommended sequence</h2>
				<p class="mt-2 text-sm text-gray-600">
					Follow the product in this order so the runtime footprint is created
					cleanly and every later action has a real execution anchor.
				</p>

				<div class="mt-6 space-y-5">
					<div
						v-for="step in steps"
						:key="step.number"
						class="flex gap-4 rounded-xl border p-4"
					>
						<div
							class="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-gray-900 text-sm font-semibold text-white"
						>
							{{ step.number }}
						</div>
						<div class="min-w-0">
							<div class="flex items-center gap-3">
								<h3 class="font-medium text-gray-900">{{ step.title }}</h3>
								<Badge :label="step.status" />
							</div>
							<p class="mt-2 text-sm leading-6 text-gray-600">
								{{ step.detail }}
							</p>
							<Button
								v-if="step.route"
								class="mt-3"
								size="sm"
								:route="step.route"
							>
								{{ step.action }}
							</Button>
						</div>
					</div>
				</div>
			</div>

			<div class="space-y-6">
				<section class="rounded-2xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Why server first</h2>
					<ul class="mt-4 space-y-3 text-sm leading-6 text-gray-600">
						<li>Everything else in 3plug attaches to the managed server.</li>
						<li>Bench discovery only makes sense after the server is known.</li>
						<li>Site creation depends on a real bench and runtime context.</li>
						<li>Jobs, plays, and forensics become useful once the runtime exists.</li>
					</ul>
				</section>

				<section class="rounded-2xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">What comes next</h2>
					<div class="mt-4 space-y-3">
						<router-link
							v-for="item in nextModules"
							:key="item.label"
							:to="item.route"
							class="block rounded-xl border px-4 py-4 transition hover:bg-gray-50"
						>
							<div class="font-medium text-gray-900">{{ item.label }}</div>
							<div class="mt-1 text-sm text-gray-600">{{ item.detail }}</div>
						</router-link>
					</div>
				</section>
			</div>
		</section>
	</div>
</template>

<script>
import { Badge, Button } from 'frappe-ui';

export default {
	name: 'Onboarding',
	components: {
		Badge,
		Button,
	},
	computed: {
		steps() {
			return [
				{
					number: 1,
					title: 'Onboard the managed server',
					status: 'First task',
					detail:
						'Register the Linux server that 3plug will manage. This creates the operational anchor for all benches, sites, jobs, and forensic records.',
					action: 'Register server',
					route: { name: 'Register Managed Server' },
				},
				{
					number: 2,
					title: 'Verify runtime readiness',
					status: 'After server',
					detail:
						'Review production readiness, security posture, and runtime health before moving on to bench registration and site work.',
					action: 'Open servers',
					route: '/servers',
				},
				{
					number: 3,
					title: 'Onboard the real bench',
					status: 'After readiness',
					detail:
						'Point 3plug at the actual bench on the server, discover the installed apps and sites, and create the managed bench record.',
					action: 'Open benches',
					route: '/benches',
				},
				{
					number: 4,
					title: 'Create or import sites',
					status: 'After bench',
					detail:
						'Once the bench is under management, create new sites or import existing ones and operate through tracked execution.',
					action: 'Open sites',
					route: '/sites',
				},
			];
		},
		nextModules() {
			return [
				{
					label: 'Servers',
					detail: 'Health, security, operations, and bench onboarding live here.',
					route: '/servers',
				},
				{
					label: 'Benches',
					detail: 'Use this module to discover benches and prepare them for site work.',
					route: '/benches',
				},
				{
					label: 'Sites',
					detail: 'Create, import, migrate, restore, and operate sites after runtime onboarding.',
					route: '/sites',
				},
			];
		},
	},
};
</script>
