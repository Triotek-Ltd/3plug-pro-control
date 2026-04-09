<template>
	<AlertBanner
		:title="
			title ??
			'Billing self-service is deferred in 3plug v1. Complete required account details from Settings.'
		"
		:type="type ?? 'warning'"
	>
		<Button class="ml-auto" @click="openSettings" variant="outline">
			Open Settings
		</Button>
	</AlertBanner>
</template>
<script>
import AlertBanner from './AlertBanner.vue';

export default {
	name: 'AlertAddPaymentMode',
	props: {
		title: String,
		type: String,
	},
	components: { AlertBanner },
	methods: {
		openSettings() {
			this.$team.reload();

			this.$router.push({
				name: 'SettingsProfile',
			});
		},
	},
};
</script>
