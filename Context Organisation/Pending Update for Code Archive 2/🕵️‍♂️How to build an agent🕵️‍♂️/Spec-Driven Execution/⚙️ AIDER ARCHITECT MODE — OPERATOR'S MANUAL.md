---
modified: 2026-04-18T22:41:27+03:00
---
# ⚙️ AIDER ARCHITECT MODE — OPERATOR'S MANUAL
### Zero-Cost Two-Agent Swarm via CLI | Sovereign Stack Edition
### Classification: TECHNICAL OPERATIONS GUIDE

---

> **Source verification:** Configuration patterns in this manual are confirmed against `aider.chat/docs/usage/modes.html` (live primary source) + community production deployments as of April 2026.

---

## OBJECTIVE 1: THE MECHANICS OF HANDOFF

### The Core Architecture

Architect mode is a **two-request-per-turn pipeline**. Every prompt you enter goes through exactly two sequential LLM API calls:

```
YOUR PROMPT
     │
     ▼ API Call #1
┌─────────────────────────────────────────────────────────┐
│  ARCHITECT MODEL (--model)                              │
│  Receives: repo map + added file contents + your prompt │
│  Task: Reason about the problem. Propose a solution.    │
│  Format: Plain text / natural language. No diff format  │
│          required. Can use markdown, bullet points,     │
│          code blocks — anything that communicates intent.│
│  Output: Natural language plan (e.g., "Add a method to  │
│          class X that does Y, update Z to call it...")  │
└─────────────────────────────┬───────────────────────────┘
                              │ Architect's full text proposal
                              │ is appended to the prompt
                              ▼ API Call #2
┌─────────────────────────────────────────────────────────┐
│  EDITOR MODEL (--editor-model)                          │
│  Receives: repo map + file contents + ORIGINAL prompt   │
│            + ARCHITECT'S COMPLETE PROPOSAL              │
│  Task: Translate the proposal into precise, syntactically│
│         correct file edits using the configured format. │
│  Format: editor-diff or editor-whole (structured diffs) │
│  Output: Formatted file editing instructions → Aider    │
│          applies them to disk → Git auto-commit         │
└─────────────────────────────┬───────────────────────────┘
                              │
                              ▼
                   Files modified on disk
                   Git commit created
                   Aider shows you the diff
```

### What the Architect Sees (Context Window)

The Architect receives a context package containing:

1. **System prompt** — Aider's architect-role instructions ("You are an expert software architect...")
2. **Repository map** — A structured index of all files, classes, functions, and their relationships. NOT raw file contents — a compressed semantic map. Generated automatically by Aider's tree-sitter analysis.
3. **Explicitly added file contents** — Full content of files you've added via `/add` or at launch
4. **Read-only file contents** — Files added with `/read-only` (structural context, not to be modified)
5. **Your prompt** — The natural language request

**Critical insight:** The Architect is NOT given a summary. It receives the actual file contents you've added, filtered by the repo map. It does NOT see the edit format spec — that is exclusively the Editor's concern. This is why you can use a reasoning model that cannot reliably produce diff syntax — it only needs to produce coherent text.

### What the Editor Sees (Context Window)

The Editor receives a context package containing:

1. **System prompt** — Aider's editor-role instructions ("Apply the proposed changes as file edits...")
2. **Repository map** — Same structural map
3. **Explicitly added file contents** — Same files (current state, pre-edit)
4. **Your ORIGINAL prompt**
5. **The Architect's COMPLETE response** — Full text of what the Architect produced
6. **Edit format specification** — The exact format (editor-diff / editor-whole) the Editor must output

**Critical insight:** The handoff payload is the **full text of the Architect's response**, not a summary. There is no compression or lossy transformation between the two calls. The Editor receives everything the Architect said.

### Is There Human Review Between the Two Calls?

**By default: No.** The pipeline runs automatically:
- Architect responds → Editor immediately receives → Editor applies edits → Files modified

**With `--auto-accept-architect` flag: Fully automated.**

**Without this flag (default behavior):** Aider will display the Architect's proposal in your terminal and **pause for your confirmation** before sending to the Editor. This is the human-in-the-loop gate.

> **The pause is your quality control checkpoint.** You can:
> - Type `y` or press Enter to proceed to the Editor
> - Edit the Architect's proposal before proceeding (not directly, but you can pivot)
> - Type `n` to reject and give a new prompt

---

## OBJECTIVE 2: SYNTAX AND CONFIGURATION

### The Direct Command (Multi-Provider Setup)

**Your exact sovereign stack configuration:**

