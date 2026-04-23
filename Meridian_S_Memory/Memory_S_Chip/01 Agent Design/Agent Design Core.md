# Agent Design Core

## Core Pattern

The strongest recurring agent design pattern is:

- planner thinks
- executor acts
- verifier checks

Do not collapse these roles unless the task is simple enough to tolerate it.

## Spec-Driven Execution

The key operating pattern is contract-first execution.

Meaning:

- define the interface or shared contract first
- assign bounded execution territory
- verify against the contract

This reduces hallucination, context degradation, and overlap between workers.

## Syntax Versus Semantics

Lighter coding models often perform well when:

- the plan is explicit
- the file scope is bounded
- the contract is stable

They perform poorly when they are forced to decide architecture on their own.

## Agent Growth Principle

Useful agents grow by:

- remembering relevant patterns
- refining execution boundaries
- carrying forward structured experience

Not by becoming vague all-purpose personalities.

