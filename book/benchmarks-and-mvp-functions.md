# Benchmarks And MVP Functions

This page captures what we learned from benchmarking the real operational
surface of Frappe Cloud.

It is not here to make 3plug copy the old Frappe Cloud product model.

It is here so we can borrow the useful lifecycle functions, execution patterns,
and notification behavior while still keeping the 3plug target state:

- one managed Linux server
- many benches on that server
- many sites on those benches
- jobs, plays, and forensic records for traceability

## Why This Page Exists

We now know that module names alone are not enough.

For `Servers`, `Benches`, `Sites`, `Jobs`, and `Notifications`, the product also
needs the correct function set:

- what actions the operator can run
- what state should be visible
- what records should exist after actions run
- what execution trail should be kept

This page is the improved target-state function map.

## What We Learned From Frappe Cloud

### Benches

Frappe Cloud treats benches as real runtime units.

Benches are not just folders or internal deploy groupings.

They are where the operator manages:

- apps and app versions
- deploys and updates
- runtime configuration
- bench lifecycle work
- sites attached to the bench
- bench-linked jobs

### Sites

Frappe Cloud treats sites as operational units with real lifecycle controls.

Important patterns:

- backup and restore
- in-place migration
- migration from existing sources
- moving a site to a different bench
- plan and domain management
- app management
- site config management
- visible job history for site work

### Jobs

Frappe Cloud treats jobs as tracked execution, not background noise.

The operator is supposed to be able to answer:

- what action was triggered
- what resource it targeted
- whether it is pending, running, failed, or complete
- what output or traceback came back
- whether the action should be retried

### Notifications

Frappe Cloud treats notifications as resource-aware.

There are team-wide defaults and resource-specific overrides.

That means notifications are not only global settings.

They are tied to things like:

- sites
- servers
- incidents
- failures
- operational events

## What 3plug Should Keep

We should keep the following product lessons:

- benches are first-class runtime units
- sites need real lifecycle controls
- jobs must be first-class tracked execution
- notifications should be resource-aware
- actions should produce traceable records

## What 3plug Should Not Copy

We should not copy the old broad Frappe Cloud infrastructure model.

In particular, we should not make the product center on:

- application server and database server as the core operator story
- multi-server cloud orchestration as the default experience
- old Frappe Cloud infrastructure categories that do not fit the 3plug model

3plug should copy the function patterns, not the old platform shape.

## Improved MVP Function Set

### Servers

The `Servers` module should support:

- managed server overview
- production status checks
- health checks
- security review
- restart and recovery actions
- snapshot and recovery history
- server-linked jobs, plays, and forensic evidence

### Benches

The `Benches` module should support:

- register existing bench
- create managed bench
- inspect bench apps
- inspect bench config and environment
- update bench apps
- deploy bench changes
- inspect sites attached to the bench
- inspect bench-linked jobs and plays

### Sites

The `Sites` module should support:

- create site
- open site
- suspend and resume site
- backup now
- restore from backup
- in-place migrate
- move to another bench
- manage domains and TLS
- manage site apps
- inspect site config
- inspect site jobs and forensic evidence

### Jobs

The `Jobs` module should support:

- unified execution list
- status visibility
- target resource visibility
- stage and output visibility
- traceback visibility
- safe retry or rerun paths where applicable

### Notifications

The `Notifications` feature should support:

- team-level defaults
- server-level notification rules
- site-level notification rules
- failure notifications
- migration and deploy notifications
- backup and certificate notifications
- incident notifications

## Build Order

With this improved target state in mind, the next implementation order should be:

1. `Sites` lifecycle functions
2. `Benches` lifecycle and deploy functions
3. `Jobs` execution detail and stage model
4. `Notifications` as a real product feature

## Working Rule

As we build from here, every module should be judged by two things:

1. does it match the single-server 3plug product model
2. does it provide the practical lifecycle functions an operator actually needs

If it does not satisfy both, it should be cleaned up, reshaped, or deferred.
