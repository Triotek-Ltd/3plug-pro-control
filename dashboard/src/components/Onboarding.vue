<template>
	<div class="mx-auto max-w-2xl rounded-lg border-0 px-2 sm:border sm:p-8">
		<div class="prose prose-sm max-w-none">
			<h1 class="text-2xl font-semibold">Welcome to 3plug Control</h1>
			<p>
				3plug Control helps you operate your managed environments from one
				dashboard with visibility into sites, apps, jobs, backups, domains, and
				other operational tasks.
			</p>
		</div>
		<p class="mt-6 text-base text-gray-800">
			Complete the steps below to unlock sites, benches, dedicated servers and
			more.
		</p>
		<div class="mt-6 space-y-6">
			<div class="rounded-md">
				<div class="flex items-center justify-between space-x-2">
					<div class="flex items-center space-x-2">
						<TextInsideCircle>1</TextInsideCircle>
						<span class="text-base font-medium">Account created</span>
					</div>
					<div
						class="grid h-4 w-4 place-items-center rounded-full bg-green-500/90"
					>
						<lucide-check class="h-3 w-3 text-white" />
					</div>
				</div>
			</div>
			<div v-if="pendingSiteRequest">
				<div class="flex items-center justify-between space-x-2">
					<div class="flex items-center space-x-2">
						<TextInsideCircle>2</TextInsideCircle>
						<span
							class="text-base font-medium"
							v-if="pendingSiteRequest.status == 'Error'"
						>
							There was an error creating your trial site for
							{{ pendingSiteRequest.title }}
						</span>
						<span class="text-base font-medium" v-else>
							Create your {{ pendingSiteRequest.title }} trial site
						</span>
					</div>
				</div>
				<div class="mt-2 pl-7" v-if="pendingSiteRequest.status == 'Error'">
					<p class="mt-2 text-p-base text-gray-800">
						Please contact support using the button below.
					</p>
					<Button class="mt-2" link="/support">Contact Support</Button>
				</div>
				<div class="mt-2 pl-7" v-else>
					<p class="mt-2 text-p-base text-gray-800">
						You can try out the {{ pendingSiteRequest.title }} app for free by
						clicking on the button below.
					</p>
					<Button
						class="mt-2"
						:route="{
							name: 'SignupSetup',
							params: { productId: pendingSiteRequest.product_trial },
							query: {
								account_request: pendingSiteRequest.account_request,
							},
						}"
					>
						Continue
					</Button>
				</div>
			</div>
			<div v-else-if="trialSite">
				<div class="flex items-center justify-between space-x-2">
					<div class="flex items-center space-x-2">
						<TextInsideCircle>2</TextInsideCircle>
						<span class="text-base font-medium">Your trial site is ready</span>
					</div>
					<div
						class="grid h-4 w-4 place-items-center rounded-full bg-green-500/90"
					>
						<lucide-check class="h-3 w-3 text-white" />
					</div>
				</div>
				<div class="pl-7">
					<div class="mt-2">
						<a
							class="flex items-center text-base font-medium underline"
							:href="`https://${trialSite.host_name || trialSite.name}`"
							target="_blank"
						>
							https://{{ trialSite.host_name || trialSite.name }}
							<lucide-external-link class="ml-1 h-3.5 w-3.5 text-gray-800" />
						</a>
					</div>
					<p class="mt-2 text-p-base text-gray-800">
						Your trial is set to expire on
						<span class="font-medium">
							{{ $format.date(trialSite.trial_end_date, 'LL') }}
						</span>
						. Complete your account setup in 3plug to ensure uninterrupted
						access to your site.
					</p>
				</div>
			</div>
			<div v-else class="rounded-md">
				<div class="flex items-center space-x-2">
					<TextInsideCircle>2</TextInsideCircle>
					<div class="text-base font-medium">Create your first site</div>
				</div>

				<Button class="ml-7 mt-4" :route="{ name: 'SignupAppSelector' }">
					Create
				</Button>
			</div>
			<div
				class="rounded-md"
				:class="{
					'pointer-events-none opacity-50': !$team.doc.onboarding.site_created,
				}"
			>
				<div v-if="!isAccountSetupComplete">
					<div class="flex items-center space-x-2">
						<TextInsideCircle>3</TextInsideCircle>
						<span class="text-base font-medium">Complete account setup</span>
					</div>
					<div class="pl-7 mt-2" v-if="$team.doc.onboarding.site_created">
						<p class="text-p-base text-gray-800">
							Add your required account details from Settings to finish
							onboarding for your managed environment. Your trial still ends on
							<span class="font-medium">
								{{ $format.date(trialSite.trial_end_date, 'LL') }}
							</span>
						</p>
						<Button class="mt-3" :route="{ name: 'SettingsProfile' }">
							Open Settings
						</Button>
					</div>
				</div>
				<div v-else>
					<div class="flex items-center justify-between space-x-2">
						<div class="flex items-center space-x-2">
							<TextInsideCircle>3</TextInsideCircle>
							<span class="text-base font-medium">
								Account setup complete
							</span>
						</div>
						<div
							class="grid h-4 w-4 place-items-center rounded-full bg-green-500/90"
						>
							<lucide-check class="h-3 w-3 text-white" />
						</div>
					</div>
					<div class="mt-1.5 pl-7 text-p-base text-gray-800">
						Required account details are now in place for 3plug onboarding.
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
import TextInsideCircle from './TextInsideCircle.vue';

export default {
	name: 'Onboarding',
	components: {
		TextInsideCircle,
	},
	computed: {
		isAccountSetupComplete() {
			return Boolean(this.$team.doc.timezone || this.$team.doc.country);
		},
		pendingSiteRequest() {
			return this.$team.doc.pending_site_request;
		},
		trialSite() {
			return this.$team.doc.trial_sites?.[0];
		},
	},
};
</script>
