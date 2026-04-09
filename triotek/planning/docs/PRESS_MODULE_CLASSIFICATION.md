# Press Module Classification

## Purpose

Classify the imported Press modules before removing any code from the live codebase.

Reference:

* `press/modules.txt`
* `press/hooks.py`

## Keep first

### `Press`

Keep first.

Why:

* this is the core app module
* it contains the main server, bench, site, app-source, and job spine we want to adapt

## Defer but do not delete yet

### `Marketplace`

Defer.

Why:

* 3plug v1 is not a marketplace-first product
* this area touches billing, approvals, listings, and public-facing flows
* direct deletion too early could break hooks, templates, and dashboards

### `SaaS`

Defer.

Why:

* 3plug v1 is not starting as a shared SaaS self-service product
* this area includes signup, subscription, and customer lifecycle flows

### `Partner`

Defer.

Why:

* partner programs are outside the first operator slice
* dashboard and permissions are likely cross-linked here

### `Infrastructure`

Defer.

Why:

* parts of this may become useful later
* the current scope does not need the broader many-server and migration-heavy features

### `Incident Management`

Defer.

Why:

* useful later, not first-slice critical
* not the first thing to remove or reshape while we are still stabilizing the base

### `Experimental`

Defer.

Why:

* by definition, it is not the safest base for v1

## Working rule

For the next cleanup steps:

* keep `Press` as the active core
* treat the other modules as present but out of active 3plug v1 scope
* do not delete deferred modules until we isolate their hooks, routes, doctypes, and scheduler references
