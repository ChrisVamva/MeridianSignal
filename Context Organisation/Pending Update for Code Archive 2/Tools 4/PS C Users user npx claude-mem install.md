---
modified: 2026-04-17T01:09:53+03:00
---
PowerShell 7.6.0
PS C:\Users\user> npx claude-mem install
Need to install the following packages:
claude-mem@12.1.6
Ok to proceed? (y) y
T   claude-mem install
|
•  Version: 12.1.6
|
•  Platform: win32 (x64)
|
o  Which IDEs do you use?
|  Claude Code, Gemini CLI, OpenCode, OpenClaw, Windsurf, Codex CLI, Cursor, Antigravity
|
o  Plugin files copied OK
|
o  Plugin cached (v12.1.6) OK
|
o  Marketplace registered OK
|
o  Plugin registered OK
|
o  Plugin enabled OK
|
o  Dependencies may need manual install !
|
🔧 Bun not found. Installing Bun runtime...
   Installing via PowerShell...
##O#-  #                                                                                                               curl: (35) schannel: next InitializeSecurityContext failed: CRYPT_E_NO_REVOCATION_CHECK (0x80092012) - Δεν ήταν δυνατός ο έλεγχος της ανάκλησης του πιστοποιητικού από τη συνάρτηση ανάκλησης.

✅ Bun 1.3.12 installed successfully
📦 Installing dependencies with Bun...
warn: incorrect peer dependency "tree-sitter@0.21.1"
  ⚙️  tree-sitter-cli [5/5] warn: tree-sitter-cli's postinstall cost you 30.8s
✅ Dependencies installed
[claude-mem] Plugin updated to v12.1.6 - restarting worker...
✅ PowerShell function added to profile
   Restart your terminal to use: claude-mem <command>
{"continue":true,"suppressOutput":true}
(node:18520) [DEP0190] DeprecationWarning: Passing args to a child process with shell option true can lead to security vulnerabilities, as the arguments are not escaped, only concatenated.
(Use `node --trace-deprecation ...` to show where the warning was created)
o  Runtime dependencies ready OK
√ Marketplace 'thedotmack' already on disk — declared in user settings
√ Successfully installed plugin: claude-mem@thedotmack (scope: user)
|
*  Claude Code: plugin installed via CLI.

Installing Claude-Mem Gemini CLI hooks...

  Using Bun runtime: C:\Users\user\.bun\bin\bun.exe
  Worker service: C:\Users\user\.claude\plugins\marketplaces\thedotmack\plugin\scripts\worker-service.cjs
  Merged hooks into C:\Users\user\.gemini\settings.json
  Setup context injection in C:\Users\user\.gemini\GEMINI.md
  Registered 8 hook events:
    SessionStart → context
    BeforeAgent → session-init
    AfterAgent → observation
    BeforeTool → observation
    AfterTool → observation
    PreCompress → summarize
    Notification → observation
    SessionEnd → session-complete

Installation complete!

Hooks installed to: C:\Users\user\.gemini\settings.json
Using unified CLI: bun worker-service.cjs hook gemini-cli <event>

Next steps:
  1. Start claude-mem worker: claude-mem start
  2. Restart Gemini CLI to load the hooks
  3. Memory will be captured automatically during sessions

Context Injection:
  Context from past sessions is injected via ~/.gemini/GEMINI.md
  and automatically included in Gemini CLI conversations.

|
*  Gemini CLI: hooks installed.

Installing Claude-Mem for OpenCode...

Could not find built OpenCode plugin bundle.
  Expected at: dist/opencode-plugin/index.js
  Run the build first: npm run build
|
x  OpenCode: plugin installation failed.

Installing Claude-Mem for OpenClaw...

  Plugin dist copied to: C:\Users\user\.openclaw\extensions\claude-mem\dist
  Plugin manifest copied to: C:\Users\user\.openclaw\extensions\claude-mem\openclaw.plugin.json
  Skills copied to: C:\Users\user\.openclaw\extensions\claude-mem\skills
  Registered in openclaw.json

Installation complete!

Plugin installed to: C:\Users\user\.openclaw\extensions\claude-mem
Config updated: C:\Users\user\.openclaw\openclaw.json

