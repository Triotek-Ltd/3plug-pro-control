<script setup lang="ts">
import { computed, onMounted, onUnmounted, getCurrentInstance } from 'vue';

import DoorOpen from '~icons/lucide/door-open';
import PanelTopInactive from '~icons/lucide/panel-top-inactive';
import Boxes from '~icons/lucide/boxes';
import Server from '~icons/lucide/server';
import WalletCards from '~icons/lucide/wallet-cards';
import Settings from '~icons/lucide/settings';
import App from '~icons/lucide/layout-grid';
import Activity from '~icons/lucide/activity';
import Logs from '~icons/lucide/scroll-text';
import FileSearch from '~icons/lucide/file-search';
import Briefcase from '~icons/lucide/briefcase-business';
import NotificationPanel from './Notifications.vue';

import { unreadNotificationsCount } from '@/data/notifications';
import { getTeam } from '@/data/team';
import { session } from '@/data/session';
import { useRoute } from 'vue-router';

const $route = useRoute();
const $team = getTeam();
const $session = session;
const $socket = getCurrentInstance().proxy.$socket;

const navigation = computed(() => {
	if (!$team?.doc) return [];

	const routeName = String($route?.name || '');
	const onboardingComplete = $team.doc.onboarding.complete;
	const isSaasUser = $team.doc.is_saas_user;
	const enforce2FA = Boolean(
		!$team.doc.is_desk_user &&
		$team.doc.enforce_2fa &&
		!$team.doc.user_info?.is_2fa_enabled,
	);

	return [
		{
			name: 'Desk',
			icon: DoorOpen,
			route: '/welcome',
			isActive: routeName === 'Welcome' || routeName === 'Home',
			disabled: enforce2FA,
		},
		{
			name: 'Notifications',
			condition: onboardingComplete && !isSaasUser,
			customComponent: NotificationPanel,
			disabled: enforce2FA,
		},
		{
			name: 'Servers',
			icon: Server,
			route: onboardingComplete ? '/servers' : '/enable-servers',
			isActive:
				['New Server', 'Register Managed Server'].includes(routeName) ||
				routeName.startsWith('Server') ||
				routeName === 'Enable Servers',
			disabled: enforce2FA,
		},
		{
			name: 'Benches',
			icon: Boxes,
			route: onboardingComplete ? '/benches' : '/enable-bench-groups',
			isActive:
				[
					'Bench List',
					'Bench Detail',
					'Bench Job',
					'Bench Log',
					'New Release Group',
					'Release Group New Site',
				].includes(routeName) ||
				routeName.startsWith('Bench') ||
				routeName.startsWith('Release Group Detail') ||
				routeName === 'Enable Benches',
			disabled: enforce2FA,
		},
		{
			name: 'Sites',
			icon: PanelTopInactive,
			route: '/sites',
			isActive:
				['Site List', 'Site Detail', 'New Site'].includes(routeName) ||
				routeName.startsWith('Site Detail'),
			disabled: enforce2FA,
		},
		{
			name: 'Tenants',
			icon: WalletCards,
			route: '/tenants',
			isActive:
				routeName === 'Team List' ||
				routeName === 'Team Detail' ||
				routeName.startsWith('Team Detail'),
			condition: onboardingComplete && !isSaasUser,
			disabled: enforce2FA,
		},
		{
			name: 'Apps',
			icon: App,
			route: '/apps',
			isActive:
				routeName.startsWith('Marketplace') ||
				routeName === 'Install App' ||
				$route.path.startsWith('/apps'),
			condition: onboardingComplete && !isSaasUser,
			disabled: enforce2FA,
		},
		{
			name: 'Analytics',
			icon: Activity,
			route: '/analytics',
			isActive: routeName === 'Analytics',
			condition: onboardingComplete && !isSaasUser,
			disabled: enforce2FA,
		},
		{
			name: 'Jobs',
			icon: Logs,
			route: '/jobs',
			isActive:
				routeName === 'Jobs' ||
				routeName === 'Site Job' ||
				routeName === 'Bench Job' ||
				routeName === 'Server Job' ||
				routeName === 'Release Group Job',
			condition: onboardingComplete && !isSaasUser,
			disabled: enforce2FA,
		},
		{
			name: 'Forensics',
			icon: FileSearch,
			route: '/forensics',
			isActive:
				routeName === 'Forensic Event List' ||
				routeName === 'Forensic Event Detail' ||
				routeName.startsWith('Forensic Event Detail') ||
				routeName === 'Forensic Incident Signals',
			condition: onboardingComplete && !isSaasUser,
			disabled: enforce2FA,
		},
		{
			name: 'Team',
			icon: Briefcase,
			route: '/access-requests',
			isActive: routeName === 'Access Requests',
			condition: onboardingComplete && !isSaasUser,
			disabled: enforce2FA,
		},
		{
			name: 'Control Settings',
			icon: Settings,
			route: '/settings',
			isActive: routeName.startsWith('Settings'),
			disabled: enforce2FA,
		},
	].filter((item) => item.condition ?? true);
});

onMounted(() => {
	$socket.emit('doctype_subscribe', 'Press Notification');
	$socket.on('press_notification', (data) => {
		if (data.team === $team.doc.name) {
			unreadNotificationsCount.setData((count) => count + 1);
		}
	});
});

onUnmounted(() => {
	$socket.off('press_notification');
});
</script>

<template>
	<slot :navigation="navigation" />
</template>
