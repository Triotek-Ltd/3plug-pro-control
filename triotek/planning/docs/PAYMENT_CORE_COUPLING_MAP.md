# Payment Core Coupling Map

## Purpose

Identify the payment assumptions still embedded in the core Press doctypes that 3plug is keeping, so cleanup can proceed without breaking the server to bench to site spine.

## Main Coupling Areas

### Team

Primary file:

* [team.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/press/doctype/team/team.py)

This is the deepest payment knot in the imported Press base.

Key coupling patterns:

* team-level `payment_mode`
* billing address and billing-name management
* Stripe payment method creation and validation
* Razorpay mandate validation
* balance and prepaid credit logic
* invoice updates and invoice-derived onboarding state
* budget alerts and failed-payment mail flows

Cleanup implication:

* do not start by deleting this code blindly
* first stop outside callers from depending on it
* then split business billing concepts from account or operator profile concepts

### Site

Primary file:

* [site.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/press/doctype/site/site.py)

Key coupling patterns:

* plan-change logic that expects valid payment state
* subscription creation and enable or disable flows
* marketplace app subscription handling
* invoice-based checks around plan eligibility
* trial-site subscription creation

Cleanup implication:

* site lifecycle still works through this file
* payment and subscription assumptions should be trimmed by targeted condition changes, not broad removal

### Server

Primary file:

* [server.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/press/doctype/server/server.py)

Key coupling patterns:

* server subscription creation
* add-on storage subscription handling
* partner-paid billing path checks during plan change

Cleanup implication:

* server creation and management are in scope for 3plug
* subscription-specific logic should be reduced without disturbing server lifecycle itself

## Secondary Payment Surfaces

These are still payment-oriented but are not the deepest core coupling:

* [auth.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/auth.py)
* [commands.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/commands.py)
* [bootstrap.py](/c:/Users/Administrator/isaac/erp/rnd/3plug-pro-root/3plug/repos/platform/3plug-control/press/bootstrap.py)

These are better early cleanup targets because they expose payment webhooks, Stripe setup utilities, or local Stripe bootstrap behavior without being required for core server, bench, or site management.

## Recommended Next Reduction Order

1. remove payment webhook and bootstrap affordances
2. classify payment-related API entry points and method permissions
3. trim site and server subscription assumptions where the behavior is clearly commercial rather than operational
4. leave the deepest `team.py` billing logic for a later focused pass

## Boundary Reminder

If a change affects:

* customer billing
* invoices
* Stripe
* Razorpay
* M-Pesa
* prepaid credits
* subscription charging

it should move toward the admin or business site, not deeper into `3plug-control`
