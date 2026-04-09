# First Doctype Map

## Press-derived starting objects

### `3plug Server`

Reference from Press:

* `Server`

3plug adaptation:

* starts with one active managed server
* stores host identity, operator context, and runtime readiness

### `3plug Bench`

Reference from Press:

* `Bench`
* `Bench App`
* `Bench Dependency`

3plug adaptation:

* stores bench path, Python/runtime details, app stack, and status for the managed server

### `3plug Site`

Reference from Press:

* `Site`
* `Site App`
* `Site Domain`

3plug adaptation:

* stores site-to-bench relationship, installed apps, site status, and config preview

### `3plug Job`

Reference from Press:

* `Agent Job`
* `Agent Job Step`

3plug adaptation:

* records queued, running, completed, and failed platform actions

### `3plug App Source`

Reference from Press:

* `App Source`
* `App Release`

3plug adaptation:

* stores approved Triotek-controlled sources and allowed branches

### `3plug Stack`

Reference from Press:

* app grouping and deploy-candidate thinking

3plug adaptation:

* stores approved app stacks for bench/site creation
