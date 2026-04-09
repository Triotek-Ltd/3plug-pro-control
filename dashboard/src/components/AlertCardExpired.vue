<template>
	<AlertBanner
		title="A legacy billing alert is still present from Press. Billing self-service is deferred in 3plug v1."
		type="warning"
	/>
</template>
<script>
import AlertBanner from './AlertBanner.vue';

export default {
	name: 'AlertCardExpired',
	components: { AlertBanner },
};
</script>
