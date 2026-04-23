---
modified: 2026-04-19T18:07:41+03:00
---
**The answer is Arize Phoenix.** Pure Python, SQLite backend, built-in UI, zero Docker. RAM footprint: ~120MB.

---

## Install

```powershell
pip install arize-phoenix openinference-instrumentation-litellm opentelemetry-sdk
```

---

## The 2 Lines

Add these **at the top** of your agent script, before any LiteLLM calls:

```python
import phoenix as px; px.launch_app()
from openinference.instrumentation.litellm import LiteLLMInstrumentor; LiteLLMInstrumentor().instrument()
```

That's it. Phoenix auto-starts its UI on **http://localhost:6006** and LiteLLMInstrumentor patches every outbound call — OpenRouter, Google, any remote API — capturing prompt, completion, token counts, and latency with zero further code changes.

---

## Minimal Working Example

```python
# sovereign_agent.py
import phoenix as px; px.launch_app()
from openinference.instrumentation.litellm import LiteLLMInstrumentor; LiteLLMInstrumentor().instrument()

import litellm, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\user\.aider\oauth-keys.env")

response = litellm.completion(
    model="openrouter/qwen/qwen3-235b-a22b:free",
    messages=[{"role": "user", "content": "Write a Python hello world."}],
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
print(response.choices[0].message.content)
# → Open http://localhost:6006 and the trace is already there
```

---

## What You Get at localhost:6006

| Column | What it shows |
|---|---|
| **Latency** | ms from request to first token |
| **Total Tokens** | prompt + completion, per call |
| **Model** | the exact model string used |
| **Input / Output** | full prompt and completion text |
| **Status** | OK / ERROR (captures timeouts too) |

---

## Persistence (optional, one extra line)

By default Phoenix stores traces in-memory (lost on restart). To persist to SQLite:

```python
import phoenix as px
px.launch_app(backend="sqlite", db_path="C:/orangetomato/traces.db")
```

No RAM overhead change — SQLite writes to disk, not RAM.

---

**RAM budget:** Phoenix ≈ 120MB. Your remaining 15.88GB is untouched.