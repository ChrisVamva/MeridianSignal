---
modified: 2026-04-21T02:00:21+03:00
---
## THIS is why you're here. Read this carefully.

You just saw something most developers never look at. Let me decode it:

---

## What DSPy Built Automatically

**1. It added `reasoning` — you never asked for it**
```
ChainOfThought = answer BUT think first
```
The model had to explain itself before answering. That's not an accident — it's why this module is called **Chain**OfThought. Forced reasoning = fewer hallucinations.

**2. The `[[ ## markers ## ]]` are a parsing contract**
```
[[ ## reasoning ## ]]   ← DSPy reads here
[[ ## answer ## ]]      ← DSPy reads here
[[ ## completed ## ]]   ← DSPy knows it's done
```
The model can't just ramble. It must fill specific slots. If it doesn't — DSPy retries. This is **structural anti-hallucination**.

**3. The objective was auto-written**
```
"Given the fields `question`, produce the fields `answer`"
```
You wrote zero prompt. DSPy wrote this. The optimizer will later *rewrite this line* to make outputs better.

---

## Connect This to Your Pain Points

| Your problem | What you just saw solving it |
|---|---|
| Hallucinated config values | Structured slots force specific answers |
| No control over what AI does | You see every word sent to the model |
| Arize Phoenix monitoring | This exact block is what Phoenix traces |
| Token cost awareness | Count those lines — this is lean |

---

## Phase 2 — Switch to Your Real Model

No more laptop heat. Same code, one line changes. Update your file:

```python
import dspy

# Switch to Ollama Cloud - runs on their servers, not your laptop
lm = dspy.LM(
    model="ollama_chat/devstral-2:123b-cloud",
    api_base="http://localhost:11434",
    api_key="ollama"
)
dspy.configure(lm=lm)

qa = dspy.ChainOfThought("question -> answer")
result = qa(question="What is the capital of France?")

print("Answer:", result.answer)
dspy.inspect_history(n=1)
```

Run it. Your laptop stays cool. A 123 billion parameter model answers. Same DSPy structure — just more intelligence behind it. 🎯