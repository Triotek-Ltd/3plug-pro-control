<template>
	<Card title="Profile" v-if="user" class="mx-auto max-w-3xl">
		<div class="flex items-center border-b pb-3">
			<div class="relative">
				<Avatar size="2xl" :label="user.first_name" :image="user.user_image" />
				<FileUploader
					@success="onProfilePhotoChange"
					fileTypes="image/*"
					:upload-args="{
						doctype: 'User',
						docname: user.name,
						method: 'press.api.account.update_profile_picture',
					}"
				>
					<template v-slot="{ openFileSelector, uploading, progress, error }">
						<div class="ml-4">
							<button
								@click="openFileSelector()"
								class="absolute inset-0 grid h-10 w-full place-items-center rounded-full bg-black text-xs font-medium text-white opacity-0 transition hover:opacity-50 focus:opacity-50 focus:outline-none"
								:class="{ 'opacity-50': uploading }"
							>
								<span v-if="uploading">{{ progress }}%</span>
								<span v-else>Edit</span>
							</button>
						</div>
					</template>
				</FileUploader>
			</div>
			<div class="ml-4">
				<h3 class="text-base font-semibold">
					{{ user.first_name }} {{ user.last_name }}
				</h3>
				<p class="mt-1 text-base text-gray-600">{{ user.email }}</p>
			</div>
			<div class="ml-auto">
				<Button icon-left="edit" @click="showProfileEditDialog = true">
					Edit
				</Button>
			</div>
		</div>
		<ListItem
			title="Notification Settings"
			subtitle="Manage notification channels"
			v-if="$team?.doc?.user === $session?.user"
		>
			<template #actions>
				<Button @click="showCommunicationInfoDialog = true"> Manage </Button>
			</template>
		</ListItem>
		<div>
			<ListItem
				:title="user.is_2fa_enabled ? 'Disable 2FA' : 'Enable 2FA'"
				:subtitle="
					user.is_2fa_enabled
						? 'Disable two-factor authentication for your account'
						: 'Enable two-factor authentication for your account to add an extra layer of security'
				"
			>
				<template #actions>
					<Button @click="show2FADialog = true">
						{{ user.is_2fa_enabled ? 'Disable' : 'Enable' }}
					</Button>
				</template>
			</ListItem>
			<ListItem
				v-if="user.is_2fa_enabled"
				title="View Recovery Codes"
				subtitle="View your two-factor authentication recovery codes"
			>
				<template #actions>
					<Button @click="show2FARecoveryCodesDialog = true"> Show </Button>
				</template>
			</ListItem>
			<ListItem
				class="border-t"
				:title="teamEnabled ? 'Disable Account' : 'Enable Account'"
				:subtitle="
					teamEnabled
						? 'Disable your account and pause managed access'
						: 'Enable your account and restore managed access'
				"
			>
				<template #actions>
					<Button
						@click="
							() => {
								if (teamEnabled) {
									showDisableAccountDialog = true;
								} else {
									showEnableAccountDialog = true;
								}
							}
						"
					>
						<span :class="{ 'text-red-600': teamEnabled }">{{
							teamEnabled ? 'Disable' : 'Enable'
						}}</span>
					</Button>
				</template>
			</ListItem>
		</div>
		<Dialog
			:options="{
				title: 'Update Profile Information',
				actions: [
					{
						variant: 'solid',
						label: 'Save Changes',
						onClick: () => $resources.updateProfile.submit(),
					},
				],
			}"
			v-model="showProfileEditDialog"
		>
			<template v-slot:body-content>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<FormControl label="First Name" v-model="user.first_name" />
					<FormControl label="Last Name" v-model="user.last_name" />
				</div>
				<ErrorMessage class="mt-4" :message="$resources.updateProfile.error" />
			</template>
		</Dialog>

		<Dialog
			:options="{
				title: 'Disable Account',
				actions: [
					{
						label: 'Disable Account',
						variant: 'solid',
						theme: 'red',
						loading: $resources.disableAccount.loading,
						onClick: () => deactivateAccount(disableAccount2FACode),
					},
				],
			}"
			v-model="showDisableAccountDialog"
		>
			<template v-slot:body-content>
				<div class="prose text-base">
					By confirming this action:
					<ul>
						<li>Your account will be disabled</li>
						<li>
							Your active sites will be suspended immediately and will be
							deleted after a week.
						</li>
						<li>Managed access from this account will be paused</li>
					</ul>
					You can log in later to enable your account. Do you want to continue?
				</div>
				<FormControl
					v-if="user.is_2fa_enabled"
					class="mt-4"
					label="Enter your 2FA code to confirm"
					v-model="disableAccount2FACode"
				/>
				<ErrorMessage class="mt-2" :message="$resources.disableAccount.error" />
			</template>
		</Dialog>

		<Dialog
			:options="{
				title: 'Enable Account',
				actions: [
					{
						label: 'Enable Account',
						variant: 'solid',
						loading: $resources.enableAccount.loading,
						onClick: () => $resources.enableAccount.submit(),
					},
				],
			}"
			v-model="showEnableAccountDialog"
		>
			<template v-slot:body-content>
				<div class="prose text-base">
					By confirming this action:
					<ul>
						<li>Your account will be enabled</li>
						<li>Your suspended sites will become active</li>
						<li>Managed access from this account will be restored</li>
					</ul>
					Do you want to continue?
				</div>
				<ErrorMessage class="mt-2" :message="$resources.enableAccount.error" />
			</template>
		</Dialog>

		<CommunicationInfoDialog
			v-if="showCommunicationInfoDialog"
			v-model="showCommunicationInfoDialog"
			@close="showCommunicationInfoDialog = false"
			reference-doctype="Team"
			:reference-name="$team.doc.name"
		/>
	</Card>
	<TFADialog v-model="show2FADialog" />
	<TFARecoveryCodesDialog v-model="show2FARecoveryCodesDialog" />
