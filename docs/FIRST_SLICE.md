# First Slice

## Goal

Start 3plug Control as a Press-derived product with the smallest real platform slice that fits Triotek's current operating model.

## Product scope

Single-server first:

* one managed server
* many benches on that server
* many sites on those benches

## Backend objects to define first

* `3plug Server`
* `3plug Bench`
* `3plug Site`
* `3plug Job`
* `3plug App Source`
* `3plug Stack`

## First UI pages to define

* server overview
* bench inventory
* bench detail
* site inventory
* site detail
* job activity

## First write flows to support

* register server
* register bench
* create site
* install app on site

## Rule

Each of these actions should be modeled as a Press-style job flow, not a foreground shell-only command flow.
