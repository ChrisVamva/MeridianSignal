# When To Build A Custom Agent

## Core Decision Rule

Build a custom agent when a general chat tool stops being enough for the real shape of the work.

## Main Thresholds

### Workflow Threshold

If the task requires a loop such as:

- observe
- plan
- execute
- verify
- retry

then the work is moving beyond a prompt and into agent territory.

### Depth Threshold

Build an agent when the task needs deep knowledge of one narrow system rather than shallow knowledge of many things.

Examples:

- a vault-specific research operator
- a project-specific coding assistant
- a market intelligence pipeline for one niche

### Arbitrage Threshold

Build an agent when careful orchestration can replace a brute-force expensive workflow.

This is where cost-conscious architecture becomes a strategic advantage rather than a limitation.

## Strong Uses

- recurring research routines
- archive synthesis
- project-specific execution
- scheduled monitoring
- narrow automation with clear success criteria

## Weak Uses

- vague ambition without a real loop
- building an agent only because the concept sounds advanced
- situations where a checklist or simple script would be enough

## Design Principle

The more specific the problem, the more defensible the custom agent.

