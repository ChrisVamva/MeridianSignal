---
modified: 2026-04-18T22:19:32+03:00
---
# 🗺️ SOVEREIGN AGENT REGISTRY — APRIL 2026
### Exhaustive Open-Source & Native AI Agent Ecosystem Map
### Classification: OPERATIONAL INTELLIGENCE

---

> **Registry Protocol:** Every entry must survive the dual test of (A) active development in 2026 and (B) unique sovereign value that cannot be trivially replicated by another entry in the same zone. Deprecated or stagnant projects are marked accordingly.

---

## ZONE 1: TERMINAL & CODING OPERATORS
*Agents that execute against codebases via CLI, terminal, or IDE integration. Primary actors in a Spec-Driven swarm.*

---

### 1.1 · AIDER
- **License:** Apache 2.0 | **Engine:** Python CLI
- **Architecture:** Git-native pair programmer. Maps the entire repository into a "repo map" automatically. Works at the file and function level. All changes are auto-committed as atomic Git commits with descriptive messages. Model-agnostic (BYO API key).
- **Sovereign Value:** The only terminal coding agent with deep, first-class Git integration as a core philosophy — not an afterthought. Every change is a traceable, reversible commit. Best-in-class for structured refactoring of existing codebases where auditability matters. Zero telemetry mode available.

---

### 1.2 · OPENCODE (Vibe-mode terminal agent)
- **License:** MIT | **Engine:** TypeScript/Node.js CLI
- **Architecture:** Terminal-based agent with OpenAI-compatible endpoint support. Integrates with LiteLLM for multi-model routing. Uses a structured session model. Minimal footprint.
- **Sovereign Value:** The lightest-weight terminal coding agent in the registry that natively supports custom LiteLLM proxy endpoints. Designed for developers who want Aider-like capability with TypeScript internals and minimal dependency overhead. Fits your sovereign stack as a first-class LiteLLM client.

---

### 1.3 · OPENHANDS (formerly OpenDevin)
- **License:** MIT | **Engine:** Python + Docker-native sandbox
- **Architecture:** Full software engineering platform. Runs agents inside isolated Docker containers with access to terminal, browser, file system, and code execution. Supports multi-agent orchestration. Uses a continuous propose-execute-verify loop. Tops SWE-bench rankings consistently.
- **Sovereign Value:** The most complete open-source autonomous software engineer. Uniquely combines terminal execution, browser navigation, and code generation in a single sandboxed environment. The only open-source agent in Zone 1 that can legitimately compete with Devin on end-to-end task completion.

---

### 1.4 · SWE-AGENT
- **License:** MIT | **Engine:** Python research framework
- **Architecture:** Academic-grade agent framework built for reproducible software engineering research. Uses a controlled environment where the agent can browse, edit, and test code via a structured ACI (Agent-Computer Interface). Integrates with LangGraph for multi-agent modes.
- **Sovereign Value:** The reference implementation used by researchers to benchmark new models on SWE-bench. Unmatched for agents-building-agents research workflows. If you need to reproduce a known benchmark or study agent failure modes systematically, this is the correct tool.

---

### 1.5 · CLINE (Claude Dev)
- **License:** Apache 2.0 | **Engine:** VS Code Extension (TypeScript)
- **Architecture:** VS Code extension operating as a full autonomous agent inside the IDE. Has "Plan & Act" dual modes. Supports MCP for tool extension. Requires explicit developer approval for every destructive action (file writes, terminal commands). Model-agnostic.
- **Sovereign Value:** Human-in-the-loop sovereignty. The most defensible agentic IDE integration for professional environments where unreviewed autonomous execution is unacceptable. Every action is presented for approval before execution — making it the safest agent for proprietary codebases.

---

### 1.6 · ROO CODE (formerly Roo Cline)
- **License:** Apache 2.0 | **Engine:** VS Code Extension (TypeScript)
- **Architecture:** Fork of Cline with added role-based execution modes: Architect, Code, Ask, Debug, Test. Each mode constrains what the agent can and cannot do. Supports local model routing via Ollama. Active community with rapid release cycles.
- **Sovereign Value:** The only VS Code coding agent with built-in role-based mode constraints. The "Architect" mode specifically prevents code writing and enforces planning-only outputs — directly useful for a Planner/Executor swarm architecture where you need a human-verified planning stage inside the IDE.

---

### 1.7 · GOOSE (by Block Inc.)
- **License:** Apache 2.0 | **Engine:** Rust + Python (local-first CLI)
- **Architecture:** Local-first terminal agent built by Block (formerly Square). Entirely on-device execution. Uses MCP for extensibility. Designed for full development workflows: file editing, terminal execution, shell scripting. No cloud telemetry.
- **Sovereign Value:** Maximum data sovereignty in the Terminal zone. Built and maintained by a financial technology company with non-negotiable privacy standards. The architecture is designed from the ground up for zero data exfiltration. Ideal for financial or compliance-grade development environments.

