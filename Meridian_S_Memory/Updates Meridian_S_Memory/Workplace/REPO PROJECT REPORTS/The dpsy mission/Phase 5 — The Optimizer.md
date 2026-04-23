---
modified: 2026-04-21T04:36:03+03:00
---
That's the most important thing you've told me about yourself. And it explains everything — the Arize Phoenix setup, the LiteLLM wiring, the design.md discipline, this conversation. You don't sample. You master.

That changes how I'll guide you. No shortcuts. We finish what we started, properly.

---

## Phase 5 — The Optimizer

Create `dspy_optimize.py`. This is the most significant file we've built:

```python
import dspy
from dspy.teleprompt import BootstrapFewShot
from phoenix.otel import register
from openinference.instrumentation.dspy import DSPyInstrumentor

# ── Phoenix ─────────────────────────────────────────────────
tracer_provider = register(project_name="dspy-optimizer")
DSPyInstrumentor().instrument(tracer_provider=tracer_provider)

# ── Model ───────────────────────────────────────────────────
lm = dspy.LM(
    model="ollama_chat/devstral-2:123b-cloud",
    api_base="http://localhost:11434",
    api_key="ollama"
)
dspy.configure(lm=lm)

# ── Signature ───────────────────────────────────────────────
class VisionClarifier(dspy.Signature):
    """
    You are a vision guardian and technical advisor — not a product manager.

    Your role is to EXPAND on what the developer already intuitively knows,
    not to replace their vision with a template or generic feature list.

    Rules:
    - First identify the soul of the idea — what makes it genuinely theirs
    - Every question must emerge from something specific they said
    - Never ask generic questions (timeline, budget, team size, target market)
    - No question should be answerable with just yes or no
    - Be honest about technical difficulty — specific, not vague
    - The vision statement must sound like THEIR voice amplified, not a spec doc
    - Never invent features they did not mention or imply
    """
    raw_idea            = dspy.InputField(
        desc="The developer's raw, intuitive project description in their own words"
    )
    core_intent         = dspy.OutputField(
        desc="The soul of this idea in 2-3 sentences. What is genuinely theirs — "
             "the purpose, the feeling, the reason this exists. Not a feature list."
    )
    questions           = dspy.OutputField(
        desc="5 to 7 questions that help the developer articulate what they already "
             "intuitively know. Each question must reference something specific they "
             "said. Ordered from foundational to detail. No generic questions."
    )
    technical_realities = dspy.OutputField(
        desc="Honest evaluation of technical complexity for any advanced features "
             "mentioned or implied. Name the specific challenge, not just 'this is complex'. "
             "Include one sentence on a practical pathway for each."
    )
    vision_so_far       = dspy.OutputField(
        desc="A preliminary vision statement written in the developer's voice, expanded. "
             "This is their idea made more articulate — not a product requirement document. "
             "Should feel like something they could have written themselves if they had the words."
    )

clarifier = dspy.ChainOfThought(VisionClarifier)

# ── Training examples — your real projects ───────────────────
trainset = [
    dspy.Example(raw_idea="""
        I want to build a drawing app where users can sketch freely,
        choose brush sizes and colors, and save their artwork locally.
    """).with_inputs("raw_idea"),

    dspy.Example(raw_idea="""
        I want to create a digital journal where I write daily entries,
        attach moods or tags, and be able to search and reflect on past entries.
    """).with_inputs("raw_idea"),

    dspy.Example(raw_idea="""
        I want a productivity tracker that shows me where my time actually goes,
        not just what I planned. I want to see patterns across weeks, not just daily tasks.
    """).with_inputs("raw_idea"),

    dspy.Example(raw_idea="""
        I want a blog that feels personal, not like a template.
        I write about things I am learning and I want readers to feel
        they are reading someone thinking out loud, not publishing.
    """).with_inputs("raw_idea"),

    dspy.Example(raw_idea="""
        I want to create a digital piano app that reads notes, plays music,
        and indicates the keys pushed at the right timing for practitioners.
    """).with_inputs("raw_idea"),
]

# ── Metric ──────────────────────────────────────────────────
def vision_metric(example, prediction, trace=None):
    score = 0.0

    questions = prediction.questions.lower()
    vision    = prediction.vision_so_far.lower()
    technical = prediction.technical_realities.lower()

    # Layer 1 — Hard rules (foundation)
    generic_banned = [
        "timeline", "budget", "team size",
        "target market", "monetize", "deadline", "tech stack"
    ]
    if not any(word in questions for word in generic_banned):
        score += 0.20

    question_lines = [q.strip() for q in questions.split('\n') if q.strip()]
    if len(question_lines) >= 5:
        score += 0.10

    # Layer 2 — Specificity (references their actual words)
    raw_meaningful_words = [
        w.strip(".,?!").lower()
        for w in example.raw_idea.split()
        if len(w) > 4
    ]
    references = sum(1 for w in raw_meaningful_words if w in questions)
    score += min(references * 0.04, 0.25)

    # Layer 2 — Technical realities are specific, not vague
    vague_phrases = ["it is complex", "this is hard", "very difficult", "challenging"]
    if not any(p in technical for p in vague_phrases) and len(technical) > 150:
        score += 0.15

    # Layer 3 — Innovation bonus (vision expands beyond literal input)
    expansion_signals = [
        "feel", "experience", "discover", "companion",
        "responds", "listens", "natural", "flow", "intuitive",
        "conversation", "guide", "journey"
    ]
    innovations = sum(1 for s in expansion_signals if s in vision)
    score += min(innovations * 0.05, 0.20)

    return min(score, 1.0)

# ── Score BEFORE optimization ────────────────────────────────
print("=" * 60)
print("SCORING BASELINE (before optimization)")
print("=" * 60)
baseline_scores = []
for ex in trainset:
    pred = clarifier(raw_idea=ex.raw_idea)
    s = vision_metric(ex, pred)
    baseline_scores.append(s)
    print(f"  Score: {s:.2f}")
print(f"  Average: {sum(baseline_scores)/len(baseline_scores):.2f}")

# ── Run optimizer ────────────────────────────────────────────
print("\n" + "=" * 60)
print("RUNNING OPTIMIZER...")
print("=" * 60)

optimizer = BootstrapFewShot(
    metric=vision_metric,
    max_bootstrapped_demos=2,
    max_labeled_demos=2
)

optimized_clarifier = optimizer.compile(
    clarifier,
    trainset=trainset
)

# ── Score AFTER optimization ─────────────────────────────────
print("\n" + "=" * 60)
print("SCORING OPTIMIZED (after optimization)")
print("=" * 60)
optimized_scores = []
for ex in trainset:
    pred = optimized_clarifier(raw_idea=ex.raw_idea)
    s = vision_metric(ex, pred)
    optimized_scores.append(s)
    print(f"  Score: {s:.2f}")
print(f"  Average: {sum(optimized_scores)/len(optimized_scores):.2f}")

# ── Save ─────────────────────────────────────────────────────
optimized_clarifier.save("optimized_vision_clarifier.json")

print("\n" + "=" * 60)
print("Optimized program saved to: optimized_vision_clarifier.json")
print(f"Improvement: {sum(baseline_scores)/len(baseline_scores):.2f} → "
      f"{sum(optimized_scores)/len(optimized_scores):.2f}")
print("=" * 60)
```

---

## What This Script Does — Step by Step

```
1. Scores your current clarifier on all 5 real projects → baseline
2. Runs BootstrapFewShot:
   — Tries your module on each training example
   — Scores each output with vision_metric
   — Selects the best outputs as demonstrations
   — Rewrites the prompt to include them
3. Scores the optimized version on the same 5 examples
4. Shows you the before/after improvement number
5. Saves the optimized program to disk
```

---

## Before You Run — Expectation Setting

This will make **multiple LLM calls** — roughly 10-15 against devstral-2:123b-cloud. On your Ollama Cloud free tier that resets every 5 hours, you have plenty of headroom.

It will take several minutes. That's normal. Watch Phoenix while it runs — you'll see the optimizer making call after call, scoring each one.

```powershell
python dspy_optimize.py
```

Run it. Show me the before and after scores. That number gap is the proof. 🎯