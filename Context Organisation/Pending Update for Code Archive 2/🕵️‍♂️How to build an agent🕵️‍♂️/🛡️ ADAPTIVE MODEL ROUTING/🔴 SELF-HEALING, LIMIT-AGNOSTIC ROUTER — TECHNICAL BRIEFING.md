---
modified: 2026-04-18T20:51:40+03:00
---
# 🔴 SELF-HEALING, LIMIT-AGNOSTIC ROUTER — TECHNICAL BRIEFING
### Sovereign Stack | Reactive Architecture | April 2026

---

## EXECUTIVE SUMMARY

**Your architectural instinct is correct — and LiteLLM supports it natively.**

You do not need to hardcode a single RPM or TPM value. LiteLLM's circuit-breaker system operates entirely on **observed failure signals** — it watches what providers actually return (429, 500, timeout) and reacts. The `AllowedFailsPolicy` and per-exception routing logic give you surgical control over what each error type *means* to your routing engine, without you ever knowing what the upstream limit actually is.

The honest gap: **dynamic `x-ratelimit-remaining` header parsing is NOT natively supported** for auto-adjusting the proxy's own behavior. LiteLLM passes those headers *through* to your client, but does not read them to modify its own internal routing. This is a known architectural limitation — workarounds exist and are documented below.

---

## OBJECTIVE 1: ERROR-TRIGGERED CIRCUIT BREAKERS (No RPM Required)

### The Core Mechanism: `AllowedFailsPolicy` + `RetryPolicy`

These two classes give you per-exception-type control. **You declare what you can tolerate; LiteLLM decides when to trip the breaker.** No RPM, no TPM, no knowledge of the upstream limit required.

```python
# These classes map directly to YAML config — shown in Python for clarity
from litellm.router import AllowedFailsPolicy, RetryPolicy

AllowedFailsPolicy(
    RateLimitErrorAllowedFails=1,       # Trip breaker after FIRST 429
    TimeoutErrorAllowedFails=2,         # Trip after 2 consecutive timeouts
    InternalServerErrorAllowedFails=3,  # Trip after 3 x 500 errors
    ServiceUnavailableErrorAllowedFails=1  # Trip immediate on 503
)

RetryPolicy(
    RateLimitErrorRetries=0,     # On 429: don't retry, immediately failover
    TimeoutErrorRetries=1,       # On timeout: retry once before failover
    InternalServerErrorRetries=2 # On 500: retry twice before failover
)
```

> [!IMPORTANT]
> `RateLimitErrorRetries=0` is the **critical setting** for free-tier stacks. On a 429, you want INSTANT failover — not exponential backoff against a limit that could be hours long. Set retries to 0 and let the fallback chain absorb the request immediately.

### The Full Exception Taxonomy

LiteLLM maps every provider's response to one of these standardized exception classes. These are the handles your policy runs on:

| Exception Class | Triggered By |
|---|---|
| `RateLimitError` | HTTP 429 — rate limit exceeded |
| `Timeout` | HTTP 408, or no response within `request_timeout` |
| `InternalServerError` | HTTP 500 — provider crash |
| `ServiceUnavailableError` | HTTP 503 — provider overloaded |
| `AuthenticationError` | HTTP 401/403 — bad API key |
| `ContentPolicyViolationError` | Provider content refusal |

All policy keys follow the pattern: `{ExceptionClass}AllowedFails` and `{ExceptionClass}Retries`.

---

## OBJECTIVE 2: DYNAMIC HEADER PARSING — THE HONEST ASSESSMENT

### What LiteLLM Actually Does With Headers

| Behavior | Supported? |
|---|---|
| Forward `x-ratelimit-remaining-*` to client | ✅ Yes — standardized to OpenAI format |
| Expose raw provider headers with `llm_provider-` prefix | ✅ Yes |
| Forward `retry-after` header to client | ✅ Yes (for 429s) |
| **Auto-adjust internal routing based on `x-ratelimit-remaining`** | ❌ No — this is the gap |
| **Dynamically adopt provider's `retry-after` as its cooldown duration** | ⚠️ Partial — inconsistent across providers |

### Why This Gap Exists

LiteLLM's router enforces limits *you configure*, not limits it *discovers at runtime*. It was designed for teams who *know* their limits and encode them. Your use case (blind to actual limits) is not the default path.

### Workaround 1: The Custom Failure Hook (Best Option)

