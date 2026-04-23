---
modified: 2026-04-21T02:11:20+03:00
---
## Phase 2 Complete. 123B model. Zero laptop noise. 🎯

Notice something subtle — the reasoning is *richer* than llama3.2:3b gave you. Same structure, more intelligence. That's the power of swapping one line.

---

## Now We Build Something Real

Enough "capital of France." You came here to sharpen your prompting for **actual development work.**

Your biggest pain point was this:
> *"Hallucinated config values and paths"*

Let's build a DSPy module that directly attacks that problem. A **structured task planner** that forces the model to think before it touches anything.

Create a new file — `dspy_planner.py`:

```python
import dspy

lm = dspy.LM(
    model="ollama_chat/devstral-2:123b-cloud",
    api_base="http://localhost:11434",
    api_key="ollama"
)
dspy.configure(lm=lm)

# Multi-field signature — this is where DSPy gets powerful
class TaskPlanner(dspy.Signature):
    """
    You are a careful software planner.
    Never invent file paths, config values, or dependencies.
    Only reference what is explicitly provided.
    If something is unknown, say UNKNOWN — never guess.
    """
    task        = dspy.InputField(desc="What the developer wants to build or fix")
    context     = dspy.InputField(desc="Existing files, configs, or code snippets provided")

    plan        = dspy.OutputField(desc="Step by step plan, numbered")
    files       = dspy.OutputField(desc="Exact files to create or modify. UNKNOWN if not determinable from context")
    risks       = dspy.OutputField(desc="What could go wrong. Be specific, not generic")

# Wrap it in ChainOfThought — forces reasoning before output
planner = dspy.ChainOfThought(TaskPlanner)

# Test it with a real scenario from your work
result = planner(
    task="Add a save button to the drawing app that saves the canvas as PNG",
    context="Project uses vanilla JavaScript. Main files: index.html, canvas.js, toolbar.js. No backend."
)

print("PLAN:\n",   result.plan)
print("\nFILES:\n", result.files)
print("\nRISKS:\n", result.risks)
```

---

## What's New Here

```python
class TaskPlanner(dspy.Signature):
    """You are a careful planner..."""
```

That docstring IS your system prompt — but now it's **part of the program**, not floating in a chat window. The optimizer can improve it. Phoenix can trace it. You can version control it.

Run it. Let's see what a 123B model does with real structure. 🎯