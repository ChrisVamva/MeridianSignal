---
modified: 2026-04-20T23:30:20+03:00
---
Now I have everything I need — from the live docs, fresh. Let me build you the complete map.

---

# 🗺️ The Complete Opencode Mastery Guide
### *Tailored to your Sovereign Stack*

---

## First: The Mental Model

Opencode has **7 distinct levers** for shaping agent behavior. Most people only find 2. Here's the full picture:

```
LEVER 1 — AGENTS.md        "Who are you and what do you know?"
LEVER 2 — Skills           "What reusable behaviors can you call on?"
LEVER 3 — Custom Agents    "Which specialist should handle this?"
LEVER 4 — Commands         "What shortcuts exist for my workflows?"
LEVER 5 — Permissions      "What are you allowed to do without asking?"
LEVER 6 — Model Routing    "Which brain powers which task?"
LEVER 7 — Sovereign Stack  "Everything flows through Phoenix."
```

---

## 📍 Your Windows File Structure
*(Verified from live docs — these are the exact real paths)*

```
C:\Users\YOU\
├── .config\opencode\
│   ├── opencode.json          ← Global config (all projects)
│   ├── AGENTS.md              ← Global rules (personal, not committed)
│   ├── agents\                ← Your custom agent .md files
│   │   ├── planner.md
│   │   ├── reviewer.md
│   │   └── sovereign.md       ← You'll build this
│   └── skills\                ← Global reusable skills
│       ├── git-release\
│       │   └── SKILL.md
│       └── obsidian-sync\
│           └── SKILL.md
│
└── .local\share\opencode\
    └── auth.json              ← Your provider keys (don't touch manually)

YOUR_PROJECT\
├── opencode.json              ← Project overrides (committed to Git)
├── AGENTS.md                  ← Project rules (committed to Git)
└── .opencode\
    ├── agents\                ← Project-specific agents
    ├── skills\                ← Project-specific skills
    └── commands\              ← Project-specific slash commands
```

---

## LEVER 1 — AGENTS.md
### *"Who are you and what do you know?"*

**The most powerful lever. Every token here shapes every response.**

There are two kinds — and both run simultaneously:

| File | Scope | Committed to Git? | Purpose |
|---|---|---|---|
| `C:\Users\YOU\.config\opencode\AGENTS.md` | All sessions, all projects | ❌ No | Your personal rules, preferences, how you work |
| `YOUR_PROJECT\AGENTS.md` | That project only | ✅ Yes | Project structure, conventions, gotchas |

### Your Global AGENTS.md — Start Here

```markdown
# Global Agent Rules

## My Working Style
- I am working on Windows with VS Code and Windsurf
- I am still building my understanding of code — explain decisions briefly
- Never overwrite a config file without showing me the diff first
- When suggesting file edits, tell me WHICH file and WHERE before making changes
- If you're unsure about a path, ASK — do not guess

## My Stack
- Python projects use pip, not conda
- Node projects use npm
- I have a LiteLLM proxy running locally (my Sovereign Stack)
- I have Arize Phoenix monitoring at [your actual port]

## My Projects
- Drawing app: [your repo path]
- Productivity tracker: [your repo path]  
- Digital journal: [your repo path]
- Blog: [your repo path]

## Hard Rules
- Never run `git push` without asking
- Never delete files — move them to _archive/ instead
- Always confirm before installing new packages
```

### Generate Project AGENTS.md Automatically

Inside Opencode, in any project directory:
```
/init
```
This scans your repo and generates a tailored `AGENTS.md` with your actual build commands, structure, and conventions. Run this in every one of your 10 repos. **Takes 30 seconds. Saves hours.**

---

## LEVER 2 — Skills
### *"Reusable behaviors you call once, use everywhere"*

Skills are Markdown files the agent **discovers and loads on demand** — they don't bloat the context until needed. Think of them as plug-in knowledge.

**Structure:**
```
C:\Users\YOU\.config\opencode\skills\
└── your-skill-name\
    └── SKILL.md          ← Must be uppercase, exactly this name
```

**Example — a skill for your Sovereign Stack workflow:**

```
C:\Users\YOU\.config\opencode\skills\sovereign-deploy\SKILL.md
```

