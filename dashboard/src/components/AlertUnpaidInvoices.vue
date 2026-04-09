<template>
	<AlertBanner :title="outstandingBalanceMessage" type="warning" />
</template>
<script>
import AlertBanner from './AlertBanner.vue';

export default {
	name: 'AlertUnpaidInvoices',
	components: { AlertBanner },
	props: {
		amount: {
			type: Number,
			required: true,
		},
		currency: {
			type: String,
		},
	},
	computed: {
		outstandingBalanceMessage() {
			return `A legacy billing balance alert from Press is still present for ${this.$format.userCurrency(
				this.amount,
			)}. Billing self-service is deferred in 3plug v1.`;
		},
	},
};
</script>
