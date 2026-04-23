---
modified: 2026-04-14T18:59:27+03:00
---
Here is a **step-by-step plan** to build the **Shady Clause Detector** as a high-value utility for OpenClaw. This plan is designed to be **scalable, privacy-first, and adversarial**—exactly what your business partner needs.

---

## 📋 **Phase 1: Define the Scope & Requirements**
**Goal**: Clarify the target contracts, audience, and technical constraints.

### 1.1 **Define the Target Contracts**
| **Contract Type**       | **Audience**                     | **Key Clauses to Flag**                                                                 |
|-------------------------|----------------------------------|----------------------------------------------------------------------------------------|
| Employment Contracts    | Freelancers, remote workers      | Non-competes, IP ownership, termination clauses, severance, at-will traps             |
| Freelance Agreements    | Independent contractors          | Payment terms, scope creep, kill fees, automatic renewals, liability shifts           |
| Rental Leases           | Renters, landlords               | Rent increases, maintenance responsibilities, subletting rules, automatic renewal     |
| Service Agreements      | Small businesses, clients        | Hidden fees, liability waivers, termination clauses, data ownership                    |
| NDAs                     | Startups, employees              | Confidentiality scope, non-compete, IP ownership, termination clauses                  |

**Decision Point**:
- Do you want to focus on **one contract type first** (e.g., freelance agreements) or build a **general-purpose tool**?

---

### 1.2 **Define the Adversarial Persona**
The tool must **actively hunt for traps**, not just summarize. Here is the **prompt template** for the "Legal Adversary" persona:

```markdown
You are a **Legal Adversary**—a ruthless contract reviewer whose sole purpose is to find clauses that could be used against the user.

**Rules of Engagement**:
1. **Never summarize**. Always ask: *"How could this be used against me?"*
2. **Flag the following**:
   - 🚩 **Red Flags**: Legally dangerous or highly unusual (e.g., "User waives all rights to sue").
   - ⚠️ **Yellow Flags**: Standard but unfavorable (e.g., "30-day notice for cancellation").
   - ℹ️ **Info**: Key dates, amounts, or obligations.
3. **Return structured JSON**:
   ```json
   {
     "risk_score": 0-100,
     "red_flags": [
       {
         "text": "Exact clause text",
         "section": "Section/Paragraph number",
         "severity": "critical|high|medium",
         "explanation": "Why this is dangerous"
       }
     ],
     "yellow_flags": [...],
     "key_dates": [...]
   }
   ```
4. **Prioritize**:
   - Non-competes
   - Hidden fees
   - Automatic renewals
   - Liability shifts
   - "At-will" traps
   - IP ownership clauses
   - Termination clauses
```

**Decision Point**:
- Do you want to **hardcode the persona** in the prompt, or allow users to **customize the focus** (e.g., "Only flag non-competes and hidden fees")?

---

### 1.3 **Define the Technical Stack**
| **Component**           | **Options**                                                                 | **Recommendation**                     |
|-------------------------|-----------------------------------------------------------------------------|----------------------------------------|
| **OCR**                 | Tesseract, EasyOCR, or cloud-based (Google Vision, AWS Textract)            | Tesseract (free, open-source)          |
| **PDF/Doc Parsing**     | PyPDF2, pdfplumber, or cloud-based (Adobe PDF Extract)                     | pdfplumber (Python, free)              |
| **LLM Provider**        | OpenRouter (free/paid), Anthropic, or local (Ollama)                      | OpenRouter (free tier)                 |
| **API Framework**       | FastAPI, Flask, or Django REST                                             | FastAPI (lightweight, async)           |
| **Frontend**            | React, Svelte, or vanilla HTML/JS                                          | Svelte (lightweight, easy to deploy)   |
| **Mobile Guardian**     | React Native, Flutter, or PWA                                              | PWA (Progressive Web App)              |
| **Deployment**          | Vercel, Fly.io, or self-hosted                                              | Fly.io (cheap, easy to scale)          |