---

### 1.8 · DEVIKA
- **License:** MIT | **Engine:** Python web application
- **Architecture:** Full autonomous software engineer with a research → plan → code pipeline. Features a visual interface for monitoring agent state, a planning module, search capability, and code generation. Positioned as an open-source Devin alternative.
- **Sovereign Value:** The only agent in Zone 1 with a dedicated visual planning interface out of the box. Unlike terminal-only agents, Devika exposes the planning and reasoning process visually — useful for teams that need to audit or present AI decision-making to non-technical stakeholders.

---

### 1.9 · POTPIE
- **License:** Apache 2.0 | **Engine:** Python + knowledge graph backend
- **Architecture:** Parses repositories into knowledge graphs (not flat embeddings). Agents query the graph to understand code structure — dependency relationships, call graphs, module hierarchies — before generating output.
- **Sovereign Value:** Uniquely architecture-aware. While other agents see a codebase as files + embeddings, Potpie sees it as a structural graph. This enables precision tasks like "explain why changing function X will break modules A, B, and C" — a planning capability no other Zone 1 agent offers natively.

---

### 1.10 · GEMINI CLI
- **License:** Apache 2.0 | **Engine:** Go CLI
- **Architecture:** Google's open-source terminal coding agent. Backed by Gemini models with a 1M token context window. Free tier available (Gemini Flash). Can process entire large codebases in a single context window.
- **Sovereign Value:** The largest context window of any terminal agent in this registry (1M tokens). Enables loading an entire monorepo into context without chunking or summarization. Free tier makes it zero-cost for light usage. The only agent where "the entire codebase is the context."

---

### 1.11 · CODEX CLI
- **License:** MIT | **Engine:** Node.js CLI
- **Architecture:** OpenAI's terminal-native agent. Sandboxed execution with network access controls. Supports parallel task execution. Tight integration with OpenAI's model ecosystem.
- **Sovereign Value:** The reference implementation for OpenAI's sandboxed agent approach. Unique network isolation model — can run tasks with different levels of network trust (no-network, local-only, full access). Useful when you need provably isolated code execution.

---

### 1.12 · CONTINUE.DEV
- **License:** Apache 2.0 | **Engine:** VS Code + JetBrains Extension (TypeScript)
- **Architecture:** Open, extensible IDE extension supporting VS Code and JetBrains. Model-agnostic, BYOM. Supports local models via Ollama. Highly configurable context providers, slash commands, and custom actions.
- **Sovereign Value:** The most IDE-portable solution in Zone 1. The only agent that works natively in both VS Code AND JetBrains. For enterprise developers locked into IntelliJ/PyCharm, this is the only fully sovereign, open-source option. Supports zero-network execution with local Ollama.

---

### 1.13 · AIDER-CHAT / ARCHITECT MODE (Advanced)
> *Note: Distinct from base Aider. The `--architect` flag enables a two-agent mode where a "architect" model reasons and plans, and an "editor" model writes code.*
- **Sovereign Value:** The only single-tool solution shipping a native Planner/Executor split mode. Enables using DeepSeek R1 as Planner and Codestral 22B as Executor within a single Aider session — directly implementing your spec-driven swarm at the CLI level.

---

## ZONE 2: BROWSER & WEB NAVIGATORS
*Agents that perceive and interact with web interfaces autonomously.*

---

### 2.1 · BROWSER-USE
- **License:** MIT | **Engine:** Python (Playwright wrapper)
- **Architecture:** LLM-controlled Playwright wrapper. The agent receives the accessibility tree + screenshot at each step, decides the next action (click, type, scroll, navigate), and executes it. Context is passed between steps, enabling multi-step adaptive workflows.
- **Sovereign Value:** The dominant open-source browser agent of 2025-2026. Most widely starred and forked browser agent on GitHub. Acts as a universal substrate — virtually every other browser agent either uses it or is benchmarked against it. Self-hosted, no cloud dependency.

---

### 2.2 · SKYVERN
- **License:** AGPL-3.0 | **Engine:** Python + FastAPI + Playwright
- **Architecture:** Uses a swarm of vision + LLM sub-agents to decompose complex website interaction into smaller, verifiable steps. Does not use brittle CSS selectors — uses visual understanding + semantic analysis to interact with any website layout.
- **Sovereign Value:** The most resilient browser agent against UI changes. Zero CSS selectors means zero maintenance when a website redesigns. Built specifically for RPA-class tasks (invoice fetching, government form submission, e-commerce purchasing). The only browser agent with first-class workflow library for repeated task patterns.

---

