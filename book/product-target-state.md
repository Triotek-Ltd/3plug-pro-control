# Product Target State

This page captures the current intended workflow for 3plug Control.

It is the product target state we are aiming to make fully true in the dashboard, backend, and operator experience.

## Core Model

3plug Control is supposed to operate as:

* one 3plug deployment per managed server
* one Linux server managed by that deployment
* many benches on that server
* many sites on those benches
* jobs, plays, and forensic records for traceability

## What The Operator Should Be Able To Do

The intended operator workflow is:

1. open the 3plug Control panel
2. register the managed Linux server
3. let 3plug verify and set up that server through the self-hosted flow
4. onboard an existing bench from that server
5. discover the real apps and sites on that bench
6. create the managed bench record
7. create or import the managed site records
8. operate through tracked jobs, plays, and forensic signals

## Main Product Surfaces

The product is supposed to center the operator on:

* server overview
* bench inventory
* bench detail
* site inventory
* site detail
* job activity
* forensic events and forensic incident signals

## Product Rules

The intended behavior is:

* keep Bench as the execution layer for Bench-owned actions
* keep records, permissions, and APIs in the Frappe backend
* keep the dashboard as the main operator surface
* run long actions behind jobs instead of loose foreground commands
* treat forensic reporting and logging as part of the core product, not an extra

## What This Product Is Not Trying To Be In V1

The current target state is not:

* a broad multi-server cloud control plane
* a billing-first product
* a marketplace-first product
* a partner-program-first product
* a general infrastructure platform for unrelated fleets

## Current Gap To Watch

The target state is already clear in the planning docs, but the product surface is not fully aligned yet.

Examples of inherited Press concepts that may still appear:

* application server
* database server
* broader infrastructure views
* other multi-server or cloud-oriented assumptions

Those concepts need to be reviewed against this target state and either:

* kept only if they still support the one-server workflow
* renamed to fit the 3plug model
* hidden or removed if they belong to the old broader Press shape
