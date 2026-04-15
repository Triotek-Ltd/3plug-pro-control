<template>
	<div class="p-5" v-if="job">
		<AlertAddressableError
			v-if="error"
			class="mb-5"
			:name="error.name"
			:title="error.title"
			@done="$resources.errors.reload()"
		/>
		<Button :route="backRoute">
			<template #prefix>
				<lucide-arrow-left class="inline-block h-4 w-4" />
			</template>
			Back to execution
		</Button>

		<div class="mt-3">
			<div>
				<div class="flex items-center">
					<h2 class="text-lg font-medium text-gray-900">{{ job.job_type }}</h2>
					<Badge class="ml-2" :label="job.status" />
					<div class="ml-auto flex items-center space-x-2">
						<Button
							@click="$resources.job.reload()"
							:loading="$resources.job.get.loading"
						>
							<template #icon>
								<lucide-refresh-ccw class="h-4 w-4" />
							</template>
						</Button>
						<Dropdown v-if="dropdownOptions.length" :options="dropdownOptions">
							<template v-slot="{ open }">
								<Button>
									<template #icon>
										<lucide-more-horizontal class="h-4 w-4" />
									</template>
								</Button>
							</template>
						</Dropdown>
					</div>
				</div>
				<div>
					<div class="mt-2 text-sm text-gray-600">
						{{ jobContext }}
					</div>
					<div class="mt-5 grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-4">
						<div
							v-for="card in summaryCards"
							:key="card.label"
							class="rounded-lg border bg-white px-4 py-3"
						>
							<div class="text-sm text-gray-500">{{ card.label }}</div>
							<div class="mt-1 text-base font-semibold text-gray-900">
								{{ card.value }}
							</div>
							<div class="mt-1 text-xs text-gray-500">{{ card.help }}</div>
						</div>
					</div>
					<div
						v-if="latestDiagnostic"
						class="mt-4 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3"
					>
						<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
							<div>
								<p class="text-sm font-medium text-amber-900">Latest diagnostic evidence</p>
								<p class="mt-1 text-sm text-amber-800">
									{{ latestDiagnostic.summary || latestDiagnostic.event_type }}
								</p>
								<p class="mt-1 text-xs text-amber-700">
									{{ latestDiagnostic.event_type }} recorded
									{{ $format.date(latestDiagnostic.creation, 'lll') }}
								</p>
							</div>
							<Button
								v-if="latestDiagnosticRoute"
								:route="latestDiagnosticRoute"
								variant="outline"
							>
								Review Evidence
							</Button>
						</div>
					</div>
					<div
						class="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5"
					>
						<div>
							<div class="text-sm font-medium text-gray-500">Creation</div>
							<div class="mt-2 text-sm text-gray-900">
								{{ $format.date(job.creation, 'lll') }}
							</div>
						</div>
						<div>
							<div class="text-sm font-medium text-gray-500">Creator</div>
							<div class="mt-2 text-sm text-gray-900">
								{{ job.owner }}
							</div>
						</div>
						<div>
							<div class="text-sm font-medium text-gray-500">Duration</div>
							<div class="mt-2 text-sm text-gray-900">
								{{ job.end ? $format.duration(job.duration) : '-' }}
							</div>
						</div>
						<div>
							<div class="text-sm font-medium text-gray-500">Start</div>
							<div class="mt-2 text-sm text-gray-900">
								{{ $format.date(job.start, 'lll') }}
							</div>
						</div>
						<div>
							<div class="text-sm font-medium text-gray-500">End</div>
							<div class="mt-2 text-sm text-gray-900">
								{{ job.end ? $format.date(job.end, 'lll') : '-' }}
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="mt-8 rounded-lg border bg-white p-5" v-if="diagnosticEvents.length">
				<div class="flex items-center justify-between gap-4">
					<div>
						<h3 class="text-lg font-semibold text-gray-900">Diagnostic Trail</h3>
						<p class="mt-1 text-sm text-gray-600">
							Automatic and manual forensic evidence captured from this job, its stage output, and related runtime logs.
						</p>
					</div>
					<Button route="/forensics" variant="ghost">
						Open Forensics
					</Button>
				</div>
				<div class="mt-4 space-y-3">
					<div
						v-for="event in diagnosticEvents"
						:key="event.name"
						class="rounded-lg border border-gray-200 px-4 py-3"
					>
						<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
							<div>
								<div class="flex items-center gap-2">
									<Badge :label="event.severity || 'Info'" />
									<p class="text-sm font-medium text-gray-900">
										{{ event.event_type }}
									</p>
								</div>
								<p class="mt-2 text-sm text-gray-700">
									{{ event.summary || 'Diagnostic evidence captured for this execution.' }}
								</p>
								<p class="mt-1 text-xs text-gray-500">
									Recorded {{ $format.date(event.creation, 'lll') }}
								</p>
							</div>
							<Button
								:route="{ name: 'Forensic Event Detail', params: { name: event.name } }"
								variant="outline"
							>
								View Evidence
							</Button>
						</div>
					</div>
				</div>
			</div>

			<div class="mt-8 space-y-4">
				<div>
					<h3 class="text-lg font-semibold text-gray-900">Execution Stages</h3>
					<p class="mt-1 text-sm text-gray-600">
						Each stage records what ran, how long it took, and any output or failure details captured during execution.
					</p>
				</div>
				<JobStep v-for="step in job.steps" :step="step" :key="step.name" />
			</div>
		</div>
	</div>
