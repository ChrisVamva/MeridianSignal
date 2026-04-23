---
modified: 2026-04-21T03:54:33+03:00
---
## You Just Wrote the Signature Yourself

Read what you said — mapped directly to DSPy fields:

```
"protect my vision"          →  core_intent output
                                (reflect back the soul of the idea first)

"expand my intuitive approach" → vision_so_far output  
                                (their voice, amplified — not a template)

"ground to practical pathways" → technical_realities output
                                (honest difficulty, specific — not generic)

"exchange gives agent info"  →  questions output
                                (emerge from what THEY said, not a checklist)
```

Four outputs. All from your words. Let's build it.

---

Create `dspy_vision.py`:

```python
import dspy
from phoenix.otel import register
from openinference.instrumentation.dspy import DSPyInstrumentor

# ── Phoenix ─────────────────────────────────────────────────
tracer_provider = register(project_name="dspy-vision-clarifier")
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

    raw_idea = dspy.InputField(
        desc="The developer's raw, intuitive project description in their own words"
    )

    core_intent = dspy.OutputField(
        desc="The soul of this idea in 2-3 sentences. What is genuinely theirs — "
             "the purpose, the feeling, the reason this exists. Not a feature list."
    )

    questions = dspy.OutputField(
        desc="5 to 7 questions that help the developer articulate what they already "
             "intuitively know. Each question must reference something specific they "
             "said. Ordered from foundational to detail. No generic questions."
    )

    technical_realities = dspy.OutputField(
        desc="Honest evaluation of technical complexity for any advanced features "
             "mentioned or implied. Name the specific challenge, not just 'this is complex'. "
             "Include one sentence on a practical pathway for each."
    )

    vision_so_far = dspy.OutputField(
        desc="A preliminary vision statement written in the developer's voice, expanded. "
             "This is their idea made more articulate — not a product requirement document. "
             "Should feel like something they could have written themselves if they had "
             "the words."
    )

clarifier = dspy.ChainOfThought(VisionClarifier)

# ── Run on your real idea ────────────────────────────────────
raw_idea = """
I want to create a digital piano app that reads notes, plays music, 
and indicates the keys pushed at the right timing for practitioners.
"""

result = clarifier(raw_idea=raw_idea)

print("=" * 60)
print("CORE INTENT")
print("=" * 60)
print(result.core_intent)

print("\n" + "=" * 60)
print("QUESTIONS TO DEFINE YOUR VISION")
print("=" * 60)
print(result.questions)

print("\n" + "=" * 60)
print("TECHNICAL REALITIES")
print("=" * 60)
print(result.technical_realities)

print("\n" + "=" * 60)
print("YOUR VISION SO FAR")
print("=" * 60)
print(result.vision_so_far)
```

---

Run it:

```powershell
python dspy_vision.py
```

When you see the output — read the `CORE INTENT` section first. That's the test. If it sounds like a generic "music learning app description" we have work to do. If it sounds like **your** idea with your intent behind it — the signature is working.

Show me everything it outputs. This is the one I'm most curious about. 🎯