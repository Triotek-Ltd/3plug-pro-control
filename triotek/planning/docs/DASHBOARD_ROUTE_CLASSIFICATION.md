# Dashboard Route Classification

## Purpose

Classify the imported Press dashboard routes before hiding or deleting UI surfaces.

Reference:

* `dashboard/src/router.js`

## Keep first

These route patterns match the first 3plug operator slice and should stay active as the base we adapt.

Keep first:

* `Home`
* `Welcome`
* `New Server`
* `New Site`
* `Server New Site`
* `Release Group New Site`
* `InstallApp`
* generic list and detail patterns fed through generated routes
* job-oriented pages such as `JobPage`

Why:

* they align with the server to bench to site to job workflow
* they are closest to the first operator actions we want

## Defer first

These route groups are outside the first 3plug v1 scope and should be candidates for hiding before deletion.

### Billing and payment

Defer:

* `Billing`
* `BillingOverview`
* `BillingForecast`
* `BillingInvoices`
* `BillingBalances`
* `BillingPaymentMethods`
* `BillingMarketplacePayouts`
* `BillingMpesaInvoices`
* `BillingUPIAutopay`
* `Checkout`
* `Subscription`

### Partner

Defer:

* `PartnerNewPayout`
* `PartnerLeadDetails`
* `SettingsPartnerAdmin`
* `PartnerList`
* `PartnerAdminLeads`
* `Partnership`
* all partner child routes

### SaaS and self-service signup

Defer:

* `Signup`
* `Signup Create Site`
* `SignupAppSelector`
* `SignupSetup`
* `SignupLoginToSite`
* `Setup Account`

## Caution

Do not remove these route groups first by deleting files only.

Before removal:

* find navigation links that reference them
* find components imported only by those routes
* find backend APIs that those pages depend on

## Working rule

First UI cleanup should likely be:

1. hide deferred navigation entry points
2. keep route files present until imports and references are mapped
3. remove deferred pages only after the route tree is clean