```bash
# DeepSeek R1 as Architect (OpenRouter) + Codestral as Editor (Ollama)
aider \
  --architect \
  --model openrouter/deepseek/deepseek-r1 \
  --editor-model ollama_chat/codestral \
  --editor-edit-format editor-diff
```

> **⚠️ Important:** Use `ollama_chat/` prefix, NOT `ollama/`, for the editor model. The `ollama_chat` prefix uses the `/api/chat` endpoint which handles multi-turn context correctly. `ollama/` uses the `/api/generate` completion endpoint, which is less reliable for structured edit-format output.

### Environment Variables Required

```bash
# Required for OpenRouter (Architect)
export OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Ollama runs locally, no API key needed
# Ensure Ollama is running: ollama serve
# Ensure model is pulled: ollama pull codestral
```

### Alternative: Route Both Models Through LiteLLM Proxy

If you want your existing self-healing proxy to handle both models (enabling circuit-breaker protection and observability for both Architect and Editor calls):

```bash
# Both routed through your sovereign LiteLLM proxy
export OPENAI_API_KEY=sk-sovereign-master-key    # Your LiteLLM master key
export OPENAI_API_BASE=http://localhost:4000      # Your LiteLLM proxy

aider \
  --architect \
  --model openai/sovereign-architect \
  --editor-model openai/sovereign-editor \
  --editor-edit-format editor-diff
```

Where your `litellm_config.yaml` maps:

```yaml
model_list:
  - model_name: sovereign-architect
    litellm_params:
      model: openrouter/deepseek/deepseek-r1
      api_key: os.environ/OPENROUTER_API_KEY

  - model_name: sovereign-editor
    litellm_params:
      model: ollama_chat/codestral
      api_base: http://localhost:11434
```

### The Persistent Config File (Zero Repetition)

Place `.aider.conf.yml` in your home directory (~/) or repository root:

```yaml
# ~/.aider.conf.yml — Sovereign Stack Architect Mode Configuration
# ─────────────────────────────────────────────────────────────────

# ── MODE ─────────────────────────────────────────────────────────
architect: true                     # Launch in architect mode by default

# ── ARCHITECT MODEL (Planner) ────────────────────────────────────
# Option A: Direct to OpenRouter (no proxy overhead)
model: openrouter/deepseek/deepseek-r1

# Option B: Route through LiteLLM proxy (circuit breaker protection)
# model: openai/sovereign-architect
# openai-api-base: http://localhost:4000
# openai-api-key: sk-sovereign-master-key

# ── EDITOR MODEL (Executor) ──────────────────────────────────────
# Option A: Direct local Ollama
editor-model: ollama_chat/codestral

# Option B: Through proxy
# editor-model: openai/sovereign-editor

# ── EDIT FORMAT ──────────────────────────────────────────────────
# editor-diff: Most efficient. Editor only outputs changed blocks.
# editor-whole: Safest. Editor outputs entire file. Use if editor-diff fails.
editor-edit-format: editor-diff

# ── GIT BEHAVIOR ─────────────────────────────────────────────────
auto-commits: true                  # Auto-commit each change (recommended)
commit-prompt: true                 # Auto-generate commit messages

# ── CONTEXT MANAGEMENT ───────────────────────────────────────────
map-tokens: 2048                    # Repo map token budget (increase for larger repos)
# max-chat-history-tokens: 8192    # Cap conversation history tokens

# ── REASONING CONTROLS (for R1 as Architect) ─────────────────────
# Uncomment if hitting thinking token limits or cost issues:
# thinking-tokens: 8000            # Cap R1's chain-of-thought tokens

# ── ANALYTICS (disable for pure sovereignty) ─────────────────────
analytics: false                    # Disable usage analytics reporting
```

### Model Aliases (Optional Shorthand)

Add to `~/.aider.conf.yml` to avoid typing full model strings:

```yaml
alias:
  - r1:openrouter/deepseek/deepseek-r1
  - codestral:ollama_chat/codestral
  - qwen3:ollama_chat/qwen3:235b
  - gemini-free:gemini/gemini-2.0-flash-exp
```

Then launch with:
```bash
aider --architect --model r1 --editor-model codestral
```

### Model Metadata File (Suppress Context Window Warnings)

When using custom/open-weight models via Ollama or proxy, Aider may warn it doesn't know the context window size. Silence this with `.aider.model.metadata.json` in your project root:

