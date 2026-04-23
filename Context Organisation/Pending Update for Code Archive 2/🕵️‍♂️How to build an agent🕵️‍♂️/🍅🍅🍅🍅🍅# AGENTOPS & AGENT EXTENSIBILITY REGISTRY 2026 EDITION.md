---
modified: 2026-04-19T16:26:51+03:00
---
# AGENTOPS & AGENT EXTENSIBILITY REGISTRY — 2026 EDITION
### Classification: ORANGE TOMATO | Sovereign CLI Architecture

> **Architect's Note:** This registry maps every viable tool across the production AI agent lifecycle as of April 2026. Tools are evaluated against the Orange Tomato criteria: **Self-hostable (S)**, **API-first (A)**, **Scalable (Sc)**. A `✅` = fully sovereign, `⚠️` = partial/hybrid, `❌` = SaaS trap.

---

## ZONE 1 — OBSERVABILITY, TRACING & ANALYTICS
### *"The X-Ray Vision" — Tools that give you eyes inside the black box*

---

### 1.1 | Langfuse
**Category:** Observability / Full-Stack LLM Engineering Platform
**GitHub:** `langfuse/langfuse` | License: MIT (core) + Commercial

**Core Mechanism:**
Langfuse wraps your LLM calls via SDK (Python/JS) using a decorator or context manager pattern. Every call, tool invocation, retrieval, and agent step is captured as a **Trace → Span → Generation** hierarchy stored in PostgreSQL (metadata) and optionally ClickHouse (analytics). It provides a UI for trace inspection, prompt versioning, cost dashboards, and manual/LLM-as-judge evaluation runs. Integrates natively with LangChain, LlamaIndex, and raw OpenAI SDK via one-line decoration.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Docker Compose self-host: `docker compose up` — ships a pre-built stack (Next.js app + PostgreSQL + ClickHouse + MinIO for blob data)
- Zero data egress when self-hosted
- Production resource floor: 4GB RAM, 20GB+ storage for meaningful trace volumes
- Managed cloud available if you want speed-to-market, then migrate

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — The **#1 recommended observability layer** for sovereign stacks. Most complete open-source offering in the category.

---

### 1.2 | Arize Phoenix
**Category:** Observability / OpenTelemetry-Native ML+LLM Monitoring
**GitHub:** `Arize-ai/phoenix` | License: Apache 2.0

**Core Mechanism:**
Phoenix is built on **OpenTelemetry (OTel)** from the ground up — this is its defining architectural advantage. Every trace emitted by your agent is a standard OTel span, meaning it integrates into any existing APM stack (Grafana, Jaeger, Datadog). Uses embedding-based **cluster visualization** to detect hallucination drift patterns and RAG quality degradation over time. Beyond simple logging, Phoenix can run embedding drift detection — comparing production embeddings to your training distribution to flag when your RAG retrieval is silently degrading.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- `pip install arize-phoenix` then `phoenix serve` — launches a local UI on port 6006
- Docker image available for containerized deployment
- Open-source core (Phoenix) vs. managed enterprise (Arize AX) — the core is fully usable

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — Best choice if your infra team already runs OTel collectors. The "bring your own observability stack" approach.

---

### 1.3 | Helicone
**Category:** Observability / Zero-Code-Change Proxy Logger
**GitHub:** `Helicone/helicone` | License: Apache 2.0

**Core Mechanism:**
Helicone is architecturally unique: it's a **reverse proxy** that sits between your agent and the LLM API. You change `base_url` from `https://api.openai.com` to your Helicone endpoint — and logging begins with **zero code changes to your agent logic**. It captures every request/response, computes cost, latency, and token usage. Supports caching (identical prompts return cached responses, cutting costs ~60-80% in repetitive agent tasks), rate limiting, and request replay for debugging.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Self-host via Docker Compose: ships with PostgreSQL, ClickHouse, and MinIO
- Proxy URL pattern works for any OpenAI-compatible endpoint (Ollama, LiteLLM, OpenRouter)
- Excellent for sovereign setups using local inference

**Orange Tomato Fit:** 🍅🍅🍅🍅 — The fastest observability path. Drop-in, zero refactor.

---

### 1.4 | LangSmith
**Category:** Observability / LangChain Ecosystem Observability
**Vendor:** LangChain Inc.

**Core Mechanism:**
LangSmith is the first-party observability companion to LangChain and LangGraph. It auto-instruments every `chain.invoke()`, tool call, and agent step with **zero additional code** when `LANGCHAIN_TRACING_V2=true` is set. Provides deep visibility into LangGraph state machines — showing the graph structure, node execution order, and intermediate state diffs. Essential for debugging multi-hop reasoning chains. Includes a Human Evaluation UI (annotation queues) and automated eval runs via `evaluate()`.

**Sovereign Viability: ⚠️ PARTIAL**
- BYOC (Bring Your Own Cloud) and self-hosted options *exist* but are enterprise-tier pricing
- Free tier and standard tier are SaaS-only
- If LangChain is your framework: **use it**, but plan to migrate data sovereignty to Langfuse long-term

**Orange Tomato Fit:** 🍅🍅🍅 — Strong tooling, poor sovereignty. Ideal for rapid prototyping, not for production sovereign stacks.

