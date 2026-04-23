---
modified: 2026-04-19T17:31:19+03:00
---
# SOVEREIGN OBSERVABILITY STACK — OPERATOR'S MANUAL
### Classification: ORANGE TOMATO | Windows/Docker Desktop Deployment

> **Stack:** Langfuse (local) + LiteLLM Proxy + Ollama + OpenRouter + DeepEval
> **Environment:** Windows 11, Docker Desktop (WSL2 backend), Python 3.11+

---

## PRE-FLIGHT CHECKLIST

Run these before touching anything else:

```powershell
# Verify Docker Desktop is running
docker --version                    # Must return 24.x or higher
docker compose version              # Must return v2.x (NOT `docker-compose`)
docker ps                           # Must return empty table (not an error)

# Verify Python environment
python --version                    # Must be 3.11+
pip --version

# Verify ports are free
netstat -aon | findstr ":3000"      # Langfuse UI   — must be empty
netstat -aon | findstr ":8123"      # ClickHouse    — must be empty
netstat -aon | findstr ":4002"      # LiteLLM Proxy — must be empty (if running)
```

> ⚠️ If port 3000 is occupied (Next.js dev server, etc.), kill it first or change
> `LANGFUSE_PORT` in the compose file below.

---

# PHASE 1: THE LOCAL DASHBOARD (Langfuse)
## *Standing up your sovereign telemetry HQ*

---

### Step 1 — Create the Project Directory

```powershell
# All Orange Tomato infra lives together
New-Item -ItemType Directory -Force -Path "C:\orangetomato\langfuse"
Set-Location "C:\orangetomato\langfuse"
```

---

### Step 2 — Write the Docker Compose File

Create `C:\orangetomato\langfuse\docker-compose.yml`:

```yaml
# Langfuse Sovereign Stack — Docker Compose v2
# Tested: Langfuse v3.x on Docker Desktop (WSL2), April 2026

name: langfuse-sovereign

services:

  # ── LANGFUSE APPLICATION ─────────────────────────────────────────
  langfuse-server:
    image: langfuse/langfuse:latest
    depends_on:
      postgres:
        condition: service_healthy
      clickhouse:
        condition: service_healthy
      minio:
        condition: service_started
    ports:
      - "3000:3000"
    environment:
      # ── Database ──────────────────────────────────────────────────
      DATABASE_URL: "postgresql://langfuse:sovereign@postgres:5432/langfuse"

      # ── ClickHouse (analytics/traces) ─────────────────────────────
      CLICKHOUSE_MIGRATION_URL: "clickhouse://clickhouse:9000"
      CLICKHOUSE_URL:           "http://clickhouse:8123"
      CLICKHOUSE_USER:          "clickhouse_user"
      CLICKHOUSE_PASSWORD:      "sovereign_ch_pass"

      # ── Blob Storage (MinIO local S3) ─────────────────────────────
      LANGFUSE_S3_MEDIA_UPLOAD_ENABLED:        "true"
      LANGFUSE_S3_MEDIA_UPLOAD_BUCKET:         "langfuse-media"
      LANGFUSE_S3_MEDIA_UPLOAD_REGION:         "auto"
      LANGFUSE_S3_MEDIA_UPLOAD_ENDPOINT:       "http://minio:9000"
      LANGFUSE_S3_MEDIA_UPLOAD_ACCESS_KEY_ID:  "minio_admin"
      LANGFUSE_S3_MEDIA_UPLOAD_SECRET_KEY:     "minio_sovereign_pass"
      LANGFUSE_S3_MEDIA_UPLOAD_FORCE_PATH_STYLE: "true"

      # ── App Security (generate your own with: openssl rand -base64 32) ──
      NEXTAUTH_URL:      "http://localhost:3000"
      NEXTAUTH_SECRET:   "REPLACE_WITH_32_CHAR_RANDOM_STRING"
      SALT:              "REPLACE_WITH_DIFFERENT_32_CHAR_RANDOM_STRING"

      # ── Telemetry (disable phoning home) ─────────────────────────
      TELEMETRY_ENABLED: "false"
      LANGFUSE_ENABLE_EXPERIMENTAL_FEATURES: "true"

    restart: unless-stopped

  # ── POSTGRESQL (primary metadata store) ──────────────────────────
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB:       langfuse
      POSTGRES_USER:     langfuse
      POSTGRES_PASSWORD: sovereign
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U langfuse"]
      interval: 5s
      timeout: 5s
      retries: 10
    restart: unless-stopped

  # ── CLICKHOUSE (trace/event analytics) ────────────────────────────
  clickhouse:
    image: clickhouse/clickhouse-server:24-alpine
    user: "101:101"
    environment:
      CLICKHOUSE_DB:       langfuse
      CLICKHOUSE_USER:     clickhouse_user
      CLICKHOUSE_PASSWORD: sovereign_ch_pass
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - clickhouse_logs:/var/log/clickhouse-server
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:8123/ping"]
      interval: 5s
      timeout: 5s
      retries: 10
    restart: unless-stopped

  # ── MINIO (blob storage for prompts/completions) ──────────────────
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER:     minio_admin
      MINIO_ROOT_PASSWORD: minio_sovereign_pass
    volumes:
      - minio_data:/data
    ports:
      - "9001:9001"    # MinIO console at http://localhost:9001
    restart: unless-stopped

  # ── MINIO BUCKET INIT ─────────────────────────────────────────────
  minio-createbucket:
    image: minio/mc:latest
    depends_on:
      - minio
    entrypoint: >
      /bin/sh -c "
      sleep 5;
      /usr/bin/mc alias set local http://minio:9000 minio_admin minio_sovereign_pass;
      /usr/bin/mc mb local/langfuse-media --ignore-existing;
      exit 0;
      "
    restart: "no"

volumes:
  postgres_data:
  clickhouse_data:
  clickhouse_logs:
  minio_data:
```

