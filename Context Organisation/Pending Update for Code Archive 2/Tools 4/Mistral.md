---
modified: 2026-04-18T06:32:48+03:00
---
**1. Mistral Vibe Compatibility** Mistral Vibe operates primarily on Mistral’s specialized coding models (like Devstral 2), but it is natively compatible with the broader Mistral ecosystem. Because it is highly configurable via its `config.toml` file, you can customize the underlying models, providers, and tool permissions. As long as the endpoint is configured correctly, Vibe can route tasks to different Mistral models depending on the complexity of the command.

**2. Free Tier Model Restrictions** Mistral’s "Experiment Tier" (the free key) does **not** restrict access to specific models. You get access to the entire roster, including their latest Small, Large, and Code models, without requiring a credit card. The restriction is entirely based on throughput rather than capability:

- **Requests Per Second (RPS):** ~1 RPS
    
- **Requests Per Minute (RPM):** ~30 RPM This tier is highly effective for slow, methodical background planning or prototyping, but it will immediately bottleneck if an autonomous coding agent attempts to run a rapid, multi-file execution loop.
    

**3. Codestral API vs. Standard Mistral API Limits** Yes, they operate entirely independently. Mistral established two separate routing structures:

- **`api.mistral.ai` (Standard):** This is the core API where queries (including Codestral requests) are bound by your standard organization rate limits and billed per token.
    
- **`codestral.mistral.ai` (IDE/Plugin Endpoint):** This is a dedicated endpoint built specifically for IDE extensions using Instruct or Fill-In-the-Middle (FIM) routing. The API key for this endpoint is managed at the personal level and **is not bound** by the usual organizational rate limits. Mistral often uses this parallel endpoint to offer free beta periods specifically to encourage developers to build local coding plugins.