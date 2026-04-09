# Press to 3plug Map

## Backend

Reference:

* `../frappe-press/press`
* `../frappe-press/press/press/doctype`
* `../frappe-press/press/hooks.py`

3plug direction:

* derive 3plug backend objects from Press platform records
* reduce the first scope to single-server Bench operations

## Dashboard

Reference:

* `../frappe-press/dashboard`

3plug direction:

* keep the dashboard split
* start with operator-facing inventory and action pages
* focus on server, bench, site, job, and stack views first

## Agent and jobs

Reference:

* `../frappe-press/press/agent.py`
* `../frappe-press/press/press/doctype/agent_job`

3plug direction:

* move real execution behind jobs
* avoid long-term dependence on foreground CLI execution
* adapt the early actions for:
  * bench create
  * bench register
  * site create
  * site install-app
