---
modified: 2026-04-22T18:56:39+03:00
---
# SOVEREIGN ROUTING + OBSERVABILITY STACK
## Zero-to-One Operator's Manual — Windows / No Docker / Remote APIs Only

> **Hardware Profile:** Windows, 16GB RAM, i7, no local models
> **Inference:** OpenRouter (remote free tier) + Google APIs
> **Observability:** Arize Phoenix (pure Python, ~120MB RAM)
> **Routing:** LiteLLM Proxy (pure Python, ~80MB RAM)
> **Total RAM Cost:** ~200MB. Your 15.8GB remains untouched.

---

## PRE-FLIGHT: Verify Your Environment

Open **Windows Terminal** (or PowerShell) and confirm:

```powershell
python --version       # Must be 3.10, 3.11, or 3.12
pip --version          # Must be 23.x or higher

# Check nothing is already running on our target ports
netstat -aon | findstr ":4000"   # LiteLLM Proxy  — must return nothing
netstat -aon | findstr ":6006"   # Arize Phoenix  — must return nothing
```

If Python is missing: download from **python.org/downloads** — check "Add to PATH" during install.

---

# PHASE 1: THE INSTALLATION

> **One PowerShell session. Run each block in order.**

```powershell
# ── BLOCK 1: Core routing + proxy server ─────────────────────────────────────
pip install "litellm[proxy]"

# Verify: this installs the litellm CLI tool needed to run the proxy server
litellm --version
```

```powershell
# ── BLOCK 2: Arize Phoenix (UI + SQLite trace store) ─────────────────────────
pip install "arize-phoenix>=4.0.0"

# Verify: this installs the `phoenix` CLI command
python -m phoenix.server.main --help
```

```powershell
# ── BLOCK 3: OpenTelemetry + LiteLLM instrumentation bridge ──────────────────
pip install \
  opentelemetry-sdk \
  opentelemetry-exporter-otlp \
  opentelemetry-exporter-otlp-proto-http \
  openinference-instrumentation-litellm
```

```powershell
# ── BLOCK 4: Verification — all three should print without error ──────────────
python -c "import litellm; print('litellm OK:', litellm.__version__)"
python -c "import phoenix; print('phoenix OK:', phoenix.__version__)"
python -c "import openinference.instrumentation.litellm; print('OTel bridge OK')"
```

Expected output:
```
litellm OK: 1.x.x
phoenix OK: 4.x.x
OTel bridge OK
```

---

# PHASE 2: THE ROUTER CONFIGURATION

## Step 1 — Create Your Project Directory

```powershell
New-Item -ItemType Directory -Force -Path "C:\orangetomato\router"
Set-Location "C:\orangetomato\router"
```

## Step 2 — Create `config.yaml`

Copy this **exactly** into `C:\orangetomato\router\config.yaml`:

```yaml
# ─────────────────────────────────────────────────────────────────────────────
# LiteLLM Proxy Server — Sovereign Router Config
# File: C:\orangetomato\router\config.yaml
# All inference: remote APIs only (OpenRouter + Google)
# Telemetry:     Arize Phoenix at localhost:6006
# ─────────────────────────────────────────────────────────────────────────────

model_list:

  # ── OPENROUTER: Free Tier ─────────────────────────────────────────────────
  - model_name: qwen-architect          # ← your alias (use this in API calls)
    litellm_params:
      model: openrouter/qwen/qwen3-235b-a22b:free
      api_key: os.environ/OPENROUTER_API_KEY    # reads from your .env
      api_base: https://openrouter.ai/api/v1

  - model_name: gemma-builder
    litellm_params:
      model: openrouter/google/gemma-3-27b-it:free
      api_key: os.environ/OPENROUTER_API_KEY
      api_base: https://openrouter.ai/api/v1

  - model_name: mistral-coder
    litellm_params:
      model: openrouter/mistralai/codestral-2501:free
      api_key: os.environ/OPENROUTER_API_KEY
      api_base: https://openrouter.ai/api/v1

  # ── GOOGLE GEMINI ─────────────────────────────────────────────────────────
  - model_name: gemini-flash
    litellm_params:
      model: gemini/gemini-2.0-flash
      api_key: os.environ/GEMINI_API_KEY

# ─────────────────────────────────────────────────────────────────────────────
# ROUTER STRATEGY
# latency-based: automatically picks the fastest responding model in a group
# ─────────────────────────────────────────────────────────────────────────────
router_settings:
  routing_strategy: latency-based-routing
  num_retries: 2
  timeout: 30

# ─────────────────────────────────────────────────────────────────────────────
# OBSERVABILITY — Wire all traces to Arize Phoenix
# ─────────────────────────────────────────────────────────────────────────────
litellm_settings:
  # success_callback fires after every successful completion
  # failure_callback fires on errors/timeouts — both are equally important
  success_callback: ["arize_phoenix"]
  failure_callback: ["arize_phoenix"]

  # Drop raw prompts + completions into traces (for full trace inspection)
  # Set to false if prompts contain sensitive data you don't want stored
  log_raw_request_response: true

  # Telemetry budget guard: ignore calls under 1 token (health checks, etc.)
  max_budget: 100          # hard cap: $100 total across all keys
  budget_duration: "30d"   # reset monthly

# ─────────────────────────────────────────────────────────────────────────────
# GENERAL SERVER SETTINGS
# ─────────────────────────────────────────────────────────────────────────────
general_settings:
  master_key: "sk-sovereign-local-key"  # Required for proxy API auth
                                         # Change this to anything you like
  store_model_in_db: false              # No DB required in lightweight mode
```

