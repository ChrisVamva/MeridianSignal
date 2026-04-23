---
modified: 2026-04-21T01:19:44+03:00
---
## Ollama Cloud — Now I Know It

Launched September 2025. Key facts:

|Plan|Price|Session limit (est.)|Weekly (est.)|
|---|---|---|---|
|**Free**|$0|~2M tokens / 5hrs|~5M tokens|
|Pro|$20/mo|~100M tokens|~250M tokens|
|Max|$100/mo|~500M tokens|~1.25B tokens|

**Critical difference from OpenRouter/Anthropic:** It charges by **GPU time**, not tokens. Shorter prompts + cached context = less usage. Which means your design.md habit and tight prompting discipline **directly reduces your Ollama Cloud bill**. Your efficiency work has compounding returns here.

Free tier resets every 5 hours and weekly. For planning sessions that are focused and structured — genuinely workable.

---

## Now — Your Real Goal Today: DSPy for Prompt Mastery

This is where it gets exciting. Let me be precise about what DSPy actually does for your situation.

**You already have the two things DSPy needs to be powerful:**

```
Arize Phoenix  →  tells you which prompts performed poorly
DSPy           →  systematically finds prompts that perform better
```

You're not just "learning prompting." You're building a **closed-loop prompt optimization system.** That's genuinely advanced.

---

## How DSPy Fits Your Stack Specifically

**Your current prompting problem:**

- You write a prompt
- You get a result
- You tweak by intuition
- You hope it's better
- Arize Phoenix shows you it wasn't

**What DSPy changes:**

- You define what "good output" looks like (a metric)
- You give it a few examples of input → good output
- It **compiles** your prompt automatically using your cheaper models
- Arize Phoenix **validates** whether the compiled prompt actually improved

Your Deepseek + Qwen free credits become the **compilation substrate** — DSPy runs hundreds of prompt variations against them cheaply. Then you validate the winner with Claude on your 4-day Antigravity window.

---

## The Concrete Starting Point

Given your stack, I'd suggest we focus on:

1. **Defining your first DSPy module** — around your design.md generation workflow (since that's your most critical prompt)
2. **Connecting it to Arize Phoenix** — you're halfway there already
3. **Using your Ollama Cloud free tier as the optimizer model** — small, fast, cheap iterations

Where are you currently in DSPy — have you installed it and run anything, or are you starting from zero with it?