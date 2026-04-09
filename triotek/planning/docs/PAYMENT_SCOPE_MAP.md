# Payment Scope Map

## Purpose

Define the payment boundary after the product decision that billing belongs in the admin or business site, not in `3plug-control`.

## Final Scope Decision

Remove the full Press-style payment layer from `3plug-control`.

This includes:

* billing details flows
* card setup
* prepaid credits
* Stripe
* Razorpay
* M-Pesa
* checkout
* subscriptions
* unpaid invoice alerts
* payment-mode gating

## Keep in 3plug-Control

Keep only documentation of the old flow during cleanup:

* `triotek/planning/docs/PAYMENT_HANDOFF_TO_ADMIN_SITE.md`
* `triotek/planning/docs/CLEANUP_ACTIVITY_LOG.md`

Reason:

* the admin or business site still needs the domain knowledge
* the control plane should not keep live payment code after the handoff decision

## Move To Admin Or Business Site

Move as business-side capabilities:

* customer billing
* invoice collection
* M-Pesa
* card payments
* vendor or marketplace payouts
* any customer wallet or prepaid balance concept

Reason:

* these are business flows, not infrastructure control-plane flows

## Remove From 3plug-Control

Remove:

* payment alerts on list pages
* billing requirements during onboarding
* payment-mode requirements for install, plan change, or server creation
* remaining card, prepaid credit, Stripe, Razorpay, and M-Pesa dialogs and forms
* remaining payment utility helpers that are only used by the removed UI

## Working Rule

During cleanup:

* document the old payment behavior first
* remove the live UI dependency second
* delete orphaned files third
* defer deeper backend deletion until references are fully mapped