Next steps:
  1. Start claude-mem worker: npx claude-mem start
  2. Restart OpenClaw to load the plugin
  3. Memory capture is automatic from then on

|
*  OpenClaw: plugin installed.

Installing Claude-Mem Windsurf hooks (user level)...

  Using Bun runtime: C:\Users\user\.bun\bin\bun.exe
  Worker service: C:\Users\user\.claude\plugins\marketplaces\thedotmack\plugin\scripts\worker-service.cjs
  Created/merged hooks.json
[SETTINGS] Created settings file with defaults: C:\Users\user\.claude-mem\settings.json
  Generating initial context...
  Created placeholder context file (will populate after first session)
  Registered for auto-context updates

Installation complete!

Hooks installed to: C:\Users\user\.codeium\windsurf\hooks.json
Using unified CLI: bun worker-service.cjs hook windsurf <command>

Events registered:
  - pre_user_prompt      (session init + context injection)
  - post_write_code      (code generation observation)
  - post_run_command     (command execution observation)
  - post_mcp_tool_use    (MCP tool results)
  - post_cascade_response (full AI response)

Next steps:
  1. Start claude-mem worker: claude-mem start
  2. Restart Windsurf to load the hooks
  3. Context is injected via .windsurf/rules/claude-mem-context.md (workspace-level)

|
*  Windsurf: hooks installed.

Installing Claude-Mem for Codex CLI (transcript watching)...

  Updated C:\Users\user\.claude-mem\transcript-watch.json
  Watch path: ~/.codex/sessions/**/*.jsonl
  Schema: codex (v0.3)

Installation complete!

Transcript watch config: C:\Users\user\.claude-mem\transcript-watch.json
Context files: <workspace>/AGENTS.md

How it works:
  - claude-mem watches Codex session JSONL files for new activity
  - No hooks needed -- transcript watching is fully automatic
  - Context from past sessions is injected via AGENTS.md in the active Codex workspace

Next steps:
  1. Start claude-mem worker: npx claude-mem start
  2. Use Codex CLI as usual -- memory capture is automatic!

|
*  Codex CLI: transcript watching configured.

Installing Claude-Mem Cursor hooks (user level)...

  Using Bun runtime: C:\Users\user\.bun\bin\bun.exe
  Created hooks.json (unified CLI mode)
  Worker service: C:\Users\user\.claude\plugins\marketplaces\thedotmack\plugin\scripts\worker-service.cjs

Installation complete!

Hooks installed to: C:\Users\user\.cursor/hooks.json
Using unified CLI: bun worker-service.cjs hook cursor <command>

Next steps:
  1. Start claude-mem worker: claude-mem start
  2. Restart Cursor to load the hooks
  3. Check Cursor Settings → Hooks tab to verify

Context Injection:
  Context from past sessions is stored in .cursor/rules/claude-mem-context.mdc
  and automatically included in every chat. It updates after each session ends.

  Configured MCP server in ~/.cursor/mcp.json
    Server path: C:\Users\user\.claude\plugins\marketplaces\thedotmack\plugin\scripts\mcp-server.cjs
|
*  Cursor: hooks + MCP installed.

Installing Claude-Mem MCP integration for Antigravity...


Installation failed: Corrupt JSON file, refusing to overwrite: C:\Users\user\.gemini\antigravity\mcp_config.json
|
x  Antigravity: MCP integration failed.
|
o  Installation Partial -------------------------------------------------------------------------------+
|                                                                                                      |
|  Version:     12.1.6                                                                                 |
|  Plugin dir:  C:\Users\user\.claude\plugins\marketplaces\thedotmack                                  |
|  IDEs:        claude-code, gemini-cli, opencode, openclaw, windsurf, codex-cli, cursor, antigravity  |
|  Failed:      opencode, antigravity                                                                  |
|                                                                                                      |
+------------------------------------------------------------------------------------------------------+
|
o  Next Steps --------------------------------------------------------+
|                                                                     |
|  Open Claude Code and start a conversation -- memory is automatic!  |
|  View your memories: http://localhost:37777                         |
|  Search past work: use /mem-search in Claude Code                   |
|  Start worker: npx claude-mem start                                 |
|                                                                     |
+---------------------------------------------------------------------+
|
—  claude-mem installed with some IDE setup failures.