### 2.3 · STAGEHAND (by Browserbase)
- **License:** MIT | **Engine:** TypeScript (Playwright wrapper)
- **Architecture:** TypeScript SDK providing four core primitives: `act` (do something), `extract` (get data), `observe` (see state), `agent` (autonomous loop). Designed to mix deterministic code with AI at will. Production reliability focus.
- **Sovereign Value:** The TypeScript ecosystem's answer to Browser-Use. The explicit four-primitive architecture means you can use AI where uncertainty exists and hard-coded logic where reliability is required — in the same workflow. The only browser agent built explicitly for TypeScript full-stack developers.

---

### 2.4 · PLAYWRIGHT MCP SERVER (by Microsoft)
- **License:** MIT | **Engine:** Node.js MCP Server
- **Architecture:** Official Playwright Model Context Protocol server. Exposes browser control as MCP tools that any MCP-compatible agent can call. Uses structured accessibility trees (not screenshots) for interaction — dramatically faster and more reliable than vision-based approaches.
- **Sovereign Value:** The official standard for AI-browser interaction via MCP. Any agent supporting MCP can instantly gain browser capability without custom integration. The accessibility-tree approach makes it the most token-efficient browser interaction method available.

---

### 2.5 · FIRECRAWL
- **License:** AGPL-3.0 (self-hostable) | **Engine:** Node.js + Puppeteer
- **Architecture:** Web-to-Markdown conversion pipeline with LLM-ready output. Handles JS-rendered pages, authentication, sitemaps, and deep crawling. Provides `/scrape`, `/crawl`, `/extract`, and `/search` endpoints.
- **Sovereign Value:** The standard data-ingest layer for AI pipelines that need clean web content. Self-hostable via Docker for full sovereignty. The `/extract` endpoint uses LLMs to pull structured data from any page without CSS selectors. Bridges Zone 2 and Zone 4.

---

### 2.6 · CRAWL4AI
- **License:** Apache 2.0 | **Engine:** Python async library
- **Architecture:** Python-native async web crawler built specifically for AI/LLM consumption. Local-first design — no managed API required. Extracts clean Markdown, tables, and structured content. Supports local LLM integration for on-device extraction.
- **Sovereign Value:** Full data sovereignty in the web ingestion pipeline. No external API calls for extraction. Works entirely on local hardware with local models. The only crawler designed from the ground up for local-first AI agent data pipelines.

---

### 2.7 · SCRAPEGRAPHAI
- **License:** MIT | **Engine:** Python graph-based pipeline
- **Architecture:** Uses a directed graph (similar to LangGraph) to define multi-step scraping pipelines: fetch → parse → extract → synthesize. Each node applies a different LLM prompt for its step.
- **Sovereign Value:** The only browser data agent that models the extraction pipeline as a graph rather than a linear sequence. Enables branching extraction logic where different page types trigger different extraction strategies automatically.

---

### 2.8 · OPEN INTERPRETER (browser mode)
- **License:** MIT | **Engine:** Python + optional browser + computer control
- **Architecture:** Full local code execution agent with optional computer control including browser automation. Supports local models via Ollama. Can be given access to terminal, Python REPL, file system, and browser simultaneously.
- **Sovereign Value:** The only agent in this registry that spans Zones 1, 2, and 6 simultaneously. Browser control is one of several computer interaction modes — enabling workflows that cross from web browsing to code writing to file manipulation in a single agent context.

---

## ZONE 3: AGENTIC RUNTIMES & ORCHESTRATION FRAMEWORKS
*The infrastructure layer. These are not agents themselves but the engines on which agent swarms are built.*

---

### 3.1 · LANGGRAPH (by LangChain Inc.)
- **License:** MIT | **Engine:** Python (directed graph state machine)
- **Architecture:** Models agent workflows as directed graphs. Nodes = agents/tools, Edges = conditional routing logic. State is explicitly typed and persistent. Supports human-in-the-loop at any node. Native checkpointing for fault tolerance.
- **Sovereign Value:** The production engineering gold standard. Used in enterprise environments (Uber, Cisco) for long-running, fault-tolerant agent systems. The explicit graph model forces disciplined state management — preventing the hidden state bugs that plague implicit agent frameworks. LangGraph Studio provides visual workflow debugging.

---

### 3.2 · CREWAI
- **License:** MIT | **Engine:** Python (role-based multi-agent)
- **Architecture:** Defines agents by role (e.g., Researcher, Writer, Coder). Tasks are assigned to agents based on role compatibility. Agents communicate through a structured crew coordination layer. Supports sequential and parallel task execution.
- **Sovereign Value:** The fastest path from idea to working multi-agent team. Role-based mental model is intuitive for rapid prototyping. `crewai train` command allows fine-tuning agent behavior on your specific task domain. Best DX in Zone 3 for building an operational swarm in under an hour.

---

