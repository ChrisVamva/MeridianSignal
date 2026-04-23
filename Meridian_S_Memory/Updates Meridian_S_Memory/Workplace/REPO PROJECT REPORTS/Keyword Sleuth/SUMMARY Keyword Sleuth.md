# Keyword Sleuth — Project Report Summary
_Compiled from 8 files. April 2026._

---

## WHAT KEYWORD SLEUTH IS

A search engine for reviews and comments across commercial platforms.
Users input a keyword or phrase — "slow shipping", "hidden fee", "vegan options" —
and the tool finds it across Amazon, Yelp, TripAdvisor, and similar platforms,
returning frequency, sentiment, and trend data over time.

**Core differentiator identified:** No existing tool combines cross-platform
keyword search with sentiment analysis and trend tracking in one place.
ReviewMeta and Fakespot detect fake reviews. Brandwatch is enterprise-only.
Platform-native filters (Yelp, Amazon) are single-platform and static.
Keyword Sleuth fills the gap between those two extremes.

---

## THE PRODUCT

### What it does (three outputs per search)
1. **Keyword matches** — how many reviews contain the phrase, on which platforms
2. **Sentiment analysis** — positive / neutral / negative breakdown per match
3. **Trend over time** — frequency of the phrase by month/year

### Target users
- Small business owners tracking their own reputation and competitors
- Market researchers identifying sentiment trends
- Consumers finding products/restaurants matching specific criteria
- PR/marketing agencies monitoring brand mentions

### Monetisation model
- **Freemium** — free for text-based search (pasted text), paid for live platform
  scraping and advanced analytics ($10/month premium)
- **Subscription** — $20/month for unlimited searches
- **Enterprise** — $500/month for market research firms and agencies

---

## TECH STACK

| Component | Tool | Cost |
|---|---|---|
| Backend API | FastAPI | Free |
| Web scraping (if used) | Scrapy | Free |
| Sentiment analysis | TextBlob (v1) → VADER → fine-tuned BERT | Free |
| Database | SQLite | Free |
| Frontend (prototype) | Streamlit | Free |
| Frontend (production) | FastAPI + React | Free |
| Dev hosting | Fly.io / Vercel free tiers | $0 |
| Production hosting | Render / Fly.io | $10–50/month |

**Total first-month cost: $0–$550 depending on marketing spend.**

---

## DATA STRATEGY (the key architectural decision)

The platform scraping problem was identified early as high-difficulty and high-risk.
Amazon, Yelp, and TripAdvisor actively block scrapers using Cloudflare, CAPTCHAs,
and IP bans. Their ToS explicitly prohibits scraping.

**Resolution: no-scraping architecture for v1.**

### Data sources that require no scraping

| Source | Access | What's available |
|---|---|---|
| Hugging Face Datasets | `load_dataset()` in Python | `yelp_polarity` (640K reviews), `amazon_polarity` |
| Kaggle | API download | Amazon Reviews 2023, Yelp Dataset |
| Common Crawl | Direct download | 1.97 billion pages, quarterly updates |
| Government / open data | CSV/JSON from city portals | Restaurant health inspection comments |

**Recommended v1 approach:**
1. Load `yelp_polarity` or `amazon_polarity` from Hugging Face
2. Filter for target keyword
3. Train sentiment model on filtered subset
4. Deploy FastAPI endpoint querying the pre-filtered dataset
5. Return risk scores, trends, and sentiment from static data

**Total cost for this approach: $0**
Scraping is deferred to v2 once the core logic is validated.

---

## COMMON CRAWL + APACHE SPARK (the scale path)

For production scale, the architecture uses Common Crawl as the data source
and Apache Spark as the processing engine.

**Common Crawl:**
- Publicly available web crawl data, updated quarterly
- March 2026 dataset (CC-MAIN-2026-12): 1.97 billion pages, 75.53 TiB of WARC files
- Contains millions of review pages from all major platforms
- Free to download and use
- Access via `warcio` Python library for WARC file parsing

**Apache Spark:**
- Distributed processing: 100x faster than single-machine Python scripts
- Role in pipeline: extract review pages → clean HTML → keyword search at scale
  → trend analysis → sentiment model training via MLlib
- Free locally; Databricks Community Edition for cloud

**Five-phase pipeline:**
1. Download WARC paths file → select subset → download WARC files
2. Extract review pages using `warcio` → output `reviews.jsonl`
3. Process with Spark → clean HTML → label by platform → output `reviews_clean.parquet`
4. Fine-tune BERT on extracted reviews → save `sentiment_model/`
5. Trend analysis with Spark → group by month/year → visualise with Matplotlib/Plotly

---

## SENTIMENT MODEL PROGRESSION

### v1 — TextBlob (baseline, not recommended for production)
Rule-based, free, simple. Fails on "not bad" (reads as negative).
Use only for initial prototyping.

