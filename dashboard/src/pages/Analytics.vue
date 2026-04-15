<template>
	<div class="mx-auto max-w-6xl px-5 py-8 space-y-6">
		<section class="rounded-2xl border bg-white p-6">
			<p class="text-sm uppercase tracking-wide text-gray-500">Analytics</p>
			<h1 class="mt-2 text-2xl font-semibold text-gray-900">
				Operational Analytics
			</h1>
			<p class="mt-3 text-sm leading-6 text-gray-600">
				Use analytics to understand runtime health, site activity, execution
				load, and incident pressure across the control plane.
			</p>
		</section>

		<section class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
			<div
				v-for="card in cards"
				:key="card.label"
				class="rounded-xl border bg-white px-5 py-4"
			>
				<div class="text-sm text-gray-500">{{ card.label }}</div>
				<div class="mt-1 text-lg font-semibold text-gray-900">
					{{ card.value }}
				</div>
				<div class="mt-2 text-sm text-gray-600">{{ card.help }}</div>
			</div>
		</section>

		<section class="rounded-2xl border bg-white p-5">
			<h2 class="text-lg font-semibold text-gray-900">Analytics Workstreams</h2>
			<div class="mt-4 grid gap-4 md:grid-cols-2">
				<router-link
					v-for="item in workstreams"
					:key="item.label"
					:to="item.route"
					class="rounded-xl border px-5 py-4 transition hover:border-gray-400 hover:bg-gray-50"
				>
					<div class="font-medium text-gray-900">{{ item.label }}</div>
					<p class="mt-2 text-sm leading-6 text-gray-600">
						{{ item.detail }}
					</p>
				</router-link>
			</div>
		</section>
	</div>
</template>

<script>
export default {
	name: 'Analytics',
	resources: {
		siteSummary() {
			return {
				url: 'press.api.client.get_list',
				params: {
					doctype: 'Site',
					fields: ['status'],
					order_by: 'creation desc',
					limit: 200,
				},
				auto: true,
				initialData: [],
			};
		},
		jobSummary() {
			return {
				url: 'press.api.client.get_list',
				params: {
					doctype: 'Agent Job',
					fields: ['status'],
					order_by: 'creation desc',
					limit: 200,
				},
				auto: true,
				initialData: [],
			};
		},
		forensicSummary() {
			return {
				url: 'press.api.client.get_list',
				params: {
					doctype: 'Forensic Event',
					fields: ['creation'],
					order_by: 'creation desc',
					limit: 200,
				},
				auto: true,
				initialData: [],
			};
		},
	},
	computed: {
		cards() {
			const sites = this.$resources.siteSummary.data || [];
			const jobs = this.$resources.jobSummary.data || [];
			const forensics = this.$resources.forensicSummary.data || [];
			return [
				{
					label: 'Active Sites',
					value: `${sites.filter((site) => site.status === 'Active').length}`,
					help: 'Managed sites currently in service.',
				},
				{
					label: 'Running Jobs',
					value: `${jobs.filter((job) => job.status === 'Running').length}`,
					help: 'Execution currently in flight.',
				},
				{
					label: 'Failed Jobs',
					value: `${jobs.filter((job) => job.status === 'Failure').length}`,
					help: 'Execution that needs attention.',
				},
				{
					label: 'Forensic Events',
					value: `${forensics.length}`,
					help: 'Recorded evidence items available for review.',
				},
			];
		},
		workstreams() {
			return [
				{
					label: 'Sites',
					detail: 'Review per-site performance, request activity, and runtime behavior.',
					route: '/sites',
				},
				{
					label: 'Servers',
					detail: 'Track server health, production readiness, and recent execution pressure.',
					route: '/servers',
				},
				{
					label: 'Jobs',
					detail: 'Follow execution load, failures, and lifecycle actions across the platform.',
					route: '/jobs',
				},
				{
					label: 'Forensics',
					detail: 'Review incident evidence, signals, and operational anomalies.',
					route: '/forensics',
				},
			];
		},
	},
};
</script>
