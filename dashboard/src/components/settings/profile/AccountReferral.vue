<template>
	<Card
		v-if="showReferralNotice"
		title="Referrals Deferred"
		subtitle="Referral signup flows are not active in 3plug v1"
		class="mx-auto max-w-3xl"
	>
		<div class="flex flex-col space-y-4 overflow-hidden">
			<span class="text-sm font-medium leading-4 text-gray-700">
				Referral and self-service signup flows are deferred while 3plug is being narrowed to the operator-first single-server model.
			</span>
		</div>
	</Card>
</template>
<script>
export default {
	name: 'AccountReferral',
	computed: {
		showReferralNotice() {
			return Boolean(this.$team.doc?.referrer_id);
		},
	},
};
</script>
