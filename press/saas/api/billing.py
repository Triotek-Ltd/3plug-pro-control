# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

import frappe

from press.api import billing as billing_api
from press.saas.api import whitelist_saas_api


def _payments_moved():
	frappe.throw("Payments and billing now live in the admin business site, not in 3plug Control.")


@whitelist_saas_api
def country_list():
	_payments_moved()


# Billing Information Related APIs
@whitelist_saas_api
def get_information(timezone=None):
	_payments_moved()


@whitelist_saas_api
def update_information(billing_details: dict):
	_payments_moved()


@whitelist_saas_api
def validate_gst(address: dict):
	return billing_api.validate_gst(address)


@whitelist_saas_api
def change_payment_mode(mode: str):
	_payments_moved()


# Stripe Payment Gateway Related APIs
@whitelist_saas_api
def get_publishable_key_and_setup_intent():
	_payments_moved()


@whitelist_saas_api
def setup_intent_success(setup_intent, address=None):
	_payments_moved()


@whitelist_saas_api
def create_payment_intent_for_micro_debit(payment_method_name):
	_payments_moved()


@whitelist_saas_api
def create_payment_intent_for_buying_credits(amount):
	_payments_moved()


# Razorpay Payment Gateway Related APIs
@whitelist_saas_api
def create_razorpay_order(amount, type, doc_name=None):
	_payments_moved()


@whitelist_saas_api
def handle_razorpay_payment_failed():
	_payments_moved()


# Invoice Related APIs
@whitelist_saas_api
def get_invoices():
	_payments_moved()


@whitelist_saas_api
def upcoming_invoice():
	_payments_moved()


@whitelist_saas_api
def get_unpaid_invoices():
	_payments_moved()


@whitelist_saas_api
def total_unpaid_amount():
	_payments_moved()


@whitelist_saas_api
def get_invoice(name: str):
	_payments_moved()


@whitelist_saas_api
def download_invoice(name: str):
	_payments_moved()


@whitelist_saas_api
def get_stripe_payment_url_for_invoice(name: str) -> str | None:
	_payments_moved()


# Payment Method Related APIs
@whitelist_saas_api
def get_payment_methods():
	_payments_moved()


@whitelist_saas_api
def set_as_default(name):
	_payments_moved()


@whitelist_saas_api
def remove_payment_method(name):
	_payments_moved()
