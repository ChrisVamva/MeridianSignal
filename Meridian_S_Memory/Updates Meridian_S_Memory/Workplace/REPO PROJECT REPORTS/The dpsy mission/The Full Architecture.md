---
modified: 2026-04-21T17:28:24+03:00
---
Great choice. This is the most powerful pattern. Let me map the full architecture before we write a single line.

---

## The Core Idea

```
YOU give a task
      ↓
DSPy THINKS     ← "what should happen and why"
      ↓
Agent ACTS      ← "actually makes it happen"
      ↓
DSPy CHECKS     ← "did that work? what next?"
      ↓
Phoenix WATCHES ← "records everything for you to review"
```

DSPy never touches the filesystem or runs commands. The agent never decides strategy. Clean separation.

---

## The Full Architecture

```
┌─────────────────────────────────────────────────────┐
│                    YOUR TASK                        │
│  "Add Stripe payments to my Flask app"              │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              DSPy REASONING LAYER                   │
│                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │TaskPlanner  │  │StepDecider   │  │Verifier   │  │
│  │             │  │              │  │           │  │
│  │task→        │  │step+context→ │  │step+result│  │
│  │ plan        │  │ tool_name    │  │→ success  │  │
│  │ steps       │  │ tool_args    │  │  or retry │  │
│  │ files       │  │ reasoning    │  │           │  │
│  │ risks       │  │              │  │           │  │
│  └─────────────┘  └──────────────┘  └───────────┘  │
└─────────────────────┬───────────────────────────────┘
                      │  tool_name + tool_args
                      ▼
┌─────────────────────────────────────────────────────┐
│              EXECUTION LAYER (Agent Tools)          │
│                                                     │
│   read_file()      write_file()    run_command()    │
│   search_code()    list_dir()      patch_file()     │
│                                                     │
│         (pure Python — no LLM involved)             │
└─────────────────────┬───────────────────────────────┘
                      │  raw results back up
                      ▼
┌─────────────────────────────────────────────────────┐
│              ARIZE PHOENIX                          │
│   Every DSPy call traced automatically              │
│   localhost:6006 — you watch in real time           │
└─────────────────────────────────────────────────────┘
```

---

## The 3 DSPy Modules You Need

### 1. `TaskPlanner` — runs once at the start
```
Input:  task (what you want built)
        codebase_summary (what already exists)

Output: plan (overall approach)
        steps (ordered list of atomic actions)  
        files_to_touch (which files will change)
        risks (what could go wrong)
```

### 2. `StepDecider` — runs once per step
```
Input:  current_step (what needs to happen now)
        codebase_context (relevant file contents)
        completed_steps (what's already done)
        last_error (if retrying)

Output: tool_name (read_file / write_file / run_command / etc.)
        tool_args (exact arguments for that tool)
        reasoning (why this tool, why these args)
```

### 3. `Verifier` — runs after each tool call
```
Input:  step (what was supposed to happen)
        tool_result (what actually happened)
        
Output: success (bool)
        issue (if failed — specific problem)
        suggestion (how to fix it)
```

---

## The Agent Loop

```python
task = "add stripe payments to flask app"

# ── Phase 1: PLAN ──────────────────────────────────
plan = TaskPlanner(task=task, codebase=scan_project())
# Phoenix records this span

# ── Phase 2: EXECUTE ────────────────────────────────
for step in plan.steps:
    
    retries = 0
    last_error = None
    
    while retries < 3:
        
        # DSPy DECIDES what tool to call
        decision = StepDecider(
            step=step,
            context=get_relevant_files(plan.files_to_touch),
            completed=completed_steps,
            last_error=last_error
        )
        # Phoenix records this span
        
        # Agent EXECUTES the tool (no LLM here)
        result = tools[decision.tool_name](**decision.tool_args)
        
        # DSPy VERIFIES the result
        check = Verifier(step=step, result=result)
        # Phoenix records this span
        
        if check.success:
            completed_steps.append(step)
            break
        else:
            last_error = check.issue
            retries += 1

# ── Phase 3: REPORT ─────────────────────────────────
print(f"Done. {len(completed_steps)} steps completed.")
print(f"Check Phoenix for full trace: localhost:6006")
```

---

## Why This Is Powerful

| Property | How it's achieved |
|----------|------------------|
| **Rigorous** | TaskPlanner structures every job the same way |
| **Token efficient** | StepDecider only loads *relevant* file context |
| **Low hallucination** | Verifier catches bad outputs before they persist |
| **Transparent** | Every decision reasoned + traced in Phoenix |
| **Improvable** | Each module optimizable independently with MIPROv2 |
| **Recoverable** | Retry loop with error context fed back to DSPy |

---

## What We Build Next (in order)

```
Step 1 → The tool belt        (read, write, run, search — pure Python)
Step 2 → TaskPlanner module   (DSPy Signature + ChainOfThought)
Step 3 → StepDecider module   (DSPy Signature + ReAct or CoT)
Step 4 → Verifier module      (DSPy Signature, lightweight)
Step 5 → The agent loop       (wires it all together)
Step 6 → Phoenix dashboard    (you watch it run live)
Step 7 → Optimize each module (MIPROv2 on real task examples)
```

---

## One Decision Before We Start

**What's your project structure?**

The agent needs to know what it's working on. Two options:

**A) Project-aware** — you point it at a directory, it scans and understands the codebase first, then acts on it. Best for ongoing projects.

**B) Greenfield** — it starts fresh, creates files from scratch based on your task. Best for new features/scripts.

Also — **do you want it to auto-execute** shell commands (run tests, install packages), or **show you each action first and ask before executing**? The second is safer to start.