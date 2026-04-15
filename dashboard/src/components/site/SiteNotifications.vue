<template>
	<div class="space-y-6">
		<section class="rounded-2xl border bg-white p-5">
			<div class="flex items-start justify-between gap-4">
				<div>
					<h3 class="text-lg font-semibold text-gray-900">Site Notifications</h3>
					<p class="mt-1 text-sm text-gray-600">
						Review how operational alerts should reach the team for this site.
						Site routing can override the team defaults for execution failures,
						backup issues, certificate problems, and active incidents.
					</p>
				</div>
				<Badge :label="notificationState" />
			</div>

			<div class="mt-5 grid gap-4 md:grid-cols-2">
				<div class="rounded-xl border p-4">
					<div class="text-sm font-medium text-gray-900">Current intent</div>
					<p class="mt-2 text-sm leading-6 text-gray-600">
						Site notifications should cover job failures, migration results,
						backup issues, certificate problems, and active incidents tied to
						this site.
					</p>
				</div>
				<div class="rounded-xl border p-4">
					<div class="text-sm font-medium text-gray-900">Current channels</div>
					<p class="mt-2 text-sm leading-6 text-gray-600">
						Notification delivery follows the site-specific routes below first,
						then falls back to the team's configured channels and the global
						control settings.
					</p>
				</div>
			</div>
		</section>

		<section class="rounded-2xl border bg-white p-5">
			<div class="flex items-center justify-between gap-4">
				<div>
					<h3 class="text-lg font-semibold text-gray-900">Current Routing</h3>
					<p class="mt-1 text-sm text-gray-600">
						These routes are currently configured for this site.
					</p>
				</div>
				<Button variant="outline" @click="showCommunicationInfoDialog = true">
					Manage routing
				</Button>
			</div>

			<div
				v-if="$resources.communicationInfos.loading"
				class="mt-4 text-sm text-gray-600"
			>
				Loading site routing...
			</div>
			<div
				v-else-if="communicationInfos.length"
				class="mt-4 grid gap-3 md:grid-cols-2"
			>
				<div
					v-for="route in communicationInfos"
					:key="`${route.type}-${route.channel}-${route.value}`"
					class="rounded-xl border px-4 py-4"
				>
					<div class="text-sm font-medium text-gray-900">
						{{ typeLabels[route.type] || route.type }}
					</div>
					<div class="mt-2 text-sm text-gray-700">
						{{ route.channel }}
					</div>
					<div class="mt-1 text-sm text-gray-600 break-all">
						{{ route.value }}
					</div>
				</div>
			</div>
			<div
				v-else
				class="mt-4 rounded-xl border border-dashed px-4 py-4 text-sm text-gray-600"
			>
				No site-specific routes are configured yet. This site is currently using
				team defaults.
			</div>
		</section>

		<section class="rounded-2xl border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">What to watch</h3>
			<div class="mt-4 grid gap-3 md:grid-cols-2">
				<div
					v-for="item in signals"
					:key="item.label"
					class="rounded-xl border px-4 py-4"
				>
					<div class="font-medium text-gray-900">{{ item.label }}</div>
					<p class="mt-2 text-sm leading-6 text-gray-600">
						{{ item.detail }}
					</p>
				</div>
			</div>
		</section>

		<section class="rounded-2xl border bg-white p-5">
			<div class="flex flex-wrap gap-3">
				<Button :route="'/notifications'">Open alert center</Button>
				<Button @click="showCommunicationInfoDialog = true" variant="outline">
					Manage site routing
				</Button>
				<Button :route="'/forensics/signals'" variant="ghost">
					Review incident signals
				</Button>
			</div>
		</section>
		<CommunicationInfoDialog
			v-if="showCommunicationInfoDialog"
			referenceDoctype="Site"
			:referenceName="site"
			@close="handleCommunicationDialogClose"
		/>
	</div>
</template>

<script>
import { Badge, Button } from 'frappe-ui';
import { getCachedDocumentResource } from 'frappe-ui';
import CommunicationInfoDialog from '../CommunicationInfoDialog.vue';

export default {
	name: 'SiteNotifications',
	props: ['site'],
	components: {
		Badge,
		Button,
		CommunicationInfoDialog,
	},
	data() {
		return {
			showCommunicationInfoDialog: false,
		};
	},
	resources: {
		communicationInfos() {
			return {
				url: 'press.api.client.run_doc_method',
				auto: true,
				makeParams() {
					return {
						dt: 'Site',
						dn: this.site,
						method: 'get_communication_infos',
					};
				},
				transform(data) {
					return data.message || [];
				},
			};
		},
	},
	computed: {
		$site() {
			return getCachedDocumentResource('Site', this.site);
		},
		communicationInfos() {
			return this.$resources.communicationInfos.data || [];
		},
		notificationState() {
			if (this.communicationInfos.length) return 'Site routing';
			if (this.$site?.doc?.send_notifications) return 'Enabled';
			return 'Team defaults';
		},
		typeLabels() {
			return {
				General: 'General Alerts',
				Incident: 'Incidents',
				'Site Activity': 'Site Activity',
				'Server Activity': 'Server Activity',
				Marketplace: 'Marketplace Activity',
			};
		},
		signals() {
			return [
				{
					label: 'Job failures',
					detail:
						'Provisioning, update, and maintenance failures for this site should create visible notifications.',
				},
				{
					label: 'Migrations and restores',
					detail:
						'Migration completion and restore failures should be surfaced quickly so operators can follow up.',
				},
				{
					label: 'Backup posture',
					detail:
						'Backup availability and backup-related issues should remain easy to notice from the site lifecycle.',
				},
				{
					label: 'Certificates and incidents',
					detail:
						'TLS problems and incident signals tied to this site should remain part of the notification trail.',
				},
			];
		},
	},
	methods: {
		handleCommunicationDialogClose() {
			this.showCommunicationInfoDialog = false;
			this.$resources.communicationInfos.reload();
		},
	},
};
</script>