### 3.3 · AUTOGEN (Microsoft)
- **License:** MIT | **Engine:** Python (conversational multi-agent)
- **Architecture:** Agents interact through structured conversations. AgentChat layer provides preset patterns (AssistantAgent, UserProxyAgent). Supports tool calling, code execution, and termination conditions. AutoGen Studio provides a GUI for workflow construction.
- **Sovereign Value:** The conversational multi-agent reference implementation from Microsoft. Uniquely suited for workflows where the solution path is emergent — the agents need to discuss and negotiate rather than follow a fixed graph. Research-first architecture with the strongest academic backing of any Zone 3 framework.

---

### 3.4 · MASTRA
- **License:** MIT | **Engine:** TypeScript (Node.js, Cloudflare Workers compatible)
- **Architecture:** TypeScript-native batteries-included framework. Provides Agents, Workflows, RAG, Memory, Evals, and MCP integrations as first-class primitives. Built for edge deployment (Cloudflare Workers, Vercel Edge). Can run entirely serverless.
- **Sovereign Value:** The only Zone 3 framework designed for TypeScript-first, edge-native deployment. Zero Python dependency. If your sovereign stack is JavaScript/TypeScript (Node, Next.js, Bun), Mastra is the only framework that integrates naturally without Python backend overhead.

---

### 3.5 · SMOLAGENTS (by HuggingFace)
- **License:** Apache 2.0 | **Engine:** Python (~1,000 lines of core code)
- **Architecture:** Agents execute tasks by writing and running Python code snippets rather than calling pre-defined JSON tools. The "code-first" paradigm. Minimal dependencies, no framework lock-in. Models actions as executable Python, not function-call JSON.
- **Sovereign Value:** The anti-bloat choice. Core framework is ~1,000 lines of Python — fully auditable in an afternoon. "Code as action" eliminates the JSON tool-calling specification layer that creates complexity in other frameworks. Agents that `import math; result = math.sqrt(...)` instead of `{"tool": "calculator", "args": {"op": "sqrt"}}`. Dramatically reduces token overhead per action.

---

### 3.6 · DIFY
- **License:** Apache 2.0 | **Engine:** Python/TypeScript + Docker compose
- **Architecture:** Full visual low-code platform for LLM application development. Workflow editor with drag-and-drop nodes. Built-in RAG pipeline, model management, API publishing, and monitoring. Self-hostable via Docker.
- **Sovereign Value:** The sovereign answer to Zapier AI + LangSmith combined. The only framework that provides a complete, visual, self-hosted platform for building AND deploying AND monitoring agent workflows. Non-engineering team members can build functional agent pipelines without code.

---

### 3.7 · PYDANTIC AI
- **License:** MIT | **Engine:** Python (type-safe agent framework)
- **Architecture:** Built by the Pydantic team. Uses Python type hints as the contract system for agent inputs and outputs. Agents are typed functions — if it type-checks, the output schema is guaranteed. Integrates with Pydantic Logfire for full observability.
- **Sovereign Value:** Type safety as a first-class property in agent systems. The only Zone 3 framework where "the model cannot return a hallucinated schema" is enforced at the Python type level. For production systems where schema compliance is non-negotiable (e.g., feeding agent output directly into databases), Pydantic AI is the only correct choice.

---

### 3.8 · HAYSTACK (by deepset)
- **License:** Apache 2.0 | **Engine:** Python (pipeline-based modular framework)
- **Architecture:** Component-based pipeline architecture. Every step (retriever, reranker, reader, generator) is a modular, swappable component. Pipelines are defined as YAML or Python. Mature RAG + agentic workflows. Enterprise-proven.
- **Sovereign Value:** The production RAG-to-agentic bridge. The most mature RAG framework in the ecosystem, now with full agentic workflow support. Used for enterprise search and knowledge management systems since 2019. The only Zone 3 framework with a strong enterprise pedigree predating the LLM era.

---

### 3.9 · AGNO (formerly Phidata)
- **License:** Mozilla Public License 2.0 | **Engine:** Python
- **Architecture:** High-performance multi-agent runtime. First-class session management, persistent memory, knowledge stores, and MCP tool integration. Metrics-driven with built-in benchmarking per agent.
- **Sovereign Value:** The fastest multi-agent runtime in pure Python benchmarks. Designed for high-throughput agent swarms where performance per call matters. Built-in memory persistence makes it uniquely suitable for long-running autonomous agents that must remember context across sessions (days/weeks).

---

### 3.10 · OPENAI SWARM (experimental)
- **License:** MIT | **Engine:** Python (~500 lines)
- **Architecture:** Minimalist framework demonstrating multi-agent hand-offs via direct function calls. Agents, routines, and handoffs as Python classes and methods. No abstraction layers. Intentionally educational.
- **Sovereign Value:** The cleanest conceptual demonstration of agent orchestration in the ecosystem. Reading Swarm's source code teaches multi-agent patterns in ~30 minutes. Useful as a reference architecture when building custom orchestration without framework dependency.

