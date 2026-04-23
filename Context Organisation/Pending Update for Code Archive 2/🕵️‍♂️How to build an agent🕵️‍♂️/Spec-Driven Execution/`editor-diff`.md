---
modified: 2026-04-18T23:15:00+03:00
---
In this specific context (AI-assisted coding tools like Aider, Cursor, or Continue), **diff** refers to a **file editing strategy**, not just the comparison tool.

Here is the exact meaning of the terms `editor-diff` and `editor-whole` as referenced in your snippet:

### 1. `editor-diff` (Search & Replace / Patching)
- **What the AI does:** It analyzes the existing file and outputs only the **changes** in **Unified Diff Format** (the same format we discussed earlier with `-` and `+` lines and `@@` headers).
- **Example Output:**
    ```diff
    @@ -15,7 +15,7 @@
     def calculate_total(items):
    -    tax = 0.05
    +    tax = 0.08
         return sum(items) * (1 + tax)
    ```
- **Why it's used:** It saves tokens (cheaper/faster) and prevents accidentally overwriting unrelated parts of a large file.
- **The Catch:** The AI must be **extremely precise** with the surrounding context lines and line numbers. If the AI hallucinates a line number or a space, the `patch` application fails with *"Search block not found."*

### 2. `editor-whole`
- **What the AI does:** It outputs the **entire content** of the file from scratch, incorporating the changes.
- **Why it's used:** It is **foolproof**. It never fails due to "matching" errors because it just overwrites the file completely.
- **The Trade-off:** It is **much more expensive**. If you ask to change one line in a 2,000-line file, `editor-whole` forces the AI to re-type (and you to pay for) the other 1,999 lines.

### Summary of Your Snippet's Logic

| Mode | Best For | Risk |
| :--- | :--- | :--- |
| **editor-diff** | Strong models (Claude, GPT-4o, DeepSeek V3, Codestral) | **High precision required.** Bad models mess up the line numbers. |
| **editor-whole** | Weak/local models (Qwen 8B fallback, Unknown models) | **High cost / Slow.** But it **always works**. |

The note *"Smaller models struggle with exact search block matching"* refers directly to the `@@` header in the diff. A small local model might generate `@@ -15,7 +15,7 @@` when the actual code is on line 14, causing the editor tool to crash.