# Shady Clause Detector — Project Report Summary
_Compiled from 7 files. April 2026._

---

## WHAT SHADY CLAUSE DETECTOR IS

A contract analysis tool that reads legal agreements the way a hostile lawyer would.
Not "what does this say?" — "how could this be used against me?"

The core insight driving the product: most people sign contracts without reading them
because contracts are deliberately designed to be unreadable. TOS agreements,
employment contracts, freelance agreements, rental leases. The tool acts as an
adversarial reader — actively hunting for traps, not summarising text.

**Named persona:** "Legal Adversary"
**Core output:** A Risk Report with Red Flags, Yellow Flags, key dates, and a
Shady Score (0–100)

---

## THE THREE-LAYER ARCHITECTURE

### Layer 1 — Contract-Analysis-Engine (API / Infrastructure)
The reusable brain. All other layers call this.
- Input: PDF, DOCX, or TXT contract
- Output: Structured JSON risk report
- Privacy: zero persistence — data lives in session memory only, wiped on refresh
- Works standalone or as an OpenClaw agent tool

### Layer 2 — Lean Web Interface (Tool Layer)
Split-screen UI: original contract on the left, Risk Feed on the right.
Click a red flag → left side scrolls to the exact shady clause.
Aesthetic defined as: forensic/clinical — dark mode, high-contrast red highlights,
monospace fonts for contract text.
Prototype: Streamlit. Production: FastAPI + React.

### Layer 3 — Mobile Guardian (Consumer Layer)
Camera → OCR → Shady Score.
Use case: you're at a gym or rental office, snap a photo of a page, get immediate
flags. "Wait, Section 4.2 says they can raise rent by 20% without notice."
OCR via Tesseract.js (client-side — no image leaves the device).
Delivery: PWA → Capacitor → native iOS and Android app.

---

## THE RISK TAXONOMY (the secret sauce)

| Type | Example | Severity |
|---|---|---|
| 🚩 Red Flag | "User waives all rights to sue." | Critical |
| 🚩 Red Flag | "Non-compete extends to unrelated industries." | Critical |
| ⚠️ Yellow Flag | "30-day notice for cancellation." | Standard |
| ⚠️ Yellow Flag | "Automatic renewal unless 60 days notice given." | Standard |
| ℹ️ Info | "Rent increase effective January 1, 2027." | Low |
| ℹ️ Info | "Hidden fee: $25/month convenience charge." | Low |

**Priority clause types the adversarial prompt hunts for:**
- Non-competes
- Hidden fees
- Automatic renewals
- Liability shifts
- At-will traps
- IP ownership clauses
- Termination clauses

---

## CONTRACT TYPES IN SCOPE

| Contract Type | Audience | Key flags |
|---|---|---|
| Employment | Freelancers, remote workers | Non-competes, IP ownership, at-will traps |
| Freelance agreements | Independent contractors | Payment terms, scope creep, kill fees |
| Rental leases | Renters | Rent increases, subletting rules, auto-renewal |
| Service agreements | Small businesses | Hidden fees, liability waivers, data ownership |
| NDAs | Startups, employees | Confidentiality scope, non-compete, IP ownership |

---

## TECH STACK (full specification)

| Component | Tool | Why |
|---|---|---|
| Backend API | FastAPI | Lightweight, async, easy to deploy |
| PDF parsing | pdfplumber | Accurate, handles formatting |
| DOCX parsing | python-docx | Simple, reliable |
| OCR | Tesseract | Free, 100+ languages, client-side via Tesseract.js |
| LLM routing | LiteLLM | 100+ LLM providers in one library |
| Prompt testing | Promptfoo | Optimise adversarial persona, test edge cases |
| Frontend (prototype) | Streamlit | Quick to build, no frontend expertise needed |
| Frontend (production) | FastAPI + React | Scalable |
| Mobile | PWA + Capacitor | Single codebase → iOS + Android |
| Hosting (API) | Fly.io | Cheap, scalable, Docker-friendly |
| Hosting (frontend) | Vercel | Free CDN |

---

## THE JSON RESPONSE STRUCTURE