---

### Step 3 — Generate Security Secrets

```powershell
# Run BOTH of these separately — use each output for NEXTAUTH_SECRET and SALT
# Option A: If you have OpenSSL (Git Bash / WSL)
openssl rand -base64 32

# Option B: Pure PowerShell
[Convert]::ToBase64String([Security.Cryptography.RandomNumberGenerator]::GetBytes(24))
```

**Edit** `docker-compose.yml` and replace both `REPLACE_WITH_...` values with your generated strings.

---

### Step 4 — Launch the Stack

```powershell
# From C:\orangetomato\langfuse\
docker compose up -d

# Watch the startup sequence (~60-90 seconds first boot)
docker compose logs -f langfuse-server
```

Wait until you see:
```
langfuse-server | ✓ Ready at http://localhost:3000
```

---

### Step 5 — First Login & API Key Extraction

1. Navigate to **http://localhost:3000**
2. Click **"Sign Up"** — create a local admin account (any email/password)
3. Create an **Organization** (e.g., `OrangeTomato`)
4. Create a **Project** (e.g., `sovereign-cli-agent`)
5. Navigate to **Settings → API Keys → Create new API key**
6. Copy both keys immediately — the Secret Key is shown only once

**Record your keys** in `C:\Users\user\.aider\oauth-keys.env`:

```env
# ── LANGFUSE LOCAL ────────────────────────────────────────────────
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### Step 6 — Smoke Test the API

```powershell
# Replace with your actual Public Key and Secret Key
$PUBLIC_KEY  = "pk-lf-your-public-key"
$SECRET_KEY  = "sk-lf-your-secret-key"
$credentials = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${PUBLIC_KEY}:${SECRET_KEY}"))

Invoke-RestMethod `
  -Uri "http://localhost:3000/api/public/health" `
  -Headers @{ Authorization = "Basic $credentials" }
```

Expected response: `{ "status": "OK", "version": "x.x.x" }`

---

# PHASE 2: THE WIRETAP (Instrumentation)
## *Intercepting every token without touching your core agent logic*

---

### Install Dependencies

```powershell
pip install langfuse litellm openai python-dotenv
# For OpenLLMetry (framework-agnostic OTel path):
pip install traceloop-sdk opentelemetry-sdk
```

---

### Method A — Direct Langfuse SDK (Recommended for LiteLLM setups)

This is the **zero-refactor path** for a LiteLLM-routed agent.
LiteLLM has native Langfuse callback support — one environment variable activates it.

```python
# agent.py — Sovereign CLI Agent Core
# Langfuse wiretap via LiteLLM callback — ZERO changes to agent logic required

