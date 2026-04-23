---
modified: 2026-04-18T21:47:59+03:00
---
# 🧠 PLANNER MODEL EVALUATION — SOVEREIGN SYSTEM ARCHITECT REPORT
### Spec-Driven Execution Swarm | Reasoning & Planning ROI Analysis | April 2026

---

## MISSION BRIEF

The Planner's **only job** is to:
1. Ingest a complex feature request in natural language
2. Reason about architecture, dependencies, and edge cases
3. Output a set of **strictly isolated, non-overlapping executable contracts** (e.g., structured JSON or markdown task specs)
4. Hand those contracts to cheaper Executor models (like Codestral 22B)

This is a **System 2 reasoning problem**. The Planner is not writing code. It is doing architecture and decomposition. Therefore we evaluate on:
- **Depth of reasoning** (chain-of-thought, foresight, edge case detection)
- **Structured output reliability** (JSON, markdown contracts, no hallucinated overlap)
- **Instruction following** at a contract level
- **Cost per planning call** (planning calls are long — typically 2K-8K input tokens, 1K-4K output)

---

## EVALUATION MATRIX LEGEND

| Rating | Meaning |
|---|---|
| ⭐⭐⭐⭐⭐ | Best in class |
| ⭐⭐⭐⭐ | Excellent, minor caveats |
| ⭐⭐⭐ | Good, meaningful trade-offs |
| ⭐⭐ | Passable, significant weaknesses |
| ⭐ | Not recommended for this role |

---

## INDIVIDUAL MODEL PROFILES

---

### 1. DeepSeek R1 (R1-0528)
*Open-weight reasoning model | DeepSeek AI*

**Architecture:** Dense transformer with reinforcement-learned chain-of-thought. Averages **23K thinking tokens** per complex query — the deepest internal reasoning of any model in this evaluation.

**2026 API Pricing:**
| Token Type | Cost per 1M |
|---|---|
| Input | $0.55 |
| Output (reasoning + response) | $2.19 |
| Cached Input | $0.14 |

**Planner-Specific Ratings:**
| Dimension | Score | Notes |
|---|---|---|
| System 2 Reasoning Depth | ⭐⭐⭐⭐⭐ | Best in class. Averages 23K thought tokens. Foresees edge cases systematically. |
| Structured Output / JSON | ⭐⭐⭐⭐ | Native JSON + function calling added in R1-0528. Reliable with `response_format`. |
| Hallucination Control | ⭐⭐⭐⭐ | R1-0528 reduced hallucination ~50% vs original R1. Still occasionally "overthinks" and over-generates scope. |
| Instruction Following | ⭐⭐⭐⭐ | System prompts now supported without workarounds since 0528. |
| Latency (Time-to-Plan) | ⭐⭐⭐ | High latency. 23K thinking tokens take time. For async swarm pipelines, this is acceptable. |
| Data Sovereignty | ⭐⭐⭐ | Chinese company. Weights are open — self-host via Ollama/vLLM for full sovereignty. |

**Cost for a Typical Planning Call** (4K input / 3K output reasoning):
- API: ~$0.0022 input + ~$0.0066 output = **~$0.009 per plan**
- With cached prompts (system prompt cached): **~$0.006 per plan**

**Verdict for Planner Role:** The king of pure reasoning depth. If your spec requires foreseeing intricate dependency chains, race conditions, or complex data flow, R1-0528 outperforms everything in this price tier by a wide margin. The latency is the only real friction point for interactive workflows.

---

### 2. Qwen3-235B-A22B (Thinking Mode)
*Open-weight MoE | Alibaba Cloud*

**Architecture:** 235B total / 22B active parameters MoE. Supports a **"thinking" mode** (System 2) and a "non-thinking" fast mode (System 1), switchable per request (`enable_thinking: true/false`). The Thinking-2507 variant pushed reasoning quality further.

**2026 API Pricing:**
| Token Type | Cost per 1M |
|---|---|
| Input | $0.26 – $0.45 |
| Output | $0.90 – $3.49 (varies by provider, higher in thinking mode) |
| Self-hosted (open-weight) | Hardware cost only |