---

### 1.5 | AgentOps
**Category:** Observability / Agent-Specific Session Debugger
**Website:** agentops.ai | License: Proprietary SaaS

**Core Mechanism:**
AgentOps is specifically designed around **multi-step agent sessions** rather than individual LLM calls. Its UI features a "session waterfall" view — think Chrome DevTools for agent runs — showing each thought, tool call, sub-agent delegation, and response in temporal order. Supports "time-travel" replay of any agent session. Native integrations with CrewAI, AutoGen, and the OpenAI Agents SDK. LLM-as-judge scoring on every session output.

**Sovereign Viability: ❌ SAAS TRAP**
- No self-hosted offering. All data sent to AgentOps cloud
- Cannot be used in air-gapped or data-sovereign environments
- **Use Langfuse + DeepEval locally as a sovereign alternative**

**Orange Tomato Fit:** 🍅🍅 — Best-in-class DX for debugging, zero for sovereignty. Use only for non-sensitive prototyping.

---

### 1.6 | OpenLLMetry (Traceloop)
**Category:** Observability / OpenTelemetry Instrumentation Layer
**GitHub:** `traceloop/openllmetry` | License: Apache 2.0

**Core Mechanism:**
OpenLLMetry is a **thin OTel instrumentation layer** — not a backend. It auto-patches LLM libraries (LangChain, LlamaIndex, OpenAI SDK, Anthropic SDK, etc.) to emit OpenTelemetry spans with LLM-specific semantic conventions (token counts, model names, prompt/completion pairs). It is **not a UI or storage system itself** — instead it routes spans to any OTel-compatible backend: Langfuse, Arize Phoenix, Jaeger, Grafana Tempo, Datadog, etc. A "universal adapter" for feeding your existing observability infrastructure with LLM-specific data.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Pure library — no cloud dependency whatsoever
- `pip install traceloop-sdk` and configure your OTel exporter endpoint
- Pair with a self-hosted Phoenix or Langfuse backend for zero data egress

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — The glue layer for sovereign, framework-agnostic observability.

---

### 1.7 | Weights & Biases Weave
**Category:** Observability + Experiment Tracking / MLOps Integration
**Vendor:** Weights & Biases

**Core Mechanism:**
W&B Weave extends the battle-tested W&B experiment tracking paradigm into LLM agent land. It captures traces, evaluation runs, and prompt experiment data in the same interface used for traditional ML training runs. Key feature: `@weave.op` decorator that auto-instruments any Python function, making it trivially easy to trace complex custom agent code without framework-specific adapters. Built-in evaluation with "scorers" — functions that grade agent output quality.

**Sovereign Viability: ⚠️ PARTIAL**
- W&B offers a self-hosted deployment option (enterprise), but it's heavy Kubernetes infrastructure
- Free tier is cloud-only
- Good for teams already using W&B for ML training who want unified experiment tracking

**Orange Tomato Fit:** 🍅🍅🍅 — MLOps-first context. Overkill if you're not running ML training pipelines.

---

### 1.8 | Braintrust
**Category:** Evaluation-First Observability
**Website:** braintrustdata.com | License: Proprietary

**Core Mechanism:**
Braintrust inverts the standard observability model: instead of "observe first, evaluate later," it builds **evaluation as the primary loop**. You define scorers (LLM-as-judge, code-based, or human), run your agent against a golden dataset, and traces are automatically captured as a by-product. Excels at regression detection — comparing two versions of your agent prompt/logic against the same evaluation suite to detect performance regressions before production.

**Sovereign Viability: ❌ SAAS (self-host in development)**
- As of 2026, fully hosted. OSS self-host path is announced but not production-stable
- Strong evaluation UX, weak sovereignty

**Orange Tomato Fit:** 🍅🍅 — Use for evaluation methodology on non-sensitive prototypes.

---

### 1.9 | DeepEval
**Category:** Agent Evaluation / CI-First Unit Testing
**GitHub:** `confident-ai/deepeval` | License: Apache 2.0

**Core Mechanism:**
DeepEval is the **pytest of LLM evaluation**. You write evaluation test cases as Python tests using familiar PyTest syntax. It ships 50+ pre-built metrics: G-Eval, Faithfulness, Answer Relevancy, Hallucination, Contextual Recall, Task Completion for agents, Toxicity, and more. The LLM-as-judge pattern runs an evaluator LLM (configurable — can use a local Ollama model) to score each test case. Integrates with any CI/CD pipeline. Run evals on every commit.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Pure Python library — no backend required
- Use any OpenAI-compatible judge model (local Ollama, OpenRouter, or your LiteLLM proxy)
- Zero data egress when paired with local inference

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — The **missing evaluation layer** for any sovereign stack. Run in CI/CD against every agent change.

---

## ZONE 2 — PROMPT & LOGIC OPTIMIZATION
### *"The Brain Training" — Programmatic optimization of agent cognition*

---

### 2.1 | DSPy (Stanford NLP)
**Category:** Programmatic Prompt Optimization / Compiler
**GitHub:** `stanfordnlp/dspy` | License: MIT

