# Live Validation Checklist

This page is the required validation checklist for the current server-first slice.

We should use this before proceeding with more product work.

The goal is to prove that:

- managed server onboarding actually works end to end
- server management works against a real server
- the first-run server flow is not just a reshaped UI

## Validation Rule

Before moving deeper into other modules, we should validate the current server slice on the real server.

That means:

- update the app on the server
- run the onboarding flow
- confirm the runtime checks and operations work
- confirm jobs, plays, and evidence are created correctly

## Before Starting

- confirm the latest repo code is on the server
- run site migrate
- build assets
- clear cache
- restart the bench web and workers
- hard refresh the browser

## Server Entry Surface

- open `Servers`
- confirm the page reads `Server Management`
- confirm the main action is `Onboard Server`
- confirm the first empty-state message points to server onboarding first

## Managed Server Onboarding

- click `Onboard Server`
- confirm the form asks for:
  - server title
  - primary contact email
  - primary domain
  - managed domains
  - sudo or SSH user
  - SSH port
- confirm the form does not ask for public IP or private IP manually
- submit onboarding

## Automatic Discovery

- confirm the public server IP is resolved automatically from the primary domain
- confirm the private IP is discovered during verification
- confirm the runtime user is detected
- confirm memory, cpu, storage, and machine facts are captured
- confirm storage layout is captured and displayed

## Onboarding Pipeline

- confirm the onboarding page opens automatically after submission
- confirm stages are visible and progress correctly:
  - queued
  - verifying access
  - validating machine capacity
  - creating database runtime
  - creating application runtime
  - applying runtime setup
  - completed
- confirm a failed onboarding run shows the error clearly
- confirm rerun works when onboarding fails

## Server Management

- open the managed server detail
- confirm these tabs load and feel coherent:
  - overview
  - health
  - security
  - operations
  - bench onboarding

## Health Validation

- run production checks
- confirm checks populate for:
  - NGINX
  - Supervisor
  - Redis
  - Workers
  - Scheduler
  - Web
  - Runtime User
  - Storage Devices
- confirm verification timestamp updates

## Operations Validation

- confirm these actions are present:
  - run production checks
  - restart production services
  - restart NGINX
  - restart Redis
  - restart Workers
- run at least one safe action
- confirm the action creates visible execution traces
- rerun checks and confirm the updated state is reflected

## Security Validation

- confirm access details are visible:
  - public IP
  - private IP
  - hostname
  - TLS domain
- confirm firewall view loads
- confirm the page stays focused on security instead of mixed server concerns

## Jobs, Plays, And Evidence

- open jobs from the server flow
- confirm onboarding created jobs and or plays
- confirm failed jobs can be:
  - retried
  - diagnosed
- confirm forensic evidence appears for failures or manual diagnose actions

## Bench Handoff

- continue from the server flow into bench onboarding
- confirm the server is treated as the single managed server context
- confirm bench discovery works from that managed-server path

## Pass Criteria

We should treat the server slice as proven only if all of these are true:

- no manual IP entry is required
- onboarding runs through worker-backed stages
- machine facts are captured automatically
- server management reflects real runtime checks
- recovery actions work and leave traces
- jobs, plays, and evidence are part of the normal operator flow
- the server flow feels like a real client-facing product surface