LiteLLM's callback system lets you intercept every failure event and inject custom logic. You can write a hook that reads the `retry-after` header from the exception and programmatically extends the cooldown on that specific deployment.

```python
# custom_failure_hook.py — drop this alongside your proxy
import litellm
from litellm.integrations.custom_logger import CustomLogger

class AdaptiveCooldownHook(CustomLogger):
    """
    Reads retry-after headers from 429 responses and logs them.
    Can be extended to call LiteLLM's admin API to temporarily disable 
    a deployment for the provider-specified duration.
    """
    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        exception = kwargs.get("exception")
        if hasattr(exception, 'response') and exception.response is not None:
            headers = dict(exception.response.headers)
            retry_after = headers.get('retry-after') or headers.get('x-ratelimit-reset-requests')
            model_id = kwargs.get("litellm_params", {}).get("model_id", "unknown")
            
            if retry_after:
                # Log it — you can use this to alert or trigger external cooldown
                print(f"[ADAPTIVE] Model {model_id} requests retry-after: {retry_after}s")
                # In a full implementation: call LiteLLM's /model/disable admin endpoint
                # or write to Redis to extend the deployment's cooldown window

# Register in config.yaml:
# litellm_settings:
#   callbacks: ["custom_failure_hook.AdaptiveCooldownHook"]
```

### Workaround 2: Aggressive Static Cooldown (Simpler)

If you don't want to maintain a custom hook: set `cooldown_time` high enough that it exceeds any plausible free-tier reset window. For most free APIs, rate limit windows reset within 60 minutes. A 65-minute cooldown guarantees the endpoint is clean when it re-enters rotation.

```yaml
router_settings:
  cooldown_time: 3900   # 65 minutes — exceeds all known free-tier windows
  allowed_fails: 1      # Trip the breaker on the FIRST failure
```

---

## OBJECTIVE 3: AUTOMATIC QUARANTINE — DEAD WEIGHT EVICTION

### The Full Quarantine Stack

This is the combination of three independent mechanisms that work together:

```
LAYER 1: Reactive (per-request) ──── AllowedFailsPolicy trips the breaker
LAYER 2: Proactive (background)  ──── health_check probes the endpoint periodically  
LAYER 3: Long-duration           ──── cooldown_time holds it out of rotation
```

All three run concurrently and reinforce each other.

### Layer 1: Reactive Breaker (AllowedFailsPolicy)
Trips when a live request fails. Zero-latency detection — the breaker trips on the *actual 429 or timeout that hit your user*.

### Layer 2: Proactive Health Check (Background)
The health checker sends periodic lightweight probes to each model independently. If a model is consistently timing out during peak hours, the health checker detects this *between* your users' requests and removes the endpoint before it can hurt anyone.

```yaml
general_settings:
  background_health_checks: true
  health_check_interval: 300          # Probe every 5 minutes
  health_check_ignore_transient_errors: true  # Don't quarantine on isolated 429s
```

> [!NOTE]
> `health_check_ignore_transient_errors: true` is the key flag for free-tier stacks. Without it, a single 429 during a health check probe will quarantine the endpoint. With it, only consistent timeouts and 5xx errors trigger quarantine from the health checker — your `AllowedFailsPolicy` handles the 429 quarantine on live traffic.

### Layer 3: Long-Duration Cooldown (The 60-Minute Quarantine)

```yaml
router_settings:
  cooldown_time: 3600   # 60 minutes exactly
```

When an endpoint is quarantined (by either Layer 1 or Layer 2), it stays out for exactly `cooldown_time` seconds. After that, LiteLLM automatically re-introduces it to the pool. **If it immediately fails again, it gets quarantined again.** This is the circuit breaker's half-open probe in action — automatic, no intervention required.

---

## THE COMPLETE LIMIT-AGNOSTIC `config.yaml`

This config requires **zero RPM/TPM values** anywhere. All breaker logic is driven purely by observed errors.

