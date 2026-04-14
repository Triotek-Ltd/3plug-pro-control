<template>
	<div v-if="$site?.doc" class="space-y-6">
		<section class="rounded-xl border bg-white p-5">
			<div class="flex items-start justify-between gap-4">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">Site</p>
					<h2 class="mt-1 text-2xl font-semibold text-gray-900">
						{{ $site.doc.host_name || $site.doc.name }}
					</h2>
					<p class="mt-2 text-sm text-gray-600">
						This site is the managed tenant runtime that sits on a bench and is
						operated through tracked jobs, updates, backups, and incident review.
					</p>
				</div>
				<div class="rounded-lg bg-gray-50 px-4 py-3 text-sm text-gray-700">
					<div>
						<span class="font-medium text-gray-900">Status:</span>
						{{ $site.doc.status || 'Unknown' }}
					</div>
					<div class="mt-1">
						<span class="font-medium text-gray-900">Bench:</span>
						{{ $site.doc.group_title || $site.doc.group || 'Not recorded' }}
					</div>
				</div>
			</div>
		</section>

		<section class="rounded-xl border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Site Summary</h3>
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
				<h3 class="text-lg font-semibold text-gray-900">Managed Runtime</h3>
				<dl class="mt-4 grid gap-4 md:grid-cols-2">
					<div>
						<dt class="text-sm text-gray-500">Managed Server</dt>
						<dd class="mt-1 text-sm font-medium text-gray-900">
							{{ $site.doc.server_title || $site.doc.server || 'Not recorded' }}
						</dd>
					</div>
					<div>
						<dt class="text-sm text-gray-500">Bench</dt>
						<dd class="mt-1 text-sm font-medium text-gray-900">
							{{ $site.doc.group_title || $site.doc.group || 'Not recorded' }}
						</dd>
					</div>
					<div>
						<dt class="text-sm text-gray-500">Version</dt>
						<dd class="mt-1 text-sm font-medium text-gray-900">
							{{ $site.doc.version || 'Not recorded' }}
						</dd>
					</div>
					<div>
						<dt class="text-sm text-gray-500">Region</dt>
						<dd class="mt-1 text-sm font-medium text-gray-900">
							{{ $site.doc.cluster?.title || 'Not recorded' }}
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
	name: 'ManagedSiteOverview',
	components: {
		Button,
	},
	props: {
		site: {
			type: String,
			required: true,
		},
	},
	computed: {
		$site() {
			return getCachedDocumentResource('Site', this.site);
		},
		summaryCards() {
			return [
				{
					label: 'Plan',
					value: this.$site.doc.current_plan?.plan_title || this.$site.doc.plan_title || 'Not set',
					help: 'The current runtime plan attached to this site.',
				},
				{
					label: 'Monitoring',
					value: this.$site.doc.is_monitoring_disabled ? 'Disabled' : 'Active',
					help: 'Whether this site is currently visible to the monitoring path.',
				},
				{
					label: 'Setup',
					value: this.$site.doc.setup_wizard_complete ? 'Complete' : 'Pending',
					help: 'Whether the runtime is fully initialized for normal use.',
				},
				{
					label: 'Domains',
					value: `${(this.$site.doc.domains || []).length || 0}`,
					help: 'Primary and additional domains attached to this site.',
				},
			];
		},
		nextAction() {
			if (!this.$site.doc.setup_wizard_complete && this.$site.doc.status === 'Active') {
				return {
					label: 'Complete Site Setup',
					detail: 'The site is active but the setup wizard is not complete yet.',
					action: 'Open site',
					route: `/sites/${this.site}`,
				};
			}
			if (this.$site.doc.is_monitoring_disabled) {
				return {
					label: 'Re-enable Monitoring',
					detail: 'Monitoring is disabled, so downtime and health changes may be missed.',
					action: 'Open actions',
					route: `/sites/${this.site}/actions`,
				};
			}
			if (this.$site.doc.status === 'Broken') {
				return {
					label: 'Investigate Runtime',
					detail: 'This site is marked broken and should be reviewed through insights, jobs, and forensics.',
					action: 'Open insights',
					route: `/sites/${this.site}/insights`,
				};
			}
			return {
				label: 'Operate Site',
				detail: 'The site is part of the managed runtime. Use insights, apps, backups, and actions for normal operations.',
				action: 'Open insights',
				route: `/sites/${this.site}/insights`,
			};
		},
	},
};
</script>