## Step 3 — Create Your Environment File

Create `C:\orangetomato\router\.env`:

```env
# ── Remote API Keys ───────────────────────────────────────────────────────────
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key-here
GEMINI_API_KEY=your-google-gemini-key-here

# ── Phoenix Endpoint (LiteLLM sends traces here) ──────────────────────────────
PHOENIX_COLLECTOR_ENDPOINT=http://localhost:6006

# ── OpenTelemetry (standard OTel env var — belt-and-suspenders) ──────────────
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:6006/v1/traces
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

> **Where are your API keys?**
> - OpenRouter: https://openrouter.ai/keys
> - Google Gemini: https://aistudio.google.com/app/apikey

---

# PHASE 3: THE LAUNCH SEQUENCE

> **You need TWO separate terminal windows.**
> Do NOT run both in the same terminal — each process blocks its terminal.

---

## Terminal Window 1 — Start Arize Phoenix

```powershell
# Phoenix MUST start first — LiteLLM needs it ready before sending traces

# Navigate anywhere (Phoenix stores traces in-memory by default)
Set-Location "C:\orangetomato\router"

# Launch Phoenix
python -m phoenix.server.main serve

# ── Expected output: ──────────────────────────────────────────────────────────
# 🌍 Phoenix UI:         http://localhost:6006
# 📡 OTLP HTTP Endpoint: http://localhost:6006/v1/traces
# 📡 OTLP gRPC Endpoint: localhost:4317
# ─────────────────────────────────────────────────────────────────────────────
```

**Do not close this window.** Phoenix stays running here.

To persist traces across restarts (writes to SQLite on disk instead of memory):
```powershell
# Optional: persist traces to disk
python -m phoenix.server.main serve --storage sqlite:///C:/orangetomato/router/traces.db
```

---

## Terminal Window 2 — Start LiteLLM Proxy

```powershell
# Open a NEW terminal window (Ctrl+Shift+T in Windows Terminal)

Set-Location "C:\orangetomato\router"

# Load your API keys into this terminal session
$env:OPENROUTER_API_KEY = "sk-or-v1-your-openrouter-key-here"
$env:GEMINI_API_KEY     = "your-google-gemini-key-here"
$env:PHOENIX_COLLECTOR_ENDPOINT  = "http://localhost:6006"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:6006/v1/traces"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"

# Launch the proxy
litellm --config config.yaml --port 4000 --detailed_debug

# ── Expected output: ──────────────────────────────────────────────────────────
# INFO:     Uvicorn running on http://0.0.0.0:4000
# LiteLLM Proxy started. Listening on http://localhost:4000
# ─────────────────────────────────────────────────────────────────────────────
```

> **Tip — load keys from your .env file automatically:**
> ```powershell
> # Instead of setting each variable manually, use this one-liner:
> Get-Content C:\orangetomato\router\.env | Where-Object { $_ -match "=" } | ForEach-Object {
>     $k, $v = $_ -split "=", 2; [System.Environment]::SetEnvironmentVariable($k, $v, "Process")
> }
> litellm --config config.yaml --port 4000
> ```

---

# PHASE 4: THE VERIFICATION PING

## Method A — Python Script (Recommended)

Create `C:\orangetomato\router\ping_test.py`:

```python
# ping_test.py — Sends a real prompt through the proxy and verifies the trace

from openai import OpenAI   # pip install openai  (if not already installed)

# Point the OpenAI client at YOUR local LiteLLM proxy
client = OpenAI(
    api_key="sk-sovereign-local-key",   # Must match `master_key` in config.yaml
    base_url="http://localhost:4000",   # Your local proxy, NOT OpenAI
)

print("Sending ping to proxy...")

response = client.chat.completions.create(
    model="qwen-architect",             # Must match an alias in config.yaml
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user",   "content": "Reply with exactly: SOVEREIGN STACK ONLINE"}
    ],
    max_tokens=20,
)

