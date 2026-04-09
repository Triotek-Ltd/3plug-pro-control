# Payment Handoff To Admin Site

## Decision

Payments are no longer part of `3plug-control`.

`3plug-control` remains the infrastructure control plane for:

* servers
* benches
* sites
* jobs
* forensic logging and reporting

The separate admin or business site becomes the home for:

* customer billing
* invoices
* subscriptions
* prepaid balances
* card payments
* M-Pesa
* any vendor or commerce payment flow

## Why

The imported Press payment layer is built for platform commerce inside the control plane.

That is not the 3plug v1 product boundary.

For 3plug v1:

* operations belong in `3plug-control`
* money movement belongs in the admin or business application

This keeps the control plane smaller, easier to secure, and easier to audit.

## Current Press-Derived Payment Flows

### Team billing state

The current payment model is centered on the `Team` record and related billing state such as:

* `payment_mode`
* `billing_details`
* balances, invoices, and prepaid credit flows
* payment-method refresh and mandate state

This is why many dashboard pages currently gate actions on team billing readiness.

### Dashboard payment UX

The current dashboard payment layer includes:

* account and billing detail dialogs
* card setup and mandate refresh dialogs
* prepaid credit purchase flows
* Stripe and Razorpay payment paths
* M-Pesa prepaid credit purchase and setup flows
* payment alerts on list pages and onboarding
* plan-change flows that force payment setup before continuing

Representative frontend files:

* `dashboard/src/components/ManageSitePlansDialog.vue`
* `dashboard/src/components/UpdateBillingDetails.vue`
* `dashboard/src/components/UpdateBillingDetailsForm.vue`
* `dashboard/src/components/StripeCardDialog.vue`
* `dashboard/src/components/BuyPrepaidCreditsForm.vue`
* `dashboard/src/components/billing/CardForm.vue`
* `dashboard/src/components/billing/BillingDetails.vue`
* `dashboard/src/components/billing/PrepaidCreditsForm.vue`
* `dashboard/src/components/billing/mpesa/BuyPrepaidCreditsMpesa.vue`

### Backend payment APIs

Representative backend payment areas:

* `press/api/billing.py`
* `press/api/account.py`
* `press/api/regional_payments/mpesa/utils.py`
* `press/press/doctype/team/*`
* `press/press/doctype/invoice/*`
* `press/press/doctype/mpesa_setup/*`
* `press/press/doctype/mpesa_payment_record/*`
* `press/press/doctype/razorpay_*/*`

### M-Pesa note

The current M-Pesa layer is not site-scoped.

It is tied to the Press team or platform billing model, so it should not be copied blindly into the admin site. If the admin site needs M-Pesa, it should re-implement it using the business-side ownership model that matches the final product.

## What The Admin Site Should Reuse

Reuse concepts, not the whole Press payment stack.

Recommended carry-over:

* billing identity capture
* invoice and payment record concepts
* M-Pesa capability, if needed for Kenyan or regional customer collections
* webhook-based payment confirmation patterns
* forensic-grade payment event logging

Recommended redesign in the admin site:

* ownership model
* payment configuration scope
* payment-to-customer mapping
* vendor and marketplace payout logic
* site-by-site or tenant-by-tenant payment configuration

## What 3plug-Control Should Remove

`3plug-control` should remove or neutralize:

* payment gating on site, app, and server actions
* billing alerts and payment reminders
* card, prepaid credit, Stripe, Razorpay, and M-Pesa dialogs
* payment-oriented onboarding steps
* checkout, subscription, and invoice UX

## Cleanup Rule

When a payment surface is removed from `3plug-control`:

* capture the old role in this handoff record or cleanup log
* remove the live UI dependency
* remove the now-orphaned component or route
* leave deeper backend deletion for later passes once dependencies are mapped
