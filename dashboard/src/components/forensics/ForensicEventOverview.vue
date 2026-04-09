<template>
	<div class="grid gap-4 lg:grid-cols-[minmax(0,2fr)_minmax(18rem,1fr)]">
		<div class="rounded-lg border bg-white p-5">
			<div class="flex items-start justify-between gap-4">
				<div>
					<p class="text-sm text-gray-500">Event Summary</p>
					<h2 class="mt-1 text-xl font-semibold text-gray-900">
						{{ document.summary || document.event_type || document.name }}
					</h2>
				</div>
				<div
					class="rounded-full px-3 py-1 text-sm font-medium"
					:class="severityClass"
				>
					{{ document.severity || 'Info' }}
				</div>
			</div>

			<div class="mt-5 grid gap-4 md:grid-cols-2">
				<div v-for="item in primaryFacts" :key="item.label">
					<p class="text-xs uppercase tracking-wide text-gray-500">
						{{ item.label }}
					</p>
					<component
						:is="item.link ? 'a' : 'p'"
						:href="item.link ? item.link.route : undefined"
						:target="item.link?.external ? '_blank' : undefined"
						class="mt-1 break-all text-sm"
						:class="
							item.link
								? 'text-blue-700 underline decoration-blue-300 underline-offset-2'
								: 'text-gray-900'
						"
					>
						{{ item.value || 'Not recorded' }}
					</component>
				</div>
			</div>
		</div>

		<div class="rounded-lg border bg-white p-5">
			<p class="text-sm font-medium text-gray-900">Investigation Context</p>
			<div class="mt-4 space-y-4">
				<div v-for="item in contextFacts" :key="item.label">
					<p class="text-xs uppercase tracking-wide text-gray-500">
						{{ item.label }}
					</p>
					<component
						:is="item.link ? 'a' : 'p'"
						:href="item.link ? item.link.route : undefined"
						:target="item.link?.external ? '_blank' : undefined"
						class="mt-1 break-all text-sm"
						:class="
							item.link
								? 'text-blue-700 underline decoration-blue-300 underline-offset-2'
								: 'text-gray-900'
						"
					>
						{{ item.value || 'Not recorded' }}
					</component>
				</div>
			</div>
		</div>

		<div class="rounded-lg border bg-white p-5 lg:col-span-2">
			<div class="flex items-center justify-between gap-4">
				<div>
					<p class="text-sm font-medium text-gray-900">Captured Payload</p>
					<p class="mt-1 text-sm text-gray-500">
						Structured evidence recorded when this forensic event was created.
					</p>
				</div>
			</div>
			<pre
				class="mt-4 overflow-auto rounded-md bg-gray-950 p-4 text-xs leading-6 text-gray-100"
			>{{ prettyPayload }}</pre>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import {
	getDeskDocumentRoute,
	getForensicDocumentRoute,
	getForensicJobRoute,
	getForensicPrimaryTargetLink,
	getForensicSourceLink,
} from '../../utils/forensics';

const props = defineProps({
	document: {
		type: Object,
		required: true,
	},
});

const document = computed(() => props.document || {});

const primaryFacts = computed(() => [
	{ label: 'Event Type', value: document.value.event_type },
	{ label: 'Status', value: document.value.status },
	{ label: 'Target Type', value: document.value.document_type },
	{
		label: 'Target Name',
		value: document.value.document_name,
		link: getForensicPrimaryTargetLink(document.value),
	},
	{ label: 'Source Type', value: document.value.source_doctype },
	{
		label: 'Source Name',
		value: document.value.source_name,
		link: getForensicSourceLink(document.value),
	},
	{ label: 'Actor', value: document.value.actor },
	{ label: 'Recorded At', value: document.value.creation },
]);

const contextFacts = computed(() => [
	{ label: 'Team', value: document.value.team },
	{
		label: 'Site',
		value: document.value.site,
		link: document.value.site
			? {
					label: document.value.site,
					route: getForensicDocumentRoute('Site', document.value.site),
					external: false,
			  }
			: null,
	},
	{
		label: 'Bench',
		value: document.value.bench,
		link: document.value.bench
			? {
					label: document.value.bench,
					route: getForensicDocumentRoute('Bench', document.value.bench),
					external: false,
			  }
			: null,
	},
	{ label: 'Server Type', value: document.value.server_type },
	{
		label: 'Server',
		value: document.value.server,
		link: (() => {
			if (!document.value.server || !document.value.server_type) return null;
			const route =
				getForensicDocumentRoute(document.value.server_type, document.value.server) ||
				getDeskDocumentRoute(document.value.server_type, document.value.server);
			if (!route) return null;
			return {
				label: document.value.server,
				route,
				external: !getForensicDocumentRoute(
					document.value.server_type,
					document.value.server,
				),
			};
		})(),
	},
	{
		label: 'Job',
		value: document.value.job,
		link: (() => {
			if (!document.value.job) return null;
			const route = getForensicJobRoute(document.value);
			if (!route) return null;
			return {
				label: document.value.job,
				route,
				external: false,
			};
		})(),
	},
	{ label: 'Owner', value: document.value.owner },
	{ label: 'Modified By', value: document.value.modified_by },
]);

const severityClass = computed(() => {
	return {
		Info: 'bg-blue-50 text-blue-700',
		Warning: 'bg-yellow-50 text-yellow-700',
		Error: 'bg-red-50 text-red-700',
		Critical: 'bg-red-100 text-red-800',
	}[document.value.severity] || 'bg-gray-100 text-gray-700';
});

const prettyPayload = computed(() => {
	const payload = document.value.payload;
	if (!payload) {
		return 'No structured payload recorded.';
	}

	try {
		return JSON.stringify(JSON.parse(payload), null, 2);
	} catch (_error) {
		return payload;
	}
});
</script>
