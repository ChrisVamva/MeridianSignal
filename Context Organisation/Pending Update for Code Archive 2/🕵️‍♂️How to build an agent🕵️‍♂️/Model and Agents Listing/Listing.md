---
modified: 2026-04-18T20:09:14+03:00
---
Nemotron 3 Super (free) OpenRouter
Gemini 2.5 Pro Google
Kilo Auto Free Kilo Gateway
Qwen 3 235B Instruct Cerebras
Gemini Flash-Lite Latest Google
xAI: Grok Code Fast 1 Optimized (experimental, free)
qwen3-coder: 480b Ollama Cloud
devstral-small-2:24b Ollama Cloud
devstral-2:123b Ollama Cloud
MiniMax M2.5 Free OpenCode Zen
Big Pickle OpenCode Zen
Nemotron 3 Super Free OpenCode Zen
Gemma 4 31B (free) OpenRouter
Elephant (free) OpenRouter

### 🧠 Tier 1: The Heavyweight Architects

_These are your slow, deep-thinking state machines. The router only wakes them up for complex logic, multi-file refactoring, or architectural planning._

- **`qwen3-coder: 480b` (Ollama Cloud)**
    
- **`Qwen 3 235B Instruct` (Cerebras)**
    
- **`devstral-2: 123b` (Ollama Cloud)**
    
- **`Gemini 2.5 Pro` (Google)**
    

### ⚡ Tier 2: The High-Speed Snipers

_These are your sub-second executors. The router blasts 80% of your daily workload to these models: syntax fixing, log reading, and basic component generation._

- **`devstral-small-2: 24b` (Ollama Cloud)**
    
- **`Gemini Flash-Lite Latest` (Google)**
    
- **`Grok Code Fast 1 Optimized` (xAI)**
    
- **`Gemma 4 31B` (OpenRouter)**
    

### 🛡️ Tier 3: The Exotic Fallbacks (Zero-Downtime Insurance)

_If Mistral or Ollama Cloud throws a rate limit, the router silently redirects to these without you ever noticing a hiccup in your terminal._

- **`Nemotron 3 Super` (OpenRouter / OpenCode Zen)**
    
- **`Kilo Auto Free` (Kilo Gateway)**
    
- **`MiniMax M2.5`, `Big Pickle`, `Elephant` (OpenRouter / Zen)**
    

### ⚙️ The Power of the Proxy

When you have a roster this deep, hardcoding them into OpenCode one by one is holding you back. If you drop LiteLLM in the middle, you just create a single endpoint called `model="orange-tomato-auto"`.

You tell the router: _"Try Flash-Lite first. If the prompt is over 10,000 tokens, dynamically route it to Devstral-2. If Devstral-2 is rate-limited, failover to Qwen 3 235B."_ Your agents never stop working, and your wallet never opens. You get the uptime of an enterprise data center using purely open-weight and free-tier infrastructure.