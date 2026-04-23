# Dev's Memory — Project Report Summary
_Compiled from: CORE FEATURES, Product Evaluation, The Plan Forward,
Performance Report, Merge Assessment, cd .devs-memory. April 2026._

---

## WHAT DEV'S MEMORY IS

A desktop-first command cheatsheet and snippet manager.
Built in Electron + React. Local-first: data stored in `data.json` on disk.
Highly stylised — warm paper aesthetic, Caveat handwriting font, ruled lines,
tree view canvas, Game Boy system stats widget.

**Repo location:** `C:\Users\user\Dev's Memory\devs-memory\`
**Build command:** `npm run dist` → produces `.exe` in `release\`
**Daily use command:** run the packaged `.exe`, not `npm run start`

---

## WHAT IT ACTUALLY DOES (VERIFIED FEATURES)

### Core functionality
- Add / rename / delete categories (appear in sidebar)
- Add / edit / delete / copy commands (card grid view)
- Persistent storage — data survives app restart
- Dark mode toggle

### Styling system
- Per-category colour + font picker
- Live preview in modal
- "Apply to all cards" or "title only" on save
- Coloured titles readable in dark mode

### Notebook
- Per-category notes (ruled paper modal)
- Notes persist independently per category

### Tree view
- Visual canvas of nodes and branches
- Drag-and-drop node repositioning
- Copy command from node to clipboard

### Global search
- `Ctrl+Shift+M` opens floating spotlight window from anywhere in OS
- Fuzzy search by label or value
- Arrow key navigation, Enter copies, Esc closes

### Import / Export
- JSON export downloads `devs-memory-export.json`
- Import merges categories back in

### AI Inbox via MCP
- MCP server allows AI agents to push commands to the app programmatically
- Pending commands appear in `📥 AI Inbox` category with `pending: true` flag
- User can approve → command moves to target category
- Tested by injecting directly via Node script

### Game Boy widget
- Live CPU + RAM display
- Collapsible to GB pill, restorable
- OT logo → opens orange-tomato.com
- GitHub icon → opens GitHub in browser

---

## TECHNICAL STACK

| Layer | Technology |
|---|---|
| Desktop wrapper | Electron |
| Frontend | React + Vite |
| Styling | Warm paper aesthetic, Caveat font, ruled lines |
| Storage | Local `data.json` (AppData) |
| Agent integration | MCP (Model Context Protocol) server |
| System stats | `systeminformation` (flagged — see performance issues) |

---

## PERFORMANCE ISSUES (KNOWN)

**Root cause of fan noise / CPU spike in dev mode:**

1. **`systeminformation` library** — `currentLoad()` samples CPU activity over intervals.
   Stresses the CPU to measure the CPU. Primary fan culprit.

2. **Electron baseline** — ~150MB RAM + noticeable CPU idle just for the runtime.
   Unavoidable tax for using web tech on desktop.

3. **Dev mode (`npm run start`)** — runs Vite dev server AND Electron simultaneously.
   Vite watches all files for HMR. Significantly heavier than the built `.exe`.

4. **File watcher loop** — `fs.watch` on `data.json` fires on every write including
   writes the app itself makes. Can create: write → fire → re-render → write again.

**Fixes already identified:**
- Replace `systeminformation` with Node's built-in `os` module (RAM only, no CPU sampling)
- Use the packaged `.exe` for daily use — not `npm run start`
- Debounce file watcher to max once per second

---

## PRODUCT EVALUATION (vs market)

**Compared against:** SnippetsLab, massCode, Pieces, Raycast/Alfred

**Strengths that differentiate:**
- **MCP server integration** — biggest superpower. No competitor does this.
  Dev's Memory acts as a shared context bridge between human developer and AI tools
  (Claude Desktop, Cursor, etc.). Agents can read and write the cheatsheet.
- **Visual identity** — warm paper aesthetic, Game Boy widget. Feels personal and made.
  Rare in developer tooling. Worth protecting.
- **Local-first** — no cloud dependency, fast, private.
- **Simplicity** — not trying to be an IDE. Tightly focused on labelled commands.

**Weaknesses vs market:**
- Search relies on manual category navigation — top tools use global fuzzy search
- Only handles simple string values — competitors support multi-line, syntax-highlighted,
  parameterised snippets (`git commit -m "{message}"`)
- No cross-machine sync

---

## COMPARISON WITH SHORTCUT DASHBOARD (v0-shortcut-dashboard)

The merge question was evaluated directly. Verdict:

> **Dev's Memory's aesthetic wins. The dashboard's architecture wins.**

Shortcut dashboard (Next.js + Tailwind + shadcn):
- Clean component architecture, TypeScript, Zustand state management
- Learning states per shortcut (new / learning / known / mastered)
- Excellent keycap component
- Weakness: generic design language — standard Linear/Raycast dark theme

Dev's Memory (Electron + Vite + React):
- Real visual identity: paper, Caveat, ruled lines, Game Boy
- Feels handmade and personal
- Weakness: weaker architecture, no learning states, no keycap component

**Recommended direction: bring dashboard strengths INTO Dev's Memory's world.**
Not the other way around. Specifically:
- Adopt the keycap component for displaying shortcuts in Dev's Memory
- Add learning state concept as optional tag on commands
- Keep paper aesthetic as unified visual language
- Dashboard dark mode should adopt Dev's Memory's warm dark ink palette,
  not the cold blue-grey it currently uses

---

## FEATURE ROADMAP (prioritised)

### Immediate / quick wins
1. **Global search shortcut** — `Ctrl+Shift+M` floating window (already built)
   *Highest daily value. Electron `globalShortcut` API. Already done.*

2. **AI Inbox** — reserved category, `pending: true` flag, MCP pushes to it
   *Already 80% there with current MCP setup.*

3. **Import/Export JSON** — trivially serialise/deserialise data.json
   *Already done per core features.*

4. **Expand Game Boy** — command history, mini-mode on desktop
   *Pure UI addition.*

### Medium effort (very doable)
5. **Parameterised commands** — detect `<placeholder>` patterns on copy,
   show inline form to fill before copying.

6. **Syntax highlighting** — swap `<textarea>` in CommandCard for CodeMirror.
   A day's work. Language dropdown. Tree-sitter based, lightweight.

7. **Contextual tags on MCP** — add `tags` array to command schema,
   expose in MCP tools, render as pills in UI.

### Larger but realistic
8. **Markdown / folder-based storage** — categories as folders, commands as `.md` files.
   Git-friendly, version-controllable, readable by other tools.
   Biggest real differentiator from all competitors.

9. **Cross-machine sync via Git** — follows naturally from folder-based storage.
   Sync button in UI that shells out to git push/pull.

10. **Global floating window** — second `BrowserWindow` in Electron, stays on top.
    Needs careful UX so it doesn't feel clunky.

---

## STATUS

| Item | Status |
|---|---|
| Core app (CRUD, persistence) | ✅ Built and verified |
| Styling system | ✅ Built and verified |
| Notebook | ✅ Built and verified |
| Tree view | ✅ Built and verified |
| Global search `Ctrl+Shift+M` | ✅ Built and verified |
| Import/Export | ✅ Built and verified |
| AI Inbox via MCP | ✅ Built and verified |
| Game Boy widget | ✅ Built and verified |
| Performance fix (systeminformation) | 🔲 Identified, not yet implemented |
| Parameterised commands | 🔲 Designed, not built |
| Syntax highlighting (CodeMirror) | 🔲 Designed, not built |
| Folder-based storage | 🔲 Designed, not built |
| Merge with shortcut dashboard | 🔲 Strategy defined — keycaps + learning states into Dev's Memory |
| Tauri migration | 🔲 Not yet evaluated |

---

## THE ONE-LINE VERDICT

Dev's Memory is a real product with genuine identity and a unique MCP superpower.
The architecture needs hardening before expansion.
The aesthetic must be preserved as the unifying visual language across all merged repos.