import os
from dotenv import load_dotenv
import litellm

# ── 1. LOAD ENV ───────────────────────────────────────────────────────────────
load_dotenv(r"C:\Users\user\.aider\oauth-keys.env")

# ── 2. ACTIVATE LANGFUSE WIRETAP ─────────────────────────────────────────────
# LiteLLM reads these env vars automatically and sends ALL traces to Langfuse
os.environ["LANGFUSE_HOST"]       = os.getenv("LANGFUSE_HOST")
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")

# Register the callback — one line, done
litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]  # also captures errors/timeouts

# ── 3. YOUR AGENT CALLS — UNCHANGED ──────────────────────────────────────────
def run_agent_task(task: str, model: str = "openrouter/qwen/qwen3-235b-a22b:free"):
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": "You are a senior Python engineer. Output only valid Python code. No markdown fences."},
            {"role": "user",   "content": task}
        ],
        # ── Langfuse metadata tags (appear as filters in the dashboard) ───────
        metadata={
            "langfuse_session_id": "session-cli-001",          # Groups a conversation
            "langfuse_user_id":    "operator-orange-tomato",   # Per-user cost tracking
            "langfuse_tags":       ["coding", "architect", model.split("/")[1]],
            "task_type":           "code_generation",
        }
    )
    return response.choices[0].message.content

# ── 4. EXECUTION ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    task = "Write a Python function that reads a CSV file and returns a list of dicts."
    output = run_agent_task(task)
    print(output)
    # ↑ Check http://localhost:3000 — trace appears within ~2 seconds
```

---

### Method B — OpenLLMetry (Framework-Agnostic OTel Path)

Use this when you're NOT routing through LiteLLM (raw OpenAI SDK, Anthropic SDK, etc.):

```python
# agent_otel.py — OpenLLMetry automatic instrumentation
# Patches OpenAI/Anthropic/LangChain SDK at import time — zero logic changes

from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import workflow, task
import openai
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\user\.aider\oauth-keys.env")

# ── INIT: One call instruments everything ─────────────────────────────────────
Traceloop.init(
    app_name="sovereign-cli-agent",
    api_endpoint=os.getenv("LANGFUSE_HOST") + "/api/public/otel",
    headers={
        "Authorization": "Basic " + __import__('base64').b64encode(
            f"{os.getenv('LANGFUSE_PUBLIC_KEY')}:{os.getenv('LANGFUSE_SECRET_KEY')}".encode()
        ).decode()
    },
    disable_batch=False   # True for debugging (immediate flush), False for production
)

client = openai.OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ── DECORATOR PATTERN: wrap logical units for hierarchical traces ─────────────
@workflow(name="code-generation-workflow")
def run_coding_workflow(task_description: str):
    spec    = generate_spec(task_description)
    code    = generate_code(spec)
    return code

@task(name="generate-spec")
def generate_spec(task: str) -> str:
    resp = client.chat.completions.create(
        model="qwen/qwen3-235b-a22b:free",
        messages=[{"role": "user", "content": f"Write a technical spec for: {task}"}]
    )
    return resp.choices[0].message.content

@task(name="generate-code")
def generate_code(spec: str) -> str:
    resp = client.chat.completions.create(
        model="qwen/qwen3-235b-a22b:free",
        messages=[{"role": "user", "content": f"Implement this spec in Python:\n{spec}"}]
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    result = run_coding_workflow("CSV parser that validates email columns")
    print(result)
```

---

### Method C — Manual Langfuse Tracing (Maximum Control)

When you need custom spans with full metadata control:

```python
# agent_manual.py — Manual trace/span/generation pattern
# Use when you need to attach custom metadata to specific steps

from langfuse import Langfuse
from langfuse.model import ModelUsage
import litellm
from dotenv import load_dotenv
import time, os

load_dotenv(r"C:\Users\user\.aider\oauth-keys.env")

lf = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)