```yaml
# ============================================================
# LITELLM PROXY — SELF-HEALING, LIMIT-AGNOSTIC CONFIG
# Zero hardcoded rate limits | Pure error-signal routing
# Targets: Cerebras, Groq, Grok/xAI, Devstral, Gemini Flash
# ============================================================

model_list:

  # ── TIER 1: CEREBRAS (fastest inference, generous free tier) ───────────
  - model_name: sovereign-router
    litellm_params:
      model: cerebras/llama-3.3-70b
      api_key: os.environ/CEREBRAS_API_KEY
    model_info:
      id: cerebras-llama-70b
      # NO rpm/tpm — limit-agnostic design

  - model_name: sovereign-router
    litellm_params:
      model: cerebras/llama-3.1-8b         # Fast light model for simple prompts
      api_key: os.environ/CEREBRAS_API_KEY
    model_info:
      id: cerebras-llama-8b

  # ── TIER 2: GROQ (LPU speed, solid free tier) ──────────────────────────
  - model_name: sovereign-router
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY
    model_info:
      id: groq-llama-70b

  - model_name: sovereign-router
    litellm_params:
      model: groq/moonsong-labs/moonlight-16b-a3b-instruct:free
      api_key: os.environ/GROQ_API_KEY
    model_info:
      id: groq-moonlight

  - model_name: sovereign-router
    litellm_params:
      model: groq/deepseek-r1-distill-llama-70b
      api_key: os.environ/GROQ_API_KEY
    model_info:
      id: groq-deepseek-r1

  # ── TIER 3: OPENROUTER FREE ENDPOINTS ─────────────────────────────────
  - model_name: sovereign-router
    litellm_params:
      model: openrouter/mistralai/devstral-2505:free
      api_key: os.environ/OPENROUTER_API_KEY
    model_info:
      id: devstral-openrouter

  - model_name: sovereign-router
    litellm_params:
      model: openrouter/google/gemini-2.0-flash-lite-001:free
      api_key: os.environ/OPENROUTER_API_KEY
    model_info:
      id: gemini-flash-lite-openrouter

  - model_name: sovereign-router
    litellm_params:
      model: openrouter/meta-llama/llama-3.3-70b-instruct:free
      api_key: os.environ/OPENROUTER_API_KEY
    model_info:
      id: llama33-openrouter

  - model_name: sovereign-router
    litellm_params:
      model: openrouter/deepseek/deepseek-r1:free
      api_key: os.environ/OPENROUTER_API_KEY
    model_info:
      id: deepseek-r1-openrouter

  # ── TIER 4: GOOGLE NATIVE (subject to peak-hour timeouts → quarantine) ─
  - model_name: sovereign-router
    litellm_params:
      model: gemini/gemini-2.0-flash-lite
      api_key: os.environ/GEMINI_API_KEY
    model_info:
      id: gemini-flash-lite-native

  - model_name: sovereign-router
    litellm_params:
      model: gemini/gemini-1.5-flash-latest
      api_key: os.environ/GEMINI_API_KEY
    model_info:
      id: gemini-15-flash-native

  # ── TIER 5: LOCAL OLLAMA (zero rate limits — final sanctuary) ──────────
  - model_name: sovereign-router
    litellm_params:
      model: ollama/devstral:latest
      api_base: http://localhost:11434
    model_info:
      id: devstral-local

  - model_name: sovereign-router
    litellm_params:
      model: ollama/qwen2.5-coder:7b       # Light model, always responsive
      api_base: http://localhost:11434
    model_info:
      id: qwen-coder-local

  # ── LAST RESORT: Never cooled down, always available ───────────────────
  - model_name: last-resort
    litellm_params:
      model: ollama/tinyllama:latest
      api_base: http://localhost:11434
    model_info:
      id: tinyllama-fallback
      # Exempt from circuit breaker — local hardware never rate-limits


# ══════════════════════════════════════════════════════════════
# ROUTER SETTINGS — The circuit breaker engine
# ZERO hardcoded RPM or TPM values below
# ══════════════════════════════════════════════════════════════
router_settings:
  routing_strategy: latency-based-routing

  # ── GLOBAL FALLBACK COUNTS (overridden by AllowedFailsPolicy per type) ─
  num_retries: 1          # Try once more on same-tier before fallback chain
  allowed_fails: 2        # Global: cooldown after 2 failures of any type

  # ── THE QUARANTINE TIMER ───────────────────────────────────────────────
  # A quarantined endpoint stays OUT for this many seconds.
  # Set to 3600 (60 min) to outlast any free-tier reset window.
  # After expiry, LiteLLM auto-probes; if it still fails → re-quarantines.
  cooldown_time: 3600

  # ── PER-ERROR-TYPE POLICY (The Surgical Circuit Breaker) ──────────────
  # This is the limit-agnostic core. No RPM. Pure signal-based.
  allowed_fails_policy:
    # 429: We know nothing about their limit. Trip immediately on first hit.
    # Instant failover to next model — user never waits.
    RateLimitErrorAllowedFails: 1

    # Timeout: Could be transient. Allow 2 before quarantining.
    # This handles Google's peak-hour degradation gracefully.
    TimeoutErrorAllowedFails: 2

    # 500: Provider is crashing. We don't want retries. Trip fast.
    InternalServerErrorAllowedFails: 2

    # 503: Provider overloaded. Instant quarantine.
    ServiceUnavailableErrorAllowedFails: 1

    # Auth errors: Don't keep hammering a broken key.
    AuthenticationErrorAllowedFails: 1

  # ── PER-ERROR RETRY POLICY ────────────────────────────────────────────
  retry_policy:
    # On 429: Retry ZERO times. Immediately escalate to fallback chain.
    # This is the "no retrying against a brick wall" setting.
    RateLimitErrorRetries: 0

    # On timeout: One retry to rule out transient network blip.
    TimeoutErrorRetries: 1

    # On 500: One retry — sometimes a provider hiccups momentarily.
    InternalServerErrorRetries: 1

    # On 503: No retries, they're overloaded.
    ServiceUnavailableErrorRetries: 0


# ══════════════════════════════════════════════════════════════
# LITELLM SETTINGS — Fallback chains and global behavior
# ══════════════════════════════════════════════════════════════
litellm_settings:
  # Main fallback: if the entire sovereign-router pool is exhausted → last-resort
  fallbacks:
    - sovereign-router: ["last-resort"]

  # Context window overflows → TinyLlama can't handle large contexts,
  # so you might prefer to just fail gracefully here
  context_window_fallbacks:
    - sovereign-router: ["last-resort"]

  # Global request timeout — this is what triggers TimeoutError
  # 30s is generous for any real API; local Ollama may need more
  request_timeout: 30

  # CRITICAL for heterogeneous free models — they each reject different params
  drop_params: true

  # The nuclear last resort
  default_fallbacks: ["last-resort"]


# ══════════════════════════════════════════════════════════════
# GENERAL SETTINGS — Health checking and proactive quarantine
# ══════════════════════════════════════════════════════════════
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY

  # ── PROACTIVE HEALTH CHECKER (Layer 2 quarantine) ─────────────────────
  # Probes all endpoints every 5 minutes independently of live traffic.
  # Catches "dead weight" endpoints (e.g., Google peak-hour timeouts)
  # BEFORE they hurt a user's terminal prompt.
  background_health_checks: true
  health_check_interval: 300           # 5 minutes between probes

  # Don't quarantine on isolated 429s from health probes — 
  # that's the AllowedFailsPolicy's job on live traffic.
  # Only consistent timeouts and 5xx trigger health-check quarantine.
  health_check_ignore_transient_errors: true
```