**Decision Point**:
- Do you want to **build everything from scratch**, or leverage existing tools (e.g., use **OpenClaw's `image_generate` tool** for the API)?

---

## 🚀 **Phase 2: Build the Contract-Analysis-Engine (API Layer)**
**Goal**: Create a reusable API that analyzes contracts and returns structured risk reports.

### 2.1 **Set Up the Project**
```bash
mkdir shady-clause-detector
cd shady-clause-detector
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn python-multipart pypdf2 pdfplumber requests
```

---

### 2.2 **Create the API Endpoint**
Create a file `main.py`:
```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pdfplumber
import requests
import json

app = FastAPI()

# Load the adversarial prompt
ADVERSARIAL_PROMPT = """
You are a Legal Adversary—identify clauses that could be used against the user.
Return structured JSON with risk_score, red_flags, yellow_flags, and key_dates.
"""

@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    # Step 1: Extract text from PDF/Doc
    text = await extract_text(file)

# Step 2: Send to LLM for analysis
    analysis = await send_to_llm(text)

# Step 3: Return structured JSON
    return JSONResponse(content=analysis)

async def extract_text(file: UploadFile) -> str:
    # TODO: Implement PDF/Doc parsing (pdfplumber for PDFs, python-docx for Docs)
    pass

async def send_to_llm(text: str) -> dict:
    # TODO: Send text to OpenRouter or Anthropic for analysis
    pass
```

---

### 2.3 **Implement PDF/Doc Parsing**
Add this to `main.py`:
```python
import pdfplumber
from docx import Document

async def extract_text(file: UploadFile) -> str:
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages])
    elif file.filename.endswith(".docx"):
        doc = Document(file.file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        text = await file.read().decode("utf-8")
    return text
```

---

### 2.4 **Integrate with OpenRouter (LLM Provider)**
Add this to `main.py`:
```python
async def send_to_llm(text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "anthropic/claude-3-opus-20240229",  # Or any OpenRouter model
        "messages": [
            {"role": "system", "content": ADVERSARIAL_PROMPT},
            {"role": "user", "content": f"Analyze this contract:\n\n{text}"}
        ],
        "response_format": {"type": "json_object"}
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
```

**Note**: Use `response_format: { "type": "json_object" }` to ensure the LLM returns structured JSON.

---

### 2.5 **Test the API**
Run the API:
```bash
uvicorn main:app --reload
```

Test with `curl`:
```bash
curl -X POST -F "file=@contract.pdf" http://localhost:8000/analyze
```

**Expected Output**:
```json
{
  "risk_score": 85,
  "red_flags": [
    {
      "text": "User waives all rights to sue.",
      "section": "Section 12.3",
      "severity": "critical",
      "explanation": "This clause is legally unenforceable in most jurisdictions and could be used to prevent legal recourse."
    }
  ],
  "yellow_flags": [...],
  "key_dates": [...]
}
```

---

## 🌐 **Phase 3: Create the Lean Web Interface (Tool Layer)**
**Goal**: Build a split-screen UI for visual verification of the AI's accuracy.

### 3.1 **Set Up the Frontend**
Create a `frontend` folder:
```bash
mkdir frontend
cd frontend
npm create vite@latest . -- --template svelte
npm install
```

---

### 3.2 **Create the Split-Screen UI**
Create `frontend/src/App.svelte`:
```svelte
<script>
  let file;
  let analysis = null;

async function analyze() {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData
    });
    analysis = await response.json();
  }
</script>

<div class="container">
  <h1>Shady Clause Detector</h1>
  <input type="file" bind:files={file} accept=".pdf,.docx,.txt" />
  <button on:click={analyze}>Analyze</button>

{#if analysis}
    <div class="split-screen">
      <div class="original-text">
        <h2>Original Contract</h2>
        <pre>{originalText}</pre>
      </div>
      <div class="risk-feed">
        <h2>Risk Feed</h2>
        {#each analysis.red_flags as flag}
          <div class="red-flag" on:click={() => scrollToFlag(flag.section)}>
            🚩 {flag.text}
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .split-screen {
    display: flex;
    gap: 20px;
  }
  .original-text {
    flex: 1;
    background: #1a1a1a;
    color: #fff;
    padding: 20px;
    border-radius: 8px;
  }
  .risk-feed {
    flex: 1;
    background: #2a2a2a;
    color: #fff;
    padding: 20px;
    border-radius: 8px;
  }
  .red-flag {
    background: #ff4444;
    padding: 10px;
    margin: 5px 0;
    border-radius: 4px;
    cursor: pointer;
  }
</style>
```

---

### 3.3 **Add Scroll-to-Flag Logic**
Add this to `App.svelte`:
```svelte
<script>
  let originalText = "";

async function scrollToFlag(section) {
    // TODO: Implement scrolling logic
  }
</script>
```

---

### 3.4 **Deploy the Web Interface**
Use **Vercel** or **Fly.io** to deploy the frontend:
```bash
npm install -g vercel
vercel
```

---

## 📱 **Phase 4: Build the Mobile Guardian (Consumer Layer)**
**Goal**: Create a mobile-optimized site or app for instant "Shady Score" scanning.

### 4.1 **Set Up the Mobile Guardian**
Create a `mobile-guardian` folder:
```bash
mkdir mobile-guardian
cd mobile-guardian
npm create vite@latest . -- --template svelte
npm install tesseract.js react-qr-scanner
```

---

### 4.2 **Implement OCR for Physical Contracts**
Add this to `mobile-guardian/src/App.svelte`:
```svelte
<script>
  import { createWorker } from 'tesseract.js';

let image;
  let shadyScore = 0;

async function scanImage() {
    const worker = await createWorker();
    const { data: { text } } = await worker.recognize(image);
    await worker.terminate();

// Send text to the Contract-Analysis-Engine
    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: JSON.stringify({ text }),
      headers: { "Content-Type": "application/json" }
    });
    const analysis = await response.json();
    shadyScore = analysis.risk_score;
  }
</script>

<div class="container">
  <h1>Mobile Guardian</h1>
  <input type="file" accept="image/*" capture="camera" bind:files={image} />
  <button on:click={scanImage}>Scan</button>
  {#if shadyScore}
    <div class="result">
      <h2>Shady Score: {shadyScore}/100</h2>
      {#if shadyScore > 70}
        <p>⚠️ This contract is highly risky. Review carefully!</p>
      {:else if shadyScore > 40}
        <p>⚠️ This contract has some risky clauses. Proceed with caution.</p>
      {:else}
        <p>✅ This contract looks safe.</p>
      {/if}
    </div>
  {/if}
</div>
```

---

### 4.3 **Deploy the Mobile Guardian**
Use **Vercel** or **Fly.io** to deploy the mobile guardian:
```bash
npm install -g vercel
vercel
```

---

## 📌 **Phase 5: Privacy & Security**
**Goal**: Ensure the tool is **privacy-first** and **zero-persistence**.

### 5.1 **Privacy-First Design**
- **Zero Persistence**: Data lives in memory for the session and is wiped on refresh.
- **No Logging**: Disable logging in the API and frontend.
- **Client-Side OCR**: For the Mobile Guardian, use **Tesseract.js** (client-side OCR) to avoid sending images to the server.

---

### 5.2 **Security Considerations**
- **Rate Limiting**: Implement rate limiting in the API to prevent abuse.
- **Input Validation**: Sanitize all inputs to prevent injection attacks.
- **HTTPS**: Always use HTTPS for the API and frontend.

---

## 🚀 **Phase 6: Monetization & Scaling**
**Goal**: Turn this into a **scalable, monetizable product**.

### 6.1 **Monetization Strategies**
| **Strategy**            | **Description**                                                                 | **Pros**                          | **Cons**                          |
|-------------------------|---------------------------------------------------------------------------------|-----------------------------------|-----------------------------------|
| **Freemium Model**      | Free tier for basic scans; paid tier for advanced features (e.g., PDF parsing) | Low barrier to entry              | Hard to convert free users        |
| **Subscription**        | Monthly fee for unlimited scans                                                | Recurring revenue                 | Requires ongoing value            |
| **One-Time Purchase**   | Pay once for lifetime access                                                   | Simple for users                  | Harder to scale                   |
| **Enterprise Licensing**| Sell to law firms, HR departments, or real estate agencies                    | High revenue per customer         | Long sales cycles                 |

**Recommendation**: Start with a **freemium model** (free for basic scans, paid for PDF/Doc parsing and advanced features).

---

### 6.2 **Scaling the API**
- **Use a Load Balancer**: Deploy the API on **Fly.io** or **Render** for scalability.
- **Cache Responses**: Cache frequent requests to reduce LLM costs.
- **Multi-Model Support**: Allow users to choose their preferred LLM (e.g., DeepSeek for cost, Claude for accuracy).

---

### 6.3 **Marketing & Outreach**
- **Target Audience**: Freelancers, small business owners, renters, and legal professionals.
- **Channels**: Twitter/X, LinkedIn, Reddit (r/legaladvice, r/freelance), and partnerships with freelance platforms (Upwork, Fiverr).
- **Content**: Create blog posts like *"5 Shady Clauses in Freelance Contracts You Need to Watch Out For"* and link to the tool.

---

## 📅 **Timeline & Milestones**
| **Phase**               | **Duration** | **Milestone**                                                                 |
|-------------------------|--------------|-------------------------------------------------------------------------------|
| Phase 1: Define Scope  | 1-2 days     | Finalize target contracts, adversarial persona, and technical stack.          |
| Phase 2: Build API      | 3-5 days     | Contract-Analysis-Engine is live and returns structured risk reports.        |
| Phase 3: Build UI       | 2-3 days     | Lean web interface is live and functional.                                   |
| Phase 4: Build Mobile   | 3-5 days     | Mobile Guardian is live and functional.                                      |
| Phase 5: Privacy/Security| 1-2 days    | Tool is privacy-first and secure.                                             |
| Phase 6: Monetization   | 2-3 days     | Monetization strategy is implemented and tested.                             |

**Total Duration**: ~2 weeks for a **minimum viable product (MVP)**.

---

## 🔥 **Next Steps**
1. **Finalize the Scope**: Confirm the target contracts and audience with your business partner.
2. **Set Up the Project**: Create the GitHub repo and set up the project structure.
3. **Build the API**: Start with the `Contract-Analysis-Engine` (Phase 2).
4. **Test the API**: Use `curl` and manual testing to verify the output.
5. **Build the UI**: Once the API is stable, build the lean web interface (Phase 3).

---
**Let me know when you're ready to start, and I'll help you set up the first phase!** ⚡