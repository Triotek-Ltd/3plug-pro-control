from __future__ import annotations

PRIMARY_CURRENCY = "GBP"
REGIONAL_CURRENCY = "KES"

PRIMARY_CURRENCY_LABEL = "GBP"
REGIONAL_CURRENCY_LABEL = "KSh"
LEGACY_PRIMARY_PRICE_FIELD = "price_usd"
LEGACY_REGIONAL_PRICE_FIELD = "price_inr"
LEGACY_PRIMARY_NET_TOTAL_FIELD = "net_total_usd"
LEGACY_REGIONAL_NET_TOTAL_FIELD = "net_total_inr"
PRIMARY_TO_REGIONAL_RATE = 160

LEGACY_PRIMARY_CURRENCIES = {"GBP", "USD"}
LEGACY_REGIONAL_CURRENCIES = {"KES", "KSH", "INR"}
REGIONAL_COUNTRIES = {"Kenya"}


def normalize_currency(currency: str | None) -> str:
	if not currency:
		return PRIMARY_CURRENCY

	normalized = currency.upper()
	if normalized in LEGACY_REGIONAL_CURRENCIES:
		return REGIONAL_CURRENCY
	if normalized in LEGACY_PRIMARY_CURRENCIES:
		return PRIMARY_CURRENCY
	return normalized


def default_currency_for_country(country: str | None) -> str:
	if country in REGIONAL_COUNTRIES:
		return REGIONAL_CURRENCY
	return PRIMARY_CURRENCY


def is_regional_currency(currency: str | None) -> bool:
	return normalize_currency(currency) == REGIONAL_CURRENCY


def is_primary_currency(currency: str | None) -> bool:
	return normalize_currency(currency) == PRIMARY_CURRENCY


def display_currency_label(currency: str | None) -> str:
	if is_regional_currency(currency):
		return REGIONAL_CURRENCY_LABEL
	return PRIMARY_CURRENCY_LABEL


def currency_prefix(currency: str | None) -> str:
	label = display_currency_label(currency)
	if label == REGIONAL_CURRENCY_LABEL:
		return f"{label} "
	return f"{label} "


def minimum_prepaid_amount(currency: str | None) -> int:
	# Preserve the old regional threshold while the underlying pricing fields
	# still live in the legacy `*_inr` columns.
	if is_regional_currency(currency):
		return 450
	return 5


def plan_price_field(currency: str | None) -> str:
	if is_regional_currency(currency):
		return LEGACY_REGIONAL_PRICE_FIELD
	return LEGACY_PRIMARY_PRICE_FIELD


def payout_net_total_field(currency: str | None) -> str:
	if is_regional_currency(currency):
		return LEGACY_REGIONAL_NET_TOTAL_FIELD
	return LEGACY_PRIMARY_NET_TOTAL_FIELD


def micro_debit_charge_field(currency: str | None) -> str:
	if is_regional_currency(currency):
		return "micro_debit_charge_inr"
	return "micro_debit_charge_usd"


def should_generate_primary_currency_pdf(currency: str | None) -> bool:
	return is_primary_currency(currency)


def convert_amount(amount: float | int | None, from_currency: str | None, to_currency: str | None) -> float:
	amount = float(amount or 0)
	source = normalize_currency(from_currency)
	target = normalize_currency(to_currency)
	if source == target:
		return amount
	if is_primary_currency(source) and is_regional_currency(target):
		return amount * PRIMARY_TO_REGIONAL_RATE
	if is_regional_currency(source) and is_primary_currency(target):
		return amount / PRIMARY_TO_REGIONAL_RATE
	return amount
