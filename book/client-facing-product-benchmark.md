# Client-Facing Product Benchmark

This page defines the benchmark for the client-facing 3plug product shell.

It does not copy another provider. It extracts the useful patterns from mature
control panels and turns them into a 3plug-specific target.

## Why This Benchmark Exists

We need the 3plug product to feel like a real operations platform at the end:

- clear like a hosting control panel
- observable like a cloud console
- traceable like an operations runbook

That means the shell, dashboards, and action surfaces should not be guessed from
legacy Press screens. They should be shaped intentionally.

## Reference Products

### Contabo

Contabo is useful as a benchmark for operational clarity.

What stands out:

- the customer panel is the main interface for account and server management
- server control is simple and direct
- restart and reinstall actions are easy to find
- snapshots are treated as practical operational tools
- billing and account controls live in the same customer-facing product

Relevant official references:

- [What is the Customer Panel and How do I Access it?](https://help.contabo.com/en/support/solutions/articles/103000268754-what-is-the-customer-control-panel-and-how-do-i-access-it-)
- [How Can I Restart My Server?](https://help.contabo.com/en/support/solutions/articles/103000270047-how-can-i-restart-my-server-)
- [How Do I Create a Snapshot of My Server?](https://help.contabo.com/en/support/solutions/articles/103000270385-how-do-i-create-a-snapshot-of-my-server-)
- [How do I reinstall my Contabo server?](https://help.contabo.com/en/support/solutions/articles/103000271913-how-do-i-reinstall-my-contabo-server-)

What 3plug should take from this:

- operational actions should be obvious
- server management should not feel buried under infrastructure jargon
- recovery actions should be close to the resource they affect
- billing, settings, and control should feel part of one product

### Oracle Cloud Infrastructure

Oracle is useful as a benchmark for dashboards, observability, and managed
operations structure.

What stands out:

- dashboards are customizable and widget-based
- health, monitoring, and usage belong in the main console experience
- operations are backed by traceable work units and system state
- the console separates high-level visibility from detailed execution trails

Relevant official references:

- [Oracle Cloud Infrastructure Console Dashboards](https://docs.oracle.com/en-us/iaas/Content/Dashboards/home.htm)
- [Overview of the Console Dashboards Service](https://docs.oracle.com/en-us/iaas/Content/Dashboards/Concepts/dashboardsoverview.htm)
- [Managing Console Dashboards](https://docs.oracle.com/en-us/iaas/Content/Dashboards/Tasks/dashboards.htm)
- [Configuring Widgets](https://docs.oracle.com/en-us/iaas/Content/Dashboards/Tasks/widgetmanagement.htm)
- [Using the Oracle Cloud Console](https://docs.oracle.com/en-us/iaas/Content/GSG/Concepts/applications-home-page.htm)

What 3plug should take from this:

- the home experience should be a true dashboard, not just a landing page
- widgets and cards should summarize status, capacity, failures, and trends
- the operator should move naturally from dashboard summary to action detail
- traceability should stay attached to jobs, plays, incidents, and recovery paths

## 3plug Product Direction

3plug should feel like:

- Contabo for direct operational control
- Oracle for visibility, dashboards, and traceability

That means the client-facing product should center on:

- a clean shell
- strong summary dashboards
- simple resource modules
- visible execution history
- easy recovery actions

## Target Client Shell

The target client-facing shell for 3plug is:

- `Home`
- `Servers`
- `Benches`
- `Sites`
- `Tenants`
- `Apps`
- `Analytics`
- `Jobs`
- `Forensics`
- `Team`
- `Control Settings`

## What Each Area Should Feel Like

### Home

The home page should work like the command center.

It should answer:

- is the managed server healthy
- are benches healthy
- are sites healthy
- are jobs failing
- are incidents active
- what needs attention next

### Servers

The server module should feel like a practical control surface.

It should include:

- overview
- health
- security
- operations
- bench onboarding

Typical actions:

- restart
- cleanup
- snapshot
- certificate refresh
- firewall review
- rerun checks

### Benches

The bench module should show:

- discovered benches
- managed benches
- bench apps
- deploy/runtime state
- bench-level jobs

### Sites

The site module should show:

- site inventory
- status
- tenancy grouping
- app plan state
- incidents and operational history

### Tenants

The tenant module should group customers and their runtime footprint:

- benches
- sites
- servers
- status
- ownership

### Apps

The apps module should show:

- approved apps
- app sources
- app releases
- installation readiness
- internal catalog and marketplace direction

### Analytics

Analytics should feel like dashboards, not just reports.

It should include cards and widgets for:

- uptime and status mix
- provisioning counts
- failed jobs
- incident trends
- storage pressure
- bench and site growth

### Jobs

Jobs should feel like traceable work requests.

Operators should be able to answer:

- what changed
- who triggered it
- where it ran
- whether it succeeded
- what should be retried

### Forensics

Forensics should keep the product trustworthy.

It should include:

- incident signals
- recovery history
- change trails
- operational evidence

### Team

Team should manage:

- operators
- roles
- ownership
- collaboration

### Control Settings

Control Settings should remain the product-wide configuration surface for:

- control plane operations
- build and delivery
- commercial
- app marketplace
- partner operations
- communications and integrations

## Dashboard Rules For 3plug

The client-facing dashboard should follow these rules:

- lead with health and next actions
- keep actions close to the resource they affect
- keep execution traces visible
- avoid infrastructure clutter that does not help operators
- prefer cards and widgets over long forms on the home page
- keep detail pages structured around how operators actually work

## Script And Action Direction

The first-class operator scripts and actions should include:

- restart server
- restart production services
- run health check
- open bench onboarding
- create snapshot
- review recent failures
- apply firewall changes
- rerun discovery
- create managed bench
- create managed sites

## What This Means For 3plug Work

This benchmark tells us what to build next:

- a real client-facing home dashboard
- practical server operations
- clearer bench and site inventory screens
- visible jobs and forensics
- a shell that feels like a real control product instead of inherited Press
