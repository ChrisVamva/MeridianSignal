---
modified: 2026-04-17T09:06:47+03:00
---
OpenCode's ecosystem is vast, and while "best" is subjective, the community has rallied around certain standout plugins that solve common, critical needs.

For a quick, ready-to-run setup, you can use a "meta-plugin" like **`oh-my-opencode`**, which bundles many popular tools together.

For a more tailored experience, here are the top plugins organized by category:

### 🧠 Core Workflow & Productivity
These plugins enhance the fundamental way you interact with and direct your AI coding assistant.

| Plugin | What It Does | Why It's Recommended |
| :--- | :--- | :--- |
| **`@fro.bot/systematic`** | Instills a disciplined, multi-step engineering methodology (Plan → Work → Review). | It prevents the AI from jumping to conclusions, leading to higher quality, more maintainable code. It's inspired by the popular Compound Engineering Plugin for Claude Code. |
| **`opencode-warcraft`** | Enforces a "plan-first" workflow. You must create and approve a plan before the AI can execute tasks. | Ideal for complex features where a structured approach prevents the AI from going off-track and reduces wasted effort. |
| **`opencode-swarm`** | Turns a single AI session into a team of 11 specialized agents (architect, coder, reviewer, etc.) that collaborate on a task. | Excellent for larger projects, as it bakes in quality assurance with a built-in review and testing pipeline. |

### 🚀 Performance & Cost Optimization
Save time and money with these essential optimizers.

| Plugin | What It Does | Why It's Recommended |
| :--- | :--- | :--- |
| **`opencode-morph-plugin`** | Provides "Fast Apply" editing (10,500+ tokens/sec) and blazing-fast code search. | It dramatically speeds up file editing, which is one of the most common operations an AI agent performs. |
| **`opencode-dynamic-context-pruning`** | Automatically removes outdated or irrelevant information from the AI's conversation history. | Reduces token usage, which directly lowers your API costs and can improve response quality by keeping the context focused. |

### 💾 Memory & Context Management
The biggest limitation of LLMs is their lack of long-term memory. These plugins fix that.

| Plugin | What It Does | Why It's Recommended |
| :--- | :--- | :--- |
| **`opencode-supermemory`** | Provides a persistent memory store across all your sessions and projects. | The AI will remember your project's quirks, your preferences, and past decisions, creating a truly personalized and efficient assistant. |
| **`opencode-codebase-graph`** | Injects a live, structural map of your entire codebase into every AI prompt. | Gives the AI a deep understanding of how your files and modules relate to each other, leading to far better architectural suggestions. |
| **`Context7`** | Keeps the AI informed with up-to-date documentation for the libraries you're using. | Prevents the AI from hallucinating outdated or incorrect API usage. |

### 🔌 Integrations & Utilities
These plugins connect OpenCode to the rest of your world and make life easier.

| Plugin                           | What It Does                                                                                | Why It's Recommended                                                                          |
| :------------------------------- | :------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------- |
| **`opencode-openai-codex-auth`** | Lets you use your personal ChatGPT Plus/Pro subscription instead of paying for API credits. | A massive cost-saver for individuals who already pay for a subscription.                      |
| **`opencode-type-inject`**       | Automatically injects TypeScript/Svelte type definitions into your files.                   | Invaluable for TypeScript developers, leading to more accurate and type-safe code generation. |
| **`opencode-pty`**               | Allows the AI to run and interact with background processes in a pseudo-terminal.           | Essential for running dev servers, watchers, or any long-running interactive command.         |
| **`opencode-vibeguard`**         | Prevents the AI from accidentally writing secrets (API keys, etc.) into the chat or files.  | A crucial security layer for any developer.                                                   |

### 🌱 How to Get Started

Installing these plugins is generally straightforward. There are two main methods:

1.  **Via npm (Recommended for most)**: The simplest way. Just add the plugin name to the `plugins` array in your `opencode.json` config file.
    ```json
    {
      "plugins": [
        "@fro.bot/systematic", 
        "opencode-morph-plugin"
      ]
    }
    ```
    OpenCode will automatically download and install them when it starts up.

2.  **From a Local File**: For development or custom plugins, you can point to a local `.js` or `.ts` file.
    ```json
    {
      "plugins": [
        "file:///path/to/your/local/plugin.js"
      ]
    }
    ```
    You can also place the plugin file directly in the global `~/.config/opencode/plugins/` or project-specific `.opencode/plugins/` directory, and it will be loaded automatically.

### 🔍 Where to Discover More

The OpenCode ecosystem is growing fast. To stay up-to-date, check out these community resources:

*   **[awesome-opencode](https://github.com/awesome-opencode/awesome-opencode)**: A community-curated list of plugins, themes, agents, and more. This is the best place to start your discovery.
*   **[opencode.cafe](https://opencode.cafe)**: A dedicated community site that aggregates information about the OpenCode ecosystem.
*   **Official Docs**: The [OpenCode ecosystem page](https://opencode.ai/docs/ecosystem) lists many of the most popular official and community projects.

I hope this curated list helps you build a more powerful and productive OpenCode environment. What kind of project are you working on? Knowing more might help me suggest a more specific starting combination.