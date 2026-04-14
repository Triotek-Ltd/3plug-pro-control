# Control Settings

This page defines what `Control Settings` should contain in 3plug Control.

It is based on:

* the 3plug target state
* the agreed product shell and features
* the current `Press Settings` doctype and what it is still being used for

The main rule is simple:

`Control Settings` should keep the settings that support the one-server control-plane workflow and stop centering the product on old Press billing, marketplace, and partner concerns.

Important note:

* the current backend still uses legacy `usd` and `inr` fieldnames in many places
* the product-facing language should now be `GBP` and `KSh`
* until we do a full billing and pricing model migration, we should prefer changing visible labels and docs first, while keeping backend fieldnames stable

## What Control Settings Is For

`Control Settings` should configure the platform-level behavior of 3plug Control.

It should answer questions like:

* what domain and runtime defaults does this control plane use
* how does it build, clone, and release app and bench changes
* how are jobs, plays, notifications, and incident actions handled
* what GitHub, asset, and storage integrations are required for operations
* what limits, toggles, and safety controls apply to this deployment

It should not be the dumping ground for every old Press concern.

## Target Setting Groups

The intended `Control Settings` surface should be grouped like this.

### 1. Platform Identity

These settings define the identity and default network shape of the control plane.

Keep or reframe:

* `domain`
* `root_domain`
* `hybrid_domain`
* `cluster`
* `hybrid_cluster`
* `production_server_ip`

Why they belong:

* they define where the control plane and managed sites live
* they still support the server -> bench -> site model

### 2. Managed Server And Bench Runtime

These settings define runtime defaults and execution limits for the managed environment.

Keep or reframe:

* `bench_configuration`
* `default_server_plan_type`
* `minimum_rebuild_memory`
* `new_bench_concurrency_limit`
* `redis_cache_size`
* `set_redis_password`
* `shared_directory`
* `cool_off_period`
* `servers_using_alternative_http_port_for_communication`

Why they belong:

* they affect real bench and server behavior
* they are part of operating one managed Linux server with many benches and sites

### 3. Build, Release, And App Delivery

These settings support the app and release workflow.

Keep or reframe:

* `build_server`
* `clone_directory`
* `build_directory`
* `suspend_builds`
* `use_app_cache`
* `compress_app_cache`
* `use_delta_builds`
* `auto_update_queue_size`
* `publish_docs`
* `default_apps`

Why they belong:

* 3plug still needs app and release operations
* these settings support controlled change delivery across benches and sites

### 4. GitHub And Source Integrations

These settings support source discovery, releases, and webhook-driven automation.

Keep or reframe:

* `github_app_id`
* `github_app_client_id`
* `github_app_client_secret`
* `github_app_private_key`
* `github_app_public_link`
* `github_webhook_secret`
* `github_access_token`
* `github_pat_token`
* `agent_repository_owner`
* `agent_github_access_token`
* `branch`

Why they belong:

* they support app sources, releases, and automation
* they belong under `Apps` and `Operations`, not under old Press branding

### 5. Storage, Assets, And Remote Files

These settings support assets, backups, and remote file access that the control plane still needs.

Keep or reframe:

* `use_asset_store`
* `asset_store_access_key`
* `asset_store_secret_access_key`
* `asset_store_endpoint`
* `asset_store_region`
* `asset_store_bucket_name`
* `remote_uploads_bucket`
* `remote_link_expiry`
* `remote_access_key_id`
* `remote_secret_access_key`
* `enforce_storage_limits`

Review carefully before removing:

* `offsite_backups_provider`
* `backup_region`
* `aws_s3_bucket`
* `offsite_backups_access_key_id`
* `offsite_backups_secret_access_key`
* `offsite_backups_count`
* `backup_interval`
* `backup_offset`
* `backup_limit`
* `max_failed_backup_attempts_in_a_day`
* `disable_physical_backup`
* `max_concurrent_physical_restorations`

Why they belong:

* asset and remote-file settings are clearly operational
* backup settings may still be critical even if we later simplify how they are presented

### 6. Jobs, Notifications, And Incident Response

These settings support the traceability spine of the product.

Keep or reframe:

* `use_agent_job_callbacks`
* `realtime_job_updates`
* `disable_agent_job_deduplication`
* `disable_auto_retry`
* `disable_binlog_indexer_service`
* `execute_incident_action`
* `enable_server_snapshot_recovery`
* `monitor_server`
* `monitor_token`
* `log_server`
* `press_monitoring_password`
* `send_telegram_notifications`
* `telegram_alert_chat_id`
* `telegram_alerts_chat_group`
* `send_email_notifications`
* `email_recipients`
* `agent_sentry_dsn`

