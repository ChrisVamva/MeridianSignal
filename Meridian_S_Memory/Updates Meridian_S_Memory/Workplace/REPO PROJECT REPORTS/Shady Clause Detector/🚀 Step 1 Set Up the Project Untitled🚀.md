---
modified: 2026-04-14T21:29:00+03:00
---
Let’s **start building** right now. We’ll begin with **Phase 1: Core Engine**—the Contract-Analysis-Engine.

---

## 🚀 **Step 1: Set Up the Project**
**Goal**: Create the backend API that will analyze contracts.

### 1.1 **Create the Project Folder**
Open a terminal and run:
```powershell
mkdir shady-clause-detector
cd shady-clause-detector
```

### 1.2 **Set Up a Python Virtual Environment**
```powershell
python -m venv venv
```
- **Windows**:
  ```powershell
  .\venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 1.3 **Install Required Packages**
```bash
pip install fastapi uvicorn python-multipart pdfplumber python-docx litellm
```

---

## 📝 **Step 2: Create the FastAPI Backend**
Create a file named `main.py` in the project folder.

### 2.1 **Add the FastAPI Code**
Paste this into `main.py`:
```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pdfplumber
from docx import Document
import os
from typing import Optional
import json

app = FastAPI()

# Load the adversarial prompt
ADVERSARIAL_PROMPT = """
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
"""

@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    # Step 1: Extract text from the file
    text = await extract_text(file)

    # Step 2: Send to LLM for analysis
    analysis = await send_to_llm(text)

    # Step 3: Return structured JSON
    return JSONResponse(content=analysis)

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

async def send_to_llm(text: str) -> dict:
    # Use LiteLLM to call Mistral Small (free tier)
    import litellm
    response = litellm.completion(
        model="mistral/mistral-small-latest",
        messages=[
            {"role": "system", "content": ADVERSARIAL_PROMPT},
            {"role": "user", "content": f"Analyze this contract:\n\n{text}"}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

---

## 🔥 **Step 3: Test the API**
### 3.1 **Run the FastAPI Server**
```bash
uvicorn main:app --reload
```
- The server will start at `http://127.0.0.1:8000`.

### 3.2 **Test with a Sample Contract**
1. **Create a sample contract** (e.g., `sample_contract.txt`):
   ```plaintext
   Section 1. Non-Compete Clause
   User agrees not to work for competitors for 2 years after termination.

   Section 2. Automatic Renewal
   This agreement renews automatically unless 30 days notice is given.

   Section 3. Hidden Fee
   User agrees to pay a $25/month convenience charge.
   ```

2. **Test with `curl`**:
   ```bash
   curl -X POST -F "file=@sample_contract.txt" http://127.0.0.1:8000/analyze
   ```

3. **Expected Output**:
   ```json
   {
     "risk_score": 90,
     "red_flags": [
       {
         "text": "User agrees not to work for competitors for 2 years after termination.",
         "section": "Section 1",
         "severity": "critical",
         "explanation": "Non-compete clauses are often unenforceable and limit career options."
       },
       {
         "text": "User agrees to pay a $25/month convenience charge.",
         "section": "Section 3",
         "severity": "high",
         "explanation": "Hidden fees are not clearly disclosed and can add up over time."
       }
     ],
     "yellow_flags": [
       {
         "text": "This agreement renews automatically unless 30 days notice is given.",
         "section": "Section 2",
         "severity": "medium",
         "explanation": "Automatic renewals can trap users into unfavorable terms."
       }
     ],
     "key_dates": []
   }
   ```

---

## 📌 **Next Steps**
1. **Verify the API works** with your sample contract.
2. **Test with real contracts** (e.g., freelance agreements, rental leases).
3. **Optimize the prompt** using Promptfoo (we’ll do this in the next step).

---
**Let me know when you’ve tested the API, and we’ll move to Phase 2: Building the Web Interface!** 🚀