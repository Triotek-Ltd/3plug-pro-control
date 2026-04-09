# First Job Map

## Goal

Use a Press-style job boundary for real platform actions.

## First jobs

### Register Bench

Purpose:

* bring an existing bench under 3plug control

### Create Site

Purpose:

* run the real Bench site-creation flow through a queued job

### Install App on Site

Purpose:

* run the real Bench install-app flow through a queued job

### Refresh Bench Status

Purpose:

* inspect bench and site state and refresh dashboard-visible status

## Rule

The UI should create these jobs.

The runner or agent should execute them.

The backend should persist their state and output.