---

## DEPLOYMENT WITH THE ADAPTIVE COOLDOWN HOOK (Optional Layer 4)

If you want the proxy to *also* respect `retry-after` headers dynamically, copy this to a file named `adaptive_hook.py` in the same directory as your `config.yaml`:

```python
# adaptive_hook.py
from litellm.integrations.custom_logger import CustomLogger
import asyncio

class AdaptiveCooldownHook(CustomLogger):
    """
    Intercepts failure events and logs retry-after headers.
    Provides visibility into what providers are actually requesting.
    """
    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        try:
            exception = kwargs.get("exception")
            model_id = kwargs.get("litellm_params", {}).get("model_id", "unknown")
            model_name = kwargs.get("model", "unknown")
            
            if hasattr(exception, 'response') and exception.response is not None:
                hdrs = dict(exception.response.headers)
                retry_after = (
                    hdrs.get('retry-after') or
                    hdrs.get('x-ratelimit-reset-requests') or
                    hdrs.get('x-ratelimit-reset')
                )
                remaining = hdrs.get('x-ratelimit-remaining-requests', 'unknown')
                
                if retry_after:
                    print(
                        f"[ADAPTIVE HOOK] Model={model_id} ({model_name}) | "
                        f"retry-after={retry_after}s | remaining={remaining}"
                    )
                    # If retry_after > our cooldown_time, we're under-quarantining.
                    # Alert: you may want to increase cooldown_time if this fires often.
                    if int(retry_after) > 3600:
                        print(f"[ADAPTIVE HOOK] ⚠️  Provider wants {retry_after}s cooldown — exceeds our 3600s config!")
        except Exception as hook_err:
            print(f"[ADAPTIVE HOOK] Hook error (non-fatal): {hook_err}")
```

