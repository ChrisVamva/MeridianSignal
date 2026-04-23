---

## How to Run It

```powershell
# From C:\Users\user\dpsy\
python agent_loop.py C:\Users\user\your-project "Add user authentication with JWT"

# Or point at current directory
python agent_loop.py . "Write unit tests for the database module"

# Or any task
python agent_loop.py C:\Users\user\myflaskapp "Add a /health endpoint that returns uptime"
```

---

## What You'll See in Your Terminal

```
============================================================
  DSPy CODING AGENT
  Task:    Add user authentication with JWT
  Project: C:\Users\user\myflaskapp
============================================================

📁 Scanning project...
   23 files found

🧠 Planning...

📋 Plan:
   Implement JWT-based auth using PyJWT. Add /login and /register endpoints...

📄 Files: ["app.py", "requirements.txt", "auth.py"]

🔢 6 steps:
    1. Read app.py to understand current structure
    2. Install PyJWT dependency
    3. Create auth.py with login/register logic
    4. Add auth routes to app.py
    5. Run tests
    6. Verify server starts

--------------------------------------------------
⚡ Step 1/6: Read app.py to understand current structure
   💭 Need to read the existing app.py before modifying it...
   🔧 read_file  args={"path": "app.py"}
   📤 from flask import Flask...
   ✅ Verified

⚡ Step 2/6: Install PyJWT dependency
   🔧 run_command  args={"command": "pip install PyJWT"}
   📤 {'returncode': 0, 'stdout': 'Successfully installed PyJWT...'}
   ✅ Verified
```

And simultaneously at `http://localhost:6006` — every plan, every decision, every verification call appears as a trace span.

---

## The Architecture in One Diagram

```
your terminal command
        │
        ▼
  agent_loop.py  ←──────────────────────────────────┐
        │                                            │
        ├─► scan_project()    [tools - no LLM]       │
        │                                            │
        ├─► TaskPlanner       [DSPy + LLM] ─► Phoenix trace
        │      └─ steps[], files[]                   │
        │                                            │
        └─► for each step:                           │
               │                                     │
               ├─► StepDecider  [DSPy + LLM] ─► Phoenix trace
               │      └─ tool_name, tool_args        │
               │                                     │
               ├─► tools[tool_name](**tool_args)      │
               │      └─ read/write/run/search  [no LLM]
               │                                     │
               └─► Verifier    [DSPy + LLM] ─► Phoenix trace
                      └─ success? retry?    ──────────┘
```

Give it a real project to try on — point it at something you're actually working on and let's see what it does.