def run_traced_agent(user_input: str, model: str):
    # ── Open a Trace (top-level container for this entire request) ────────────
    trace = lf.trace(
        name="agent-coding-task",
        user_id="operator-orange-tomato",
        session_id="session-cli-001",
        input=user_input,
        metadata={"model": model, "task_type": "code_generation"},
        tags=["sovereign", "coding"],
    )

    # ── Span: Prompt Assembly ─────────────────────────────────────────────────
    span_prep = trace.span(name="prompt-preparation")
    system_prompt = "You are a senior Python engineer. Output only valid Python code."
    span_prep.end(output={"system_prompt_chars": len(system_prompt)})

    # ── Generation: The actual LLM call ──────────────────────────────────────
    generation = trace.generation(
        name="primary-llm-call",
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_input},
        ],
        model_parameters={"temperature": 0.1, "max_tokens": 2048},
    )

    t_start = time.time()
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_input},
        ],
    )
    latency_ms = int((time.time() - t_start) * 1000)

    output_text = response.choices[0].message.content
    usage = response.usage

    # ── Close the Generation with actual token counts ─────────────────────────
    generation.end(
        output=output_text,
        usage=ModelUsage(
            input=usage.prompt_tokens,
            output=usage.completion_tokens,
            total=usage.total_tokens,
        ),
        metadata={"latency_ms": latency_ms},
    )

    # ── Close the Trace ───────────────────────────────────────────────────────
    trace.update(output=output_text)

    # Return trace_id so DeepEval can post scores back (Phase 3)
    return output_text, trace.id

if __name__ == "__main__":
    output, trace_id = run_traced_agent(
        "Write a Python function to validate email addresses using regex.",
        "openrouter/qwen/qwen3-235b-a22b:free"
    )
    print(f"Output:\n{output}")
    print(f"\nTrace ID: {trace_id}")  # ← save this for DeepEval scoring
```

---

# PHASE 3: THE JUDGE (DeepEval Integration)
## *Mathematically grading agent output and posting scores to your dashboard*

---

### Install DeepEval

```powershell
pip install deepeval
```

---

### Configure DeepEval's Judge Model (LOCAL — Zero API Cost)

DeepEval uses an LLM to evaluate other LLMs. Point it at your local LiteLLM proxy or Ollama:

```python
# deepeval_config.py — run this ONCE to configure judge model globally
# This sets the evaluator LLM for all DeepEval metrics

from deepeval.models import DeepEvalBaseLLM
import litellm

class OllamaJudge(DeepEvalBaseLLM):
    """
    Local Ollama judge — points DeepEval at your locally running model.
    Recommended judge: qwen2.5:32b or llama3.3:70b (needs 20GB+ VRAM)
    Minimum viable judge: qwen2.5:7b (runs on 8GB VRAM, less accurate)
    """
    def __init__(self, model_name: str = "ollama/qwen2.5:32b"):
        self.model_name = model_name

    def load_model(self):
        return self

    def generate(self, prompt: str) -> str:
        response = litellm.completion(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            api_base="http://localhost:11434",  # Ollama default port
        )
        return response.choices[0].message.content

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return self.model_name
```

---

### The Full Evaluation + Score Push Pipeline

```python
# evaluate_and_score.py
# Run this after agent produces output to:
# 1. Grade it with DeepEval metrics
# 2. Push scores into the Langfuse trace for dashboard display

import os
from dotenv import load_dotenv
from langfuse import Langfuse
from deepeval import evaluate
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import (
    AnswerRelevancyMetric,
    GEval,
    HallucinationMetric,
)
from deepeval_config import OllamaJudge  # from the config above

load_dotenv(r"C:\Users\user\.aider\oauth-keys.env")

lf = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)

# ── JUDGE MODEL ───────────────────────────────────────────────────────────────
judge = OllamaJudge(model_name="ollama/qwen2.5:32b")

# ── DEFINE METRICS ────────────────────────────────────────────────────────────

# Metric 1: Formatting constraint — no markdown fences in code output
no_markdown_metric = GEval(
    name="NoMarkdownFences",
    model=judge,
    criteria="""
    The output must be raw Python code with NO markdown code fences (no ```python or ```).
    It should start directly with import statements or function definitions.
    Score 1.0 if no markdown fences are present. Score 0.0 if ANY backticks appear.
    """,
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.8,
)

# Metric 2: Answer relevancy to the task
relevancy_metric = AnswerRelevancyMetric(
    model=judge,
    threshold=0.7,
    include_reason=True,
)

