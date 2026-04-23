---
modified: 2026-04-21T03:19:02+03:00
---
## What You Actually Described

You have a **hierarchy of values**, not a flat list:

```
FOUNDATION (must always be true)
├── No hallucinated paths, files, configs
├── Transparent reasoning (show your work)
└── Token efficiency (don't waste)

PERFORMANCE (optimise toward these)
├── Rigorous planning
└── Fast, decisive execution

ASPIRATION (welcome when foundation is solid)
└── Genuinely innovative reasoning
    — not creative for creativity's sake
    — innovation that emerges from rigorous thinking
```

The aspiration only matters **after** the foundation holds. You wouldn't want a brilliantly creative plan built on hallucinated file paths.

---

## My Suggestion for Your Metric

Given you're coding — apps, sites, mixed development — I'd build the metric on **3 layers** that match your hierarchy:

**Layer 1 — Hard rules (pass/fail)**

```
- Did it reference only files mentioned in context?
- Did it say UNKNOWN instead of inventing?
- Is the plan numbered and sequential?
```

**Layer 2 — Quality score (0 to 1)**

```
- Is each step actionable (verb + specific target)?
- Are risks specific, not generic?
- Is the output concise? (penalise padding)
```

**Layer 3 — Innovation bonus (optional +)**

```
- Did it suggest an approach not obvious from the task?
- Did reasoning reveal a non-trivial dependency or risk?
```

Layer 3 only adds points — it never saves a failing Layer 1. **Foundation first, always.**

---

## One Question Before We Write the Metric

The metric needs examples to score against. I want to use **your real projects** so the optimizer trains on situations you actually face.

Give me **3 real tasks** you've actually given an AI agent recently — from any of your projects (drawing app, journal, productivity tracker, blog). Just the task description, rough context, and whether the output you got was good, bad, or mixed.

Real examples will make the optimizer 10x more useful than synthetic ones. You don't need to format them — just describe them naturally. 🎯