```markdown
---
name: sovereign-deploy
description: Route tasks through the LiteLLM proxy and verify in Arize Phoenix
license: MIT
compatibility: opencode
---

## What I do
- Confirm which proxy model to use for this task type
- Check that the LiteLLM proxy is running before proceeding
- Remind to verify token usage in Phoenix after completion

## When to use me
Use when working on tasks you want to monitor in Arize Phoenix.
Ask which proxy model fits: Cerebras Qwen (fast), DeepSeek Cloud (deep reasoning),
Devstral Heavy (coding), Nemotron Architect (architecture).

## Steps
1. Confirm: `curl http://localhost:[YOUR_PORT]/health`
2. Select model based on task type
3. After completion: check Phoenix dashboard for latency/token data
```

**Other skills worth building for your setup:**

| Skill Name | What It Does |
|---|---|
| `obsidian-capture` | Saves decisions/notes to your vault in standard format |
| `git-safe-commit` | Verifies changes before any git operation |
| `config-verify` | Fetches live docs before touching any config file |
| `drawing-app-context` | Loads your drawing app's architecture context |

---

## LEVER 3 — Custom Agents
### *"Which specialist handles this task?"*

Opencode has **2 built-in primary agents** (Build, Plan) and **2 built-in subagents** (General, Explore). You can create your own.

**Two types:**
- **Primary** — you talk to them directly, switch with `Tab`
- **Subagent** — invoked via `@mention` or by a primary agent delegating

**Create an agent:**
```bash
opencode agent create
```
*(Interactive — it asks questions and generates the file)*

**Or create manually. Here are agents designed for YOUR setup:**

### Agent 1: The Planner (already built-in, but tune it)

```json
// In C:\Users\YOU\.config\opencode\opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "plan": {
      "temperature": 0.1,
      "model": "openrouter/google/gemini-2.5-pro",
      "permission": {
        "edit": "deny",
        "bash": "deny",
        "write": "deny"
      }
    }
  }
}
```
*Plan agent: reads everything, changes nothing. Use it for architecture decisions.*

### Agent 2: Your Sovereign Monitor (custom subagent)

```
C:\Users\YOU\.config\opencode\agents\sovereign-monitor.md
```

```markdown
---
description: Routes tasks through Sovereign Stack proxy and monitors in Phoenix
mode: subagent
permission:
  edit: ask
  bash:
    "*": ask
    "curl *": allow
---

You are a monitoring-aware developer assistant.

Before any significant task:
1. Confirm the LiteLLM proxy is accessible
2. Select the appropriate proxy model for this task type:
   - Fast iteration: Cerebras Qwen
   - Deep code analysis: DeepSeek Cloud  
   - Heavy implementation: Devstral Heavy
   - System architecture: Nemotron Architect
3. After completion, remind the user to check Phoenix for metrics

Never make changes without explaining what file will be affected and why.
```

### Agent 3: The Reviewer (read-only, for code review)

```
C:\Users\YOU\.config\opencode\agents\reviewer.md
```

```markdown
---
description: Reviews code for issues without making any changes
mode: subagent
permission:
  edit: deny
  write: deny
  bash:
    "*": deny
    "git diff*": allow
    "git log*": allow
---

You are a code reviewer. You READ and ANALYZE only — never write or edit.

Focus on:
- Logic errors and edge cases
- Security vulnerabilities
- Performance issues
- Consistency with the project's existing patterns

Always format your review as:
## Summary
## Issues Found (Critical / Warning / Suggestion)
## What's Good
```

---

## LEVER 4 — Custom Commands
### *"Slash commands for your most common workflows"*

```json
// In C:\Users\YOU\.config\opencode\opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "review": {
      "description": "Full code review of current changes",
      "template": "Review all changes since last commit. Focus on bugs, security, and consistency with existing code.",
      "agent": "reviewer",
      "model": "openrouter/google/gemini-2.5-pro"
    },
    "obsidian": {
      "description": "Capture decision to Obsidian vault",
      "template": "Summarize the key decision we just made about $ARGUMENTS into a concise Obsidian note. Format: ## Decision\n## Why\n## Alternatives Rejected\n## Date: today"
    },
    "sovereign": {
      "description": "Check Sovereign Stack health",
      "template": "Check if my LiteLLM proxy is running and show me recent Phoenix metrics if available. My proxy is at [YOUR PORT].",
      "agent": "sovereign-monitor"
    },
    "checkpoint": {
      "description": "Save session progress to project AGENTS.md",
      "template": "Summarize what we've built in this session and add it to the '## Session Notes' section of AGENTS.md. Include: what changed, any gotchas discovered, current state."
    }
  }
}
```

Use them in Opencode with `/review`, `/obsidian`, `/sovereign`, `/checkpoint`.

---

## LEVER 5 — Permissions
### *"What can the agent do without asking you first?"*

This is the most important safety layer given your history. The default is **allow everything** — that's what caused your nightmare sessions.

**Your baseline config:**

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "write": "ask",
    "bash": {
      "*": "ask",
      "git status": "allow",
      "git diff*": "allow",
      "git log*": "allow",
      "ls *": "allow",
      "cat *": "allow",
      "curl *": "allow"
    },
    "webfetch": "allow",
    "skill": {
      "*": "allow",
      "experimental-*": "ask"
    }
  },
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git push*": "ask",
          "git status": "allow",
          "npm install*": "ask",
          "pip install*": "ask"
        }
      }
    },
    "plan": {
      "permission": {
        "edit": "deny",
        "write": "deny",
        "bash": "deny"
      }
    }
  }
}
```