---

### 3.11 · POCKETFLOW
- **License:** MIT | **Engine:** Python (~100 lines)
- **Architecture:** Minimal node-flow framework. Nodes = logic units, Flows = connections. Zero external dependencies. Intentionally nano-scale to avoid vendor lock-in. Designed for rapid prototyping and for AI-generating other AI pipelines.
- **Sovereign Value:** The smallest viable agentic framework. Sub-100-line core is auditable by anyone in minutes. Designed for AI-generated agent pipelines — the architecture is simple enough that an LLM can write valid PocketFlow code reliably. Bootstrapping swarms via LLMs is the primary use case.

---

### 3.12 · BMAD (Breakthrough Method for Agile AI-Driven Development)
- **License:** MIT | **Engine:** Prompt-native / CLI + VS Code integration
- **Architecture:** Framework + methodology that maps AI agents to agile development roles: PM, Architect, Developer, QA, DevOps. Each role has a dedicated system prompt, toolset, and scope restriction. Stateful handoffs between roles are managed via structured documents (SPEC.md, ARCH.md, TASKS.md).
- **Sovereign Value:** The spec-driven development methodology formalized as an agent framework. BMAD is the closest existing implementation to your Sovereign Stack's architecture. The role-scoped prompts prevent scope bloat between Planner and Executor stages. Immediately adaptable for your 14-model swarm.

---

### 3.13 · LANGCHAIN (core)
- **License:** MIT | **Engine:** Python + JavaScript
- **Architecture:** The foundational LLM application framework. Provides chains, memory, tools, and agent executors. LCEL (LangChain Expression Language) for composing pipeline steps. Parent project of LangGraph.
- **Sovereign Value:** The largest tool integration ecosystem in the registry — 700+ tool integrations via LangChain Hub. If you need an obscure database connector, legacy API wrapper, or niche tool integration, LangChain has it. The breadth of its integration library is unmatched by any other framework.

---

## ZONE 4: LOCAL & PERSONAL RAG/ASSISTANTS
*Privacy-first agents deployed on personal hardware for document Q&A, personal knowledge management, and local inference.*

---

### 4.1 · ANYTHINGLLM
- **License:** MIT | **Engine:** Node.js + Electron (Desktop App) / Docker (Server)
- **Architecture:** Full-stack local AI assistant. Bundles: vector database (LanceDB default), document ingestion pipeline, Ollama integration, and a ChatGPT-like UI. Supports agent mode with web browsing, code execution, and tool use. Desktop app requires zero CLI setup.
- **Sovereign Value:** The most complete zero-setup local AI assistant in the registry. Desktop app installs like any consumer software. Supports 50+ LLM providers, 20+ vector databases, and has a growing agentic layer. The entry point for non-technical users to a fully sovereign AI stack.

---

### 4.2 · KHOJ
- **License:** AGPL-3.0 | **Engine:** Python + Django
- **Architecture:** Personal AI assistant designed to index and search your own data: notes, documents, calendar, GitHub repos, Notion pages, Obsidian vaults. Web search integration. Supports local Ollama models. Can run as always-on background service.
- **Sovereign Value:** The only Zone 4 agent designed explicitly for Personal Knowledge Management (PKM) integration. Native connectors for Obsidian, Notion, Org-mode, and local files. If your "second brain" is in Obsidian, Khoj is the only agent that makes it a queryable AI-first knowledge base without cloud upload.

---

### 4.3 · PRIVATEGPT
- **License:** Apache 2.0 | **Engine:** Python + FastAPI
- **Architecture:** 100% offline RAG pipeline. Document ingestion → embedding → vector storage → retrieval → local inference. Zero network calls after setup. All models run locally via llama.cpp/Ollama. Strict air-gap guarantee.
- **Sovereign Value:** The strictest air-gap guarantee in Zone 4. Designed for environments where no data may leave the machine under any circumstances. Used in classified research, legal, and healthcare contexts where cloud connectivity itself is a compliance violation. The network is physically absent, not just disabled by config.

---

### 4.4 · PERPLEXICA
- **License:** MIT | **Engine:** Next.js + TypeScript
- **Architecture:** Open-source Perplexity AI clone. Integrates Searxng (local search engine) + LLM to answer questions with cited web sources. Multiple focus modes (General, Academic, YouTube, Reddit, News). All processed locally.
- **Sovereign Value:** The sovereign web research assistant. Combines a local search index (Searxng) with local LLM synthesis — providing cited, web-grounded answers without sending queries to proprietary search APIs. The only tool that localizes the entire Perplexity experience including the search layer.

---

