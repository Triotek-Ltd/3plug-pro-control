# Product Status Tracker

This page tracks where the 3plug product stands right now.

It is not the final product spec.

It is the working status board for implementation.

## Status Legend

- `Done For Now`
- `In Progress`
- `Not Started`
- `Needs Rework`

## Shell And Product Identity

### Desk Shell

Status: `In Progress`

What is true:

- app identity has been shifted toward `3plug Control`
- the old stale Desk entry workspace issue was identified and fixed on the server
- the Desk app now has target-state workspace files in the repo

What still remains:

- live Desk sidebar needs to be reloaded and reviewed end to end
- labels and grouping still need final polish after live review

### Dashboard Sidebar

Status: `In Progress`

What is true:

- the Vue dashboard sidebar is cleaner than the inherited Press shape
- major MVP modules are visible

What still remains:

- live validation after server update
- final alignment with the target-state shell

## First-Run Onboarding

### Server Onboarding

Status: `In Progress`

What is true:

- managed server registration exists
- the product model now clearly treats server onboarding as the first task
- server registration flow has been narrowed toward the one-server model

What still remains:

- live end-to-end validation on the real server
- confirm automatic public-IP resolution works from the primary domain
- confirm private-IP discovery works during verification
- confirm worker-backed onboarding stages complete successfully

## Core Runtime Modules

### Servers

Status: `Done For Now`

What is true:

- server module has overview, health, security, operations, and bench onboarding direction
- operator-facing flow is closer to server management than old Press infrastructure

What still remains:

- live validation of health checks and recovery actions
- confirmation that real runtime checks and restart actions work against the production server

### Benches

Status: `In Progress`

What is true:

- bench overview pass exists
- bench wording is cleaner
- benches are being treated more like product-facing runtime units

What still remains:

- deploy and update lifecycle
- app/version management depth
- clearer bench actions

### Sites

Status: `In Progress`

What is true:

- site overview pass exists
- site wording is cleaner

What still remains:

- true lifecycle functions
- create site flow
- backup and restore
- in-place migration
- move site to another bench
- domains and TLS as part of the main operational flow

### Tenants

Status: `In Progress`

What is true:

- tenant module exists as a first pass on top of `Team`

What still remains:

- stronger tenant story in the live product
- clearer distinction between tenant and team/operator concepts

### Apps

Status: `In Progress`

What is true:

- app module wording is cleaner
- app catalog direction is clearer

What still remains:

- curated approved app set
- cleaner installability rules
- connection to site creation flow

## Execution And Trust

### Jobs

Status: `In Progress`

What is true:

- execution wording is cleaner
- job detail is more traceability-oriented

What still remains:

- stronger stage model
- clearer outputs and rerun paths
- better job-centered operator workflow

### Forensics

Status: `In Progress`

What is true:

- forensics wording now reads more like evidence and incident review

What still remains:

- deeper link between incidents, jobs, and recovery
- stronger live operator flow

### Notifications

Status: `Not Started`

What is true:

- the need is documented

What still remains:

- team defaults
- site-level rules
- server-level rules
- operational notifications as a product feature

## Platform Configuration

### Control Settings

Status: `Done For Now`

What is true:

- settings were reshaped into a clearer 3plug control-plane surface
- commercial, app marketplace, partner operations, and integrations were reframed

What still remains:

- live review
- deeper cleanup of legacy fields over time

## Analytics

Status: `In Progress`

What is true:

- analytics wording has been improved
- dashboard direction is documented

What still remains:

- real operator cards and module-level analytics
- stronger home/dashboard execution

## Documentation And Guidance

### Book

Status: `In Progress`

What is true:

- product target state documented
- shell and features documented
- benchmark documented
- MVP function set documented
- roadmap and tracker now exist

What still remains:

- feature-by-feature onboarding/tutorial chapters
- implementation notes tied to live UI

## Current Focus

The current focus should be:

1. first-run server onboarding
2. site lifecycle
3. bench lifecycle
4. jobs and notifications

## Immediate Next Action

The next required action should be:

- run the live validation checklist for the current server-first slice

Only after that:

- continue with the next product slice