**Translation of what this does:**
- Agent must ask before editing or creating any file ✅
- Agent can run read-only git/bash commands freely ✅
- `git push`, `npm install`, `pip install` always require confirmation ✅
- Plan agent literally cannot touch your filesystem ✅

---

## LEVER 6 — Model Routing Strategy
### *"The right brain for the right task"*

Based on your actual model list, here's the routing logic that makes sense:

| Task Type | Best Model From Your List | Why |
|---|---|---|
| Architecture / design decisions | Qwen 3 235B (Cerebras) | Fast, large context, reasoning |
| Heavy implementation | devstral-2:123b (Ollama Cloud) | Built for coding |
| Quick iterations / fixes | Gemini Flash-Lite | Fast and free |
| Research / planning | Gemini 2.5 Pro | Deep reasoning |
| Coder-specific tasks | qwen3-coder:480b (Ollama Cloud) | Specialized for code |
| Cost-zero exploration | Nemotron 3 Super Free (Zen) | Free, solid |
| Monitored tasks | Your 4 Proxy models | Goes through Phoenix |

**Wire this into your agents:**

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "openrouter/google/gemini-flash-lite-latest",
  "small_model": "opencode/nemotron-3-super",
  "agent": {
    "plan": {
      "model": "openrouter/google/gemini-2.5-pro",
      "temperature": 0.1
    },
    "build": {
      "temperature": 0.3
    }
  }
}
```

---

## LEVER 7 — Sovereign Stack Integration
### *"Every Opencode session flows through Phoenix"*

This is where your setup becomes genuinely powerful. Your LiteLLM proxy is an OpenAI-compatible endpoint. Opencode can connect to it as a custom provider — meaning **every session gets Phoenix telemetry automatically**.

**What you need from YOUR LiteLLM config first:**
1. What port is your proxy running on? (default: `4000`)
2. Do you have a master key set? (`LITELLM_MASTER_KEY` or similar)
3. What are the exact model names as defined in your LiteLLM `config.yaml`?

**Once you have those, the config block is:**

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "sovereign": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Sovereign Stack",
      "options": {
        "baseURL": "http://localhost:[YOUR_PORT]/v1",
        "apiKey": "{env:LITELLM_API_KEY}"
      },
      "models": {
        "[your-cerebras-model-name]": {
          "name": "Cerebras Qwen (Proxy)"
        },
        "[your-deepseek-model-name]": {
          "name": "DeepSeek Cloud (Proxy)"
        },
        "[your-devstral-model-name]": {
          "name": "Devstral Heavy (Proxy)"
        },
        "[your-nemotron-model-name]": {
          "name": "Nemotron Architect (Proxy)"
        }
      }
    }
  }
}
```

The model names in `[brackets]` must exactly match what you defined in your LiteLLM `config.yaml` — not display names, the internal IDs.

---

## Your Learning Path — Ordered by Impact

```
WEEK 1: Foundation
  ✅ Step 1: Create your Global AGENTS.md (personal rules)
  ✅ Step 2: Set permissions to "ask" baseline
  ✅ Step 3: Run /init in each of your 10 repos

WEEK 2: Specialization  
  ✅ Step 4: Create the Plan agent (tuned, read-only)
  ✅ Step 5: Create the Reviewer subagent
  ✅ Step 6: Set up /checkpoint and /obsidian commands

WEEK 3: The Sovereign Stack
  ✅ Step 7: Get your LiteLLM proxy port + model names
  ✅ Step 8: Add sovereign provider to opencode.json
  ✅ Step 9: Create the sovereign-monitor subagent
  ✅ Step 10: Verify in Phoenix — every Opencode session now has metrics

WEEK 4: Skills + Optimization
  ✅ Step 11: Build your first skill (git-safe-commit)
  ✅ Step 12: Tune temperature per agent based on Phoenix latency data
  ✅ Step 13: Build per-project AGENTS.md for drawing app + journal
```

---

**One immediate action you can take right now:**

Open Opencode in any of your repos and type:
```
/init
```

That one command will give you a baseline `AGENTS.md` built from your actual codebase. Everything above builds on top of that foundation. What do you want to tackle first — the global rules, the permissions, or getting the Sovereign Stack wired in?