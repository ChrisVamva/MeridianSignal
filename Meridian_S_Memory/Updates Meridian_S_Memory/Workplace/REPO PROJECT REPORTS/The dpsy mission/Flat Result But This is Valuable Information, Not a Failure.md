---
modified: 2026-04-21T04:52:50+03:00
---
## Flat Result — But This is Valuable Information, Not a Failure

Let me read exactly what happened:

```
Baseline:   0.50  0.85  0.40  0.75  0.85  → avg 0.67
Optimized:  0.50  0.75  0.50  0.80  0.80  → avg 0.67

Journal entry:      0.85 → 0.75  (got slightly worse)
Productivity:       0.40 → 0.50  (improved)
Piano app:          0.85 → 0.80  (got slightly worse)
```

**Two things happened simultaneously — and they cancelled each other out.**

---

## Why BootstrapFewShot Didn't Move the Needle

BootstrapFewShot works by adding **demonstration examples** to the prompt — showing the model "here's a good output, do something like this."

But your model is **devstral-2 at 123 billion parameters.** It already follows your detailed instructions precisely. Adding examples to a 123B model is like giving a master chef a recipe card — the card doesn't help, the chef already knows.

```
BootstrapFewShot is powerful for:  smaller/weaker models
Your situation needs:              instruction optimization
```

The optimizer that rewrites the **actual instructions** — the docstring — is **MIPROv2.** That's the right tool here.

---

## What the Scores Actually Tell You

```
Drawing app:     0.50 baseline  ← your metric is finding a real weakness here
Productivity:    0.40 baseline  ← another genuine weak spot
Journal + Piano: 0.85 baseline  ← near ceiling on current metric
```

Your metric is **working correctly** — it's discriminating. The drawing app and productivity tracker score lower because the raw ideas you gave them were more abstract, giving the model less specific language to reference back.

This is useful. It tells you where your workflow is weakest.

---

## The Fix — Two Paths, Both Correct

**Path A — Switch to MIPROv2** *(rewrites instructions, not examples)*
```python
# Replace BootstrapFewShot with this:
from dspy.teleprompt import MIPROv2

optimizer = MIPROv2(
    metric=vision_metric,
    auto="light"    # light = fewer iterations, good for first run
)
optimized_clarifier = optimizer.compile(
    clarifier,
    trainset=trainset,
    requires_permission_to_run=False
)
```
This will actually rewrite the docstring to produce better outputs. More LLM calls, more time — but real instruction improvement.

**Path B — Fix the compilation model** *(use a weaker model to find gaps)*
```python
# Add a weak model for the optimizer to work against
weak_lm = dspy.LM(
    model="ollama_chat/llama3.2:3b",   # local, tiny
    api_base="http://localhost:11434",
    api_key="ollama"
)

optimizer = BootstrapFewShot(metric=vision_metric, max_bootstrapped_demos=3)
optimized_clarifier = optimizer.compile(
    clarifier,
    trainset=trainset,
    teacher_settings=dict(lm=weak_lm)  # find gaps using weak model
)
```
The optimizer finds what the weak model gets wrong, creates demonstrations that fix those gaps, then those demonstrations help the strong model be even more consistent.

---

## My Recommendation

**MIPROv2, Path A.** 

It's the honest answer for your situation — a capable model, detailed instructions, a metric that's already working. MIPROv2 is designed to improve exactly this: instructions that are good but not yet optimal.

It will make more calls and take longer — maybe 10-15 minutes. But you'll see the actual docstring rewritten by the optimizer, which is the fascinating part.

Shall I give you the full updated `dspy_optimize.py` with MIPROv2? 🎯