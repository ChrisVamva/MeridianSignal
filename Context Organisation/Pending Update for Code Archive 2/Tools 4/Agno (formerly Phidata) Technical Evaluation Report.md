---
modified: 2026-04-20T16:41:28+03:00
---
# Agno (formerly Phidata) Technical Evaluation Report

## 1. Framework Weight & Speed

> [!TIP]
> Agno is explicitly designed for high-performance and low-latency environments, significantly outperforming heavier enterprise-grade orchestration frameworks in raw execution and instantiation speed.

*   **Memory Footprint:** Agno is extremely lightweight, with an estimated memory utilization of **3.75 - 6.6 KiB** per instantiated agent. In contrast, LangGraph consumes roughly **25x - 50x** more memory per agent due to its robust state-machine and graph-based tracking overhead.
*   **Instantiation Speed:** Agno boasts agent instantiation speeds in the microsecond range (approx. **~2μs**), which can be up to **10,000x faster** than standard LangGraph node initializations.

**Verdict:** For swarms, high-concurrency pipelines, or rapid prototyping, Agno provides a vastly superior token and resource economy over LangGraph.

## 2. OS Environment Stability

> [!NOTE]
> Since the Orange Tomato stack operates in a sovereign local environment, bare-metal and OS stability—particularly on Windows—is critical.

*   **Local Python Execution:** Agno is built with a minimalist, "pure-Python" architecture. This avoids the bloated dependency chaining that often complicates cross-platform execution.
*   **Windows Resilience:** Tool calling native functions and local file operations execute smoothly under Windows. By utilizing modern dependency managers like `uv` or standard Python `venv` to prevent path-length issues and dependency clashes, Agno provides high stability without needing complex containerization or daemon management.

## 3. Memory & State Management

*   **SQLite Integration:** Local, file-based memory persistence is natively supported using SQLite. Because SQLite requires no background database server, it integrates natively into Windows environments with practically zero configuration overhead.
*   **Agentic RAG & Token Bloat:** Agno is well-recognized for its "Agentic RAG" capabilities. Instead of continually stuffing the prompt with unbounded conversation histories, it integrates with local vector databases (e.g., LanceDB) to semantically retrieve only the most relevant context chunks. This surgical retrieval drastically curbs token bloat while giving the agent a highly effective long-term memory.

## 4. Orange Tomato Criteria Match

> [!IMPORTANT]
> The Orange Tomato Project requires sovereign infrastructure to be Self-hostable, API-first, and Scalable.

*   **Self-hostable:** **10/10** – Minimal external cloud dependencies. Its built-in affinity for SQLite and local vector databases makes it perfectly suited for an air-gapped or entirely local sovereign stack.
*   **API-first:** **9/10** – Extremely modular. It can be easily wrapped inside FastAPI, Litellm, or equivalent proxies to serve agent logic as endpoints dynamically.
*   **Scalable:** **9/10** – Due to the microsecond instantiation times and ~6 KiB footprint per agent, horizontal scaling of parallel agents on limited local hardware is highly viable. 

---

## Final Rating & Conclusion

### **Overall Stack Rating: 9.2 / 10**

*   **Computational Efficiency:** A+. The ~2μs instantiation and near-zero memory bloat make it a definitive leader for sovereign local swarms.
*   **Token Economy:** A. Native Agentic RAG and structured vector retrieval enforce strict token discipline, ensuring optimal OpenRouter or local SLM usage.

**Recommendation:** **Approve for Permanent Adoption.**
Agno (Phidata) secures a permanent spot in the core local infrastructure. While LangGraph remains superior for complex, highly regulated human-in-the-loop enterprise pipelines, Agno’s blazing execution speed, Windows stability, and minimalist philosophy perfectly align with the goals of building a lightweight, high-performance, token-economical sovereign AI ecosystem.
