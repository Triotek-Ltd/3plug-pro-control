# 3plug-control Press-Based Plan

## Purpose

`3plug-control` is the correct long-term home for the main 3plug control plane.

This should be built from Press, not merely inspired by Press.

## Local reference checked

Reference workspace:

* `../frappe-press`

Important local reference areas:

* `../frappe-press/press/hooks.py`
* `../frappe-press/press/agent.py`
* `../frappe-press/press/press/doctype/`
* `../frappe-press/dashboard/src/`

## Architecture target

`3plug-control` should follow the same broad split as Press:

* Frappe app backend for state and API
* dashboard SPA for operator UI
* job/agent orchestration layer for real execution

The initial product adaptation should simplify Press's wider infrastructure model into:

* one managed server first
* many benches on that server
* many sites on those benches
* Triotek-controlled app and stack governance

## First scope for 3plug-control

Backend:

* `3plug Server`
* `3plug Bench`
* `3plug Site`
* `3plug Job`
* `3plug App Source`
* `3plug Stack`

Dashboard:

* bench inventory page
* site inventory page
* job activity page
* bench detail page
* site detail page

Job model:

* UI submits an action
* backend records the job
* runner/agent executes the action
* UI reads job progress and final state

## What should not happen

Do not keep treating this as only a CLI project.

The CLI work from the coordination repo is useful as a reference, but the real control plane should move here.

Do not keep re-implementing large parts of Press beside Press if the local Press codebase already gives the right base shape.

## Immediate implementation direction

1. define the first Press-derived 3plug scope for single-server operation
2. identify which Press doctypes and dashboard areas can be reused with minimal reshaping
3. scaffold backend app structure
4. scaffold dashboard structure
5. port validated bench/site/job flows from the coordination repo into backend job methods
6. expose those flows through UI pages instead of shell-only interaction