**Planner-Specific Ratings:**
| Dimension | Score | Notes |
|---|---|---|
| System 2 Reasoning Depth | ⭐⭐⭐⭐⭐ | Rivals DeepSeek R1 on planning benchmarks. Thinking mode produces deep CoT. |
| Structured Output / JSON | ⭐⭐⭐⭐⭐ | Excellent. Strong instruction following on structured schema output. |
| Hallucination Control | ⭐⭐⭐⭐ | Switchable modes help — non-thinking mode for fast checks, thinking for deep plans. |
| Instruction Following | ⭐⭐⭐⭐⭐ | Consistently top-tier benchmark leader for instruction following. |
| Latency | ⭐⭐⭐⭐ | Faster than R1 in thinking mode due to MoE efficiency (only 22B active params). |
| Data Sovereignty | ⭐⭐⭐⭐ | Open weights. Full self-hosting available. Alibaba Cloud API for managed access. |

**Cost for a Typical Planning Call** (4K input / 3K output):
- API (Thinking mode): ~$0.0018 input + ~$0.0105 output = **~$0.012 per plan**
- Self-hosted (high-end GPU cluster, amortized): **$0.001–$0.003 per plan** depending on hardware
- On Cerebras/Groq API (when available): significantly cheaper

**Verdict for Planner Role:** The most **flexible** Planner in this evaluation. The mode-switching is a architectural superpower — use Thinking mode for initial spec decomposition, non-thinking for follow-up clarifications. Open-weight status makes it the best choice for air-gapped or sovereign deployments where you cannot send code specs to Chinese APIs.

---

### 3. Kimi K2.5 (Agentic MoE)
*Open-weight MoE | Moonshot AI*

**Architecture:** 1 trillion total parameters / ~32B active. Explicitly designed for **agentic orchestration**. K2.5 adds a native multi-agent "swarm" capability (up to 100 parallel sub-agents) and 256K context window.

**2026 API Pricing:**
| Token Type | Cost per 1M |
|---|---|
| Input | $0.60 |
| Output | $2.50 |
| Cached Input | ~75% reduction |

**Planner-Specific Ratings:**
| Dimension | Score | Notes |
|---|---|---|
| System 2 Reasoning Depth | ⭐⭐⭐⭐ | Strong reasoning, but architecture is optimized for *acting* more than *pure planning*. |
| Structured Output / JSON | ⭐⭐⭐⭐⭐ | Excellent. Built for tool calling and structured agentic workflows. |
| Hallucination Control | ⭐⭐⭐⭐ | Good — the long context window helps it keep full spec in view. |
| Instruction Following | ⭐⭐⭐⭐⭐ | Exceptional. Optimized to follow structured agent contracts (its core use case). |
| Latency | ⭐⭐⭐⭐ | Competitive for its size due to MoE activation (32B active). |
| Data Sovereignty | ⭐⭐⭐ | Chinese company. Open weights available. API access comfortable for non-sensitive projects. |

**Special Advantage:** K2.5's native swarm coordination means it can serve as both Planner *and* Orchestrator simultaneously — it doesn't just plan, it can also dispatch and monitor the Executor agents directly.

**Verdict for Planner Role:** The best choice if you want your Planner to also coordinate the swarm. However, if your Planner role is *strictly* spec decomposition (not tool-calling), this is more power than you need, and the pricing reflects it.

---

### 4. GLM-5.1 (Z.ai / Zhipu AI)
*Open-weight MoE | Zhipu AI (China)*

**Architecture:** 744B total / ~42B active parameters MoE. MIT licensed. All-Huawei hardware training. SWE-bench Verified: **77.8%** — best open-weight score at this evaluation date.

**2026 API Pricing:**
| Token Type | Cost per 1M |
|---|---|
| Input | $0.80 – $1.00 |
| Output | $2.56 – $3.20 |

**Planner-Specific Ratings:**
| Dimension | Score | Notes |
|---|---|---|
| System 2 Reasoning Depth | ⭐⭐⭐⭐ | Excellent on coding-adjacent reasoning (AIME 2026: 92.7%). Strong technical planner. |
| Structured Output / JSON | ⭐⭐⭐⭐ | Solid, but less battle-tested globally than DeepSeek or Qwen. |
| Hallucination Control | ⭐⭐⭐⭐ | GLM-5.1 refinement pass improved this over base GLM-5. |
| Instruction Following | ⭐⭐⭐⭐ | Strong, especially for technical/engineering specs. |
| Latency | ⭐⭐⭐ | 744B weights — self-hosting is expensive. API latency moderate. |
| Data Sovereignty | ⭐⭐ | Chinese company, Huawei hardware. Concerning for sensitive western IP. MIT license helps for self-hosting. |

