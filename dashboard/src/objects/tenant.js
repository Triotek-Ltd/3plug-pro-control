export default {
	doctype: 'Team',
	whitelistedMethods: {
		getTeamMembers: 'get_team_members',
		inviteTeamMember: 'invite_team_member',
		removeTeamMember: 'remove_team_member',
	},
	list: {
		route: '/tenants',
		title: 'Tenants',
		orderBy: 'modified desc',
		fields: [
			'team_title',
			'user',
			'country',
			'enabled',
			'banned',
			'self_hosted_servers_enabled',
			'benches_enabled',
			'servers_enabled',
			'modified',
		],
		searchField: 'team_title',
		filterControls() {
			return [
				{
					type: 'select',
					label: 'Status',
					fieldname: 'enabled',
					options: ['', 1, 0],
				},
				{
					type: 'select',
					label: 'Managed Servers',
					fieldname: 'self_hosted_servers_enabled',
					options: ['', 1, 0],
				},
				{
					type: 'select',
					label: 'Benches',
					fieldname: 'benches_enabled',
					options: ['', 1, 0],
				},
			];
		},
		columns: [
			{
				label: 'Tenant',
				fieldname: 'team_title',
				width: 1.6,
				class: 'font-medium',
				format(value, row) {
					return value || row.user || row.name;
				},
			},
			{
				label: 'Owner',
				fieldname: 'user',
				width: 1.2,
			},
			{
				label: 'Country',
				fieldname: 'country',
				width: 0.8,
			},
			{
				label: 'Status',
				fieldname: 'enabled',
				type: 'Badge',
				width: 0.7,
				format(value, row) {
					if (row.banned) return 'Banned';
					return value ? 'Active' : 'Disabled';
				},
			},
			{
				label: 'Managed Server',
				fieldname: 'self_hosted_servers_enabled',
				width: 0.8,
				format(value) {
					return value ? 'Yes' : 'No';
				},
			},
			{
				label: 'Benches',
				fieldname: 'benches_enabled',
				width: 0.6,
				format(value) {
					return value ? 'Yes' : 'No';
				},
			},
			{
				label: '',
				fieldname: 'modified',
				type: 'Timestamp',
				align: 'right',
				width: 0.8,
			},
		],
	},
	detail: {
		titleField: 'team_title',
		route: '/tenants/:name',
		statusBadge({ documentResource: tenant }) {
			return {
				label: tenant.doc?.banned ? 'Banned' : tenant.doc?.enabled ? 'Active' : 'Disabled',
			};
		},
		breadcrumbs({ documentResource: tenant }) {
			return [
				{
					label: 'Tenants',
					route: '/tenants',
				},
				{
					label: tenant.doc?.team_title || tenant.doc?.user || tenant.doc?.name,
					route: `/tenants/${tenant.doc?.name}`,
				},
			];
		},
		tabs: [
			{
				label: 'Overview',
				route: 'overview',
				type: 'Component',
				component: () => import('../components/tenant/TenantOverview.vue'),
				props: (tenant) => {
					return { documentResource: tenant };
				},
			},
			{
				label: 'Sites',
				route: 'sites',
				type: 'list',
				list: {
					doctype: 'Site',
					filters: (tenant) => ({ team: tenant.doc.name }),
					orderBy: 'modified desc',
					fields: ['host_name', 'status', 'bench', 'server'],
					columns: [
						{
							label: 'Site',
							fieldname: 'host_name',
							width: 1.5,
							class: 'font-medium',
							format(value, row) {
								return value || row.name;
							},
						},
						{ label: 'Status', fieldname: 'status', type: 'Badge', width: 0.7 },
						{ label: 'Bench', fieldname: 'bench', width: 1 },
						{ label: 'Server', fieldname: 'server', width: 1 },
					],
					route(row) {
						return { name: 'Site Detail', params: { name: row.name } };
					},
				},
			},
			{
				label: 'Benches',
				route: 'benches',
				type: 'list',
				list: {
					doctype: 'Bench',
					filters: (tenant) => ({ team: tenant.doc.name }),
					orderBy: 'modified desc',
					fields: ['status', 'server', 'group'],
					columns: [
						{ label: 'Bench', fieldname: 'name', width: 1.4, class: 'font-medium' },
						{ label: 'Status', fieldname: 'status', type: 'Badge', width: 0.7 },
						{ label: 'Server', fieldname: 'server', width: 1 },
						{ label: 'Group', fieldname: 'group', width: 1 },
					],
					route(row) {
						return { name: 'Bench Detail', params: { name: row.name } };
					},
				},
			},
			{
				label: 'Servers',
				route: 'servers',
				type: 'list',
				list: {
					doctype: 'Server',
					filters: (tenant) => ({ team: tenant.doc.name }),
					orderBy: 'modified desc',
					fields: ['title', 'status', 'cluster'],
					columns: [
						{
							label: 'Server',
							fieldname: 'title',
							width: 1.5,
							class: 'font-medium',
							format(value, row) {
								return value || row.name;
							},
						},
						{ label: 'Status', fieldname: 'status', type: 'Badge', width: 0.7 },
						{ label: 'Region', fieldname: 'cluster', width: 1 },
					],
					route(row) {
						return { name: 'Server Detail', params: { name: row.name } };
					},
				},
			},
		],
	},
};
