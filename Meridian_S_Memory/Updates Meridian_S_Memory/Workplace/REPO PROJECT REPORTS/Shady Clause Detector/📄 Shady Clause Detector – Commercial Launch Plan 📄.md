---
**Subject:** Shady Clause Detector – Business Plan & Timeline
**To:** Sophia
**From:** LUX (Lead Research Architect, OpenClaw)
**Date:** 2026-04-14

---

# 📄 **Shady Clause Detector – Commercial Launch Plan**
*A high-value utility to protect users from hidden traps in contracts*

---

## 🎯 **What We’re Building**
A **standalone commercial tool** that analyzes contracts (employment, freelance, rental, etc.) and flags **shady clauses** that could be used against the user. Think of it as a **"Legal Adversary"** that reads contracts the way a lawyer would—**not to summarize, but to find traps**.

### **Why This Matters**
- **Problem**: Most people sign contracts without reading them because they’re designed to be unreadable.
- **Solution**: A tool that **actively hunts for dangerous clauses** (e.g., non-competes, hidden fees, automatic renewals) and gives users a **"Shady Score"** (0-100).
- **Market**: Freelancers, small business owners, renters, and legal professionals—**a wide consumer base**.

---

## 🚀 **Our Plan (Step-by-Step)**
We’re taking a **lean, open-source-first approach** to avoid reinventing the wheel. Here’s how we’ll build and launch the product:

---

### **Phase 1: Build the Core Engine (1-2 Weeks)**
**Goal**: Create the **"Contract-Analysis-Engine"**—the brain of the tool.

#### **What We’ll Do:**
1. **Set Up the Backend API**
   - Use **FastAPI** (a lightweight framework) to create an API that:
     - Takes a contract (PDF, Word doc, or text) as input.
     - Extracts the text using **open-source tools** like `pdfplumber` and `python-docx`.
     - Sends the text to an **LLM** (e.g., Claude 3 Opus via OpenRouter) with a **custom "Legal Adversary" prompt** to flag shady clauses.
     - Returns a **structured report** with:
       - **Risk Score** (0-100)
       - **Red Flags** (e.g., "User waives all rights to sue")
       - **Yellow Flags** (e.g., "30-day notice for cancellation")
       - **Key Dates** (e.g., "Rent increase effective January 1, 2027")

2. **Test the Engine**
   - Feed it **real contracts** (e.g., freelance agreements, rental leases) to ensure it catches **all shady clauses**.
   - Use **Promptfoo** (an open-source tool) to **optimize the "Legal Adversary" prompt** and make it as effective as possible.

#### **Tools We’ll Use:**
| **Tool**               | **Purpose**                                                                 | **Why It’s Great**                                                                 |
|------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **FastAPI**            | Backend API framework                                                       | Lightweight, fast, and easy to deploy.                                            |
| **pdfplumber**         | Extract text from PDFs                                                     | Free, accurate, and handles formatting well.                                      |
| **python-docx**        | Extract text from Word docs                                                | Simple and reliable.                                                              |
| **LiteLLM**            | Call LLMs (Claude, GPT, etc.) in a unified way                             | Supports **100+ LLMs** and simplifies integration.                                |
| **Promptfoo**          | Test and optimize the "Legal Adversary" prompt                             | Ensures the AI is **as aggressive as a human lawyer** in spotting traps.          |

#### **Timeline:**
- **Week 1**: Set up the API and test with sample contracts.
- **Week 2**: Optimize the prompt and finalize the engine.

---

### **Phase 2: Build the Web Interface (1 Week)**
**Goal**: Create a **simple, user-friendly website** where users can upload contracts and see the results.

#### **What We’ll Do:**
1. **Prototype with Streamlit**
   - Use **Streamlit** (an open-source framework) to quickly build a **split-screen UI**:
     - **Left side**: The original contract text (dark mode, high-contrast for readability).
     - **Right side**: The "Risk Feed" (Red/Yellow/Green flags).
     - Click a flag → the left side scrolls to the exact shady clause.

2. **Test with Real Users**
   - Ask **freelancers and small business owners** to try it and give feedback.

#### **Tools We’ll Use:**
| **Tool**               | **Purpose**                                                                 | **Why It’s Great**                                                                 |
|------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **Streamlit**          | Build the web interface                                                     | Free, easy to use, and perfect for quick prototyping.                             |

#### **Timeline:**
- **Week 3**: Build the prototype and gather feedback.

---

### **Phase 3: Build the Mobile Guardian (1 Week)**
**Goal**: Create a **mobile-friendly version** where users can take a photo of a physical contract and get an instant "Shady Score."

#### **What We’ll Do:**
1. **Add OCR (Optical Character Recognition)**
   - Use **Tesseract** (free, open-source OCR) to extract text from images.
   - Send the text to the **Contract-Analysis-Engine** for analysis.

2. **Turn It into a PWA (Progressive Web App)**
   - Use **PWA Starter Kit** to build a **mobile-friendly website** that works like an app.
   - Use **Capacitor** to wrap the PWA into a **native mobile app** (for iOS and Android).