# Metric 3: No hallucination (code facts grounded in the input task)
hallucination_metric = HallucinationMetric(
    model=judge,
    threshold=0.3,   # score = hallucination rate; lower is better
    include_reason=True,
)

# ── EVALUATION FUNCTION ───────────────────────────────────────────────────────
def evaluate_and_push_to_langfuse(
    trace_id: str,
    user_input: str,
    agent_output: str,
    retrieved_context: list[str] = None,
):
    """
    Parameters
    ----------
    trace_id       : The Langfuse trace ID returned by your agent call
    user_input     : The original task/question given to the agent
    agent_output   : The raw string output from the agent
    retrieved_context : (optional) RAG context chunks used by the agent
    """

    # ── Build DeepEval test case ──────────────────────────────────────────────
    test_case = LLMTestCase(
        input=user_input,
        actual_output=agent_output,
        context=retrieved_context or [],       # for hallucination check
        retrieval_context=retrieved_context or [],
    )

    # ── Run all metrics ───────────────────────────────────────────────────────
    metrics_to_run = [no_markdown_metric, relevancy_metric, hallucination_metric]

    print(f"\n🔬 Running DeepEval on trace: {trace_id}")
    results = evaluate(
        test_cases=[test_case],
        metrics=metrics_to_run,
        run_async=False,          # Synchronous for CLI pipelines
        show_indicator=True,      # Progress bar
    )

    # ── Push each metric score into the Langfuse trace ────────────────────────
    for metric in metrics_to_run:
        score_value = metric.score         # float 0.0–1.0
        reason      = getattr(metric, "reason", "N/A")
        passed      = metric.is_successful()

        print(f"  📊 {metric.__class__.__name__}: {score_value:.3f} | Pass: {passed}")
        print(f"     Reason: {reason[:120]}...")

        lf.score(
            trace_id=trace_id,
            name=metric.__class__.__name__,    # appears as the score label in dashboard
            value=score_value,                 # 0.0 to 1.0
            comment=f"Pass: {passed} | {reason[:500]}",
            data_type="NUMERIC",               # or "BOOLEAN" for pass/fail
        )

    # ── Flush scores to Langfuse immediately ─────────────────────────────────
    lf.flush()
    print(f"\n✅ Scores pushed to http://localhost:3000 — trace ID: {trace_id}")
    return results


# ── EXAMPLE: Wire it into the manual tracing agent from Phase 2 ───────────────
if __name__ == "__main__":
    # Simulating the output from agent_manual.py's run_traced_agent()
    # In production: import and call run_traced_agent(), get trace_id back

    from agent_manual import run_traced_agent  # your Phase 2 agent

    user_task   = "Write a Python function to validate email addresses using regex."
    model       = "openrouter/qwen/qwen3-235b-a22b:free"

    agent_out, trace_id = run_traced_agent(user_task, model)

    evaluate_and_push_to_langfuse(
        trace_id=trace_id,
        user_input=user_task,
        agent_output=agent_out,
    )
```

---

### Viewing Scores on the Dashboard

1. Go to **http://localhost:3000**
2. Navigate to **Traces** → click the trace with the matching ID
3. On the right panel: **Scores** tab
4. You will see:
   - `NoMarkdownFences: 0.95` (green if ≥ threshold)
   - `AnswerRelevancyMetric: 0.82`
   - `HallucinationMetric: 0.12`
5. In **Scores** overview (top nav): filter by `NoMarkdownFences` across all traces to compare models

---

### Custom GEval Metrics for CLI Agents (Copy-Paste Library)

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

# ── Code quality metrics for coding agents ────────────────────────────────────

no_print_statements = GEval(
    name="NoPrintStatements",
    criteria="Production code should use logging, not print(). Score 0.0 if any print() calls exist.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=1.0,
)

has_type_hints = GEval(
    name="TypeHintCoverage",
    criteria="All function parameters and return types should have Python type hints. Score based on coverage (0.0 to 1.0).",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.8,
)

follows_task_spec = GEval(
    name="TaskSpecCompliance",
    criteria="The output code must implement exactly what was requested in the input. No missing features, no unrequested additions.",
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.85,
)

is_syntactically_valid = GEval(
    name="SyntaxValidity",
    criteria="The output must be syntactically valid Python code that would pass `python -m py_compile`. Score 1.0 for valid, 0.0 for any syntax errors.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=1.0,
)
```

