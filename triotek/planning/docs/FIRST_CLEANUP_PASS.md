# First Cleanup Pass

## Goal

Make the first cleanup pass on the imported Press base without breaking the whole project.

## What we learned from the import

Press is deeply integrated through:

* `press/hooks.py`
* `press/modules.txt`
* dashboard routes in `dashboard/src/router.js`
* doctype-level permissions and scheduler hooks

That means direct deletion is risky as a first move.

## Safe first-pass rule

The first cleanup pass should be an isolation pass, not a destructive pass.

This means:

* classify modules and routes first
* identify what 3plug v1 keeps active
* identify what is out of v1 scope
* avoid deleting large areas until their references are known

## Active 3plug v1 areas

Focus first on these live surfaces:

* core Press backend records for server, bench, site, app source, and job flow
* core dashboard patterns for list, detail, job, site, and server views
* job and agent execution path

## Deferred areas for now

Treat these as imported but not yet adopted:

* billing
* marketplace
* partner
* broad SaaS self-service flows
* multi-server infrastructure-role features

## Next cleanup steps

1. classify dashboard routes into keep or defer groups
2. classify hook entries into keep or defer groups
3. identify the first low-risk UI removals or hides
4. identify the first low-risk backend hook reductions
5. only then start deleting deferred code

## Important caution

This repo is now the real Press-based product base.

Any cleanup should preserve:

* importability
* dashboard bootability
* backend hook integrity
* the core server to bench to site to job spine