**Core Mechanism:**
DSPy is the most paradigm-shifting framework in this category. It treats prompts as **optimizable parameters in a software program**, not as static text files. You define:
1. **Signatures** — input/output type contracts (`question -> answer`)
2. **Modules** — composable reasoning steps (`ChainOfThought`, `ReAct`, `Predict`)
3. **Optimizers (Teleprompters)** — algorithms that compile your program: `BootstrapFewShot` (selects good examples), `MIPROv2` (automated instruction optimization), `BayesianSignatureOptimizer` (meta-prompt tuning)

The compiler runs your program against a training set + metric function and iteratively generates better instructions/few-shot examples. The output is a serializable compiled `program.json` that embeds the discovered prompts. Swap the underlying model without rewriting prompts — DSPy recompiles for the new model.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Pure Python library
- Optimizer calls go to whatever LLM you configure — use Ollama, LiteLLM proxy, or any OpenAI-compatible endpoint
- No cloud infrastructure required

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — The **highest-leverage optimization tool** in your stack. Treat your agent's cognitive logic as code, not magic text.

---

### 2.2 | TextGrad
**Category:** Automatic Differentiation for Text / Gradient-Based Prompt Optimization
**GitHub:** `zou-group/textgrad` | License: MIT

**Core Mechanism:**
TextGrad implements **automatic "differentiation" through text** — inspired by PyTorch's autograd but for natural language. Instead of numerical gradients, it computes "textual gradients": an LLM critiques the output of your pipeline and proposes a natural-language update direction for the prompt or variable that caused the error. This enables multi-hop optimization across complex agent pipelines where you can't compute a clean loss function. Think: backpropagation but the gradients are sentences like "The agent was too verbose in step 2; constrain the response format."

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Pure Python library
- Gradient computation uses any configured LLM critic
- Can be fine-tuned to use local critic models

**Orange Tomato Fit:** 🍅🍅🍅🍅 — Advanced. Use when DSPy's discrete optimizers don't capture enough nuance in multi-step pipelines.

---

### 2.3 | Microsoft PromptWizard
**Category:** Automated Prompt Engineering / Task-Specific Optimization
**GitHub:** `microsoft/PromptWizard` | License: MIT

**Core Mechanism:**
PromptWizard is Microsoft Research's answer to programmatic prompt generation. It combines a **Critique-Synthesize-Refine** loop with a **chain-of-thought augmented dataset generation** strategy. Given a task description and a few examples, it generates candidate prompts, executes them against synthetic or real evaluation examples, critiques failures, and iteratively refines. Key innovation: it synthesizes its own training examples using the LLM — reducing dependency on large human-labeled datasets. Excels at few-shot instruction optimization for specialized domains.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- MIT-licensed Python library
- Uses any OpenAI-compatible API endpoint
- Works with local inference (Ollama, LM Studio)

**Orange Tomato Fit:** 🍅🍅🍅🍅 — Excellent complement to DSPy for task-specific agents that need domain-optimized system prompts.

---

### 2.4 | LiteLLM (Proxy + SDK)
**Category:** LLM Routing / Unified API Gateway
**GitHub:** `BerriAI/litellm` | License: MIT

**Core Mechanism:**
LiteLLM is the **universal translation layer** for LLM APIs. Its SDK unifies calls to 100+ LLM providers under a single interface. Its **Proxy Server** mode (critical for agent swarms) acts as a local OpenAI-compatible API gateway that routes requests to different backends based on rules:
- **Model Routing:** Route `gpt-4o` calls to DeepSeek R1 via OpenRouter, route `gpt-3.5-turbo` calls to local Ollama Codestral
- **Fallbacks:** If primary model times out, auto-failover to backup
- **Load Balancing:** Distribute requests across multiple API keys / providers
- **Budget Controls:** Hard-cap per-model, per-user, or per-project spending
- **Logging:** Export all traces to Langfuse, Helicone, or any other logger

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- `docker run litellm/litellm` — runs on your machine
- Store your provider API keys locally in `.env`
- All routing decisions happen on your infrastructure

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — **Mandatory infrastructure layer** for any multi-model agent swarm. This is the foundation your Aider Architect/Builder routing already uses.

---

### 2.5 | MLflow (Tracking + Prompt Engineering Registry)
**Category:** Experiment Tracking / Prompt Registry / Evaluation
**GitHub:** `mlflow/mlflow` | License: Apache 2.0

**Core Mechanism:**
MLflow in 2026 has evolved a dedicated LLM-focused surface. Its **Prompt Engineering UI** lets you compare prompt variants against a dataset using a visual table. `mlflow.evaluate()` runs LLM-as-judge evaluations and stores results alongside traditional ML metrics. The **MLflow Tracking Server** provides versioned experiment storage, parameter logging, and artifact management — all in a self-hosted SQLite or PostgreSQL backend. Acts as the "version control system for prompts and evals" when DSPy or PromptWizard generates candidate programs.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- `mlflow server` runs entirely on localhost or your own server
- SQLite (zero-setup) to PostgreSQL (production) backends
- No cloud dependencies

**Orange Tomato Fit:** 🍅🍅🍅🍅 — Use as the experiment log and artifact store alongside DSPy optimization runs.

---

## ZONE 3 — TOOLING & FEATURE EXTENSIBILITY
### *"The Hands" — Protocols and libraries that connect agents to the real world*