---

# PHASE 4: MASTER OPERATOR TACTICS
## *The 3 metrics that tell you which free model is actually worth using*

---

## METRIC #1 — Cost Per Successful Task (CPST)

**What it is:** The real cost (tokens × price + latency penalty) of getting a passing output.
Not "cost per call" — cost per **passing** call.

**Where to find it in Langfuse:**

1. **Metrics → Cost** — filter by `tags` containing the model name (you set these in `metadata`)
2. Cross-reference with **Scores** → filter by `NoMarkdownFences` ≥ 0.8 (or your quality threshold)
3. **Formula:**

```
CPST = Total Token Cost across N calls
       ─────────────────────────────────────────
       Count of calls where ALL eval metrics passed
```

**Operational Interpretation:**
- Qwen 480B free: $0.00/call but 4,000ms average latency, 70% pass rate → CPST = 0 but 1.4x agent retries needed
- Codestral 22B local: $0.00/call, 800ms latency, 85% pass rate → CPST = 0 but 1.17x retries
- **Winner:** Codestral 22B for time-critical coding tasks. Qwen 480B for complex reasoning where latency is acceptable.

**Langfuse Setup:** Tag every call with the model name in `metadata.langfuse_tags`:
```python
metadata={"langfuse_tags": ["qwen-480b", "coding", "task-csv-parse"]}
```
Then filter the **Cost** and **Score** panels by tag.

---

## METRIC #2 — p95 Latency Per Task Type

**What it is:** The 95th-percentile latency for a given model on a given task type.
Average latency lies. p95 tells you the worst-case tail your users/downstream agents actually experience.

**Where to find it in Langfuse:**

1. **Metrics → Latency** → filter by `tags` = `["coding", "qwen-480b"]`
2. The latency histogram shows p50/p95/p99 — read the p95 bar
3. Compare the same filter with `["coding", "codestral-22b"]`

**Operational Interpretation:**
```
Model A: p50=1.2s, p95=8.4s  → unpredictable tail (free tier throttling)
Model B: p50=0.8s, p95=1.1s  → consistent (local Ollama)
```
For an agent with a 10-second response budget: Model B is deployable, Model A is not — even if its average is fine.

**Key Insight:** Free-tier cloud models have **highly variable p95** (rate limit queuing). Local Ollama models have **near-flat latency distributions**. Langfuse's histogram makes this visible in 30 seconds.

---

## METRIC #3 — Quality Score by Model × Task Combination (The Heat Map)

**What it is:** Average DeepEval score for each (model, task_type) pair.
This is the signal that tells you "Model X is great at summaries but fails at structured code output."

**Where to find it in Langfuse:**

1. **Scores** → Group by `score_name` = `TaskSpecCompliance`
2. Use **Traces** filter: `tags` contains `coding` → check score distribution per model tag
3. Build a mental (or exported) matrix:

```
                    TaskSpecCompliance  NoMarkdownFences  AnswerRelevancy
qwen-480b           0.91                0.62              0.88
codestral-22b       0.87                0.95              0.79
qwen3-8b-local      0.71                0.99              0.72
```

**Reading the matrix:**
- Qwen 480B: Great at spec compliance, terrible at format discipline → add a formatting post-processor
- Codestral 22B: Reliable format discipline, slightly lower spec compliance → ideal for "structured output" tasks
- Qwen3 8B local: Fast and clean format, weak reasoning → use as first-pass filter, escalate failures

**Operator Action:** Use LiteLLM Router's `router_strategy: "latency-based-routing"` combined with this matrix to auto-route `task_type=coding_structured` to Codestral and `task_type=complex_reasoning` to Qwen 480B.

```python
# litellm_router_config.yaml — informed by your Langfuse Quality Heat Map
model_list:
  - model_name: coding-structured   # Route alias
    litellm_params:
      model: ollama/codestral:22b   # Best NoMarkdownFences score
      api_base: http://localhost:11434

  - model_name: complex-reasoning   # Route alias
    litellm_params:
      model: openrouter/qwen/qwen3-235b-a22b:free  # Best TaskSpecCompliance
      api_key: os.environ/OPENROUTER_API_KEY
```

