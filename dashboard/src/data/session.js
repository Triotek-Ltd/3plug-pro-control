import { computed, reactive } from 'vue';
import { createResource } from 'frappe-ui';
import { clear } from 'idb-keyval';
import router from '../router';

export let session = reactive({
	login: createResource({
		url: 'login',
		makeParams({ email, password }) {
			return {
				usr: email,
				pwd: password,
			};
		},
	}),
	logout: createResource({
		url: 'logout',
		async onSuccess() {
			session.user = getSessionUser();
			await router.replace({ name: 'Login' });
			localStorage.removeItem('current_team');
			// On logout, reset posthog user identity and device id
			if (window.posthog?.__loaded) {
				posthog.reset(true);
			}

			// clear all cache from the session
			clear();

			window.location.reload();
		},
	}),
	logoutWithoutReload: createResource({
		url: 'logout',
		async onSuccess() {
			session.user = getSessionUser();
			localStorage.removeItem('current_team');
			// On logout, reset posthog user identity and device id
			if (window.posthog?.__loaded) {
				posthog.reset(true);
			}

			clear();
		},
	}),
	userPermissions: createResource({
		url: 'press.api.account.user_permissions',
		cache: [
			'userPermissions',
			localStorage.getItem('current_team'),
			getSessionUser(),
		],
		initialData: {
			owner: false,
			admin: false,
			billing: false,
			webhook: false,
			apps: false,
			partner: false,
			partner_dashboard: false,
			partner_leads: false,
			partner_customer: false,
			partner_contribution: false,
			site_creation: false,
			bench_creation: false,
			server_creation: false,
		},
	}),
	isTeamAdmin: computed(() => session.userPermissions.data.admin),
	// Triotek v1 defers billing and partner-program surfaces in the dashboard.
	hasBillingAccess: computed(() => false),
	hasWebhookConfigurationAccess: computed(
		() => session.userPermissions.data.webhook,
	),
	hasAppsAccess: computed(() => session.userPermissions.data.apps),
	hasPartnerAccess: computed(() => false),
	hasPartnerDashboardAccess: computed(() => false),
	hasPartnerLeadsAccess: computed(() => false),
	hasPartnerCustomerAccess: computed(() => false),
	hasPartnerContributionAccess: computed(() => false),
	hasSiteCreationAccess: computed(
		() => session.userPermissions.data.site_creation,
	),
	hasBenchCreationAccess: computed(
		() => session.userPermissions.data.bench_creation,
	),
	hasServerCreationAccess: computed(
		() => session.userPermissions.data.server_creation,
	),
	user: getSessionUser(),
	userFullName: getSessionCookies().get('full_name') || '',
	isLoggedIn: computed(() => !!session.user),
	isSystemUser: getSessionCookies().get('system_user') === 'yes',
});

export default session;

export function getSessionUser() {
	let cookies = getSessionCookies();
	let sessionUser = cookies.get('user_id');
	if (!sessionUser || sessionUser === 'Guest') {
		sessionUser = null;
	}
	return sessionUser;
}

function getSessionCookies() {
	return new URLSearchParams(document.cookie.split('; ').join('&'));
}