---

### 3.1 | Model Context Protocol (MCP)
**Category:** Universal Tool Integration Protocol / Standard
**Author:** Anthropic | Spec: modelcontextprotocol.io | License: Open Standard

**Core Mechanism:**
MCP is the **USB-C port for AI agents** — an open, standardized protocol that defines how an AI host application (your agent) connects to external "MCP servers" that expose Tools, Resources (file systems, databases), and Prompts. The client-server architecture uses JSON-RPC 2.0 over stdio (local) or HTTP+SSE (remote). When your agent wants to "use a tool," it sends a `tools/call` message to the appropriate MCP server; the server executes the action and returns structured results. The official MCP server registry now exceeds 3,000+ community-maintained servers.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- The protocol itself is a spec — no cloud dependency
- MCP servers run as local processes (stdio transport) — zero network exposure
- You control which servers your agent connects to

**Key MCP Servers for CLI Agents:**
| Server | Capability |
|---|---|
| `mcp-server-filesystem` | Read/write local file system |
| `mcp-server-git` | Git operations |
| `mcp-server-sqlite` | Query local SQLite databases |
| `mcp-server-fetch` | HTTP GET with content extraction |
| `mcp-server-puppeteer` | Browser automation |
| `mcp-server-postgres` | PostgreSQL query execution |

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — The primary extensibility standard. Build your CLI agent to be an MCP client and you get immediate access to thousands of tools.

---

### 3.2 | Composio
**Category:** Managed Tool Integration Platform / MCP Gateway
**Website:** composio.dev | License: Proprietary (open-source SDK)

**Core Mechanism:**
Composio solves the **authentication crisis** in agent tooling. Connecting an agent to GitHub, Slack, Google Drive, Salesforce, etc. requires OAuth flows, token refresh logic, and per-API quirks. Composio abstracts all of this into a managed service. Its **Tool Router** solves the "context rot" problem: instead of injecting all 3,000+ tools into the agent's context (destroying reasoning quality), it dynamically retrieves only the 10-15 most relevant tools for the current task using semantic search over tool descriptions.

**Sovereign Viability: ⚠️ PARTIAL**
- Authentication management is cloud-hosted (data minimally exposed during OAuth flows)
- The SDK and tool definitions are open source
- For sovereign setups: use Composio for the auth layer + local MCP servers for execution
- Self-hosted Composio planned but not GA as of April 2026

**Orange Tomato Fit:** 🍅🍅🍅 — Acceptable tradeoff for 250+ API integrations vs. building OAuth flows yourself. Use with caution for sensitive workloads.

---

### 3.3 | Browser Use
**Category:** Web Browser Automation / Agent UI Control
**GitHub:** `browser-use/browser-use` | License: MIT

**Core Mechanism:**
Browser Use provides a Playwright-based browser controller wrapped in an LLM-agent–friendly API. Your agent sees the browser page as structured data (accessibility tree + screenshots), selects actions (`click`, `type`, `navigate`, `extract`), and the library executes them in a real Chromium instance. Supports **multi-tab workflows**, form filling, file uploads, and JavaScript execution. Crucially, it uses a **custom DOM processing pipeline** that converts complex web pages into minimal, agent-digestible text representations to fit within context windows. Works with any local LLM powerful enough for reasoning (Qwen2.5, Mistral Large).

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Pure Python library + Playwright
- Runs entirely on local machine — no SaaS dependency
- Compatible with local Ollama models (though frontier models give better accuracy)

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — **The web interaction layer for CLI agents.** No API? No problem. Your agent can operate any website as a human would.

---

### 3.4 | Firecrawl
**Category:** Web Data Extraction / LLM-Ready Scraping
**GitHub:** `mendableai/firecrawl` | License: Apache 2.0 (self-host)

**Core Mechanism:**
Firecrawl crawls websites and converts them to **clean Markdown** suitable for LLM consumption — handling JavaScript rendering (via Playwright), bot-detection bypass, PDF extraction, and recursive site crawling. It exposes a REST API that integrates natively as an MCP server, meaning your agent can call `scrape_url(url)` and receive clean, structured content in a single tool call. Anti-hallucination critical: feeds agents ground-truth web content instead of relying on training data.

**Sovereign Viability: ✅ FULLY SOVEREIGN (self-host)**
- Apache 2.0 self-hosted version via Docker Compose
- Managed SaaS available (firecrawl.dev) with generous free tier
- MCP server available for both hosted and self-hosted versions

**Orange Tomato Fit:** 🍅🍅🍅🍅 — Essential "eyes on the web" capability for research-heavy CLI agents.

---

### 3.5 | Crawl4AI
**Category:** Web Scraping / Open-Source LLM-Ready Crawler
**GitHub:** `unclecode/crawl4ai` | License: Apache 2.0

**Core Mechanism:**
Crawl4AI is the **fully sovereign alternative to Firecrawl**. Pure Python, runs entirely locally. It uses Playwright for JS rendering, implements smart chunking strategies for RAG-ready output, and ships with extraction schemas that use LLMs for structured data extraction from web pages. Key advantage: **direct vector database integration** — it can chunk webpage content and push directly to Chroma or Qdrant, making it a complete "web → memory" pipeline in one library.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- 100% local execution — `pip install crawl4ai`
- No API keys for the scraping layer
- Community-maintained MCP server available

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — **The sovereign default** for web extraction. Use Firecrawl managed for convenience, Crawl4AI local for sovereignty.