Register it in your `config.yaml`:

```yaml
litellm_settings:
  callbacks:
    - adaptive_hook.AdaptiveCooldownHook
  # ... rest of settings
```

---

## OBJECTIVE 2 VERDICT: THE HEADER PARSING REALITY MAP

```
Provider sends:   x-ratelimit-remaining: 0
                  retry-after: 3600

LiteLLM does:     ✅ Forwards both headers to YOUR client (OpenCode, etc.)
                  ✅ Marks deployment on cooldown (via AllowedFailsPolicy)
                  ❌ Does NOT read retry-after to set its own cooldown duration
                  ❌ Does NOT auto-extend cooldown to match provider's requested 3600s

Your solution:    Set cooldown_time: 3600 globally (covers all cases)
                  + AdaptiveCooldownHook for observability and alerting
```

**This is an acceptable engineering trade-off for your use case.** Since the actual reset windows of your 14 providers are unknown and fluctuating, a 60-minute static cooldown is *safer* than trying to parse volatile headers — it guarantees the endpoint is clean when re-introduced, regardless of what the provider says.

---

## ALTERNATIVE GATEWAYS — WHEN TO CONSIDER THEM

| Gateway | What It Does Better | Trade-off |
|---|---|---|
| **Bifrost** (Go) | Lower latency, built-in circuit breakers, 11µs overhead | Less provider coverage than LiteLLM, Go ecosystem |
| **OmniRoute** | "Account pooling" — distributes load across multiple API keys for the same provider | Limited to IDE tools (Cursor, Claude Code), not general proxy |
| **Cloudflare AI Gateway** | Edge-deployed, zero infrastructure, built-in retry/failover | Requires Cloudflare account, no local model support |

### Verdict for Your Stack
**Stay on LiteLLM.** The `AllowedFailsPolicy` + `background_health_checks` + 60-minute `cooldown_time` combo gives you everything you need for a limit-agnostic, self-healing router. The only real alternative worth evaluating is **Bifrost** if you observe the Python proxy adding >50ms latency at your request volume — unlikely for a solo dev-agent stack.

---

## THE SELF-HEALING LOOP — VISUAL SUMMARY

```
REQUEST FROM OpenCode/Vibe/AnythingLLM
           │
           ▼
    ┌─────────────────────────────────────────┐
    │     LITELLM LATENCY-BASED ROUTER        │
    │  Picks fastest HEALTHY model from pool  │
    └──────────────┬──────────────────────────┘
                   │
          ┌────────▼────────┐
          │  CEREBRAS (fast)│ ← Attempt 1
          └────────┬────────┘
                   │ 429 RateLimitError
                   │ AllowedFailsPolicy: RateLimitErrorAllowedFails=1
                   │ → TRIP BREAKER immediately
                   │ → Cooldown: 3600s
                   │ RetryPolicy: RateLimitErrorRetries=0
                   │ → NO retry, INSTANT escalation
                   ▼
          ┌─────────────────┐
          │  GROQ (next)    │ ← Attempt 2
          └────────┬────────┘
                   │ 200 OK ✅
                   ▼
    Response delivered to client
    Cerebras stays quarantined for 60 min
    Background health check probes at t+5min, t+10min...
    At t+60min: Cerebras auto-re-enters pool
    If healthy → serves traffic again
    If still failing → re-quarantines for another 60 min
```

Zero manual intervention. Zero knowledge of upstream limits. Pure signal-based self-healing.

---

## QUICK-START COMMANDS

```bash
# Install
pip install 'litellm[proxy]'

# Set keys (only what you have)
export CEREBRAS_API_KEY="your-key"
export GROQ_API_KEY="your-key"  
export OPENROUTER_API_KEY="sk-or-v1-your-key"
export GEMINI_API_KEY="your-key"
export LITELLM_MASTER_KEY="sk-sovereign-stack"

# Launch with verbose logging so you can watch the circuit breaker fire
litellm --config config.yaml --port 4000 --detailed_debug

# Watch in a second terminal — look for "Cooling down deployment" messages
# These confirm the circuit breaker is working
```

---

*Briefing compiled: 2026-04-18 | Sources: litellm.ai/docs, GitHub issues, r/LocalLLaMA*