```json
{
  "ollama_chat/codestral": {
    "max_tokens": 4096,
    "max_input_tokens": 32768,
    "max_output_tokens": 4096,
    "input_cost_per_token": 0.0,
    "output_cost_per_token": 0.0,
    "litellm_provider": "ollama_chat",
    "mode": "chat"
  },
  "openrouter/deepseek/deepseek-r1": {
    "max_tokens": 8000,
    "max_input_tokens": 128000,
    "max_output_tokens": 8000,
    "input_cost_per_token": 0.00000055,
    "output_cost_per_token": 0.00000219,
    "litellm_provider": "openrouter",
    "mode": "chat"
  },
  "openai/sovereign-architect": {
    "max_tokens": 8192,
    "max_input_tokens": 128000,
    "max_output_tokens": 8192,
    "input_cost_per_token": 0.0,
    "output_cost_per_token": 0.0,
    "litellm_provider": "openai",
    "mode": "chat"
  },
  "openai/sovereign-editor": {
    "max_tokens": 4096,
    "max_input_tokens": 32768,
    "max_output_tokens": 4096,
    "input_cost_per_token": 0.0,
    "output_cost_per_token": 0.0,
    "litellm_provider": "openai",
    "mode": "chat"
  }
}
```

### Mid-Session Model Switching

You can change models without restarting Aider using in-session commands:

```bash
# Switch Architect model on the fly
architect> /model openrouter/deepseek/deepseek-r1

# Switch Editor model on the fly (not a built-in command — use config flag instead)
# Workaround: restart with new --editor-model flag

# Switch entire chat mode
architect> /chat-mode code          # Revert to single-model code mode
architect> /chat-mode ask           # Switch to discussion-only mode
architect> /chat-mode architect     # Back to architect mode
```

---

## OBJECTIVE 3: FAILURE MODES AND CONTEXT DRIFT

### Failure Mode 1: Editor Format Rejection ("Failed to apply edit")

**What happens:** The Editor model generates a diff, but Aider cannot apply it because the search block doesn't match the current file content exactly. Error: `Failed to apply edit...`

**Root cause:** Codestral (or any editor model) slightly misquotes the existing code in the `SEARCH` block of the diff — whitespace issues, off-by-one characters, or hallucinated lines.

**Immediate fixes:**
```bash
# Step 1: Switch to editor-whole format (safe fallback)
# The entire file is rewritten — no search matching required
aider --architect --model openrouter/deepseek/deepseek-r1 \
      --editor-model ollama_chat/codestral \
      --editor-edit-format editor-whole

# Step 2: If still failing, try a more capable editor model
aider --architect --model openrouter/deepseek/deepseek-r1 \
      --editor-model openrouter/anthropic/claude-3-haiku
```

**In-session fix:**
```bash
# After a failed edit, you can retry with a fresh approach
architect> /clear          # Clear chat history
architect> /drop           # Drop all files
architect> /add target.py  # Re-add only the specific file you need
# Then re-enter your request
```

### Failure Mode 2: Context Overload / "Lazy Coding"

**What happens:** Models start refusing to write complete implementations, saying "...and so on" or truncating code. The Architect's proposal becomes vague. The Editor cuts corners.

**Root cause:** Context window saturation. The combined context exceeds ~25K tokens. Both models start losing coherence.

**Fix: Surgical context management**
```bash
architect> /tokens          # Check current token count
architect> /drop             # Remove all files
architect> /add src/api.py   # Re-add only what's needed
```

**Structural fix in config:**
```yaml
# .aider.conf.yml
map-tokens: 1024             # Reduce repo map budget (default is 2048)
# Only add files when explicitly needed — never bulk-add a directory
```

### Failure Mode 3: Architect Scope Creep

**What happens:** The Architect proposes changes to files you didn't intend to modify. The Editor applies them. You now have unexpected unstaged changes across unrelated files.

**Root cause:** The Architect reasons about the "correct" architectural solution without scope constraints, and Aider's auto-commit records all changes.

**Prevention:** Use explicit scope constraints in your prompt:
```
architect> Refactor the authentication flow in auth.py ONLY.
           Do NOT modify any other files. Do NOT change the
           database schema. Do NOT add new dependencies.
```

**Recovery:**
```bash
# Git is your safety net — every change is committed
git log --oneline    # See the commits Aider made
git revert HEAD      # Revert the last commit
git diff HEAD~1      # See exactly what changed
/undo               # Aider's own undo command (last change only)
```

### Failure Mode 4: "Plan Drift" — Editor Ignores the Architect

**What happens:** The Architect produces a clear, reasonable plan. The Editor generates completely different edits that don't reflect the plan at all. The Architect is effectively bypassed.

**Root cause:** Common with weaker or uncalibrated Editor models (budget models, aggressively quantized local models). The Editor model "knows" how to solve the problem itself and ignores the incoming proposal.

