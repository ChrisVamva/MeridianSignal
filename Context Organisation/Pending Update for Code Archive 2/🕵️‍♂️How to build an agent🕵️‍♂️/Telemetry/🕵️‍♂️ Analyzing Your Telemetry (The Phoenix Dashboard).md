---
modified: 2026-04-20T03:20:27+03:00
---
### 🕵️‍♂️ Analyzing Your Telemetry (The Phoenix Dashboard)

Open `http://localhost:6006` and click on the **Traces** icon on the left sidebar (it looks like a few horizontal lines or a list).

Click on the top row (your interrupted Nemotron test) to open the **Trace Details** panel. Here is your x-ray vision:

**1. The Span / Waterfall View**

- Look at the top of the details panel. You will see a horizontal bar representing the timeline of the request.
    
- This shows you the **Latency** (how many seconds Nemotron was spinning its wheels before you killed it). In the future, this is how you will hunt down slow models that are bottlenecking your agents.
    

**2. The Input & Output Payload**

- Scroll down to the **Attributes** or **Metadata** section.
    
- Look for `input.value` (or `llm.prompt`). You will see the exact JSON payload OpenCode sent to LiteLLM. This is incredibly valuable for debugging agents, because you can see the _hidden system prompts_ OpenCode uses behind the scenes.
    
- Look at `output.value`. Since you interrupted it, it might be blank, or it might show a partial chunk of its infinite thinking loop.
    

**3. Token Economics (The Most Important Metric)**

- Find the fields labeled `llm.token_count.prompt` and `llm.token_count.completion`.
    
- Even though this was a free model, Phoenix tracks this. When you eventually use paid APIs (like Anthropic or deep datacenter models), this exact section tells you if a model is burning your budget by writing unnecessary code comments or bloated JSON.
    

**4. The Status Code**

- Look for the HTTP status. Because you interrupted it, LiteLLM likely recorded a `499` (Client Closed Request) or a similar abort code, perfectly capturing the fact that _you_ killed the connection, not the server.