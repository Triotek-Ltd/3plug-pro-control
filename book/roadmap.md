# Product Roadmap

This page is the working roadmap for 3plug Control.

It translates the target state, benchmark findings, and cleanup work into an
ordered build plan.

The goal is to keep us focused on the actual product:

- one managed Linux server
- many benches on that server
- many sites on those benches
- jobs, plays, and forensic records for traceability

## Roadmap Rules

Every roadmap item should satisfy at least one of these:

- improves the first-run operator workflow
- improves a core runtime workflow
- improves traceability
- removes inherited Press confusion

If it does not do one of those, it should wait.

## Current Product Sequence

The intended user journey is:

1. open 3plug Control
2. onboard the managed server
3. verify server readiness
4. discover or register benches
5. create or import sites
6. operate through jobs, plays, and forensics

That means the roadmap should follow the same order.

## Phase 1 - Product Shell

Purpose:

- make the app feel like a real 3plug product
- remove the worst inherited Press shell confusion

Scope:

- Desk shell and app identity
- Desk workspace/sidebar structure
- main product module naming
- home/dashboard direction
- control settings reshaping

Success criteria:

- the app entry point feels like 3plug, not Press
- the main modules match the target-state shell
- inherited Frappe Cloud entry clutter is removed

## Phase 2 - First-Run Onboarding

Purpose:

- make server onboarding the first real task

Scope:

- server onboarding as the primary first-run flow
- clear empty states when no managed server exists yet
- guided first action from home/desk
- readiness checks after server onboarding

Success criteria:

- a new user knows the first task immediately
- the product guides the user into server onboarding
- benches and sites clearly follow from server readiness

## Phase 3 - Server Management

Purpose:

- make the server module operationally useful

Scope:

- server overview
- health
- security
- operations
- bench onboarding entry
- production checks
- restart and recovery actions

Success criteria:

- the server module feels like server management
- the operator can see status, review security, and run actions

## Phase 4 - Site Lifecycle

Purpose:

- make sites a true managed product surface

Scope:

- create site flow
- site plan as runtime/resource profile
- app selection
- tenant selection
- domains and TLS
- backups and restore
- in-place migration
- move site to another bench
- site operations and history

Success criteria:

- site creation is product-driven, not shell-driven
- key site lifecycle actions are visible and tracked

## Phase 5 - Bench Lifecycle

Purpose:

- make benches first-class runtime units

Scope:

- register existing bench
- create managed bench
- bench overview
- apps and versions
- config and environment
- deploy and update actions
- bench-linked sites
- bench-linked jobs and plays

Success criteria:

- benches feel like real managed runtime units
- bench actions are visible and tracked

## Phase 6 - Execution And Traceability

Purpose:

- make the product trustworthy during change and failure

Scope:

- jobs
- plays
- stage and output visibility
- traceback visibility
- retry and rerun paths where safe
- forensics and incident signals
- links back to server, bench, and site

Success criteria:

- operators can answer what changed, where, why, and what failed

## Phase 7 - Notifications

Purpose:

- make the product proactive, not only reactive

Scope:

- team-level defaults
- server-level rules
- site-level rules
- failure notifications
- migration and deploy completion notifications
- certificate and backup notifications
- incident notifications

Success criteria:

- important runtime events reach the operator without manual polling

## Phase 8 - Catalog And Controlled Apps

Purpose:

- make app management intentional

Scope:

- approved apps
- app sources
- app releases
- installability rules
- curated app set for site creation

Success criteria:

- site creation can choose from the right approved apps
- new approved apps can be added through a clear process

## Phase 9 - Analytics

Purpose:

- make the product readable at a glance

Scope:

- dashboard cards and summaries
- runtime counts
- incident trends
- job failure visibility
- storage and capacity signals
- site and bench growth signals

Success criteria:

- home and analytics pages help operators decide what needs attention

## Priority Order

The active implementation order should be:

1. first-run onboarding
2. server management
3. site lifecycle
4. bench lifecycle
5. jobs and forensics
6. notifications
7. apps and catalog
8. analytics

## Immediate Next Slice

The next practical implementation slice should be:

1. make server onboarding the first-run product task
2. tighten the server-first home state
3. build the real site lifecycle flow starting with `Create Site`

That keeps us aligned with both the product model and the benchmarked function set.