---

### 3.6 | E2B Code Interpreter
**Category:** Sandboxed Code Execution / Agent Runtime Environment
**GitHub:** `e2b-dev/e2b` | License: Apache 2.0

**Core Mechanism:**
E2B provides **secure, sandboxed micro-VM environments** for executing agent-generated code. When your agent writes Python/JavaScript/Bash, E2B spins up an isolated gVisor-based container in ~150ms, executes the code, captures stdout/stderr/artifacts, and returns results to the agent. Prevents agent-generated code from contaminating your host environment. Supports file I/O within the sandbox, internet access (configurable), and persistent sandboxes for multi-step coding workflows.

**Sovereign Viability: ⚠️ PARTIAL**
- Cloud-hosted execution environments (SaaS model)
- Open-source SDK and self-hosted sandbox templates exist but require infrastructure setup
- For fully sovereign code execution: use Docker-in-Docker with `gVisor` as a DIY alternative

**Orange Tomato Fit:** 🍅🍅🍅 — Critical for any agent that writes and executes code. Acceptable cloud tradeoff given security isolation benefits.

---

### 3.7 | Neon (Serverless Postgres) + pgvector
**Category:** Hybrid Relational+Vector Database / Agent State Backend
**GitHub:** `neondatabase/neon` | License: Apache 2.0 (self-host)

**Core Mechanism:**
Neon is a serverless PostgreSQL with branching capabilities. What makes it agent-relevant: coupled with the `pgvector` extension, it provides **relational + semantic search in a single database** — eliminating the need to maintain separate relational and vector stores. Your agent can execute SQL for structured reasoning AND run `SELECT ... ORDER BY embedding <-> $query_vec` for semantic memory retrieval in the same query. Native PostgreSQL means all standard tooling (backups, ACID transactions, triggers) applies.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Full self-host via Docker (standard PostgreSQL + pgvector extension)
- Neon's branching feature requires their managed service but core DB is pure OSS

**Orange Tomato Fit:** 🍅🍅🍅🍅 — Eliminates tool sprawl. One database serves relational state management AND vector memory.

---

## ZONE 4 — MEMORY & CONTEXT MANAGEMENT
### *"The Hippocampus" — Persistent, stateful intelligence for agents*

---

### 4.1 | Mem0
**Category:** Adaptive Agent Memory / Personalization Layer
**GitHub:** `mem0ai/mem0` | License: Apache 2.0

**Core Mechanism:**
Mem0 implements a **hybrid vector + optional graph memory architecture** with automated fact extraction. When an agent finishes a session, Mem0 processes the conversation transcript through an LLM to extract discrete facts ("User prefers Python over Go," "Project deadline is Q3 2026"). These facts are embedded and stored in a vector database (default: Qdrant, configurable). On subsequent session start, Mem0 retrieves the N most relevant memories based on semantic similarity to the current context and injects them. Automatic **deduplication and conflict resolution** — if a new fact contradicts an old one, Mem0 resolves the discrepancy. Graph memory support is available on Pro tier but the vector-only OSS tier handles 90% of personalization use cases.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Apache 2.0 `pip install mem0ai`
- Self-hosted vector backend (Qdrant, Chroma, Milvus — your choice)
- No mandatory cloud dependency; Mem0 cloud is optional

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — **The personalization backbone.** Every CLI agent session should inject user-specific memories.

---

### 4.2 | Zep (Graphiti Engine)
**Category:** Temporal Knowledge Graph Memory / Agent Long-Term Recall
**GitHub:** `getzep/graphiti` (engine) / `getzep/zep` (platform) | License: Apache 2.0 (engine)

**Core Mechanism:**
Zep is powered by **Graphiti** — a temporal knowledge graph engine that treats memory as a living graph of facts with time dimensions. Facts stored in Zep exist as edges between entity nodes, each with a `valid_from` / `valid_until` window. When a fact changes ("Project X budget was $50K" → "Project X budget is $100K"), Graphiti **invalidates the old edge** and creates a new one — preserving history while ensuring the agent retrieves the current truth. Retrieval is a hybrid: semantic search (embedding similarity) + BM25 keyword search + graph traversal — all three run simultaneously and results are fused. No LLM call needed at query time (unlike naive RAG).

**Sovereign Viability: ✅ FULLY SOVEREIGN (with complexity)**
- Graphiti engine is Apache 2.0 and fully self-hostable
- Requires a **Neo4j** or compatible graph database backend — additional operational burden
- Zep cloud platform available but engine is separable

**Orange Tomato Fit:** 🍅🍅🍅🍅 — Use when your agents need **temporal reasoning**: tracking how facts evolve over time. Essential for enterprise knowledge management agents.

---

### 4.3 | Letta (formerly MemGPT)
**Category:** OS-Inspired Tiered Agent Memory / Persistent Agent Framework
**GitHub:** `letta-ai/letta` | License: Apache 2.0

