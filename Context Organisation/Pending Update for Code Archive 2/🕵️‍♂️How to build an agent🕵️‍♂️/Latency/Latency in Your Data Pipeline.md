---
modified: 2026-04-20T07:29:01+03:00
---
### Latency in Your Data Pipeline

Since you are monitoring AI agents and models through a routing proxy, latency is not just one number. On your dashboard, it is typically broken down into a few highly specific metrics:

- **Time to First Token (TTFT):** The delay before the model starts "typing." This measures the time it takes for the request to travel from your machine to the datacenter, for the model to process your prompt, and for it to calculate and send back the very first word.
    
- **Time Between Tokens (TBT):** The speed at which the model streams the rest of the response. If this latency is high, the text stutters; if it is low, the generation flows smoothly.
    
- **Round-Trip Time (RTT):** The total, comprehensive time from the exact millisecond you hit "enter" to the moment the final piece of data arrives back on your screen.

### 1. The Infrastructure Route

Nemotron is running through `openrouter/nvidia/nemotron-3-super-120b-a12b:free`. You are hitting a free-tier proxy aggregator. Free endpoints often have lower rate limits, heavy traffic queues, and deprioritized compute. Devstral is now punching straight through to Mistral's direct, native, paid-tier API. Direct connections almost always win the race.

### 2. The Context Weight

Remember that JSON trace we looked at earlier? OpenCode silently jammed an **11,000-token system prompt** down Nemotron's throat just to ask "What is the capital of France?". That creates massive "Time to First Token" (TTFT) latency just to process the prompt. Vibe is likely sending a significantly leaner system prompt to Devstral.

### 3. The "Thinking" Tax

We saw Nemotron physically burn 57 reasoning tokens in a `Thinking:` block before it output the word "Paris." That internal monologue takes physical time to generate.

### 4. Dense vs. Mixture of Experts (MoE)

Mistral is famous for MoE architectures. Even if Devstral has 124 billion parameters total, it might only activate ~30 billion of them per token. If Nemotron is a dense model, it has to light up all 120 billion parameters for every single syllable. MoEs are mathematically designed to be blistering fast despite their massive total size.