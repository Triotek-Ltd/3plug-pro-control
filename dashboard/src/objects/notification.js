import { h } from 'vue';
import router from '../router';
import { getDocResource } from '../utils/resource';
import { unreadNotificationsCount } from '../data/notifications';
import { Tooltip, frappeRequest } from 'frappe-ui';
import { icon } from '../utils/components';
import { getTeam } from '../data/team';
import { toast } from 'vue-sonner';

const getNotification = (name) => {
	return getDocResource({
		doctype: 'Press Notification',
		name: name,
		whitelistedMethods: {
			markNotificationAsRead: 'mark_as_read',
		},
	});
};

export default {
	doctype: 'Press Notification',
	whitelistedMethods: {},
	list: {
		resource() {
			let $team = getTeam();
			return {
				type: 'list',
				doctype: 'Press Notification',
				url: 'press.api.notifications.get_notifications',
				auto: true,
				filters: {
					read: 'Unread',
				},
				cache: ['Notifications'],
			};
		},
		route: '/notifications',
		title: 'Alert Center',
		orderBy: 'creation desc',
		filterControls() {
			return [
				{
					type: 'tab',
					label: 'Read',
					fieldname: 'read',
					options: ['All', 'Unread'],
					default: 'Unread',
				},
			];
		},
		onRowClick(row) {
			const notification = getNotification(row.name);

			notification.markNotificationAsRead.submit().then(() => {
				unreadNotificationsCount.setData((data) => data - 1);
				if (row.route) router.push(row.route);
			});
		},
		actions({ listResource: notifications }) {
			return [
				{
					label: 'Mark all as reviewed',
					slots: {
						prefix: icon('check-circle'),
					},
					async onClick() {
						toast.promise(
							frappeRequest({
								url: '/api/method/press.api.notifications.mark_all_notifications_as_read',
							}),
							{
								success: () => {
									notifications.reload();
									return 'All alerts marked as reviewed';
								},
								loading: 'Marking all alerts as reviewed...',
								error: (error) =>
									error.messages?.length
										? error.messages.join('\n')
										: error.message,
							},
						);
					},
				},
			];
		},
		columns: [
			{
				label: 'Signal',
				fieldname: 'title',
				width: '20rem',
				format(value, row) {
					return value || row.type;
				},
				suffix(row) {
					if (row.is_actionable && !row.is_addressed) {
						let AlertIcon = icon('alert-circle');
						return h(
							Tooltip,
							{
								text: 'This notification requires your attention',
							},
							{
								default: () =>
									h(
										'div',
										{
											class: 'ml-2  text-red-500',
										},
										h(AlertIcon),
									),
							},
						);
					}
				},
			},
			{
				label: 'Summary',
				fieldname: 'message',
				type: 'Component',
				width: '40rem',
				component({ row }) {
					return h('div', {
						class: 'truncate text-base text-gray-600',
						// replace all html tags except <b>
						innerHTML: row.message
							.replace(/<(?!\/?b\b)[^>]*>/g, '')
							.split('\n')[0],
					});
				},
			},
			{
				label: 'Received',
				fieldname: 'creation',
				type: 'Timestamp',
				align: 'right',
			},
		],
	},
	routes: [],
};
