---
modified: 2026-04-21T03:31:38+03:00
---
## Stop. This is More Important Than a Metric.

You just described your entire workflow — and it maps **perfectly** to DSPy architecture. Look at what you actually have:

```
Step 1 → VisionClarifier      "Ask questions that define my vision"
Step 2 → DesignArchitect      "Break into steps, document in design.md"
Step 3 → TaskExecutor         "Execute exactly as described, test, report"
```

These aren't 3 prompts. These are **3 DSPy modules in a pipeline.** Each one optimizable independently. Each one traceable in Phoenix. Each one improvable without touching the others.

---

## Your Pipeline, Drawn Out

```
[Your idea]
     ↓
VisionClarifier
  Input:  raw_idea
  Output: targeted_questions → your answers
     ↓
DesignArchitect  
  Input:  idea + your_answers
  Output: design.md (structured, no hallucinations)
     ↓
TaskExecutor
  Input:  current_task + design.md section + codebase
  Output: code + test_result + progress_declaration
```

The piano app you described flows straight through this. So does every project you'll ever build.

---

## Now the Metric Makes Sense

Each module gets its own metric:

**VisionClarifier — good output means:**
```
✓ Questions are domain-specific (piano ≠ generic music app)
✓ Covers: technical platform, target user, scope boundaries
✓ Uncovers constraints you didn't mention (MIDI? browser? mobile?)
✓ No question is answerable with just "yes" or "no"
✗ Penalise: generic questions ("What's your timeline?")
```

**DesignArchitect — good output means:**
```
✓ Every file path comes from context or is marked TBD
✓ Steps are numbered and have a testable end condition
✓ Dependencies between steps are explicit
✓ No step says "implement X" without specifying where
✗ Penalise: vague steps, invented structure, missing tests
```

**TaskExecutor — good output means:**
```
✓ Does exactly what design.md says — no more, no less
✓ Declares what was done, what was tested, what passed
✓ Stops and reports if something doesn't match the plan
✗ Penalise: silent deviations, untested changes, assumed context
```

---

## My Suggestion for Today

We build **VisionClarifier first** — because it's the hardest one to prompt well and the one where current AI agents fail you most.

A bad VisionClarifier asks: *"What features do you want?"*

A good one asks: *"Does the app need to detect key presses from a MIDI device or mouse/keyboard? Should it work offline? Is the timing indicator for self-paced practice or fixed-tempo songs?"*

**That gap — between generic and domain-specific questions — is exactly what the DSPy optimizer closes.**

---

Shall we build the VisionClarifier module now, run it against your piano app idea, and then set up the metric that scores question quality? You'll see the difference between the unoptimised and optimised version within the same session. 🎯