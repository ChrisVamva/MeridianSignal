---
modified: 2026-04-11T16:29:27+03:00
---
Here's a practical checklist you can run through manually, feature by feature:

**Core app**

```javascript
✓ Add a new category → appears in sidebar
✓ Rename a category → name updates
✓ Delete a category → removed from sidebar
✓ Add a command → card appears in grid
✓ Edit a command → label/value updates
✓ Delete a command → card disappears
✓ Copy a command → paste in terminal to verify
✓ Restart the app → all data still there (persistence check)
```

**Styling**

```javascript
✓ Click 🎨 on a category → modal opens
✓ Pick a color + font → preview updates live
✓ Save → "apply to all cards?" prompt appears
✓ Choose "Title only" → only header changes
✓ Choose "Yes, apply all" → cards tint too
✓ Dark mode toggle → whole app switches, colored titles still readable
```

**Notebook**

```javascript
✓ Click 📓 → modal opens with ruled paper
✓ Type a note, save → reopen, note persists
✓ Different categories have independent notes
```

**Tree view**

```javascript
✓ Click 🌿 → canvas appears with nodes and branches
✓ Drag a node → repositions freely
✓ Click ⎘ on a command node → copies to clipboard
✓ Click ▦ → back to card view
```

**Global search**

```javascript
✓ Press Ctrl+Shift+M anywhere → spotlight window opens
✓ Type part of a command label or value → results filter
✓ Arrow keys navigate, Enter copies, Esc closes
```

**Import / Export**

```javascript
✓ Click ⇅ Import / Export in sidebar
✓ Export → downloads devs-memory-export.json
✓ Open the file → valid JSON with your categories
✓ Delete a category, then Import the file → category comes back (merge)
```

**AI Inbox via MCP**

Open a terminal and run this directly to simulate an agent suggestion:

```bash
node -e "
const fs = require('fs');
const p = process.env.APPDATA + '/devs-memory/data.json';
const data = JSON.parse(fs.readFileSync(p));
let inbox = data.find(c => c.inbox);
if (!inbox) { inbox = { id: 'inbox1', name: '📥 AI Inbox', commands: [], style: { color: '#d4c4e8' }, note: '', inbox: true }; data.push(inbox); }
inbox.commands.push({ id: 'test1', label: 'Dev server', value: 'npm run dev', pending: true, suggestedCategory: 'Docker', reason: 'Useful for local development' });
fs.writeFileSync(p, JSON.stringify(data, null, 2));
console.log('Done');
"
```

Then check the app — `📥 AI Inbox` should appear with the pending card. Hit ✓ Approve and verify it moves to Docker.

**Game Boy**

```javascript
✓ Click the widget → stats screen shows CPU + RAM live
✓ Click − → collapses to GB pill
✓ Click GB pill → widget restores
✓ Click OT logo → orange-tomato.com opens in browser
✓ Click GitHub icon → github.com opens in b
```