</template>

<script>
import { toast } from 'vue-sonner';
import { defineAsyncComponent, h } from 'vue';
import FileUploader from '@/components/FileUploader.vue';
import { renderDialog } from '../../../utils/components';
import TFADialog from './TFADialog.vue';
import TFARecoveryCodesDialog from './TFARecoveryCodesDialog.vue';
import CommunicationInfoDialog from '../../CommunicationInfoDialog.vue';

export default {
	name: 'AccountProfile',
	components: {
		TFADialog,
		TFARecoveryCodesDialog,
		FileUploader,
	},
	data() {
		return {
			show2FADialog: false,
			show2FARecoveryCodesDialog: false,
			disableAccount2FACode: '',
			showProfileEditDialog: false,
			showEnableAccountDialog: false,
			showDisableAccountDialog: false,
			showCommunicationInfoDialog: false,
			showActiveServersDialog: false,
		};
	},
	computed: {
		teamEnabled() {
			return this.$team.doc.enabled;
		},
		user() {
			return this.$team?.doc?.user_info;
		},
	},
	resources: {
		updateProfile() {
			let { first_name, last_name, email } = this.user;
			return {
				url: 'press.api.account.update_profile',
				params: {
					first_name,
					last_name,
					email,
				},
				onSuccess() {
					this.showProfileEditDialog = false;
					this.notifySuccess();
				},
			};
		},
		disableAccount: {
			url: 'press.api.account.disable_account',
			onSuccess() {
				this.showDisableAccountDialog = false;

				const ChurnFeedbackDialog = defineAsyncComponent(
					() => import('../../ChurnFeedbackDialog.vue'),
				);

				renderDialog(
					h(ChurnFeedbackDialog, {
						team: this.$team.doc.name,
						onUpdated: () => {
							toast.success('Your feedback was submitted successfully');
						},
					}),
				);
				toast.success('Your account was disabled successfully');
				this.reloadAccount();
			},
		},
		enableAccount: {
			url: 'press.api.account.enable_account',
			onSuccess() {
				toast.success('Your account was enabled successfully');
				this.reloadAccount();
				this.showEnableAccountDialog = false;
			},
		},
		hasActiveServers() {
			return {
				url: 'press.api.account.has_active_servers',
				auto: true,
				params: {
					team: this.$team.doc.name,
				},
				onSuccess(data) {
					if (data) {
						this.showActiveServersDialog = true;
					}
				},
			};
		},
	},
	methods: {
		reloadAccount() {
			this.$team.reload();
		},
		onProfilePhotoChange() {
			this.reloadAccount();
			this.notifySuccess();
		},
		notifySuccess() {
			toast.success('Your profile was updated successfully');
		},
		deactivateAccount(disableAccount2FACode) {
			// validate if any active servers
			if (this.showActiveServersDialog) {
				const activeServersDialog = defineAsyncComponent(
					() => import('../../ActiveServersDialog.vue'),
				);
				renderDialog(h(activeServersDialog));
				return;
			}
			this.$resources.disableAccount.submit({
				totp_code: disableAccount2FACode,
			});
		},
	},
};
</script>
