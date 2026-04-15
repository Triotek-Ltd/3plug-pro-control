<template>
	<div v-if="$bench?.doc" class="space-y-6">
		<section class="rounded-xl border bg-white p-5">
			<div class="flex items-start justify-between gap-4">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">Bench</p>
					<h2 class="mt-1 text-2xl font-semibold text-gray-900">
						{{ $bench.doc.title || $bench.doc.name }}
					</h2>
					<p class="mt-2 text-sm text-gray-600">
						This bench is the managed runtime layer for approved apps, deploys,
						and the sites attached to it.
					</p>
				</div>
				<div class="rounded-lg bg-gray-50 px-4 py-3 text-sm text-gray-700">
					<div>
						<span class="font-medium text-gray-900">Status:</span>
						{{ $bench.doc.status || 'Unknown' }}
					</div>
					<div class="mt-1">
						<span class="font-medium text-gray-900">Version:</span>
						{{ $bench.doc.version || 'Not recorded' }}
					</div>
				</div>
			</div>
		</section>

		<section class="rounded-xl border bg-white p-5">
				<h3 class="text-lg font-semibold text-gray-900">Bench Summary</h3>
			<div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
				<div
					v-for="card in summaryCards"
					:key="card.label"
					class="rounded-lg border px-4 py-3"
				>
					<div class="text-sm text-gray-500">{{ card.label }}</div>
					<div class="mt-1 text-lg font-semibold text-gray-900">
						{{ card.value }}
					</div>
					<div class="mt-1 text-xs text-gray-500">{{ card.help }}</div>
				</div>
			</div>
		</section>

		<div class="grid gap-6 xl:grid-cols-[1.1fr_minmax(0,1fr)]">
			<section class="rounded-xl border bg-white p-5">
				<h3 class="text-lg font-semibold text-gray-900">Runtime Details</h3>
				<dl class="mt-4 grid gap-4 md:grid-cols-2">
					<div>
						<dt class="text-sm text-gray-500">Managed Server</dt>
						<dd class="mt-1 text-sm font-medium text-gray-900">
							{{ $bench.doc.server_title || $bench.doc.server || 'Not recorded' }}
						</dd>
					</div>
					<div>
						<dt class="text-sm text-gray-500">Bench Name</dt>
						<dd class="mt-1 text-sm font-medium text-gray-900">
							{{ $bench.doc.name }}
						</dd>
					</div>
					<div>
						<dt class="text-sm text-gray-500">Sites</dt>
						<dd class="mt-1 text-sm font-medium text-gray-900">
							{{ $bench.doc.site_count || 0 }}
						</dd>
					</div>
					<div>
						<dt class="text-sm text-gray-500">Deploy In Progress</dt>
						<dd class="mt-1 text-sm font-medium text-gray-900">
							{{ deployInfo.deploy_in_progress ? 'Yes' : 'No' }}
						</dd>
					</div>
				</dl>
			</section>

			<section class="rounded-xl border bg-white p-5">
				<h3 class="text-lg font-semibold text-gray-900">Next Action</h3>
				<div class="mt-4 rounded-lg bg-gray-50 px-4 py-4">
					<div class="font-medium text-gray-900">{{ nextAction.label }}</div>
					<div class="mt-2 text-sm text-gray-600">{{ nextAction.detail }}</div>
					<Button v-if="nextAction.route" class="mt-3" size="sm" :route="nextAction.route">
						{{ nextAction.action }}
					</Button>
				</div>
			</section>
		</div>
	</div>
</template>

<script>
import { Button, getCachedDocumentResource } from 'frappe-ui';

export default {
	name: 'BenchOverview',
	components: {
		Button,
	},
	props: {
		bench: {
			type: String,
			required: true,
		},
	},
	computed: {
		$bench() {
			return getCachedDocumentResource('Release Group', this.bench);
		},
		deployInfo() {
			return this.$bench?.doc?.deploy_information || {};
		},
		summaryCards() {
			const apps = this.deployInfo.apps || [];
			const updateAvailable = this.deployInfo.update_available;
			return [
				{
					label: 'Sites',
					value: `${this.$bench.doc.site_count || 0}`,
					help: 'Managed sites currently attached to this bench.',
				},
				{
					label: 'Apps',
					value: `${apps.length}`,
					help: 'Approved apps currently attached to this bench runtime.',
				},
				{
					label: 'Deploy Status',
					value: this.deployInfo.deploy_in_progress ? 'Running' : 'Idle',
					help: 'Whether this bench is actively applying runtime changes right now.',
				},
				{
					label: 'Update State',
					value: updateAvailable ? 'Available' : 'Current',
					help: 'Whether this bench has app or release changes ready to deploy.',
				},
			];
		},
		nextAction() {
			if (this.deployInfo.deploy_in_progress) {
				return {
					label: 'Track Deploy',
					detail: 'A bench deploy is already running. Follow the execution trail before starting another runtime change.',
					action: 'Open deploy history',
					route: `/groups/${this.bench}/deploys`,
				};
			}
			if (this.deployInfo.update_available) {
				return {
					label: 'Review App Updates',
					detail: 'This bench has app or release changes available. Review apps and start a deploy when ready.',
					action: 'Open apps',
					route: `/groups/${this.bench}/apps`,
				};
			}
			if (!(this.$bench.doc.site_count || 0)) {
				return {
					label: 'Create First Site',
					detail: 'This bench is ready, but no managed sites are attached to it yet.',
					action: 'Open sites',
					route: `/groups/${this.bench}/sites`,
				};
			}
			return {
				label: 'Operate Bench',
				detail: 'This bench is part of the active runtime. Use sites, execution, and bench operations for day-to-day work.',
				action: 'Open execution',
				route: `/groups/${this.bench}/jobs`,
			};
		},
	},
};
</script>