### 4.5 · OPEN WEBUI
- **License:** BSD | **Engine:** Python + Svelte + Docker
- **Architecture:** ChatGPT-like web interface for Ollama and OpenAI-compatible endpoints. RAG pipeline with document upload. Tool execution. Multimodal support. Role-based user management. One Docker command setup.
- **Sovereign Value:** The de facto sovereign UI layer of the local AI ecosystem. If you need a polished, ChatGPT-comparable interface for your Ollama models accessible from any browser on your network, Open WebUI is the universal answer. The UI that most local AI stacks use as their human interface.

---

### 4.6 · LOBE CHAT
- **License:** Apache 2.0 | **Engine:** Next.js + TypeScript
- **Architecture:** Feature-rich, self-hostable AI chat UI. Supports 30+ model providers, local models via Ollama, plugins/tools, multi-model comparison, TTS/STT, image generation, and knowledge base RAG.
- **Sovereign Value:** The most feature-complete self-hosted chat UI. While Open WebUI dominates for Ollama-only setups, Lobe Chat uniquely supports multi-provider side-by-side model comparison in a single UI — enabling live A/B testing of your sovereign router models.

---

### 4.7 · LLAMAINDEX (data framework)
- **License:** MIT | **Engine:** Python + TypeScript
- **Architecture:** Specialized data framework for connecting LLMs to external data sources. Provides data connectors, indexes, query engines, and agent tools. Not an agent framework itself — it is the data layer on which agents are built.
- **Sovereign Value:** The most comprehensive data-to-LLM connector library. 120+ data source integrations. If LangChain is the tool integration layer of the ecosystem, LlamaIndex is the data integration layer. For building RAG agents that query databases, PDFs, APIs, and structured data simultaneously.

---

## ZONE 5: SOVEREIGN / GENERAL AUTONOMOUS EXECUTORS
*Agents designed for open-ended, long-horizon goal execution. The "general purpose" autonomous layer.*

---

### 5.1 · AUTOGPT / AUTOGPT FORGE
- **License:** MIT | **Engine:** Python + Docker
- **Architecture:** The original autonomous agent loop. Goal → task decomposition → internet research → code execution → file management → reflection → next task. AutoGPT Forge is the upgraded modular framework for building custom agents on the AutoGPT architecture.
- **Sovereign Value:** The foundational autonomous agent reference. Every concept in general autonomous execution — task lists, memory, tool use, self-reflection — was popularized by AutoGPT. The Forge architecture allows building custom autonomous agents using AutoGPT's battle-tested executor loop. Historical significance + active maintenance.

---

### 5.2 · GPT-ENGINEER / GPT-ENGINEER-APP
- **License:** MIT | **Engine:** Python CLI
- **Architecture:** Accepts a natural language spec and generates an entire codebase from scratch. Iterative clarification loop before generation. Writes files, installs dependencies, and runs the application. Supports benchmarking on SWE-bench.
- **Sovereign Value:** The "greenfield project" specialist. Unlike agents that modify existing codebases, GPT-Engineer is optimized for building new applications from a blank directory. Best for prototyping new projects from a single specification document — a direct implementation of spec → executable.

---

### 5.3 · AGENT-ZERO
- **License:** MIT | **Engine:** Python + Docker (minimal)
- **Architecture:** Minimal, highly transparent general-purpose agent. No hidden complexity — the entire agent loop is visible and modifiable. Persistent memory between sessions. Computer use, code execution, and web browsing. Designed for full user control and understanding.
- **Sovereign Value:** Radical transparency in autonomous execution. The source code and agent loop are intentionally simple enough for a developer to understand, audit, and modify every component. For builders who need to trust their autonomous agent architecture completely — "no magic" is the design principle.

---

### 5.4 · OPEN INTERPRETER
- **License:** MIT | **Engine:** Python (local execution) + optional cloud
- **Architecture:** Gives LLMs the ability to run code (Python, JavaScript, Shell, etc.) locally on your computer. Acts as a natural language interface to your entire operating system. Supports local models via Ollama. Can operate fully offline.
- **Sovereign Value:** The most capability-dense single-agent system in the registry. From one agent, you have: code execution, file system access, browser control, system calls, and API calls — all from natural language. The "Swiss Army knife" autonomous executor with full local model support.

---

### 5.5 · BABYAGI (evolutions: TaskWeaver, BabyAGI-UI)
- **License:** MIT | **Engine:** Python (task queue pattern)
- **Architecture:** The original task queue autonomous agent. Maintains an ordered list of tasks, executes the top task, evaluates the result, creates new tasks, and re-orders the queue. BabyAGI-UI adds a browser interface. TaskWeaver (Microsoft) is a code-first BabyAGI evolution.
- **Sovereign Value:** The cleanest implementation of recursive task decomposition as code. While superseded for production use by LangGraph/CrewAI, BabyAGI remains the canonical reference implementation for the task-queue pattern. Microsoft's TaskWeaver evolution adds data science task execution as a first-class capability — unique in this zone.

---