Why they belong:

* jobs and forensics are core product features
* this is platform operations, not optional admin clutter

### 7. Certificates, Network Trust, And Access

These settings define how the platform handles TLS, SSH trust, and certificates.

Keep or reframe:

* `certbot_directory`
* `webroot_directory`
* `rsa_key_size`
* `eff_registration_email`
* `use_staging_ca`
* `ssh_certificate_authority`
* `tls_renewal_queue_size`

Why they belong:

* these are required for real managed infrastructure operations

### 8. Communication And Outbound Services

These settings support alerts, mail, and operator communication.

Keep or reframe:

* `telegram_bot_token`
* `telegram_chat_id`
* `mailgun_api_key`
* `default_outgoing_id`
* `default_outgoing_pass`
* `enable_spam_check`
* `spamd_endpoint`
* `spamd_api_key`
* `spamd_api_secret`
* `twilio_account_sid`
* `twilio_api_key_sid`
* `twilio_api_key_secret`
* `twilio_phone_number`

Why they belong:

* the control plane still needs notifications and outbound integrations

### 9. Feature Flags

These should stay, but they should be framed as product switches for 3plug Control.

Keep or reframe:

* `enable_google_oauth`
* `disallow_disposable_emails`
* `enable_email_pre_verification`
* `enable_app_grouping`

Review carefully before keeping:

* `verify_cards_with_micro_charge`

Why they belong:

* some of these are still real product behavior toggles
* payment-verification behavior should not dominate the settings surface

## What Should Be Hidden Or Deferred

These are the settings that do not belong at the center of a control-first 3plug product.

### Billing And Payment Operations

Keep, but reframe as Triotek commercial controls:

* `free_credits_usd`
* `free_credits_inr`
* `micro_debit_charge_usd`
* `micro_debit_charge_inr`
* `gst_percentage`
* `npo_discount`
* `autoscale_discount`
* `stripe_publishable_key`
* `stripe_secret_key`
* `stripe_product_id`
* `stripe_usd_plan_id`
* `stripe_inr_plan_id`
* `stripe_webhook_endpoint_id`
* `stripe_webhook_secret`
* `razorpay_key_id`
* `razorpay_key_secret`
* `razorpay_webhook_secret`
* `paypal_enabled`
* `ic_key`

Reason:

* billing is not the center of the current product target
* but it is still part of the product and should be presented as Triotek commercial policy rather than inherited Press billing admin

### Marketplace And Partnership

Keep, but reframe as Triotek channel and partner operations:

* `max_allowed_screenshots`
* `threshold`
* `commission`
* `usd_rate`
* `app_include_script`
* `plausible_url`
* `plausible_site_id`
* `plausible_api_key`
* `partnership_fee_usd`
* `partnership_fee_inr`
* `drive_resource_link`

Reason:

* these are not the center of the one-server control story
* but they remain part of the product and should be presented as marketplace channel policy, partner operations, and app distribution controls

### ERPNext, Frappe.io, And School-Specific Account Flows

Hide or defer:

* `erpnext_url`
* `erpnext_api_key`
* `erpnext_api_secret`
* `erpnext_domain`
* `erpnext_cluster`
* `erpnext_plan`
* `erpnext_group`
* `erpnext_apps`
* `central_migration_server`
* `staging_plan`
* `staging_expiry`
* `enable_site_pooling`
* `standby_pool_size`
* `standby_queue_size`
* `disable_frappe_auth`
* `frappe_url`
* `frappeio_api_key`
* `frappeio_api_secret`
Reason:

* these represent old product extensions and account ecosystems that are not central to 3plug Control right now
* if any school-specific controls remain visible, they should be framed as partner-sector integrations rather than as standalone product identity

## Product Decision

We should not rename the backend doctype immediately.

`Press Settings` is still referenced too widely in the codebase, and a direct rename would create unnecessary risk.

The safer path is:

1. keep the backend single doctype for now
2. treat it as the backing store
3. present it in the product as `Control Settings`
4. curate the visible sections around the target groups above
5. hide or defer the old Press-first sections from the main operator path

## Immediate Build Meaning

The next implementation step should be:

* keep `Press Settings` as the underlying doctype
* relabel the product-facing shortcut as `Control Settings`
* reorganize the visible settings experience around the target groups on this page
* stop exposing billing, marketplace, and partner-first settings as the default settings story