**Diagnosis:** Check `llm.logs` to see exactly what the Editor received and what it output:
```bash
# Launch with logging enabled
aider --architect --model r1 --editor-model ollama_chat/codestral \
      --verbose 2>&1 | tee aider-session.log
```

**Fix:** Upgrade the Editor model. Plan drift is a symptom of an Editor that's too capable — it doesn't need the Architect. Use the Architect as Planner and the Editor strictly as a syntax transformer:
- Best Editor models: Claude Haiku, Codestral, DeepSeek V3 (via OpenRouter)
- Avoid as Editor: models >70B that will "think for themselves"

### Failure Mode 5: R1 Latency Timeout

**What happens:** DeepSeek R1 takes 60-120 seconds to produce its architectural plan (23K thinking tokens). The terminal appears frozen. Users cancel prematurely.

**Root cause:** R1's deep chain-of-thought is a feature, not a bug — but its wall-clock time is real.

**Mitigation:**
```yaml
# .aider.conf.yml — Cap R1's thinking budget
thinking-tokens: 6000      # Reduce thinking tokens for faster response
                           # Trade-off: less thorough planning
```

**Workflow mitigation:** Use `/ask` mode to pre-discuss the plan with a faster model, then switch to `/architect` only for execution:
```bash
# Start fast with ask mode
aider --model ollama_chat/qwen3:8b

> /ask How should I refactor the auth module to support OAuth2?
# Discuss, iterate on approach
> /chat-mode architect
# Now invoke R1 with the already-established context
> implement the OAuth2 approach we discussed
```

### Does the Architect Auto-Correct the Editor? — The Honest Answer

**No.** Aider's architect mode is a **single-pass, two-step pipeline**, not a feedback loop. There is no automatic correction cycle where the Architect reviews the Editor's output.

The loop is:
```
User → Architect → Editor → File Changes → DONE
```

NOT:
```
User → Architect → Editor → Architect Review → Editor Retry → ...
```

If the Editor fails or produces incorrect output, the correction mechanism is **you** — via:
1. `/undo` — to revert the incorrect change
2. A new prompt in architect mode with more explicit constraints
3. Switching to `/ask` mode to re-plan before trying again
4. Manually editing the target file and letting Aider resume

This is a fundamental limitation of Aider's current architecture. For a true correction loop, you would need an external orchestration layer (e.g., a Python script that runs `aider` as a subprocess and evaluates the git diff against a test suite).

---

## OBJECTIVE 4: LITELLM PROXY COMPATIBILITY

### Scenario A: Both Models Through One LiteLLM Endpoint

This is the **recommended configuration** for your sovereign stack. Both Architect and Editor route through your self-healing proxy — they get circuit-breaker protection, cooldown quarantine, and observability via Langfuse:

```bash
# Your proxy is already running at localhost:4000
# LiteLLM config already defines model aliases

export OPENAI_API_KEY=sk-sovereign-master-key  # Your LiteLLM LITELLM_MASTER_KEY
export OPENAI_API_BASE=http://localhost:4000

aider \
  --architect \
  --model openai/sovereign-architect \
  --editor-model openai/sovereign-editor \
  --editor-edit-format editor-diff
```

LiteLLM proxy config (`litellm_config.yaml`):
```yaml
model_list:
  # Architect: DeepSeek R1 via OpenRouter with Groq fallback
  - model_name: sovereign-architect
    litellm_params:
      model: openrouter/deepseek/deepseek-r1
      api_key: os.environ/OPENROUTER_API_KEY
  
  # Editor: Local Codestral (zero cost, zero latency)
  - model_name: sovereign-editor
    litellm_params:
      model: ollama_chat/codestral
      api_base: http://localhost:11434

  # Architect fallback if R1 is rate-limited or down
  - model_name: sovereign-architect
    litellm_params:
      model: openrouter/qwen/qwen3-235b-a22b:free
      api_key: os.environ/OPENROUTER_API_KEY

router_settings:
  cooldown_time: 3600
  allowed_fails_policy:
    RateLimitErrorAllowedFails: 1
  retry_policy:
    RateLimitErrorRetries: 0
```

### Scenario B: Split Routing (Architect via Proxy, Editor Direct to Ollama)

If you want the Architect to benefit from proxy circuit-breaking but don't want Ollama traffic routed through LiteLLM (zero overhead for local calls):

```bash
# Architect via LiteLLM proxy
export OPENAI_API_KEY=sk-sovereign-master-key
export OPENAI_API_BASE=http://localhost:4000

# Editor: direct Ollama (bypasses proxy)
# Requires: Aider to support per-model API base (it does via env prefix or separate model settings)

aider \
  --architect \
  --model openai/sovereign-architect \
  --editor-model ollama_chat/codestral \
  --editor-edit-format editor-diff
```

