---
modified: 2026-04-11T16:10:13+03:00
---
Great evaluation — and yes, every single one of these is buildable. Let me give you an honest assessment of each:

**Straightforward, we can do these soon:**

- Global search / command palette — Electron has a `globalShortcut` API, we register `Ctrl+Shift+M`, open a small frameless window with a fuzzy search input. A few hours of work.
- Import/Export (JSON) — trivial, just serialize/deserialize the data.json. CSV and basic massCode JSON format are also easy to map.
- "Suggested by AI" Inbox — just a reserved category with a `pending: true` flag. The MCP server pushes to it, the UI shows a badge. Already 80% there with the current MCP setup.
- Expand the Game Boy — command history and a mini-mode are purely UI additions on top of what's already there.

**Medium effort, very doable:**

- Syntax highlighting — swap the `<textarea>` in CommandCard for CodeMirror (lightweight, tree-sitter based). A day's work. Monaco is heavier but also possible.
- Parameterized commands — detect `<placeholder>` patterns on copy, show a small inline form to fill them in before copying. Clean, self-contained feature.
- Contextual tags on MCP — add a `tags` array to the command schema, expose it in the MCP tools. The UI just renders them as small pills.

**Bigger but realistic:**

- Markdown/folder-based storage — restructuring from `data.json` to `categories/<name>/commands/<label>.md` is a meaningful refactor but the MCP server and file watcher already abstract the storage layer, so it's mostly a rewrite of the read/write functions. Git-friendliness would be a real differentiator.
- Cross-machine sync via Git — with the folder-based storage above, this becomes `git push/pull` on the data directory. We could even add a sync button in the UI that shells out to git.
- Global floating window — requires a second `BrowserWindow` in Electron that stays on top. Doable, just needs careful UX design so it doesn't feel clunky.

**What I'd prioritize first:**

1. Global search shortcut — highest daily value, relatively quick
2. Parameterized commands — makes the tool genuinely more powerful
3. AI Inbox — completes the MCP story and makes the agent integration feel intentional
4. Syntax highlighting — polish that matches the quality of the rest of the UI

Want to start on any of these now?