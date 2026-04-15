<template>
	<div class="sticky top-0 z-10 shrink-0">
		<Header>
			<Breadcrumbs
				:items="[
					{ label: 'Servers', route: '/servers' },
					{ label: 'Register Managed Server', route: '/servers/register-managed' },
				]"
			/>
		</Header>
	</div>

	<div
		v-if="!$team.doc?.is_desk_user && !$session.hasServerCreationAccess"
		class="mx-auto mt-60 w-fit rounded-md border border-dashed px-12 py-8 text-center text-gray-600"
	>
		<lucide-alert-triangle class="mx-auto mb-4 h-6 w-6 text-red-600" />
		<ErrorMessage message="You aren't permitted to register managed servers" />
	</div>

	<div
		v-else-if="!$team.doc?.self_hosted_servers_enabled"
		class="mx-auto mt-24 max-w-3xl rounded-xl border bg-white p-8 text-gray-700"
	>
		<h2 class="text-xl font-semibold text-gray-900">
			Self-hosted server registration is not enabled
		</h2>
		<p class="mt-3 text-sm">
			This 3plug flow is meant for the single managed-server model. Enable
			self-hosted server access for this team before registering the target
			server.
		</p>
	</div>

	<div v-else class="mx-auto max-w-6xl px-5 py-8">
		<div class="grid gap-6 xl:grid-cols-[minmax(0,1.35fr)_24rem]">
			<div class="space-y-6">
				<section class="overflow-hidden rounded-2xl border bg-gradient-to-br from-slate-950 via-slate-900 to-sky-950 p-6 text-white">
					<p class="text-sm uppercase tracking-[0.18em] text-sky-200">
						Managed Server Registration
					</p>
					<h1 class="mt-2 text-3xl font-semibold tracking-tight">
						Onboard the Linux server 3plug will manage
					</h1>
					<p class="mt-3 max-w-3xl text-sm leading-6 text-slate-200">
						This is the first real task in 3plug. Enter the server basics once,
						then 3plug verifies the machine, captures the runtime facts it can
						discover, creates the managed server records, and moves straight into
						bench onboarding.
					</p>
					<div class="mt-6 grid gap-3 sm:grid-cols-3">
						<div
							v-for="card in heroCards"
							:key="card.label"
							class="rounded-xl border border-white/10 bg-white/5 px-4 py-4 backdrop-blur"
						>
							<div class="text-xs uppercase tracking-wide text-sky-200">{{ card.label }}</div>
							<div class="mt-2 text-lg font-semibold text-white">{{ card.value }}</div>
							<div class="mt-1 text-xs text-slate-300">{{ card.help }}</div>
						</div>
					</div>
					<div class="mt-6 flex flex-wrap gap-3">
						<Button
							variant="solid"
							@click="registerServer"
							:loading="$resources.registerManagedServer.loading"
						>
							Start Server Onboarding
						</Button>
						<Button
							v-if="sshKey"
							variant="outline"
							@click="copySshKey"
						>
							Copy Bootstrap SSH Key
						</Button>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Onboarding Profile</h2>
					<div class="mt-5 grid gap-5 md:grid-cols-2">
						<FormControl
							label="Server Title"
							type="text"
							v-model="form.title"
							placeholder="Triotek Production Server"
						/>
						<FormControl
							label="Primary Contact Email"
							type="email"
							v-model="form.onboarding_email"
							placeholder="ops@triotek.co.ke"
						/>
						<FormControl
							label="Primary Domain"
							type="text"
							v-model="form.server_url"
							placeholder="control.example.com"
						/>
						<FormControl
							label="Sudo / SSH User"
							type="text"
							v-model="form.ssh_user"
							placeholder="ubuntu"
						/>
						<div class="md:col-span-2">
							<FormControl
								label="Managed Domains"
								type="textarea"
								v-model="form.managed_domains"
								placeholder="example.com&#10;apps.example.com&#10;erp.example.com"
							/>
							<p class="mt-2 text-xs text-gray-500">
								Use one domain per line. 3plug stores these as the intended
								domain set for this managed server.
							</p>
						</div>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Access and Runtime Detection</h2>
					<div class="mt-5 grid gap-5 md:grid-cols-2">
						<div>
							<p class="text-sm font-medium text-gray-900">Default Plan</p>
							<div class="mt-2 rounded-lg border bg-gray-50 px-4 py-3 text-sm text-gray-700">
								{{ planLabel }}
							</div>
						</div>
						<FormControl
							label="SSH Port"
							type="number"
							v-model="form.ssh_port"
							placeholder="22"
						/>
						<div class="md:col-span-2 rounded-lg border bg-slate-50 px-4 py-4">
							<div class="text-sm font-medium text-gray-900">Automatic Detection</div>
							<div class="mt-2 space-y-2 text-sm text-gray-600">
								<p>
									3plug resolves the public server IP from the primary domain you enter
									above.
								</p>
								<p>
									The private IP, runtime user, storage layout, memory, and process
									state are discovered during verification.
								</p>
							</div>
						</div>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<div class="flex items-start justify-between gap-4">
						<div>
							<h2 class="text-lg font-semibold text-gray-900">
								Bootstrap Access
							</h2>
							<p class="mt-2 text-sm text-gray-600">
								The target server must trust the default SSH key so 3plug can
								verify the machine, inspect memory and storage facts, and run the
								initial setup scripts.
							</p>
						</div>
						<Button
							v-if="sshKey"
							variant="ghost"
							@click="copySshKey"
						>
							Copy SSH Key
						</Button>
					</div>
					<pre
						class="mt-4 overflow-auto rounded-lg bg-gray-950 p-4 text-xs leading-6 text-gray-100"
					>{{ sshKey || 'Loading SSH key...' }}</pre>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<div class="flex items-start justify-between gap-4">
						<div>
							<h2 class="text-lg font-semibold text-gray-900">Create Record</h2>
							<p class="mt-2 text-sm text-gray-600">
								This runs the scripted onboarding path. 3plug verifies the
								target server, captures the core machine facts it can detect,
								creates the managed server chain, and starts the one-server
								setup flow automatically.
							</p>
						</div>
						<Button
							variant="solid"
							@click="registerServer"
							:loading="$resources.registerManagedServer.loading"
						>
							Start Server Onboarding
						</Button>
					</div>
					<div
						v-if="$resources.registerManagedServer.error"
						class="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
					>
						{{ $resources.registerManagedServer.error }}
					</div>
				</section>
			</div>

			<div class="space-y-6">
				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">First-run Path</h2>
					<div class="mt-4 space-y-3">
						<div
							v-for="step in onboardingPath"
							:key="step.label"
							class="rounded-lg border px-4 py-3"
						>
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">{{ step.label }}</div>
								<div class="rounded-full bg-slate-900 px-2.5 py-1 text-xs font-medium text-white">
									{{ step.index }}
								</div>
							</div>
							<div class="mt-1 text-sm text-gray-600">{{ step.detail }}</div>
						</div>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Readiness Checks</h2>
					<ul class="mt-4 space-y-3 text-sm text-gray-600">
						<li>SSH access must work from 3plug to the target Linux server.</li>
						<li>The sudo user must be able to run the onboarding scripts cleanly.</li>
						<li>The primary domain must already resolve to the target server.</li>
						<li>3plug will inspect CPU, memory, storage, and runtime basics during verification.</li>
					</ul>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">What happens next</h2>
					<ul class="mt-4 space-y-3 text-sm text-gray-600">
						<li>3plug creates the managed server records behind the scenes.</li>
						<li>The platform verifies reachability and captures core machine facts.</li>
						<li>Setup jobs and plays become visible on the server detail page.</li>
						<li>After that, we move straight into bench discovery and site operations.</li>
					</ul>
				</section>
			</div>
		</div>
	</div>