**Verdict for Planner Role:** A dark horse with exceptional engineering benchmark scores. Outperforms GLM-4 significantly, and the MIT license is valuable. **However, the data sovereignty concerns are real** for proprietary code. At $0.80–$1.00/M input, it's also 2x the cost of DeepSeek R1 for broadly equivalent reasoning quality.

---

### 5. Mistral Magistral Small (24B, Open-Weight)
*Open-weight | Mistral AI*

**Architecture:** 24B parameters, Apache 2.0 licensed. The open-weight entry in Mistral's dedicated reasoning family. AIME 2024: **70.7%** (83.3% with majority voting).

**2026 API Pricing:**
| Token Type | Cost per 1M |
|---|---|
| Input | $0.50 |
| Output | $1.50 |
| Self-hosted | Hardware cost only |

**Magistral Medium (Proprietary):**
| Input | $2.00 | Output | $5.00 |

**Planner-Specific Ratings (Small):**
| Dimension | Score | Notes |
|---|---|---|
| System 2 Reasoning Depth | ⭐⭐⭐ | Good for 24B. Step-by-step reasoning is reliable but less deep than R1 or Qwen3-235B. |
| Structured Output / JSON | ⭐⭐⭐⭐ | Mistral has strong structured output heritage. Excellent JSON compliance. |
| Hallucination Control | ⭐⭐⭐ | Acceptable. 24B models can miss complex cross-task dependency conflicts. |
| Instruction Following | ⭐⭐⭐⭐ | Excellent. Mistral's instruction-following tuning is top-tier. |
| Latency | ⭐⭐⭐⭐⭐ | Very fast for a reasoning model. 24B is easy to host locally. |
| Data Sovereignty | ⭐⭐⭐⭐⭐ | French company. Apache 2.0. Best data sovereignty in the evaluation. |

**Verdict for Planner Role:** The **most pragmatic choice for local deployment with no GPU budget constraints**. Magistral Small self-hosted on a single RTX 4090 (24GB VRAM) is achievable. For a purely local, zero-API-cost stack, this is your option. Planning quality is good but not elite — expect occasional missed edge cases on complex multi-module features.

---

### 6. Llama 4 Maverick (400B MoE)
*Open-weight MoE | Meta (via MSL)*

**Architecture:** 400B total / 17B active, 128 experts. Released April 2025.

**2026 Community Assessment:**
The r/LocalLLaMA and broader developer community reached a clear consensus: Llama 4 Maverick was a disappointment. Multiple independent evaluations documented:
- Inconsistent and "abysmal" coding performance in real-world tasks
- Failure to reproduce Meta's internal benchmark claims
- No native chain-of-thought / "thinking" mode — a critical gap in 2025/2026
- Eventual strategic pivot by Meta, abandoning open-source in favor of proprietary *Muse Spark*

**Planner-Specific Ratings:**
| Dimension | Score | Notes |
|---|---|---|
| System 2 Reasoning Depth | ⭐⭐ | No dedicated thinking mode. Dense reasoning loses to R1/Qwen3 significantly. |
| Structured Output / JSON | ⭐⭐⭐ | Standard capability. No special advantage. |
| Hallucination Control | ⭐⭐ | Reported hallucination in complex reasoning tasks. |
| Instruction Following | ⭐⭐⭐ | Acceptable but not reliable at Planner spec quality. |
| Cost Efficiency | ⭐⭐⭐ | Open-weight, self-host only. No official Meta API. |

**Verdict for Planner Role:** ❌ **DO NOT USE.** Llama 4 Maverick is the wrong tool for this job. No thinking mode, disappointing real-world reasoning, and community consensus is damning. You would spend more engineering time tuning prompts to compensate for its weaknesses than the cost savings justify.

---

