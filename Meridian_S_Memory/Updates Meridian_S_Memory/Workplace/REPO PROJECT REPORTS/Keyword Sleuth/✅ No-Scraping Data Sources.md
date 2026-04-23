---
modified: 2026-04-15T01:50:21+03:00
---


---

## 🎯 **Goal**
Build a **search engine for reviews** that finds specific keywords (e.g., “slow shipping,” “hidden fee”) and shows sentiment/risk trends — **without web scraping**.

---

## ✅ **No-Scraping Data Sources**

| **Source**               | **Why It Works**                                                                 | **Access Method**                     |
|--------------------------|----------------------------------------------------------------------------------|---------------------------------------|
| **OpenRouter Public Datasets** | Many apps publish free datasets of reviews (restaurants, products, services).   | Direct download (CSV/JSON).           |
| **Kaggle Datasets**       | Thousands of labeled review datasets (Amazon, Yelp, TripAdvisor).               | `pip install kaggle` + API key.        |
| **Hugging Face Datasets** | Pre-loaded review datasets (e.g., `amazon_polarity`, `yelp_polarity`).          | `datasets.load_dataset()` in Python.  |
| **Government/Open Data**  | Some cities publish restaurant health inspection reports with comments.         | CSV/JSON download from city portals.  |

---

## 🛠️ **Step-by-Step Execution Plan**

### **Phase 1: Get Training Data (No Scraping)**
1. **Download Yelp or Amazon reviews from Hugging Face**:
   ```python
   from datasets import load_dataset

   dataset = load_dataset("yelp_polarity")  # or "amazon_polarity"
   dataset.save_to_disk("reviews_dataset")
   ```
2. **Filter for your keywords** (e.g., “slow shipping”):
   ```python
   import pandas as pd

   df = pd.read_json("reviews_dataset/train.json", lines=True)
   mask = df["text"].str.contains("slow shipping", case=False, na=False)
   filtered = df[mask]
   filtered.to_parquet("reviews_slow_shipping.parquet")
   ```

---

### **Phase 2: Train Sentiment Model (No Scraping)**
1. **Fine-tune a small BERT model** on the filtered reviews:
   ```python
   from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer

   model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)
   tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

   # Tokenize and train on `reviews_slow_shipping.parquet`
   ```
2. **Save the model** and load it in your API.

---

### **Phase 3: Build the API (No Scraping)**
1. **FastAPI endpoint** that:
   - Accepts a **keyword** (e.g., “slow shipping”).
   - Queries the **pre-filtered dataset**.
   - Returns **risk scores, trends, and sentiment** from the dataset.

   ```python
   @app.post("/search")
   async def search_keyword(keyword: str):
       df = pd.read_parquet("reviews_slow_shipping.parquet")
       matches = df[df["text"].str.contains(keyword, case=False)]
       return {"keyword": keyword, "count": len(matches), "samples": matches.head(10).to_dict()}
   ```

---

### **Phase 4: Add Trend Analysis (No Scraping)**
1. **Use time metadata** (if available in the dataset):
   - Group by month/year.
   - Plot trends with **Matplotlib/Plotly**.

   ```python
   df["date"] = pd.to_datetime(df["date"])
   df["month"] = df["date"].dt.to_period("M")
   trends = df.groupby("month").size()
   ```

---

### **Phase 5: Deploy (Low-Cost Hosting)**
| **Component**       | **Hosting**                     | **Cost**                     |
|---------------------|---------------------------------|------------------------------|
| **API**             | Fly.io (free tier)              | $0 (up to 3GB RAM)           |
| **Frontend**        | Vercel (free tier)              | $0                           |
| **Dataset Storage** | Hugging Face Datasets (free)    | $0                           |
| **Model Hosting**   | Hugging Face Inference API      | Free for small models        |

**Total Cost: $0** (if staying within free tiers).

---

## 📊 **What You’ll Deliver**
| **Component**       | **Description**                                                                 |
|---------------------|---------------------------------------------------------------------------------|
| **Keyword Search API** | Accepts a keyword, returns matching reviews with sentiment.                     |
| **Trend Dashboard**    | Shows how often a keyword appears over time (e.g., “slow shipping” in 2024 vs. 2025). |
| **Risk Score**         | Based on frequency and sentiment (e.g., 100 reviews mentioning “hidden fee” = High Risk). |

---

## 🚀 **Why This Works**
- **No scraping** → No legal/technical risks.
- **No cost** → Uses free datasets and hosting.
- **Fast to build** → Leverages pre-existing data and models.
- **Scalable later** → Once proven, you can add scraping for custom data.

---

## 📌 **Next Steps**
1. **Download a Yelp/Amazon dataset** from Hugging Face.
2. **Filter for a keyword** (e.g., “slow shipping”).
3. **Train a sentiment model** on that subset.
4. **Deploy the API** on Fly.io.

---