### v2 — VADER Sentiment (recommended starting point)
Better than TextBlob for informal text and slang.
Handles emoji, exclamation marks, negation better.
No training required. Install: `pip install vaderSentiment`

### v3 — Fine-tuned BERT (production target)
Uses Hugging Face `bert-base-uncased` fine-tuned on Yelp/Amazon reviews.
Training on 10K sample: 10–30 minutes on CPU, ~85–90% accuracy.
Handles context, sarcasm, mixed sentiment correctly.
Model size: ~400MB. Inference: ~100ms per review.
Can run on CPU (no GPU required for inference).

### Training approach (no scraping required)
```
Load yelp_polarity from Hugging Face
→ Filter for keyword subset
→ Tokenize with bert-base-uncased tokenizer
→ Fine-tune with Hugging Face Trainer (3 epochs, 10K samples)
→ Save model
→ Load in FastAPI pipeline endpoint
```

---

## CHALLENGES AND SOLUTIONS

### Challenge 1: Platform restrictions (HIGH difficulty)
Amazon, Yelp, TripAdvisor block scrapers. ToS violation risk. IP bans.

Solutions ranked by feasibility:
1. **Official APIs** — Yelp Fusion, Google Maps API (rate-limited but compliant)
2. **Residential proxies** — Luminati/Smartproxy $50–200/month (medium risk)
3. **Pre-scraped datasets** — Kaggle, Hugging Face (zero cost, zero risk)
4. **Ethical scraping** — rate-limited, user-agent rotation (slow, risky, last resort)
5. **Platform partnerships** — unrealistic for early stage

**Recommendation:** Start with official APIs + Hugging Face datasets.
Add residential proxies for supplementary data only if needed.
Never use ethical scraping in production.

### Challenge 2: Data volume (MEDIUM difficulty)
Scraping millions of reviews is slow and resource-intensive.

Solutions:
- Pagination + Redis caching in FastAPI (cheapest, simplest)
- Async processing via FastAPI background tasks or Celery
- Distributed scraping via Scrapy Cluster (complex, multiple machines)
- Cloud scraping services: ScrapingBee/Apify (~$0.01–0.10 per 1K requests)
- Pre-scraped datasets: Kaggle, Common Crawl (zero cost)

**Recommendation:** Pagination + caching for v1. Async processing for v2.
Pre-scraped datasets avoid the problem entirely for initial deployment.

### Challenge 3: Sentiment accuracy (MEDIUM difficulty)
TextBlob misclassifies negation ("not bad"), sarcasm, mixed reviews.

**Recommendation:** Start with VADER. Upgrade to fine-tuned BERT for production.
Avoid commercial APIs (Google Cloud NLP at $1/1K requests) unless budget allows.

---

## MARKET EVALUATION

**Uniqueness verdict: YES — genuinely differentiated in its specific combination.**

Highlighted gap: no tool offers cross-platform keyword search + sentiment +
trend tracking in one place at mass-market pricing.

**Market size:** Global review platforms market ~$10B (2026).
Keyword Sleuth targets a niche within this — keyword intelligence layer.

**Revenue model at scale (projected):**
- 10K freemium users at $10/month premium: $50K/month
- 5K subscription users at $20/month: $100K/month
- 100 enterprise users at $500/month: $50K/month
- **Total potential: $200K/month**

Note: these are projected figures from the market evaluation doc,
not validated revenue. Treat as directional, not operational.

---

## DEVELOPMENT PHASES (timeline)

| Phase | Duration | Milestone |
|---|---|---|
| Phase 1: Core Engine | 2 weeks | FastAPI backend live, can query pre-scraped datasets |
| Phase 2: Web Interface | 1 week | Streamlit prototype for testing |
| Phase 3: Sentiment Integration | 1 week | VADER or fine-tuned BERT integrated and tested |
| Phase 4: Deploy | 1 week | Live on Fly.io / Vercel free tier |
| Phase 5: Monetisation | Ongoing | Freemium + subscription |

---

## STATUS

| Item | Status |
|---|---|
| Product concept | ✅ Defined and documented |
| Market evaluation | ✅ Completed — differentiated gap confirmed |
| Tech stack | ✅ Defined |
| No-scraping v1 architecture | ✅ Fully specified |
| Common Crawl + Spark pipeline | ✅ Fully specified with code |
| Sentiment model training guide | ✅ Step-by-step with code |
| Challenge analysis (3 challenges) | ✅ All three with ranked solutions |
| Prototype / working code | 🔲 Not yet built |
| API deployed | 🔲 Not yet deployed |
| Dataset downloaded | 🔲 Not yet — Hugging Face datasets specified but not loaded |

---

## THE ONE-LINE VERDICT

Keyword Sleuth has a real product gap to fill, a clear zero-cost v1 path
using Hugging Face datasets, and a credible scale path via Common Crawl + Spark.
Nothing has been built yet. The entire folder is research and specification.
The next action is writing code, not more documentation.
