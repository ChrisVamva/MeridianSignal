# Routing and Observability Core

## Dynamic Routing

Treat models as specialized workers, not as one universal brain.

Route by:

- reasoning difficulty
- context size
- execution boundedness
- cost and rate limits
- sensitivity of the task

## Adaptive Broker Logic

The broker layer matters because it creates resilience.

Its role is to:

- choose the right model or path for the job
- recover from limits or failures
- preserve system continuity under changing conditions

## Observability Principle

Tracing, telemetry, and evaluation are part of the system architecture.

They make it possible to:

- inspect decisions
- detect failure patterns
- compare planner quality
- improve prompts and workflows with evidence

## Operational Lesson

Blind agent execution is fragile.
Inspectable agent execution is improvable.