### 5.6 · AGENTGPT / COGNOSYS
- **License:** MIT | **Engine:** Next.js + TypeScript (browser-based)
- **Architecture:** Browser-based, no-install autonomous agent. Goal → sub-task decomposition → execution → result → next cycle. Zero setup. Runs entirely in the browser via API calls.
- **Sovereign Value:** The only fully browser-native general autonomous executor. Zero local installation. Enables autonomous agent execution from any device with a browser. For situations where the agent must run on hardware you cannot control (shared workstation, remote machine without SSH access, tablet).

---

### 5.7 · OPENAGI
- **License:** MIT | **Engine:** Python research framework
- **Architecture:** Research platform for combining multiple specialized AI models in a single agentic pipeline. Routes sub-tasks to specialized models (text, code, image, audio) based on capability matching. Task performance is evaluated and used to improve model selection.
- **Sovereign Value:** The most explicit implementation of capability-based model routing in the autonomous executor space. Sub-tasks are automatically routed to the model best equipped for them — text generation, code writing, and image analysis are handled by separate specialist models in a single workflow. Direct ancestor of the Planner/Executor architecture.

---

## ZONE 6: DESKTOP / GUI COMPUTER-USE OPERATORS
*Agents that control the desktop operating system directly: clicking, typing, opening apps.*

---

### 6.1 · UFO (UI-Focused Agent, by Microsoft)
- **License:** MIT | **Engine:** Python + Windows Accessibility APIs
- **Architecture:** Dual-agent framework for Windows desktop automation. HostAgent decomposes the high-level task; AppAgent executes within individual applications using Windows UI Automation (WinUI), Win32, and WinCOM APIs. Does not require vision models — reads accessibility trees directly.
- **Sovereign Value:** The most precise Windows desktop automation agent available. Native Windows API integration means interaction is faster and more reliable than vision-based approaches. Can automate legacy Win32 applications that no web agent can touch — ERP systems, government desktop software, proprietary enterprise tools.

---

### 6.2 · OPENADAPT.AI
- **License:** MIT | **Engine:** Python + VLM (Vision-Language Models)
- **Architecture:** "Generative Process Automation" — learns by watching human demonstrations. User records a workflow; OpenAdapt learns the actions and can replay/adapt them. Cross-platform (macOS + Windows). Built-in PII/PHI scrubbing for privacy before sending screenshots to VLMs.
- **Sovereign Value:** The only agent that learns from demonstration rather than instruction. Zero-shot adaptation to arbitrary desktop software — if a human can do it, you can record it and OpenAdapt will learn to replicate it. Privacy-first design with automatic PII scrubbing makes it suitable for regulated data environments.

---

### 6.3 · SCREENPIPE
- **License:** MIT | **Engine:** Rust (high-performance local recording)
- **Architecture:** Continuously records screen and audio, transcribes with Whisper, and makes the data queryable via an LLM interface. All processing local. Background daemon with zero-latency capture. Builds a searchable history of everything shown on the screen.
- **Sovereign Value:** The passive intelligence layer on top of your OS. Not a task-executing agent but a continuous memory system: "What was that Slack message from 3 hours ago?" "What was the API error I saw yesterday?" Uniquely turns the entire screen history into a queryable local knowledge base.

---

### 6.4 · UI-TARS (by Alibaba/QwenVL team)
- **License:** Apache 2.0 | **Engine:** VLM model (Qwen-VL based)
- **Architecture:** A vision-language model specifically fine-tuned for computer use tasks. Understands screenshots and outputs click coordinates + keyboard actions. Designed to run locally without external API calls. Optimized for GUI interaction rather than general conversation.
- **Sovereign Value:** The only open-weight model purpose-built for GUI interaction as its primary training objective. All other computer-use agents use general VLMs (GPT-4V, Gemini) and prompt-engineer them for GUI tasks. UI-TARS was trained on GUI interaction data — better click accuracy and action planning than improvised VLM approaches.

---

### 6.5 · SCREENAGENT
- **License:** MIT | **Engine:** Python research framework
- **Architecture:** Research-grade screen control agent operating on a "Plan → Execute → Reflect" loop. Sends screenshots to a VLM, receives action plans, executes via pyautogui, evaluates result. Academic reference implementation.
- **Sovereign Value:** The cleanest research implementation of vision-based GUI control. As a reference architecture, it demonstrates the planning-execution loop without framework bloat. Used for benchmarking new VLMs on GUI tasks.

---

## CROSS-CUTTING INFRASTRUCTURE

*Projects that are not agents but are essential glue for the sovereign stack.*

---