**Core Mechanism:**
Letta reimagines the agent as an **operating system process** with a tiered memory hierarchy mirroring hardware:
- **Core Memory (RAM):** Structured blocks always present in the context window (persona block, user profile block, goal block). Each block is a defined, editable field.
- **Recall Memory (Cache):** Recent conversation history, stored in a database, selectively loaded
- **Archival Memory (Disk):** Unlimited external storage (vector DB + relational), agent searches it via tool calls

The key innovation: the agent **actively manages its own memory** using built-in tools: `memory_replace()` to update core memory, `archival_memory_insert()` to save new knowledge, `archival_memory_search()` to retrieve it. This makes the agent a **stateful, self-evolving entity** — not a stateless function call.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Full Docker self-host available
- REST API server (`letta server`) exposes all agent management endpoints
- Agents persist across sessions by design

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — The framework for **persistent agent personalities** in a CLI swarm. Give each agent its own Letta instance and it will remember everything.

---

### 4.4 | Chroma
**Category:** Vector Database / Developer-First Memory Store
**GitHub:** `chroma-core/chroma` | License: Apache 2.0

**Core Mechanism:**
Chroma is the fastest path to agent semantic memory. Collections store embedding+document pairs. `collection.add(documents=[], embeddings=[], ids=[])` then `collection.query(query_embeddings=[], n_results=10)`. Ships with built-in embedding functions (Sentence Transformers, OpenAI). For persistent storage: `PersistentClient` saves to disk. No schema required — document metadata is arbitrary JSON. Hybrid search (vector + metadata filtering) supported.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- `pip install chromadb` — zero infrastructure beyond Python
- Embedded mode: runs inside your process (no server)
- Client-server mode: Docker image for persistent multi-client usage

**Orange Tomato Fit:** 🍅🍅🍅 — Start here for prototyping. Migrate to Qdrant for production scale.

---

### 4.5 | Qdrant
**Category:** Vector Database / Production-Grade Memory Store
**GitHub:** `qdrant/qdrant` | License: Apache 2.0

**Core Mechanism:**
Written in Rust, Qdrant is the **production vector database** most sovereign AI engineers default to. Key differentiators over Chroma: **dense + sparse hybrid search** (combine embedding similarity with BM25/TF-IDF keyword matching), **payload filtering** (filter by arbitrary JSON metadata at query time with Rust-speed execution), **quantization** (4-bit scalar/binary quantization for 4x memory reduction), and **on-disk indexing** (handle billions of vectors without RAM overflow). Its collection-snapshot system enables instant backup/restore.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- `docker run -p 6333:6333 qdrant/qdrant` — running in under 30 seconds
- Persistent storage via mounted volume (`-v ./qdrant_storage:/qdrant/storage`)
- REST + gRPC APIs — no library required, works with any HTTP client

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — **The production default vector store.** Use it. Period.

---

### 4.6 | Weaviate
**Category:** Vector Database / Multimodal Memory Store
**GitHub:** `weaviate/weaviate` | License: BSD 3-Clause

**Core Mechanism:**
Weaviate's superpower is **built-in vectorization modules** — you push raw text/images/audio and Weaviate calls the embedding model internally, storing both the original content and its embedding. Native **BM25 + vector hybrid search** via the `hybrid` operator. Schema-based — you define your data classes with properties, enabling strong typing. The **Generative Search** module lets you embed an LLM call inside the search query: `nearText(concepts: ["bug fix"]) { generate { result } }` — retrieve AND generate in one step.

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Docker/Kubernetes deployment with Helm charts
- Schema-based design adds config overhead but enforces data quality
- Resource-heavier than Qdrant; plan for 2GB+ RAM per node

**Orange Tomato Fit:** 🍅🍅🍅🍅 — Best when your agent memory includes images, audio, or multimodal documents.

---

### 4.7 | RAGAS
**Category:** RAG Evaluation / Memory Retrieval Quality Assessment
**GitHub:** `explodinggradients/ragas` | License: Apache 2.0

**Core Mechanism:**
RAGAS quantifies the quality of your agent's memory retrieval pipeline with **reference-free metrics**: Faithfulness (does the answer come from the retrieved context?), Contextual Precision (is retrieved context relevant?), Contextual Recall (did retrieval miss anything?), Answer Relevancy (does the answer address the question?). Run `evaluate(dataset, metrics=[faithfulness, answer_relevancy])` against a set of question→retrieved_context→answer triples. Works with any configurable LLM judge (local or remote).

**Sovereign Viability: ✅ FULLY SOVEREIGN**
- Pure Python library
- Judge LLM is configurable — point it at your local Ollama instance
- Zero cloud dependency

**Orange Tomato Fit:** 🍅🍅🍅🍅🍅 — Non-negotiable for any agent with a vector memory backend. Run RAGAS before declaring your retrieval "working."

---

## THE STACK COMBINATIONS

---

## 🟢 COMBINATION 1: "The Zero-Cost Local Stack"
### *For: Air-gapped, fully sovereign, zero API spend. The Orange Tomato ideal.*

