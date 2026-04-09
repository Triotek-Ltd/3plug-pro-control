# Payment Scope Map

## Purpose

Separate the remaining payment-related dashboard code into:

* keep for 3plug v1
* defer and remove with cleanup

This avoids mixing the kept M-Pesa path with the broader Press billing and subscription product surface.

## Keep for 3plug v1

### Account details and minimal payment setup

Keep:

* `components/UpdateBillingDetails.vue`
* `components/UpdateBillingDetailsForm.vue`
* `components/AlertAddressDetails.vue`
* `components/AlertMandateInfo.vue`
* `components/StripeCardDialog.vue`
* `components/billing/BillingDetails.vue`
* `components/billing/CardForm.vue`
* `components/billing/NewAddressForm.vue`

Reason:

* these still support reachable account-detail and card-refresh flows
* they are the smallest shared set still wired into live settings or plan-management surfaces

### M-Pesa path

Keep:

* `components/billing/mpesa/BuyPrepaidCreditsMpesa.vue`
* `components/billing/mpesa/AddMpesaCredentials.vue`
* `components/billing/mpesa/AddPaymentGateway.vue`
* `components/billing/mpesa/PartnerPaymentPayout.vue`

Reason:

* M-Pesa remains in 3plug scope
* cleanup must not remove regional payment support we still want

### Temporary keep until plan-management decision is finalized

Keep for now:

* `components/ManageSitePlansDialog.vue`
* `components/billing/PrepaidCreditsForm.vue`
* `components/billing/BuyCreditsStripe.vue`
* `components/billing/BuyCreditsRazorpay.vue`
* `components/BuyPrepaidCreditsForm.vue`
* `components/BuyPrepaidCreditsStripe.vue`
* `components/BuyPrepaidCreditsRazorpay.vue`

Reason:

* these are still imported by live site-plan or onboarding flows
* they should be revisited if 3plug v1 decides to remove generic payment-mode setup entirely

## Defer and remove

### Generic Press commercial flows

Defer and remove:

* `pages/Checkout.vue`
* `pages/CheckoutApps.vue`
* `pages/CheckoutPlans.vue`
* `pages/CheckoutAddress.vue`
* `pages/CheckoutPayment.vue`
* `pages/Subscription.vue`
* `components/StripeCard.vue`

Reason:

* these are generic Press checkout/subscription product flows
* they are already deferred by route guard and should not stay as product-shaping code in 3plug v1

## Working rule

Until the forensic layer starts:

* keep account-detail support
* keep M-Pesa
* keep only the smallest payment pieces still required by live plan-management flows
* continue deleting generic Press checkout and subscription surfaces