#### **Tools We’ll Use:**
| **Tool**               | **Purpose**                                                                 | **Why It’s Great**                                                                 |
|------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **Tesseract**          | Extract text from images                                                    | Free, accurate, and supports **100+ languages**.                                  |
| **PWA Starter Kit**    | Build a mobile-friendly website                                             | Provides a **solid foundation** for the Mobile Guardian.                          |
| **Capacitor**          | Turn the PWA into a native mobile app                                       | Works for **iOS and Android** without needing separate codebases.                  |

#### **Timeline:**
- **Week 4**: Build the Mobile Guardian and test it with real contracts.

---

### **Phase 4: Deploy & Launch (1 Week)**
**Goal**: Get the tool **live and accessible** to users.

#### **What We’ll Do:**
1. **Deploy the Backend API**
   - Use **Fly.io** (cheap, scalable hosting) to deploy the API.
   - Set up **rate limiting** to prevent abuse.

2. **Deploy the Web Interface**
   - Use **Vercel** (fast, global CDN) to deploy the website.

3. **Deploy the Mobile Guardian**
   - Publish the **PWA** on the web.
   - Submit the **native mobile app** to the **App Store** and **Google Play Store**.

#### **Tools We’ll Use:**
| **Tool**               | **Purpose**                                                                 | **Why It’s Great**                                                                 |
|------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **Fly.io**             | Deploy the backend API                                                      | Cheap, scalable, and easy to use.                                                 |
| **Vercel**             | Deploy the web interface                                                    | Fast, global CDN, and free for small projects.                                    |
| **App Store / Google Play** | Publish the mobile app                                                  | Reach **millions of users** on iOS and Android.                                   |

#### **Timeline:**
- **Week 5**: Deploy everything and run final tests.

---

### **Phase 5: Monetization & Growth (Ongoing)**
**Goal**: Turn this into a **profitable, sustainable product**.

#### **How We’ll Make Money:**
1. **Freemium Model**
   - **Free**: Users can scan **text-based contracts** (e.g., pasted text).
   - **Paid**: Users pay for **PDF/Doc parsing** and **advanced features** (e.g., detailed reports, API access).

2. **Subscription (Optional)**
   - **Monthly fee** for unlimited scans and premium features.

3. **Enterprise Licensing (Future)**
   - Sell to **law firms, HR departments, or real estate agencies** for bulk usage.

#### **How We’ll Grow:**
1. **Content Marketing**
   - Write blog posts like:
     - *"5 Shady Clauses in Freelance Contracts You Need to Watch Out For"*
     - *"How to Spot a Predatory Rental Lease"*
   - Share on **Twitter/X, LinkedIn, Reddit (r/legaladvice, r/freelance)**, and **freelance platforms (Upwork, Fiverr)**.

2. **Partnerships**
   - Partner with **freelance platforms, co-working spaces, and legal aid organizations** to promote the tool.

3. **Paid Ads (Optional)**
   - Run **targeted ads** on Google and social media to reach freelancers and small business owners.

---

## 📅 **Timeline Summary**
| **Phase**               | **Duration** | **Milestone**                                                                 |
|-------------------------|--------------|-------------------------------------------------------------------------------|
| Phase 1: Core Engine    | 2 weeks      | Contract-Analysis-Engine is live and returns structured risk reports.        |
| Phase 2: Web Interface  | 1 week       | Lean web interface is live and functional.                                   |
| Phase 3: Mobile Guardian| 1 week       | Mobile Guardian is live and functional.                                      |
| Phase 4: Deploy & Launch| 1 week       | Tool is live and accessible to users.                                        |
| Phase 5: Monetization   | Ongoing      | Product is monetized and growing.                                             |

**Total Time to Launch**: **5 weeks** for a **minimum viable product (MVP)**.

---

## 💰 **Budget & Costs**
| **Item**                | **Estimated Cost** | **Notes**                                                                     |
|-------------------------|--------------------|-------------------------------------------------------------------------------|
| **Hosting (Fly.io)**    | $10-$20/month      | Scalable and cheap for small projects.                                        |
| **LLM API Calls**       | $50-$100/month     | Depends on usage (Claude 3 Opus is ~$15 per 1M tokens).                      |
| **Domain & SSL**        | $10-$20/year       | For the website (e.g., shadyclausedetector.com).                              |
| **Marketing**           | $0-$500/month      | Optional: Ads, partnerships, and content creation.                           |
| **Total (First Month)** | **$70-$620**       | Depends on usage and marketing spend.                                         |

---

## 🎯 **Why This Will Succeed**
1. **High Demand**: Everyone hates reading contracts, but they’re forced to sign them.
2. **Clear Value**: Users get **instant, actionable insights**—no need to hire a lawyer.
3. **Scalable**: The tool can be **white-labeled** for partners (e.g., freelance platforms, co-working spaces).
4. **Monetizable**: Freemium model ensures **recurring revenue** from power users.

---
## 📌 **Next Steps for You**
1. **Review this plan** and let me know if you have any questions or concerns.
2. **Approve the timeline** so we can start Phase 1 (Core Engine).
3. **Provide feedback** on the monetization strategy (e.g., freemium vs. subscription).

---
**Let’s build something amazing together!** 🚀

---
**LUX**
*Lead Research Architect, OpenClaw*
*For: Sophia