</template>
<script>
import { FeatherIcon, Tooltip } from 'frappe-ui';
import { toast } from 'vue-sonner';
import AlertAddressableError from '../components/AlertAddressableError.vue';
import call from '../controllers/call';
import { duration } from '../utils/format';
import { getObject } from '../objects';
import JobStep from '../components/JobStep.vue';

export default {
	name: 'JobPage',
	props: ['id', 'objectType'],
	components: { Tooltip, FeatherIcon, JobStep, AlertAddressableError },
	resources: {
		job() {
			return {
				type: 'document',
				doctype: 'Agent Job',
				name: this.id,
				transform(job) {
					for (let step of job.steps) {
						step.title = step.step_name;
						step.duration = duration(step.duration);
						step.isOpen =
							this.job?.steps?.find((s) => s.name === step.name)?.isOpen ||
							false;
					}

					// on delivery failure, there'll be no output for any step
					// so show the job output (error) in the first step
					if (['Undelivered', 'Delivery Failure'].includes(job.status)) {
						job.steps[0].output = job.output;
					}

					return job;
				},
				onSuccess() {
					this.lastLoaded = Date.now();
				},
			};
		},
		errors() {
			return {
				type: 'list',
				cache: ['Press Notification', 'Error', 'Agent Job', this.id],
				doctype: 'Press Notification',
				auto: true,
				fields: ['title', 'name'],
				filters: {
					document_type: 'Agent Job',
					document_name: this.id,
					is_actionable: true,
					class: 'Error',
				},
				limit: 1,
				orderBy: 'creation desc',
			};
		},
		diagnostics() {
			return {
				type: 'list',
				doctype: 'Forensic Event',
				auto: true,
				fields: ['name', 'creation', 'severity', 'event_type', 'summary', 'status'],
				filters: {
					job: this.id,
				},
				orderBy: 'creation desc',
				pageLength: 10,
			};
		},
	},
	computed: {
		object() {
			return getObject(this.objectType);
		},
		backRoute() {
			const parentName = this.$route?.params?.name;
			if (this.objectType === 'Site') {
				return parentName ? `/sites/${parentName}/insights/jobs` : '/sites';
			}
			if (this.objectType === 'Bench') {
				return parentName ? `/benches/${parentName}/jobs` : '/benches';
			}
			if (this.objectType === 'Server') {
				return parentName ? `/servers/${parentName}/jobs` : '/servers';
			}
			if (this.objectType === 'Release Group') {
				return parentName ? `/groups/${parentName}/jobs` : '/groups';
			}
			return '/';
		},
		job() {
			return this.$resources.job.doc;
		},
		jobContext() {
			if (!this.job) return '';
			const target =
				this.job.site || this.job.bench || this.job.server || this.job.group;
			if (!target) {
				return 'Tracked execution for this product action.';
			}
			return `Tracked execution for ${target}. Review the stage timeline below to see what ran and what still needs attention.`;
		},
		summaryCards() {
			if (!this.job) return [];
			const steps = this.job.steps || [];
			const failedSteps = steps.filter((step) => step.status === 'Failure').length;
			const completedSteps = steps.filter((step) => step.status === 'Success').length;
			const runningStep =
				steps.find((step) => step.status === 'Running')?.title || 'None';
			return [
				{
					label: 'Resource',
					value:
						this.job.site || this.job.bench || this.job.server || this.job.group || 'Platform',
					help: 'The resource this execution is acting on.',
				},
				{
					label: 'Stages',
					value: `${steps.length}`,
					help: 'Recorded execution stages for this job.',
				},
				{
					label: 'Completed',
					value: `${completedSteps}`,
					help: failedSteps ? `${failedSteps} stage failures recorded.` : 'No stage failures recorded.',
				},
				{
					label: 'Current Stage',
					value: runningStep,
					help: this.job.status === 'Running' ? 'Execution is still active.' : 'Execution is not currently running.',
				},
			];
		},
		error() {
			return this.$resources.errors?.data?.[0] ?? null;
		},
		diagnosticEvents() {
			return (this.$resources.diagnostics?.data || [])
				.filter((event) => String(event.event_type || '').includes('Diagnostics'))
				.slice(0, 5);
		},
		latestDiagnostic() {
			return this.diagnosticEvents[0] || null;
		},
		latestDiagnosticRoute() {
			if (!this.latestDiagnostic) return null;
			return {
				name: 'Forensic Event Detail',
				params: { name: this.latestDiagnostic.name },
			};
		},
		canDiagnose() {
			return ['Failure', 'Delivery Failure', 'Undelivered', 'Running'].includes(
				this.job?.status,
			);
		},
		canRetry() {
			return ['Failure', 'Delivery Failure', 'Undelivered'].includes(
				this.job?.status,
			);
		},
		canRetryInPlace() {
			return this.job?.status === 'Undelivered';
		},
		canRetrySkipPatches() {
			return this.canRetry && /patch/i.test(this.job?.job_type || '');
		},
		canCancel() {
			return ['Pending', 'Running'].includes(this.job?.status);
		},
		dropdownOptions() {
			return [
				{
					label: 'Diagnose',
					icon: 'search',
					condition: () => this.canDiagnose,
					onClick: () =>
						this.runJobAction('diagnose', {
							loading: 'Capturing diagnostic evidence...',
							success: 'Diagnostic evidence captured',
							error: 'Failed to capture diagnostic evidence',
						}),
				},
				{
					label: 'Retry Job',
					icon: 'rotate-ccw',
					condition: () => this.canRetry,
					onClick: () =>
						this.runJobAction('retry', {
							loading: 'Queueing retry...',
							success: 'Retry queued',
							error: 'Failed to queue retry',
						}),
				},
				{
					label: 'Retry In Place',
					icon: 'refresh-ccw',
					condition: () => this.canRetryInPlace,
					onClick: () =>
						this.runJobAction('retry_in_place', {
							loading: 'Retrying this execution...',
							success: 'Retry started for this execution',
							error: 'Failed to retry this execution',
						}),
				},
				{
					label: 'Retry and Skip Failing Patches',
					icon: 'shield-alert',
					condition: () => this.canRetrySkipPatches,
					onClick: () =>
						this.runJobAction('retry_skip_failing_patches', {
							loading: 'Queueing patch-safe retry...',
							success: 'Patch-safe retry queued',
							error: 'Failed to queue patch-safe retry',
						}),
				},
				{
					label: 'Cancel Execution',
					icon: 'x-circle',
					condition: () => this.canCancel,
					onClick: () =>
						this.runJobAction('cancel_job', {
							loading: 'Cancelling execution...',
							success: 'Execution cancel requested',
							error: 'Failed to cancel execution',
						}),
				},
				{
					label: 'Review Latest Evidence',
					icon: 'file-search',
					condition: () => !!this.latestDiagnostic,
					onClick: () => {
						this.$router.push(this.latestDiagnosticRoute);
					},
				},
				{
					label: 'View in Desk',
					icon: 'external-link',
					condition: () => this.$team?.doc?.is_desk_user,
					onClick: () => {
						window.open(
							`${window.location.protocol}//${window.location.host}/app/agent-job/${this.id}`,
							'_blank',
						);
					},
				},
			].filter((option) => option.condition?.() ?? true);
		},
	},
	mounted() {
		this.$socket.emit('doc_subscribe', 'Agent Job', this.id);
		this.$socket.on('agent_job_update', (data) => {
			if (data.id === this.id) {
				data.steps = data.steps.map((step) => {
					step.title = step.step_name;
					step.duration = duration(step.duration);
					step.isOpen =
						this.job?.steps?.find((s) => s.name === step.name)?.isOpen || false;
					return step;
				});

				this.$resources.job.doc = {
					...this.$resources.job.doc,
					...data,
				};
			}
		});
		// reload job every minute, in case socket is not working
		this.reloadInterval = setInterval(() => {
			this.reload();
		}, 1000 * 60);
	},
	beforeUnmount() {
		this.$socket.emit('doc_unsubscribe', 'Agent Job', this.id);
		this.$socket.off('agent_job_update');
		clearInterval(this.reloadInterval);
	},
	methods: {
		reload() {
			if (
				!this.$resources.job.loading &&
				// reload if job was loaded more than 5 seconds ago
				Date.now() - this.lastLoaded > 5000
			) {
				this.$resources.job.reload();
			}
		},
		runJobAction(method, messages) {
			return toast.promise(
				call('press.api.client.run_doc_method', {
					dt: 'Agent Job',
					dn: this.id,
					method,
				}).then(() => {
					this.$resources.job.reload();
					this.$resources.errors.reload();
					this.$resources.diagnostics.reload();
				}),
				{
					loading: messages.loading,
					success: messages.success,
					error: (error) => error?.messages?.[0] || messages.error,
				},
			);
		},
	},
};
</script>