> **Note:** When using `ollama_chat/` prefix, Aider communicates directly with Ollama on `http://127.0.0.1:11434` regardless of what `OPENAI_API_BASE` is set to. The `openai/` prefix goes to your `OPENAI_API_BASE`. The two prefixes route independently — you get the split routing for free.

### Scenario C: AnythingLLM as Routing Endpoint

AnythingLLM's API endpoint is OpenAI-compatible:

```bash
export OPENAI_API_KEY=your-anything-llm-api-key
export OPENAI_API_BASE=http://localhost:3001/api/v1  # AnythingLLM default

aider \
  --architect \
  --model openai/your-workspace-model-name \
  --editor-model ollama_chat/codestral
```

> **Caveat:** AnythingLLM is RAG-optimized and may add document context to every request, which will bloat the Architect's context unnecessarily. A raw LiteLLM proxy is cleaner for this use case.

---

## OPTIMIZED EDIT FORMAT DECISION TREE

```
What is your Editor model?
│
├─ Codestral (via Ollama)
│   └─ Use: editor-diff
│      Codestral was trained on editing tasks. Produces clean unified diffs.
│
├─ DeepSeek V3 (via OpenRouter/API)
│   └─ Use: editor-diff
│      V3 is highly reliable with diff format. Best cost/quality editor.
│
├─ Qwen3 8B-30B (local Ollama)
│   └─ Start with: editor-diff
│      Fallback to: editor-whole if diffs fail
│      Smaller models struggle with exact search block matching.
│
├─ Claude Haiku / GPT-4o-mini
│   └─ Use: editor-diff
│      These models are the most reliable diff generators.
│
└─ Unknown / Untested model
    └─ Use: editor-whole (safe default)
       Whole-file output never fails on format issues.
       Trade-off: More expensive (full file in every output token)
```

---

## COMPLETE QUICK-START SEQUENCE

```bash
# 1. Install Aider
pip install aider-install aider-chat

# 2. Pull Codestral for local editing
ollama pull codestral

# 3. Set OpenRouter key
export OPENROUTER_API_KEY=sk-or-v1-your-key

# 4. Navigate to your repository
cd /path/to/your/project

# 5. Initialize Aider config (one time)
cat > .aider.conf.yml << 'EOF'
architect: true
model: openrouter/deepseek/deepseek-r1
editor-model: ollama_chat/codestral
editor-edit-format: editor-diff
auto-commits: true
analytics: false
map-tokens: 2048
EOF

# 6. Launch
aider

# 7. Add files to context
architect> /add src/auth.py src/models/user.py

# 8. Check token usage
architect> /tokens

# 9. Make a request
architect> Add OAuth2 support to the authentication module.
           The new provider should integrate with the existing
           User model. Do NOT modify the database schema.

# 10. Review Architect's plan in the terminal, confirm with Enter

# 11. Codestral applies the edits locally, Aider commits

# 12. Review the diff
git show HEAD
```

---

## SESSION COMMANDS REFERENCE CARD

| Command | Effect |
|---|---|
| `/architect` | Send next message through architect pipeline |
| `/ask <question>` | Discuss without editing (no Editor call) |
| `/code <request>` | Single-model code mode (no Architect) |
| `/chat-mode architect` | Sticky: all messages use architect mode |
| `/add <file>` | Add file contents to context |
| `/drop <file>` | Remove file from context |
| `/read-only <file>` | Add as reference (Architect sees it, Editor won't modify it) |
| `/tokens` | Show current context token usage |
| `/clear` | Clear conversation history (keep files) |
| `/undo` | Revert last commit Aider made |
| `/run <cmd>` | Run a shell command (e.g., your test suite) |
| `/model <name>` | Change Architect model mid-session |
| `/diff` | Show the diff from the last edit |

---

## WARNING: THE AUTO-ACCEPT TRAP

Aider has a `--auto-accept-architect` flag that removes the human confirmation step between Architect and Editor. **Do not use this in production.** You lose your quality control checkpoint — the only moment you can reject a faulty plan before it becomes a git commit.

The correct approach for semi-automation:

```bash
# Safe: Human confirms Architect plan before Editor applies it (default)
aider --architect --model r1 --editor-model ollama_chat/codestral

# Fully autonomous (use only for well-tested, low-risk tasks)
aider --architect --model r1 --editor-model ollama_chat/codestral \
      --auto-accept-architect
```

---

*Manual compiled: 2026-04-18 | Source: aider.chat official docs + community production configurations*
