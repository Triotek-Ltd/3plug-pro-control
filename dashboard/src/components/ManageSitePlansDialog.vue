<template>
	<Dialog
		:options="{
			title: 'Change Plan',
			size: '3xl',
		}"
		v-model="show"
	>
		<template #body-content>
			<div>
				<SitePlansCards
					v-model="plan"
					:isPrivateBenchSite="!$site.doc.group_public"
					:isDedicatedServerSite="$site.doc.is_dedicated_server"
					:selectedProvider="$site.doc.server_provider"
				/>
				<div class="mt-4 text-xs text-gray-700">
					<div
						class="flex items-center rounded bg-gray-50 p-2 text-p-base font-medium text-gray-800"
					>
						<lucide-badge-check class="mr-2 h-5 w-12 text-gray-600" />
						<span>Choose the plan that best fits this site's operational needs.</span>
					</div>
				</div>
				<ErrorMessage class="mt-2" :message="$site.setPlan.error" />
			</div>
		</template>
		<template #actions>
			<Button
				variant="solid"
				:disabled="!plan || ($site?.doc && plan === $site.doc.plan)"
				@click="changePlan()"
				class="w-full"
			>
				{{ changeButtonLabel }}
			</Button>
		</template>
	</Dialog>
</template>
<script>
import { getCachedDocumentResource } from 'frappe-ui';
import SitePlansCards from './SitePlansCards.vue';
import { getPlan } from '../data/plans';

export default {
	name: 'ManageSitePlansDialog',
	components: {
		SitePlansCards,
	},
	props: {
		site: {
			type: String,
			required: true,
		},
	},
	data() {
		return {
			show: true,
			plan: null,
		};
	},
	watch: {
		site: {
			immediate: true,
			handler(siteName) {
				if (siteName && this.$site?.doc?.plan) {
					this.plan = getPlan(this.$site.doc.plan);
				}
			},
		},
	},
	methods: {
		changePlan() {
			return this.$site.setPlan.submit(
				{ plan: this.plan.name },
				{
					onSuccess: () => {
						this.show = false;
						this.$toast.success('Plan changed successfully');
					},
				},
			);
		},
	},
	computed: {
		$site() {
			return getCachedDocumentResource('Site', this.site);
		},
		changeButtonLabel() {
			return this.$site.doc?.current_plan?.is_trial_plan
				? 'Upgrade Plan'
				: 'Change plan';
		},
	},
};
</script>