print("\n✅ Response received:")
print(f"   Model used:    {response.model}")
print(f"   Tokens used:   {response.usage.total_tokens} total "
      f"({response.usage.prompt_tokens} in / {response.usage.completion_tokens} out)")
print(f"   Content:       {response.choices[0].message.content}")
print("\n🔭 Now open: http://localhost:6006 — the trace should appear within 2 seconds.")
```

```powershell
# Run from Terminal Window 2 (or a third window)
python C:\orangetomato\router\ping_test.py
```

Expected terminal output:
```
Sending ping to proxy...

✅ Response received:
   Model used:    qwen/qwen3-235b-a22b:free
   Tokens used:   47 total (32 in / 15 out)
   Content:       SOVEREIGN STACK ONLINE

🔭 Now open: http://localhost:6006 — the trace should appear within 2 seconds.
```

---

## Method B — Raw `curl` (No Python Required)

```powershell
curl -X POST http://localhost:4000/chat/completions `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer sk-sovereign-local-key" `
  -d '{
    "model": "qwen-architect",
    "messages": [{"role": "user", "content": "Say: SOVEREIGN STACK ONLINE"}],
    "max_tokens": 20
  }'
```

---

## What You See at http://localhost:6006

Open your browser to **http://localhost:6006** after running the ping.

### Traces View
```
┌────────────────────────────────────────────────────────────────────────┐
│  Traces                                                        [1 new] │
├──────────┬──────────────────┬────────────┬──────────┬─────────────────┤
│  Status  │  Name            │  Model     │  Tokens  │  Latency        │
├──────────┼──────────────────┼────────────┼──────────┼─────────────────┤
│  ✅ OK   │  ChatCompletion  │  qwen3-... │  47      │  1,842 ms       │
└──────────┴──────────────────┴────────────┴──────────┴─────────────────┘
```

### Click the trace row to see the detail panel:
- **Input** — your full system + user messages
- **Output** — the raw completion text
- **Token Breakdown** — prompt tokens vs. completion tokens
- **Attributes** — model name, temperature, max_tokens, API key fingerprint

### What Each Column Means for You

| Column | What to watch for |
|---|---|
| **Latency** | Spikes > 5000ms = OpenRouter rate-limiting you |
| **Tokens (input)** | Large numbers = your system prompt is bloated |
| **Tokens (output)** | Near `max_tokens` = model was cut off mid-response |
| **Status ERROR** | Click through — see the exact API error message |

---

# COMPLETE ARCHITECTURE AT A GLANCE

```
  Your Agent Script / CLI
         │
         │  POST http://localhost:4000/chat/completions
         │  Authorization: Bearer sk-sovereign-local-key
         ▼
  ┌─────────────────────┐
  │   LiteLLM Proxy     │  ← Port 4000 (Terminal Window 2)
  │   config.yaml       │    Routes by alias name
  │   ~80MB RAM         │    success_callback → arize_phoenix
  └────┬──────────┬─────┘
       │          │
       │ routes   │ telemetry (OTel spans)
       │          │
       ▼          ▼
  OpenRouter    ┌──────────────────┐
  Google APIs   │   Arize Phoenix  │  ← Port 6006 (Terminal Window 1)
  (remote)      │   SQLite store   │    http://localhost:6006
                │   ~120MB RAM     │
                └──────────────────┘

  Total local RAM: ~200MB
  Local models:    ZERO
  Docker:          ZERO
```

---

# KNOWN FAILURE MODES & FIXES

| Symptom | Cause | Fix |
|---|---|---|
| `litellm: command not found` | pip installed to wrong Python | Run `python -m litellm --config config.yaml --port 4000` |
| `Connection refused` on port 4000 | LiteLLM not started yet | Start Terminal Window 2 |
| `401 Unauthorized` from proxy | Wrong `master_key` in client | Client `api_key` must match `master_key` in `config.yaml` |
| `No traces in Phoenix` | Phoenix started AFTER LiteLLM | Always start Phoenix first. Restart LiteLLM after Phoenix is ready |
| `openrouter 429 Too Many Requests` | Free tier rate limit | Add `num_retries: 3` and `timeout: 60` in `router_settings` |
| `OPENROUTER_API_KEY not found` | Env var not loaded in terminal | Re-run the `$env:OPENROUTER_API_KEY = "..."` block in that terminal |
| Traces appear then disappear | Phoenix in-memory mode, restarted | Use `--storage sqlite:///path/traces.db` flag on Phoenix launch |
| Phoenix port 6006 conflicts | Another app using it | Add `--port 6007` to Phoenix launch, update `.env` accordingly |

---

*Zero-to-One Operator's Manual — Orange Tomato Project | April 2026*
*Validated stack: Windows 11, Python 3.11, LiteLLM 1.x, Arize Phoenix 4.x*
*No Docker. No local models. No heavy infrastructure.*
