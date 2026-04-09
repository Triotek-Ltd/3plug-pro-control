# 3plug Control

3plug Control is the future Triotek control plane derived from Press.

The direction is not to rebuild Press behavior from scratch beside Press.

The direction is:

* use Press as the base
* adapt it into Triotek's 3plug product
* narrow the first operating model to one managed server
* keep Bench-first lifecycle management as the first product scope

## Base reference

Local base reference:

* `../frappe-press`

Important reference areas:

* `../frappe-press/press`
* `../frappe-press/dashboard`
* `../frappe-press/press/agent.py`
* `../frappe-press/press/press/doctype`

## First product adaptation

Press is broader and more cloud-heavy.

3plug Control should start with:

* one managed server
* many benches on that server
* many sites on those benches
* Triotek-controlled app sources and stacks

## Workspace shape

This repo now mirrors the broad Press split:

* `app/` for backend/Frappe-app adaptation notes and starting points
* `dashboard/` for operator UI adaptation notes and starting points
* `agent/` for runner/agent adaptation notes and starting points
* `docs/` for the 3plug-specific Press adaptation plan

## What comes next

1. define the first 3plug doctypes from the Press model
2. define the first dashboard pages from the Press dashboard model
3. define the first agent/job flows for single-server Bench operations
4. start porting validated 3plug prototype behavior into this real control-plane shape