</template>

<script>
import { FormControl, Breadcrumbs, Button, ErrorMessage } from 'frappe-ui';
import Header from '../components/Header.vue';

export default {
	name: 'RegisterManagedServer',
	components: {
		Breadcrumbs,
		Button,
		ErrorMessage,
		FormControl,
		Header,
	},
	data() {
		return {
			form: {
				title: '',
				onboarding_email: '',
				server_url: '',
				managed_domains: '',
				ssh_user: '',
				ssh_port: 22,
			},
		};
	},
	resources: {
		managedServerOptions() {
			return {
				url: 'press.api.selfhosted.options_for_new',
				auto: true,
			};
		},
		registerManagedServer() {
			return {
				url: 'press.api.selfhosted.create_and_verify_selfhosted',
				makeParams: () => ({
					server: {
						title: this.form.title,
						onboarding_email: this.form.onboarding_email,
						server_url: this.form.server_url,
						managed_domains: this.form.managed_domains,
						ssh_user: this.form.ssh_user,
						ssh_port: this.form.ssh_port,
						plan: this.defaultPlan,
					},
				}),
				validate: () => {
					for (const [key, value] of Object.entries(this.form)) {
						if (value === null || value === undefined || value === '') {
							throw new Error(`${this.prettyLabel(key)} is required`);
						}
					}
					if (!String(this.form.onboarding_email).includes('@')) {
						throw new Error('Primary contact email must be valid');
					}
					if (!this.defaultPlan) {
						throw new Error('No self-hosted server plan is available');
					}
				},
				onSuccess: (server) => {
					this.$router.push({
						name: 'Managed Server Onboarding',
						params: { name: server.self_hosted_server },
					});
				},
			};
		},
	},
	computed: {
		sshKey() {
			return this.$resources.managedServerOptions.data?.ssh_key || '';
		},
		defaultPlan() {
			return this.$resources.managedServerOptions.data?.plans?.[0] || null;
		},
		planLabel() {
			if (!this.defaultPlan) return 'No self-hosted plan found';
			return this.$format.planTitle(this.defaultPlan);
		},
		heroCards() {
			return [
				{
					label: 'Default Runtime Plan',
					value: this.planLabel,
					help: 'The first managed runtime profile used for this server.',
				},
				{
					label: 'Bootstrap Access',
					value: this.sshKey ? 'Ready' : 'Loading',
					help: 'The SSH trust path 3plug uses for verification and setup.',
				},
				{
					label: 'Next Outcome',
					value: 'Managed Server',
					help: 'A real server record, runtime facts, and onboarding progress tracking.',
				},
			];
		},
		onboardingPath() {
			return [
				{
					index: '01',
					label: 'Register Server',
					detail: 'Capture the managed hostname, domains, contact email, and bootstrap access path.',
				},
				{
					index: '02',
					label: 'Verify Machine',
					detail: 'Inspect SSH access, private IP ownership, CPU, memory, storage, and runtime prerequisites.',
				},
				{
					index: '03',
					label: 'Create Runtime',
					detail: 'Create the managed runtime records and apply the production setup pipeline automatically.',
				},
				{
					index: '04',
					label: 'Hand Off To Management',
					detail: 'Move directly into server management, then bench discovery and site operations.',
				},
			];
		},
	},
	watch: {
		'$resources.managedServerOptions.data': {
			handler(data) {
				if (!this.form.ssh_user) {
					this.form.ssh_user = data?.default_ssh_user || 'root';
				}
				if (!this.form.ssh_port) {
					this.form.ssh_port = data?.default_ssh_port || 22;
				}
			},
			immediate: true,
		},
	},
	methods: {
		prettyLabel(key) {
			return key.replaceAll('_', ' ').replace(/\b\w/g, (char) => char.toUpperCase());
		},
		async copySshKey() {
			if (!this.sshKey) return;
			await navigator.clipboard.writeText(this.sshKey);
		},
		registerServer() {
			this.$resources.registerManagedServer.submit();
		},
	},
};
</script>
