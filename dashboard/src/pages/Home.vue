<template>
	<div class="sticky top-0 z-10 shrink-0">
		<Header>
			<Breadcrumbs :items="[{ label: 'Home', route: { name: 'Home' } }]" />
			<Dropdown :options="createOptions">
				<Button variant="solid" label="Create new">
					<template #suffix>
						<lucide-chevron-down class="h-4 w-4 text-gray-300" />
					</template>
				</Button>
			</Dropdown>
		</Header>
	</div>
	<div class="p-5" v-if="$team?.doc">
		<Onboarding v-if="!$team.doc?.onboarding.complete" />
		<HomeSummary v-else />
	</div>
</template>

<script>
import { defineAsyncComponent } from 'vue';
import Header from '../components/Header.vue';
import HomeSummary from '../components/HomeSummary.vue';
import { getTeam } from '../data/team';

export default {
	name: 'Home',
	components: {
		Header,
		HomeSummary,
		Onboarding: defineAsyncComponent(
			() => import('../components/Onboarding.vue'),
		),
	},
	setup() {
		return {
			$team: getTeam(),
		};
	},
	computed: {
		createOptions() {
			if (!this.$team?.doc?.onboarding?.complete) {
				return [
					{
						label: 'Managed Server',
						route: { name: 'Register Managed Server' },
					},
				];
			}

			return [
				{
					label: 'Managed Server',
					route: { name: 'Register Managed Server' },
				},
				{ label: 'Bench', route: { name: 'New Release Group' } },
				{ label: 'Site', route: { name: 'New Site' } },
			];
		},
	},
};
</script>