```
┌─────────────────────────────────────────────────────────────┐
│                    ZERO-COST LOCAL STACK                    │
├─────────────────────────────────────────────────────────────┤
│  INFERENCE ROUTING    │  LiteLLM Proxy (local)              │
│                       │  → Ollama (local models)            │
│                       │  → OpenRouter free tier (fallback)  │
├─────────────────────────────────────────────────────────────┤
│  OBSERVABILITY        │  Langfuse (Docker self-host)         │
│                       │  + OpenLLMetry (instrumentation)    │
├─────────────────────────────────────────────────────────────┤
│  EVALUATION           │  DeepEval + RAGAS (local pytest)    │
│                       │  Ollama judge model                 │
├─────────────────────────────────────────────────────────────┤
│  PROMPT OPTIMIZATION  │  DSPy (Ollama backend)              │
├─────────────────────────────────────────────────────────────┤
│  TOOL EXTENSIBILITY   │  MCP stdio servers (local) +        │
│                       │  Crawl4AI (local scraping) +        │
│                       │  Browser Use (local Playwright)     │
├─────────────────────────────────────────────────────────────┤
│  MEMORY               │  Mem0 + Qdrant (Docker)             │
│                       │  Letta server (persistent agents)   │
└─────────────────────────────────────────────────────────────┘
```

**How They Fit Together:**
- LiteLLM Proxy is the single gateway — all agent calls route through it. Local Ollama models serve most tasks; OpenRouter free tiers provide capable fallback.
- OpenLLMetry instruments all LLM calls and exports OTel spans to the local Langfuse instance.
- DeepEval + RAGAS run in a CI-style loop using a local Ollama judge (Qwen2.5 32B recommended as judge).
- DSPy compiles optimized prompts using Ollama as the optimizer backbone; compiled programs serialized to `./compiled/`.
- MCP stdio servers handle file system, git, and database operations without network exposure.
- Crawl4AI feeds fresh web content into Qdrant. Mem0 extracts and stores facts from every session.
- Letta gives each agent an identity and persistent memory across CLI invocations.

**Cost:** ~$0/month infrastructure (your compute only). Cloud-zero.

---

## 🟡 COMBINATION 2: "The High-Velocity Prototyping Stack"
### *For: Moving fast on new agent features without the infra overhead. Acceptable SaaS tradeoffs.*

```
┌─────────────────────────────────────────────────────────────┐
│                 HIGH-VELOCITY PROTO STACK                   │
├─────────────────────────────────────────────────────────────┤
│  INFERENCE ROUTING    │  LiteLLM Proxy + OpenRouter         │
│                       │  (frontier models, pay-per-call)    │
├─────────────────────────────────────────────────────────────┤
│  OBSERVABILITY        │  Helicone (proxy, zero code change) │
│                       │  + LangSmith (for LangGraph agents) │
├─────────────────────────────────────────────────────────────┤
│  EVALUATION           │  Braintrust (eval-first, cloud)     │
│                       │  + DeepEval (local augmentation)    │
├─────────────────────────────────────────────────────────────┤
│  PROMPT OPTIMIZATION  │  DSPy + MLflow tracking server      │
├─────────────────────────────────────────────────────────────┤
│  TOOL EXTENSIBILITY   │  Composio (managed auth) +          │
│                       │  Firecrawl (managed scraping) +     │
│                       │  E2B (sandboxed code execution) +   │
│                       │  Browser Use (local Playwright)     │
├─────────────────────────────────────────────────────────────┤
│  MEMORY               │  Mem0 cloud (fast setup) +          │
│                       │  Chroma (local dev) / Qdrant (prod) │
└─────────────────────────────────────────────────────────────┘
```

**How They Fit Together:**
- LiteLLM routes calls to frontier models (Claude 3.7, DeepSeek, Gemini) via OpenRouter with budget guards.
- Helicone proxy wraps LiteLLM's upstream calls — zero instrumentation code needed, immediate cost dashboards.
- LangSmith captures LangGraph-specific state machine traces for deep agent debugging.
- Braintrust runs continuous evaluation against golden datasets, alerting on regression before deployment.
- Composio handles the OAuth hell for GitHub, Slack, Notion integrations so you never write OAuth flows.
- Firecrawl + E2B give agents "read the web" and "execute code safely" capabilities without self-managed infrastructure.
- DSPy optimization runs against OpenRouter's frontier models for maximum compilation quality; MLflow tracks each optimization run.

**Cost:** $50–$500/month depending on call volume. Optimized for **feature shipping speed** over sovereignty.

---

## 🔴 COMBINATION 3: "The Enterprise Sovereign Stack"
### *For: Production scale, compliance requirements, temporal reasoning, audit trails.*

```
┌─────────────────────────────────────────────────────────────┐
│                 ENTERPRISE SOVEREIGN STACK                  │
├─────────────────────────────────────────────────────────────┤
│  INFERENCE ROUTING    │  LiteLLM Proxy (Kubernetes) +        │
│                       │  Internal vLLM cluster              │
├─────────────────────────────────────────────────────────────┤
│  OBSERVABILITY        │  Langfuse (K8s) + OpenLLMetry +      │
│                       │  Arize Phoenix (OTel backend) +      │
│                       │  Grafana dashboards                 │
├─────────────────────────────────────────────────────────────┤
│  EVALUATION           │  DeepEval (CI/CD) + RAGAS +          │
│                       │  Custom LLM-as-judge (internal)     │
├─────────────────────────────────────────────────────────────┤
│  PROMPT OPTIMIZATION  │  DSPy + TextGrad + MLflow            │
├─────────────────────────────────────────────────────────────┤
│  TOOL EXTENSIBILITY   │  Custom MCP servers (local) +        │
│                       │  Crawl4AI (self-hosted) +           │
│                       │  neon/pgvector (unified DB) +       │
│                       │  Browser Use (headless fleet)       │
├─────────────────────────────────────────────────────────────┤
│  MEMORY               │  Zep/Graphiti (temporal graph) +     │
│                       │  Letta (persistent agent identity) + │
│                       │  Qdrant (semantic memory cluster)   │
└─────────────────────────────────────────────────────────────┘
```

