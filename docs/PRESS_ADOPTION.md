# Press Adoption

## Decision

3plug Control should be built from Press.

This is not a loose inspiration exercise.

This repo should become Triotek's adapted Press-style control plane.

## Local reference

Use the local repo:

* `../frappe-press`

## Adaptation rule

Keep:

* Frappe app backend
* dashboard SPA
* persistent platform doctypes
* agent/job orchestration
* permission and guard patterns

Simplify first:

* one server instead of broad multi-server hosting scope
* Bench-first lifecycle
* site and app operations for Triotek-managed stacks

## First records to define

* `3plug Server`
* `3plug Bench`
* `3plug Site`
* `3plug Job`
* `3plug App Source`
* `3plug Stack`
