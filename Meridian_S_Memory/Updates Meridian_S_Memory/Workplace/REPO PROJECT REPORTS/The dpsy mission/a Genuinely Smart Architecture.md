---
modified: 2026-04-21T00:48:38+03:00
---
## Yes — This Is a Genuinely Smart Architecture

You've independently discovered what professional teams do with AI toolchains: **use expensive/heavy tools for planning, cheap/focused tools for execution.** Let me break down why this works and where the edges are.

---

## Why the Token Gap Exists

**Opencode's 10k "initial tax" comes from:**
- Its own large system prompt (agentic instructions, tool definitions)
- Automatic file indexing / codebase context loading
- Tool call schemas sent with every request (read_file, run_command, etc.)
- Multi-turn state tracking

**Pi's 500 tokens works because:**
- Minimal system prompt
- No automatic file loading
- No tool definitions overhead
- You control exactly what context goes in

This gap is **structural, not a bug**. Opencode will always be heavier because it's doing more automatically.

---

## The Viability Assessment

| Task | Best Tool | Why |
|------|-----------|-----|
| "What files need to change for this feature?" | Opencode | Reads your actual repo |
| "How should I architect this?" | Opencode | High reasoning, full context |
| "Write this function" | Pi + Codestral | Laser-focused, cheap |
| "Implement this plan step by step" | Pi + Devstral | Agent-capable, multi-step |
| "Refactor this file" | Pi + Codestral | Single-file, Codestral excels here |
| Debugging unknown errors | Opencode | Needs file access to trace |

**Verdict: Highly viable.** Your $10 OpenRouter budget goes roughly **20x further** on Pi vs Opencode for equivalent coding output.

---

## Your Two Models Are Well Chosen

**Devstral 2** — use for:
- Tasks requiring multi-file reasoning
- When Pi acts as an agent (planning + executing steps)
- Understanding how pieces connect

**Codestral** — use for:
- Single-file generation or edits
- Autocomplete-style "write this function"
- Refactoring, syntax fixes
- Fill-in-the-middle tasks

This is the **right split** — Devstral thinks, Codestral writes.

---

## The Critical Weakness: The Handoff

This is the only real risk in your plan. When you switch from Opencode → Pi, **context doesn't transfer automatically.** Pi won't know what Opencode understood about your repo.

**Solution — A "Plan Export" habit:**

After your Opencode planning session, ask it:

```
Summarize the plan as a structured handoff document:
- Files to modify (with paths)
- What changes in each file
- Order of operations
- Any dependencies or gotchas
- Relevant existing code snippets I'll need
```

Then paste that document as **the first message** to Pi. This costs maybe 1-2k tokens but gives Pi full orientation without Opencode's overhead.

---

## Practical Workflow

```
1. OPENCODE SESSION (planning)
   → "I want to add X feature to my drawing app"
   → Opencode reads files, reasons about architecture
   → You ask it to produce the handoff doc
   → Copy the output

2. PI + DEVSTRAL SESSION (orchestration)
   → Paste handoff doc
   → "Execute step 1: modify DrawingCanvas.js as described"
   → Devstral implements, you verify

3. PI + CODESTRAL (specific coding)
   → For any single-file deep work
   → Paste just the relevant file + the specific instruction
```

---

## One Thing to Watch

Pi doesn't have **file system access** the way Opencode does. You'll need to paste file contents manually, or check if Pi supports file uploads/attachments. This is the trade-off for the token savings — **you become the context pipe** between your files and Pi.

If that becomes friction, **Aider** (which you already have) is worth reconsidering for the execution phase — it has file access, is much lighter than Opencode, and works cleanly with Codestral via OpenRouter.

---

**Bottom line:** Your instinct is correct. Opencode = expensive architect, Pi = cheap builder. Wire them with a structured handoff and you've got a lean, budget-smart pipeline. Want me to help you design the exact handoff prompt template for your specific project types?