```json
{
  "contract_name": "Employment Agreement",
  "total_clauses": 25,
  "risk_summary": {
    "red": 3,
    "yellow": 5,
    "info": 17
  },
  "flags": [
    {
      "clause": "Section 4.2",
      "text": "Employee waives all rights to sue for any reason.",
      "flag": "red",
      "reason": "Extremely broad liability waiver.",
      "suggestion": "Remove or limit to specific, reasonable cases."
    }
  ]
}
```

---

## THE ADVERSARIAL PROMPT (core logic)

```
You are a Legal Adversary — a ruthless contract reviewer whose sole purpose
is to find clauses that could be used against the user.

Rules:
1. Never summarise. Always ask: "How could this be used against me?"
2. Flag: Red (legally dangerous), Yellow (unfavorable but standard), Info (key dates/amounts)
3. Return structured JSON with risk_score, red_flags, yellow_flags, key_dates
4. Prioritise: non-competes, hidden fees, automatic renewals, liability shifts,
   at-will traps, IP ownership, termination clauses
```

---

## BUILD PLAN (fully specified)

| Phase | Duration | Milestone |
|---|---|---|
| Phase 1: Core Engine | 2 weeks | FastAPI live, returns structured risk JSON |
| Phase 2: Web Interface | 1 week | Streamlit prototype, split-screen UI |
| Phase 3: Mobile Guardian | 1 week | OCR + camera scan + Shady Score |
| Phase 4: Deploy | 1 week | Live on Fly.io + Vercel |
| Phase 5: Monetisation | Ongoing | Freemium + subscription + enterprise |

**Total to MVP: 5 weeks**

---

## STEP 1 CODE (ready to run)

FastAPI server skeleton is fully written in the project reports.
Setup commands:
```bash
mkdir shady-clause-detector && cd shady-clause-detector
python -m venv venv && venv\Scripts\activate
pip install fastapi uvicorn python-multipart pdfplumber python-docx litellm
uvicorn main:app --reload
```

Test with:
```bash
curl -X POST -F "file=@sample_contract.txt" http://127.0.0.1:8000/analyze
```

The full `main.py` with adversarial prompt, PDF/DOCX extraction, and
LiteLLM/Mistral integration is documented in the step-by-step plan file.

---

## MONETISATION MODEL

**Freemium:**
- Free: text-based scans (pasted text)
- Paid: PDF/DOCX parsing + advanced reports + API access

**Subscription:** $X/month for unlimited scans

**Enterprise:** Law firms, HR departments, real estate agencies — bulk licensing

**Content marketing channels:**
- r/legaladvice, r/freelance on Reddit
- Twitter/X, LinkedIn
- Freelance platforms (Upwork, Fiverr partnerships)
- Blog posts: "5 Shady Clauses in Freelance Contracts You Need to Watch Out For"

---

## BUDGET

| Item | Monthly cost |
|---|---|
| Fly.io hosting | $10–20 |
| LLM API (Mistral Small free tier → paid) | $0–100 |
| Domain | ~$1/month amortised |
| Marketing | $0–500 (optional) |
| **Total first month** | **$10–620** |

---

## OPENCLAW INTEGRATION

The API can be called directly as an OpenClaw tool:
```
scan_contract(file_path) → calls Contract-Analysis-Engine → returns risk report
```

Also usable as a CLI tool: `npx contract-scan contract.pdf`

Fits naturally into the existing sovereign stack:
OpenClaw triggers analysis → returns structured JSON → Director reviews

---

## STATUS

| Item | Status |
|---|---|
| Product concept | ✅ Defined |
| Three-layer architecture | ✅ Specified |
| Risk taxonomy | ✅ Defined (Red/Yellow/Info + 7 priority clause types) |
| Adversarial prompt | ✅ Written and ready |
| JSON response structure | ✅ Defined |
| Full tech stack | ✅ Specified |
| main.py (Step 1 code) | ✅ Written, documented, ready to run |
| Svelte frontend code | ✅ Written in step-by-step plan |
| Mobile Guardian code | ✅ Written in step-by-step plan |
| Working deployed API | 🔲 Not yet built |
| Prompt tested on real contracts | 🔲 Not yet |
| Streamlit prototype | 🔲 Not yet |

---

## THE ONE-LINE VERDICT

Shady Clause Detector has a real use case, a sharp adversarial concept,
a complete build plan, and working starter code sitting in the docs.
The entire folder is specification. The next action is running three commands
and testing the adversarial prompt against a real contract.
