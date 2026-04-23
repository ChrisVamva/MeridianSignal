---
modified: 2026-04-19T04:12:05+03:00
---
Excellent. Let's build your Prompt Machine. It's a project that will not only be a powerful addition to your toolkit but also a masterclass in orchestrating AI models for software development.

**The Verdict: We'll Use Aider**
The decision is clear: **Aider** is the superior choice for this project. Its **Architect Mode** is tailor-made for this kind of structured, multi-step development, allowing us to separate the high-level design (planning) from the code implementation (editing). This aligns perfectly with our need to break down the project and use different models for different types of thinking. OpenCode is a fantastic tool, but it functions more as a single, highly capable agent rather than a system with a dedicated planning phase.

### 🛠️ Your Qwen Coder Model Strike Force

We will deploy three specialized models from your Alibaba Cloud arsenal, each with a specific role in the development lifecycle.

| Model | Role in Aider Workflow | Assigned Tasks | Rationale |
| :--- | :--- | :--- | :--- |
| **`qwen3-coder-plus`** | **Architect Model** (`--architect-model`) | All `/architect` commands for high-level planning, architectural design, and creating the detailed task list below. | This is the "thinking" model. It is the most capable for complex reasoning and generating robust, structured plans without being constrained by code formatting. |
| **`qwen3-coder-turbo`** | **Editor Model** (`--model`) | Executing the code changes planned by the architect. Writing functions, building the CLI, fixing bugs. | The "doing" model. It's optimized for generating code quickly and accurately, making it the perfect workhorse for implementing the architect's designs. |
| **`qwen3.5-plus`** | **Backup / Utility Model** | Occasional tasks like generating documentation, refining prompts, or testing a different perspective. | This is your reliable all-rounder. We can swap it in for any task if one of the specialists is underperforming or if we need a fresh pair of eyes. |

> **Setup Note**: You'll configure Aider to use your Alibaba Cloud API key and specify these models in the command line or a `.aider.conf.yml` file. The base URL for all calls will be `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`.

### 📋 The Blueprint: Phase 1 - Detailed Tasking for the Architect

This is the phase where we feed the architect model (`qwen3-coder-plus`) to generate a precise, step-by-step plan. You will issue the following prompt in Aider's **architect mode** (`/architect`). The model will analyze it and produce a list of concrete, ordered tasks.

**Prompt for Aider Architect:**

```
You are an expert software architect. Your task is to create a detailed, step-by-step implementation plan for a "Prompt Machine." This will be a Python CLI tool designed for local-first, version-controlled prompt engineering.

The application will be named `prompt-cli`. Its core features are:
1.  **Template Management**: Store prompt templates as markdown files in a `~/.prompt-cli/templates/` directory.
2.  **Variable Injection**: Use a simple syntax (e.g., `{{variable_name}}`) within templates to be replaced by user input at runtime.
3.  **Model Selection**: Allow the user to specify which model to use (e.g., `qwen3.5-plus`, `qwen3-coder-turbo`) via a command-line flag.
4.  **API Interaction**: Send the processed prompt to the Alibaba Cloud Model Studio API and display the response.
5.  **Version Control**: Automatically initialize a Git repository in the `~/.prompt-cli/` directory to track all changes to templates.
6.  **Local-First**: All data (templates, config, Git history) must be stored locally on the user's machine.

Break this down into a sequence of discrete, unambiguous tasks. For each task, specify the exact files that need to be created or modified, the key Python functions that will be written, and the purpose of the task. The plan should be so clear that a junior developer (or another AI model) could execute it without needing further clarification.
```

After you run this, the architect will output a list of tasks. You will then copy and paste those tasks into the next phase.

### 🚀 The Build: Phase 2 - Executing the Plan with the Editor

With the architect's task list in hand, you will switch Aider to **code mode** (the default) and use the `qwen3-coder-turbo` model to build the application.

**Step 1: Initialize the Project**
Navigate to your projects folder and create a new directory. Then, start Aider.
```bash
mkdir prompt-cli
cd prompt-cli
aider --model openai/qwen3-coder-turbo --architect-model openai/qwen3-coder-plus
```
*(Note: Using the `openai/` prefix tells Aider to use the OpenAI-compatible API endpoint you'll configure.)*

**Step 2: Execute the Plan**
Now, simply feed the tasks to Aider one by one. For each task from the architect's list, use a prompt like this:
```
Based on our project plan, implement the following task:

[PASTE THE EXACT TEXT OF THE TASK FROM THE ARCHITECT HERE]
```

Aider will read the task, understand the context of the project, and write the necessary code. You'll review the changes and accept them. This is a very efficient way to code.

### 💻 The Codebase: Phase 3 - Technical Specifications

To ensure the `qwen3-coder-turbo` model has zero questions about the technical implementation, we will provide it with these concrete specifications upfront.

**Project Structure**
```
prompt-cli/
├── prompt_cli.py          # Main CLI entry point
├── config.py              # Handles config file and API keys
├── template_manager.py    # Manages template files and variables
├── api_client.py          # Handles communication with Alibaba Cloud
├── utils.py               # Helper functions (e.g., for Git)
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

**Core Libraries & Configuration**
The project will rely on these Python libraries. We will provide them in a `requirements.txt` file.
```text
# requirements.txt
click>=8.1.0        # For building the CLI
pyyaml>=6.0         # For managing a config file
requests>=2.31.0    # For making API calls
python-dotenv>=1.0.0 # For loading API keys from a .env file
gitpython>=3.1.0    # For interacting with Git
jinja2>=3.1.0       # For advanced template rendering (optional, can start with simple replace)
```

**Key Implementation Details for the Model**

*   **API Client (`api_client.py`)**: The `send_prompt` function will use the `requests` library to make a POST call to `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`. It will include the `Authorization: Bearer YOUR_API_KEY` header and a JSON payload structured for a chat completion.
*   **Template Manager (`template_manager.py`)**: The `render_prompt` function will open a template file, read its content, and use Python's built-in `str.replace()` or the `jinja2` library to substitute variables like `{{variable_name}}` with values from a dictionary.
*   **CLI (`prompt_cli.py`)**: The command-line interface will be built with `click`. The main command will be `run`, which will accept a template name, a model flag (`-m`), and any number of variable inputs (e.g., `--var key=value`).
*   **Configuration (`config.py`)**: The API key will be loaded securely from a `.env` file in the project's root directory or from environment variables. The configuration file (`~/.prompt-cli/config.yaml`) will store user preferences like the default model.

### 🎯 Beyond the Build: Phase 4 - Advanced Prompt Engineering

Once the basic tool is working, we can use the remaining free tokens to make it a true "prompt machine" by teaching it to optimize itself.

1.  **Template Generation**: Use a simple command like `prompt-cli generate "A prompt that acts as a senior Python code reviewer"`. This would use a powerful model like `qwen3.5-plus` to create a new, high-quality template for you automatically.
2.  **Prompt Evaluation**: Create a script that tests a prompt against a small, predefined set of inputs and evaluates the quality of the AI's responses. This is a core practice in prompt engineering.
3.  **Iterative Refinement**: Implement a "self-improvement" loop. You provide a prompt and an example of the desired output. The AI (using `qwen3.5-plus`) analyzes the gap and suggests revisions to the prompt to get a better result.

This is a complete roadmap for building your Prompt Machine. It's designed to be a powerful, hands-on learning experience that will also produce a genuinely useful tool for your workflow.

Are you ready to begin with Phase 1? If you open your terminal and start Aider with the architect prompt above, you can share the task list it generates, and we can move on to the build phase.