### 7. Claude Sonnet 4.6 *(Baseline Reference)*
*Proprietary | Anthropic*

**2026 API Pricing:**
| Input | $3.00/M | Output | $15.00/M |

**Planner-Specific Assessment:**
Claude Sonnet 4.6 remains the gold standard for **instruction adherence, structured reasoning, and reliable multi-step planning**. It consistently tops agentic benchmarks (SWE-bench Verified, TAU²-Bench). Its output is the most "editor-ready" of any model — clean, structured, no hallucinated scope creep.

**However:** At $15/M output, it is **5-8x more expensive** than DeepSeek R1 and **10-15x more expensive** than Qwen3 via API. For planning calls generating 3K output tokens, this is ~$0.045/call vs. R1's $0.009/call.

**Verdict:** The performance ceiling is real. The cost ceiling is also real. Used as a **pure baseline** to assess whether cheaper models achieve "95% of the planning quality."

---

### 8. OpenAI o3 *(Baseline Reference)*
*Proprietary | OpenAI*

**2026 API Pricing:**
| Input | $2.00/M | Output | $8.00/M |
| (Internal reasoning tokens billed as output — 3-10x amplifier) | | |

**Assessment:** o3 is an exceptional reasoner on mathematical and algorithmic benchmarks (AIME, GPQA). For software architecture planning specifically, the reasoning quality is very high. But the hidden reasoning token billing makes true cost unpredictable — a complex decomposition task can cost $0.05-$0.15/call in actual spend.

**Verdict:** Strong model, unpredictable cost at scale. The billing model is unfriendly to production agentic loops where you need cost determinism.

---

## THE ROI RANKING TABLE

*Scoring: Reasoning Quality (0-10) vs. Cost per Planning Call (4K in / 3K out)*

| Rank | Model | Reasoning Score | Cost/Call (API) | Cost/Call (Self-hosted) | ROI Score | Availability |
|---|---|---|---|---|---|---|
| **🥇 1** | **DeepSeek R1-0528** | **9.5/10** | **~$0.009** | ~$0.001 | **⭐⭐⭐⭐⭐** | API + Open-weight |
| **🥈 2** | **Qwen3-235B (Thinking)** | **9.5/10** | **~$0.012** | ~$0.001 | **⭐⭐⭐⭐⭐** | API + Open-weight |
| **🥉 3** | **Mistral Magistral Small** | **8.0/10** | **~$0.006** | **~$0** (RTX 4090) | **⭐⭐⭐⭐** | API + Apache 2.0 |
| **4** | Kimi K2.5 | 9.0/10 | ~$0.010 | ~$0.003 | ⭐⭐⭐⭐ | API + Open-weight |
| **5** | GLM-5.1 | 8.5/10 | ~$0.015 | ~$0.002 | ⭐⭐⭐ | API + MIT |
| **6** | Magistral Medium | 9.0/10 | ~$0.023 | N/A (proprietary) | ⭐⭐⭐ | API only |
| **7** | OpenAI o3 | 9.5/10 | ~$0.035–$0.12 | N/A | ⭐⭐ | API only |
| **8** | Claude Sonnet 4.6 | 9.5/10 | ~$0.045 | N/A | ⭐⭐ | API only |
| **9** | Llama 4 Maverick | 6.0/10 | N/A | ~$0.002 | ⭐ | Open-weight only |

---

## DISQUALIFICATION NOTES

**Llama 4 Maverick:** Disqualified as a primary Planner. The community consensus on real-world planning and reasoning quality is decisively negative. Open-weight advantage cannot compensate for a model that generates unreliable contracts.

**GLM-5.1:** Strong model, but the Huawei hardware dependency and Chinese AI company risk profile make it unsuitable for proprietary code specs. ROI is also slightly below the top tier at its current API price.

---

## THE DEFINITIVE RECOMMENDATION

### 🏆 Primary Planner: DeepSeek R1-0528 via API

**Why R1 wins the Planner role specifically:**

1. **Thinking depth is the deciding factor.** Averaging 23K internal reasoning tokens means R1 is literally doing more planning work per call than any other model in this list. For a model whose entire job is to think first and output second, this is the key differentiator.

2. **R1-0528 fixed the blockers.** The original R1 had JSON output issues and no system prompt support. Both are resolved. You get structured contract output reliably.