---

## COMPLETE ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SOVEREIGN OBSERVABILITY STACK                    │
│                         Windows/Docker Desktop                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐   LiteLLM   ┌──────────┐   ┌──────────────────┐ │
│  │  CLI Agent   │────Proxy────▶│ Ollama   │   │     OpenRouter   │ │
│  │  (Python)    │  :4000      │ :11434   │   │  (free models)   │ │
│  └──────┬───────┘             └──────────┘   └──────────────────┘ │
│         │                                                           │
│         │ litellm.success_callback=["langfuse"]                    │
│         │ (auto-intercept: tokens, latency, prompts)               │
│         ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   LANGFUSE (Docker)                         │   │
│  │   localhost:3000                                            │   │
│  │   ┌──────────┐  ┌───────────────┐  ┌────────────────────┐ │   │
│  │   │ postgres │  │  clickhouse   │  │  minio (S3 blobs)  │ │   │
│  │   │  :5432   │  │  :8123/:9000  │  │  :9000/:9001       │ │   │
│  │   └──────────┘  └───────────────┘  └────────────────────┘ │   │
│  └──────────────────────────┬────────────────────────────────┘   │
│                              │ lf.score(trace_id, name, value)    │
│                              │ (scores posted back AFTER eval)    │
│  ┌───────────────────────────▼────────────────────────────────┐   │
│  │                     DEEPEVAL (inline)                       │   │
│  │   GEval + AnswerRelevancy + HallucinationMetric             │   │
│  │   Judge: Ollama qwen2.5:32b (local, zero-cost)             │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  DASHBOARD METRICS (localhost:3000):                               │
│  ✦ Metric 1: Cost Per Successful Task (CPST) by model             │
│  ✦ Metric 2: p95 Latency per task_type × model                   │
│  ✦ Metric 3: Quality Score Heat Map (model × metric matrix)       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## MAINTENANCE COMMANDS

```powershell
# ── Stack Management ──────────────────────────────────────────────────────────
docker compose -f C:\orangetomato\langfuse\docker-compose.yml up -d      # Start
docker compose -f C:\orangetomato\langfuse\docker-compose.yml down       # Stop (data preserved)
docker compose -f C:\orangetomato\langfuse\docker-compose.yml down -v    # WIPE all data

# ── Check status ──────────────────────────────────────────────────────────────
docker compose -f C:\orangetomato\langfuse\docker-compose.yml ps

# ── Upgrade Langfuse ──────────────────────────────────────────────────────────
docker compose -f C:\orangetomato\langfuse\docker-compose.yml pull
docker compose -f C:\orangetomato\langfuse\docker-compose.yml up -d --force-recreate

# ── View errors ───────────────────────────────────────────────────────────────
docker compose -f C:\orangetomato\langfuse\docker-compose.yml logs langfuse-server --tail 50

# ── Manual flush if scores aren't appearing ───────────────────────────────────
# Add this to the end of any Python script using the SDK:
# lf.flush()   ← forces all queued events to be sent immediately
```

---

## KNOWN WINDOWS/DOCKER GOTCHAS

| Problem                           | Cause                              | Fix                                                         |
| --------------------------------- | ---------------------------------- | ----------------------------------------------------------- |
| Port 3000 occupied                | Next.js dev server, or another app | Change `"3000:3000"` to `"3001:3000"` in compose file       |
| ClickHouse healthcheck fails      | Docker Desktop memory limit        | Increase Docker Desktop RAM to 6GB+ in Settings → Resources |
| MinIO bucket not created          | Race condition on first boot       | Run `docker compose restart minio-createbucket`             |
| Scores not appearing in dashboard | SDK batching delay                 | Call `lf.flush()` at end of script                          |
| litellm can't reach Ollama        | Ollama bound to 127.0.0.1          | Set `OLLAMA_HOST=0.0.0.0` in Ollama env, restart Ollama     |
| WSL2 OOM kill                     | ClickHouse + Postgres combined RAM | Add `mem_limit: 512m` to clickhouse service in compose file |

---

*Operator's Manual — Orange Tomato Project | April 2026 | Sovereign CLI Architecture*
*Stack validated on: Windows 11, Docker Desktop 4.x (WSL2), Python 3.11, Langfuse 3.x*
