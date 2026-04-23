---
modified: 2026-04-17T07:07:49+03:00
---
Yes, you can run OpenCode inside your IDE's terminal. It's built for this kind of workflow, and it works quite seamlessly across different environments.

Here's a quick guide for the most popular IDEs:

### 🛠️ VS Code (and Cursor, Windsurf, VSCodium)

This is the most streamlined experience. Simply open the integrated terminal and run the `opencode` command; the necessary extension will be installed automatically. If it fails, check that your IDE's CLI (like the `code` command for VS Code) is correctly installed in your system's PATH.

*   **Quick Launch**: `Cmd+Esc` (macOS) / `Ctrl+Esc` (Win/Linux)
*   **New Session**: `Cmd+Shift+Esc` (macOS) / `Ctrl+Shift+Esc` (Win/Linux)

> **🪟 A Note for Windows Users**
> If you're on Windows, the default terminal is `cmd.exe`, which can cause issues with the extension. The recommended workaround is to use WSL 2 (Windows Subsystem for Linux). This gives you a native Ubuntu environment that's tightly integrated with Windows and where OpenCode will run without any problems.

### 🧩 JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)

You have two solid options for JetBrains IDEs:

1.  **The Native Plugin (Recommended)**: Install the "OpenCode" plugin from the JetBrains Marketplace. This provides a fully integrated AI terminal interface and gives you a seamless, native experience.
2.  **The Built-in Terminal**: Alternatively, you can just run `opencode` in the IDE's integrated terminal (`Alt+F12`). However, you might run into minor issues with typing or pasting multiline commands.

### 💻 Neovim / Vim / Emacs / Any Terminal-Based Editor

For terminal-based editors, just open a new terminal pane and run the `opencode` command to start an interactive session. OpenCode's creators are Neovim users, so the terminal user interface (TUI) is built to feel fast and native.

### ✨ Extra Tip: The Interactive TUI

No matter which IDE you use, you can always use OpenCode's powerful interactive TUI, which is packed with features for managing sessions, selecting models, and more. For example, you can press `Ctrl+E` to open your message in your preferred external editor (set by the `$EDITOR` environment variable) for more complex prompts.

It's designed to be a terminal-first tool, so it integrates with nearly any development setup.