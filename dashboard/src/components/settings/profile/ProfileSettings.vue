<template>
	<div class="p-5">
		<div class="space-y-5">
			<AccountProfile />
			<AccountReferral />
		</div>
	</div>
</template>

<script setup>
import AccountProfile from './AccountProfile.vue';
import AccountReferral from './AccountReferral.vue';

document.title = 'Settings - Profile';
</script>
