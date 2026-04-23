---
modified: 2026-04-19T18:57:08+03:00
---
### 🏛️ The Tactical Model Selection

#### 1. The Terminal Executor (The "Hands")

_For running commands, reading error logs, and writing standard boilerplate._

- **The Pick:** `qwen3-coder-flash` (or `qwen3.6-flash`)
    
- **Why:** Flash models are designed specifically for high-speed, high-volume, low-complexity tasks. When OpenCode needs to execute the `.bat` file creation or read through 50 lines of Windows PowerShell output, this model will process it in milliseconds and burn a fraction of the "cognitive load." It doesn't overthink; it just executes.
    

#### 2. The Architect (The "Brain")

_For writing the `config.yaml`, routing logic, and complex application structuring._

- **The Pick:** `qwen3-coder-480b-a35b-instruct`
    
- **Why:** Having a 480-billion parameter Mixture-of-Experts (MoE) coding model on a free quota is an absolute cheat code. You only wake this model up when you need flawless logic. You use it to draft the LiteLLM configuration file and the DSPy signatures. It will give you surgical, zero-shot accuracy.
    

#### 3. The Deep Reasoner (The "Failsafe")

_For when the system breaks and you need to debug a massive architectural failure._

- **The Pick:** `qwen3-235b-a22b-thinking` (or `qvq-max`)
    
- **Why:** These are the o1-class "Thinking" models. They use inner monologues to double-check their own logic before outputting text. You keep these in reserve. If the LiteLLM proxy suddenly throws a `401 Unauthorized` and you can't figure out why, you feed the stack trace to this model.