**How They Fit Together:**
- vLLM serves internally-hosted FOSS models (Llama 4, Qwen3, Mistral) at full throughput. LiteLLM Proxy distributes load and enforces budget policies.
- OpenLLMetry instruments everything; Arize Phoenix receives all OTel spans and provides drift detection across embedding distributions. Langfuse handles human evaluation queues and prompt versioning. All data stays on-prem.
- DSPy + TextGrad form a two-stage optimization pipeline: DSPy handles instruction discrete optimization, TextGrad refines edge cases with gradient-based text critique. MLflow tracks every compilation run.
- Custom MCP servers expose internal tools (internal APIs, proprietary DBs) with no third-party auth. Crawl4AI scrapes from behind firewalls where needed.
- Zep/Graphiti handles the **temporal knowledge layer**: changes to facts about projects, clients, and procedures are tracked with full history. Letta gives each agent a persistent, CPU-local identity that survives reboots. Qdrant handles high-volume semantic recall across millions of agent memories.
- neon+pgvector unifies structured state (task logs, agent status, audit records) with semantic search in a single ACID-compliant database.

**Cost:** Infrastructure-only (compute, storage). Zero SaaS vendor dependency. Audit-complete.

---

## QUICK REFERENCE: SOVEREIGNTY SCORECARD

| Tool | Zone | Self-Host | OSS License | OT Fit |
|---|---|---|---|---|
| Langfuse | Observability | ✅ | MIT | 🍅🍅🍅🍅🍅 |
| Arize Phoenix | Observability | ✅ | Apache 2.0 | 🍅🍅🍅🍅🍅 |
| Helicone | Observability | ✅ | Apache 2.0 | 🍅🍅🍅🍅 |
| LangSmith | Observability | ⚠️ | Proprietary | 🍅🍅🍅 |
| AgentOps | Observability | ❌ | Proprietary | 🍅🍅 |
| OpenLLMetry | Observability | ✅ | Apache 2.0 | 🍅🍅🍅🍅🍅 |
| W&B Weave | Observability | ⚠️ | Proprietary | 🍅🍅🍅 |
| Braintrust | Observability | ❌ | Proprietary | 🍅🍅 |
| DeepEval | Evaluation | ✅ | Apache 2.0 | 🍅🍅🍅🍅🍅 |
| DSPy | Optimization | ✅ | MIT | 🍅🍅🍅🍅🍅 |
| TextGrad | Optimization | ✅ | MIT | 🍅🍅🍅🍅 |
| PromptWizard | Optimization | ✅ | MIT | 🍅🍅🍅🍅 |
| LiteLLM | Routing | ✅ | MIT | 🍅🍅🍅🍅🍅 |
| MLflow | Experiment | ✅ | Apache 2.0 | 🍅🍅🍅🍅 |
| MCP (Protocol) | Tooling | ✅ | Open Spec | 🍅🍅🍅🍅🍅 |
| Composio | Tooling | ⚠️ | OSS SDK | 🍅🍅🍅 |
| Browser Use | Tooling | ✅ | MIT | 🍅🍅🍅🍅🍅 |
| Firecrawl | Tooling | ✅ | Apache 2.0 | 🍅🍅🍅🍅 |
| Crawl4AI | Tooling | ✅ | Apache 2.0 | 🍅🍅🍅🍅🍅 |
| E2B | Tooling | ⚠️ | Apache 2.0 | 🍅🍅🍅 |
| neon+pgvector | Tooling/DB | ✅ | Apache 2.0 | 🍅🍅🍅🍅 |
| Mem0 | Memory | ✅ | Apache 2.0 | 🍅🍅🍅🍅🍅 |
| Zep/Graphiti | Memory | ✅ | Apache 2.0 | 🍅🍅🍅🍅 |
| Letta (MemGPT) | Memory | ✅ | Apache 2.0 | 🍅🍅🍅🍅🍅 |
| Chroma | Memory/VDB | ✅ | Apache 2.0 | 🍅🍅🍅 |
| Qdrant | Memory/VDB | ✅ | Apache 2.0 | 🍅🍅🍅🍅🍅 |
| Weaviate | Memory/VDB | ✅ | BSD 3-Clause | 🍅🍅🍅🍅 |
| RAGAS | Evaluation | ✅ | Apache 2.0 | 🍅🍅🍅🍅🍅 |

---

*Report generated: April 2026 | Orange Tomato Project | Sovereign CLI Architecture*
*Data sovereignty criterion: All `✅` tools can operate with zero data leaving your local environment.*
