<template>
	<div v-if="documentResource?.doc" class="space-y-6">
		<section class="rounded-xl border bg-white p-5">
			<div class="flex items-start justify-between gap-4">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">Tenant</p>
					<h2 class="mt-1 text-2xl font-semibold text-gray-900">
						{{ title }}
					</h2>
					<p class="mt-2 text-sm text-gray-600">
						{{ documentResource.doc.user || documentResource.doc.name }}
					</p>
				</div>
				<div class="rounded-lg bg-gray-50 px-4 py-3 text-sm text-gray-700">
					<div><span class="font-medium text-gray-900">Status:</span> {{ statusLabel }}</div>
					<div class="mt-1">
						<span class="font-medium text-gray-900">Country:</span>
						{{ documentResource.doc.country || 'Not set' }}
					</div>
				</div>
			</div>
		</section>

		<section class="rounded-xl border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Feature Access</h3>
			<div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
				<div
					v-for="item in featureCards"
					:key="item.label"
					class="rounded-lg border px-4 py-3"
				>
					<div class="flex items-center justify-between gap-3">
						<div class="font-medium text-gray-900">{{ item.label }}</div>
						<span
							class="rounded-full px-2.5 py-1 text-xs font-medium"
							:class="
								item.enabled
									? 'bg-green-50 text-green-700'
									: 'bg-gray-100 text-gray-600'
							"
						>
							{{ item.enabled ? 'Enabled' : 'Disabled' }}
						</span>
					</div>
					<div class="mt-2 text-sm text-gray-600">{{ item.help }}</div>
				</div>
			</div>
		</section>

		<section class="rounded-xl border bg-white p-5">
			<h3 class="text-lg font-semibold text-gray-900">Tenant Profile</h3>
			<dl class="mt-4 grid gap-4 md:grid-cols-2">
				<div>
					<dt class="text-sm text-gray-500">Billing Name</dt>
					<dd class="mt-1 text-sm font-medium text-gray-900">
						{{ documentResource.doc.billing_name || 'Not set' }}
					</dd>
				</div>
				<div>
					<dt class="text-sm text-gray-500">Parent Tenant</dt>
					<dd class="mt-1 text-sm font-medium text-gray-900">
						{{ documentResource.doc.parent_team || 'None' }}
					</dd>
				</div>
				<div>
					<dt class="text-sm text-gray-500">Notifications</dt>
					<dd class="mt-1 text-sm font-medium text-gray-900">
						{{ documentResource.doc.send_notifications ? 'Enabled' : 'Disabled' }}
					</dd>
				</div>
				<div>
					<dt class="text-sm text-gray-500">2FA Policy</dt>
					<dd class="mt-1 text-sm font-medium text-gray-900">
						{{ documentResource.doc.enforce_2fa ? 'Enforced' : 'Optional' }}
					</dd>
				</div>
			</dl>
		</section>
	</div>
</template>

<script>
export default {
	name: 'TenantOverview',
	props: {
		documentResource: {
			type: Object,
			required: true,
		},
	},
	computed: {
		title() {
			return (
				this.documentResource.doc.team_title ||
				this.documentResource.doc.billing_name ||
				this.documentResource.doc.user ||
				this.documentResource.doc.name
			);
		},
		statusLabel() {
			if (!this.documentResource.doc.enabled) return 'Disabled';
			if (this.documentResource.doc.banned) return 'Banned';
			return 'Active';
		},
		featureCards() {
			return [
				{
					label: 'Managed Servers',
					enabled: Boolean(this.documentResource.doc.self_hosted_servers_enabled),
					help: 'Controls the one-server onboarding and managed server flow.',
				},
				{
					label: 'Benches',
					enabled: Boolean(this.documentResource.doc.benches_enabled),
					help: 'Allows bench records and bench-led runtime operations.',
				},
				{
					label: 'Servers',
					enabled: Boolean(this.documentResource.doc.servers_enabled),
					help: 'Controls access to runtime server records and server operations.',
				},
				{
					label: 'Database Access',
					enabled: Boolean(this.documentResource.doc.database_access_enabled),
					help: 'Allows database-facing tooling and privileged runtime access.',
				},
				{
					label: 'Performance Tuning',
					enabled: Boolean(this.documentResource.doc.enable_performance_tuning),
					help: 'Enables tuning and advanced runtime optimization features.',
				},
				{
					label: 'In-place Updates',
					enabled: Boolean(this.documentResource.doc.enable_inplace_updates),
					help: 'Allows update flows that operate directly on the active runtime.',
				},
			];
		},
	},
};
</script>