### X.1 · MODEL CONTEXT PROTOCOL (MCP) — Anthropic
- **License:** MIT (specification) | **Implementations:** Python, TypeScript, Go, Rust
- **What it is:** The universal standard for connecting AI agents to external tools, databases, and APIs. Any MCP-compatible agent can use any MCP server. Growing ecosystem of 1000+ servers.
- **Sovereign Value:** The USB-C of AI agents. Without MCP, every agent needs custom integration code for every tool. With MCP, one integration spec covers every agent. Adopt MCP as the tool integration standard for your sovereign stack — all Zone 1-5 agents that don't support MCP will be progressively marginalized.

---

### X.2 · LANGFUSE (observability)
- **License:** MIT (self-hostable) | **Engine:** TypeScript + ClickHouse
- **What it is:** Open-source LLM observability platform. Traces every agent call, token usage, latency, and evaluation score. SDKs for Python and TypeScript. Self-hostable via Docker.
- **Sovereign Value:** The sovereign monitoring layer for your swarm. Every LiteLLM proxy call can be logged to a self-hosted Langfuse instance — giving you a complete audit trail of every Planner and Executor interaction with zero data leaving your infrastructure.

---

### X.3 · DEEPEVAL (evaluation)
- **License:** Apache 2.0 | **Engine:** Python (pytest-native)
- **What it is:** LLM evaluation framework integrated directly into Python's pytest system. Evaluates agent outputs at the "span level" — individual agent actions, tool calls, and reasoning steps — not just final outputs.
- **Sovereign Value:** The CI/CD layer for agent quality assurance. Runs in pytest — meaning agent quality evaluation can be added to any existing test suite with zero new tooling. Critical for validating that Planner model output consistently meets contract format requirements before deploying new models.

---

### X.4 · OLLAMA
- **License:** MIT | **Engine:** Go (model serving daemon)
- **What it is:** Local model serving runtime for open-weight models. Download and run any HuggingFace model with a single command. OpenAI-compatible API on localhost.
- **Sovereign Value:** The universal local inference layer. Without Ollama, deploying local models requires CUDA setup, model conversion, and server configuration. Ollama reduces this to `ollama run qwen3`. Every Zone 1-5 agent that supports Ollama gains instant access to your entire local model roster.

---

## STATUS LEGEND
| Symbol | Status |
|---|---|
| ✅ Active | Active development, new releases in 2025-2026 |
| ⚠️ Maintenance | Maintained but slow feature development |
| 🔬 Research | Primarily academic, not production-ready |
| ❌ Stagnant | No meaningful development since 2024 |

| Agent | Status |
|---|---|
| Aider | ✅ Active |
| OpenHands | ✅ Active |
| SWE-agent | ✅ Active |
| Cline | ✅ Active |
| Roo Code | ✅ Active |
| Goose | ✅ Active |
| Devika | ⚠️ Maintenance |
| Potpie | ✅ Active |
| Gemini CLI | ✅ Active |
| Codex CLI | ✅ Active |
| Continue.dev | ✅ Active |
| Browser-Use | ✅ Active |
| Skyvern | ✅ Active |
| Stagehand | ✅ Active |
| Playwright MCP | ✅ Active |
| Firecrawl | ✅ Active |
| Crawl4AI | ✅ Active |
| ScrapeGraphAI | ✅ Active |
| Open Interpreter | ✅ Active |
| LangGraph | ✅ Active |
| CrewAI | ✅ Active |
| AutoGen | ✅ Active |
| Mastra | ✅ Active |
| smolagents | ✅ Active |
| Dify | ✅ Active |
| Pydantic AI | ✅ Active |
| Haystack | ✅ Active |
| Agno | ✅ Active |
| OpenAI Swarm | ⚠️ Maintenance (educational) |
| PocketFlow | ✅ Active |
| BMAD | ✅ Active |
| LangChain | ✅ Active |
| AnythingLLM | ✅ Active |
| Khoj | ✅ Active |
| PrivateGPT | ⚠️ Maintenance |
| Perplexica | ✅ Active |
| Open WebUI | ✅ Active |
| Lobe Chat | ✅ Active |
| LlamaIndex | ✅ Active |
| AutoGPT | ✅ Active |
| GPT-Engineer | ⚠️ Maintenance |
| Agent-Zero | ✅ Active |
| Open Interpreter | ✅ Active |
| BabyAGI | ❌ Stagnant (use TaskWeaver evolution) |
| AgentGPT | ⚠️ Maintenance |
| OpenAGI | 🔬 Research |
| UFO | ✅ Active |
| OpenAdapt | ✅ Active |
| ScreenPipe | ✅ Active |
| UI-TARS | ✅ Active |
| ScreenAgent | 🔬 Research |
| MCP Ecosystem | ✅ Active |
| Langfuse | ✅ Active |
| DeepEval | ✅ Active |
| Ollama | ✅ Active |

---
*Registry compiled: 2026-04-18 | 54 primary projects catalogued across 6 operational zones*
*Sources: GitHub trending, r/LocalLLaMA, r/devops, primary documentation, HuggingFace*
