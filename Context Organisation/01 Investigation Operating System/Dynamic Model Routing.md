# Dynamic Model Routing

## Core Claim

Models should be treated as specialized workers, not as a single universal intelligence.

## Why This Survives

This idea appears repeatedly across the archive and has both conceptual and operational value.
It is one of the clearest durable ideas in the material because it affects cost, reliability, speed, and system design.

## Routing Logic

Route by the physics of the task:

- use fast and cheap models for categorization, filtering, and repetitive passes
- use large-context models for archive-scale review and synthesis
- use stronger reasoning models for architecture decisions, difficult comparisons, or ambiguity resolution
- use local or privacy-preserving models when data sensitivity matters more than maximum performance

## Benefits

- lowers cost
- reduces vendor dependence
- makes systems more modular
- encourages explicit task decomposition
- creates resilience when a preferred tool becomes unavailable or overpriced

## Design Consequence

Dynamic routing only works well if the task itself has already been split into stages.
That means routing depends on a stronger investigation operating system, not merely on having many APIs.

## Practical Rule

When one model is being asked to do everything, either:

- the task has not been decomposed enough
- or the system has not yet learned what different model strengths are for

