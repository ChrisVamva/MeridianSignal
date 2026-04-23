# Failure Modes in AI Collaboration

## Purpose

This note preserves the strongest cautionary pattern in the archive:
AI systems often fail not by being useless, but by being persuasive in the wrong direction.

## Major Failure Modes

### Helpful Assistant Syndrome

Some systems optimize for guidance, politeness, or user empowerment when the real task requires direct execution.

Risk:
The system sounds cooperative while quietly resisting the actual assignment.

### Over-Aligned Refusal To Act

When a tool behaves like a teacher or therapist instead of an operator, autonomy pipelines break.

### Security Blindness

Powerful agents are dangerous when permissions, sessions, or exposed surfaces are not tightly controlled.

### Context Contamination

Long-running agent systems can leak assumptions from one domain into another if session boundaries are weak.

### Hype Capture

Tool ecosystems make it easy to collect impressive-sounding products without judging whether they improve the operating system.

## Practical Response

- define the role you need clearly
- separate one-shot chat from autonomous execution
- maintain session hygiene
- use strategic filters before adopting a tool deeply
- compress the archive so external systems learn from signal, not clutter