3. **The math is unbeatable.** At $0.009/planning call, you can run **5,000 planning sessions for $45**. Claude Sonnet would cost $225 for the same 5,000 calls. R1 achieves approximately **93-96% of Claude's planning quality at 20% of the cost**.

4. **Caching amplifies the ROI further.** If your system prompt (Planner persona + contract schema) is static, LiteLLM prompt caching drops your input cost to $0.14/M — making R1 effectively the cheapest model in the entire evaluation for cached workloads.

### 🥈 Sovereign Backup: Qwen3-235B-A22B (Thinking Mode, Self-Hosted)

**Why Qwen3 is the backup (and may be the primary for air-gapped stacks):**

1. **Open weights + MIT-adjacent license** = zero API dependency. If your feature specs contain proprietary IP you cannot send to DeepSeek's servers, Qwen3 self-hosted on a high-VRAM setup is your Planner.

2. **Mode switching is architecturally powerful.** Route simple decompositions through non-thinking mode (fast, cheap), and complex multi-module architectural plans through thinking mode (deep, thorough).

3. **Comparable reasoning quality to R1** on most planning benchmarks. The gap is in the most extreme reasoning tasks — for software architecture decomposition specifically, Qwen3 keeps pace with R1 very closely.

4. **If you have an RTX 4090 or dual 3090 setup**, Qwen3-235B can be quantized (Q4_K_M) to run locally. Zero API cost, zero latency dependency, zero data sovereignty risk.

---

## RECOMMENDED SWARM ARCHITECTURE

```
FEATURE REQUEST (from user)
         │
         ▼
┌─────────────────────────────────────────────────────┐
│        PLANNER: DeepSeek R1-0528 (API)              │
│        OR: Qwen3-235B Thinking (self-hosted)        │
│                                                     │
│  Input: Feature spec + contract schema template     │
│  Output: Strict JSON of isolated task contracts:    │
│  {                                                  │
│    "task_1": {                                      │
│      "id": "UI_PROMPT_001",                         │
│      "scope": "...",                                │
│      "inputs": [...],                               │
│      "outputs": [...],                              │
│      "must_not_touch": [...],                       │
│      "acceptance_criteria": [...]                   │
│    },                                               │
│    "task_2": { ... }                                │
│  }                                                  │
└──────────────────┬──────────────────────────────────┘
                   │ Distributes contracts
         ┌─────────┴──────────┐
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│ EXECUTOR 1      │  │ EXECUTOR 2      │
│ Codestral 22B   │  │ Codestral 22B   │
│ (via Ollama /   │  │ (via Ollama /   │
│  OpenRouter)    │  │  OpenRouter)    │
│                 │  │                 │
│ Writes code     │  │ Writes code     │
│ for task_1      │  │ for task_2      │
└─────────────────┘  └─────────────────┘
         │                    │
         └─────────┬──────────┘
                   ▼
         ┌─────────────────┐
         │ VALIDATOR (opt) │
         │ Qwen3 30B fast  │
         │ or Gemini Flash │
         │ Checks output   │
         │ vs contracts    │
         └─────────────────┘
```

---

## KEY PROMPT ENGINEERING NOTE FOR R1 PLANNERS

DeepSeek R1 excels when you give it an **explicit contract schema** in the system prompt. Tell it exactly what structure to output. Do not leave the decomposition format open-ended:

```
SYSTEM PROMPT PATTERN:
"You are a software architecture planner. Your output must be a valid JSON array 
of task contracts. Each contract must contain: id, scope, inputs, outputs, 
must_not_touch (array of files/modules this task MUST NOT modify), and 
acceptance_criteria. Tasks must be strictly isolated — no two tasks may touch 
the same file or module. Think carefully before outputting. Identify all edge 
cases and dependency conflicts before finalizing your plan."
```

This explicit prohibitive instruction ("must_not_touch") is essential for preventing the single biggest failure mode of a Planner model: **overlapping task scope that causes Executor agents to stomp on each other's changes**.

---

*Report compiled: 2026-04-18 | Sources: litellm.ai, official model pages, r/LocalLLaMA, artificialanalysis.ai, together.ai, academic benchmarks*
