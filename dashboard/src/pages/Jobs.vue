<template>
	<div class="mx-auto max-w-6xl px-5 py-8 space-y-6">
		<section class="rounded-2xl border bg-white p-6">
			<p class="text-sm uppercase tracking-wide text-gray-500">Jobs</p>
			<h1 class="mt-2 text-2xl font-semibold text-gray-900">
				Execution Across 3plug Control
			</h1>
			<p class="mt-3 text-sm leading-6 text-gray-600">
				Use this view to follow provisioning, deploys, migrations, restores, and
				other tracked actions across the control plane.
			</p>
		</section>

		<section class="grid gap-4 md:grid-cols-3">
			<div
				v-for="card in summaryCards"
				:key="card.label"
				class="rounded-xl border bg-white px-5 py-4"
			>
				<div class="text-sm text-gray-500">{{ card.label }}</div>
				<div class="mt-1 text-2xl font-semibold text-gray-900">
					{{ card.value }}
				</div>
				<div class="mt-2 text-sm text-gray-600">{{ card.help }}</div>
			</div>
		</section>

		<section class="rounded-2xl border bg-white p-5">
			<ObjectList :options="listOptions" />
		</section>
	</div>
</template>

<script>
import ObjectList from '../components/ObjectList.vue';
import { duration } from '../utils/format';

export default {
	name: 'Jobs',
	components: { ObjectList },
	resources: {
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
	},
	computed: {
		listOptions() {
			return {
				doctype: 'Agent Job',
				fields: ['end', 'job_id', 'site', 'bench', 'server', 'group'],
				orderBy: 'creation desc',
				pageLength: 50,
				searchField: 'job_type',
				filterControls: () => [
					{
						type: 'select',
						label: 'Status',
						fieldname: 'status',
						options: ['', 'Pending', 'Running', 'Success', 'Failure'],
					},
				],
				columns: [
					{
						label: 'Action',
						fieldname: 'job_type',
						class: 'font-medium',
					},
					{
						label: 'Status',
						fieldname: 'status',
						type: 'Badge',
						width: 0.5,
					},
					{
						label: 'Resource',
						fieldname: 'site',
						format: (value, row) =>
							row.site || row.bench || row.server || row.group || 'Platform',
						width: 1.2,
					},
					{
						label: 'Duration',
						fieldname: 'duration',
						format: (value, row) => {
							if (row.job_id === 0 || !row.end) return;
							return duration(value);
						},
						width: 0.4,
					},
					{
						label: 'Started',
						fieldname: 'creation',
						type: 'Timestamp',
						align: 'right',
						width: 0.75,
					},
				],
				rowActions: ({ row }) => [
					{
						label: 'Open in Desk',
						onClick() {
							window.open(
								`${window.location.protocol}//${window.location.host}/app/agent-job/${row.name}`,
								'_blank',
							);
						},
					},
				],
				emptyStateMessage: 'No tracked jobs found yet',
			};
		},
		summaryCards() {
			const jobs = this.$resources.jobSummary.data || [];
			const pending = jobs.filter((job) => job.status === 'Pending').length;
			const running = jobs.filter((job) => job.status === 'Running').length;
			const failures = jobs.filter((job) => job.status === 'Failure').length;
			return [
				{
					label: 'Pending',
					value: `${pending}`,
					help: 'Jobs waiting to start.',
				},
				{
					label: 'Running',
					value: `${running}`,
					help: 'Jobs currently executing.',
				},
				{
					label: 'Failures',
					value: `${failures}`,
					help: 'Jobs that need review or retry.',
				},
			];
		},
	},
};
</script>
