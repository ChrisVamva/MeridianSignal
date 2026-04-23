---
modified: 2026-04-14T23:40:41+03:00
---
Perfect — you now have the **exact file listings** for the **March 2026 Common Crawl (CC-MAIN-2026-12)**. This is a **massive dataset** (1.97 billion pages, 75.53 TiB of WARC files), and we need to **focus on extracting review pages efficiently**.

---

## 🎯 **Goal**
Extract **review pages** (Amazon, Yelp, TripAdvisor, etc.) from the **March 2026 Common Crawl** using the **WARC files** and **Apache Spark** for scalability.

---

## 📌 **Step-by-Step Plan**

---

### **Phase 1: Download the WARC Files**
**Goal**: Download a **subset of WARC files** containing review pages.

#### **1.1 Download the WARC Paths File**
The `warc.paths.gz` file lists all WARC files in the crawl. Download it:
```bash
wget https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-12/segments/1421/warc.paths.gz
```

#### **1.2 Extract the WARC File Paths**
```bash
gunzip warc.paths.gz
```
This will give you a file (`warc.paths`) with **100,000 WARC file paths**.

#### **1.3 Select a Subset of WARC Files**
Since downloading **all 100,000 files** is impractical, let’s **focus on a small subset** (e.g., 10 files) for testing.

Example `warc.paths` subset (first 10 lines):
```
https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-12/segments/1421/warc/000000000000.warc.gz
https://data.commoncrawl.org/crawl-data/CC-MAIN-2026-12/segments/1421/warc/000000000001.warc.gz
...
```

---

### **Phase 2: Extract Reviews Using `warcio` (Python)**
**Goal**: Extract **review pages** from the WARC files using `warcio`.

#### **2.1 Install `warcio`**
```bash
pip install warcio
```

#### **2.2 Create a Python Script (`extract_reviews.py`)**
```python
from warcio import ArchiveIterator
import gzip
import json
from pathlib import Path

def extract_reviews_from_warc(warc_file, output_file):
    with gzip.open(warc_file, 'rb') as f:
        for record in ArchiveIterator(f):
            if record.rec_type == 'response':
                url = record.rec_headers.get_header('WARC-Target-URI')
                payload = record.content_stream().read().decode('utf-8', errors='ignore')

# Check if the page is a review page
                if any(keyword in payload.lower() for keyword in ['review', 'rating', 'comment', 'testimonial']):
                    # Save the review data (URL + text)
                    with open(output_file, 'a') as f_out:
                        f_out.write(json.dumps({"url": url, "text": payload}) + "\n")

# Example usage
extract_reviews_from_warc("000000000000.warc.gz", "reviews.jsonl")
```

#### **2.3 Run the Script**
```bash
python extract_reviews.py
```
- This will create a `reviews.jsonl` file with **all review pages** from the WARC file.

---

### **Phase 3: Process Reviews with Apache Spark**
**Goal**: Use Spark to **process, clean, and analyze** the extracted reviews at scale.

#### **3.1 Set Up Apache Spark**
Install Spark locally or use **Databricks Community Edition** (free for small-scale projects).

#### **3.2 Load Reviews into Spark**
Create a Spark script (`process_reviews.py`):
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, when, regexp_extract
import json

# Initialize Spark
spark = SparkSession.builder.appName("ReviewProcessor").getOrCreate()

# Load reviews from JSONL file
df = spark.read.json("reviews.jsonl")

# Clean and extract review text
df_clean = df.withColumn(
    "clean_text",
    regexp_extract(col("text"), r"(?s)<body.*?</body>", 0)  # Extract HTML body
).withColumn(
    "platform",
    when(col("url").contains("amazon"), "amazon")
    .when(col("url").contains("yelp"), "yelp")
    .when(col("url").contains("tripadvisor"), "tripadvisor")
    .otherwise("other")
)

# Save cleaned reviews
df_clean.write.parquet("reviews_clean.parquet")
```

#### **3.3 Run the Script**
```bash
spark-submit process_reviews.py
```
- This will create a `reviews_clean.parquet` file with **structured review data**.

---

### **Phase 4: Train Sentiment Models**
**Goal**: Train a **sentiment model** (e.g., fine-tuned BERT) using the extracted reviews.

#### **4.1 Use Hugging Face Transformers**
Install the required libraries:
```bash
pip install transformers datasets torch
```

#### **4.2 Fine-Tune BERT for Sentiment Analysis**
Create a script (`train_sentiment.py`):
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# Load your dataset (example: reviews with sentiment labels)
dataset = load_dataset("json", data_files="reviews_clean.parquet")

# Tokenize the data
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)  # Positive, Neutral, Negative

def tokenize_function(examples):
    return tokenizer(examples["clean_text"], padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Train the model
training_args = TrainingArguments(
    output_dir="./sentiment_model",
    per_device_train_batch_size=8,
    num_train_epochs=3,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

trainer.train()
```

#### **4.3 Save the Model**
```python
model.save_pretrained("./sentiment_model")
tokenizer.save_pretrained("./sentiment_model")
```

---

### **Phase 5: Perform Trend Analysis**
**Goal**: Analyze **trends in customer sentiment** over time (e.g., "slow shipping" complaints in 2023 vs. 2024).

#### **5.1 Use Spark for Trend Analysis**
Create a Spark script (`trend_analysis.py`):
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, count, year, month
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# Initialize Spark
spark = SparkSession.builder.appName("TrendAnalyzer").getOrCreate()

# Load cleaned reviews
df = spark.read.parquet("reviews_clean.parquet")

# Extract year and month from URL (example: "amazon.com/reviews/2023/10/...")
df_trends = df.withColumn(
    "year",
    regexp_extract(col("url"), r"(\d{4})", 1)
).withColumn(
    "month",
    regexp_extract(col("url"), r"/(\d{1,2})/", 1)
)

# Count mentions of "slow shipping" by year/month
trend_df = df_trends.filter(
    lower(col("clean_text")).contains("slow shipping")
).groupBy("year", "month").agg(
    count("*").alias("mention_count")
)

# Save trends
trend_df.write.parquet("trends_slow_shipping.parquet")
```

#### **5.2 Visualize Trends**
Use **Matplotlib** or **Plotly** to visualize the trends:
```python
import matplotlib.pyplot as plt
import pandas as pd

# Load trends data
trends_df = pd.read_parquet("trends_slow_shipping.parquet")

# Plot
plt.plot(trends_df["year"] + "-" + trends_df["month"], trends_df["mention_count"])
plt.xlabel("Year-Month")
plt.ylabel("Mentions of 'slow shipping'")
plt.title("Trends in 'Slow Shipping' Complaints")
plt.show()
```

---

## 📊 **Expected Output**
| **Phase**               | **Output**                                                                                     |
|-------------------------|------------------------------------------------------------------------------------------------|
| **Phase 1**             | `reviews.jsonl` (raw review data from Common Crawl).                                           |
| **Phase 2**             | `reviews_clean.parquet` (structured review data with platform labels).                        |
| **Phase 3**             | `sentiment_model/` (fine-tuned BERT model for sentiment analysis).                             |
| **Phase 4**             | `trends_slow_shipping.parquet` (trend data for "slow shipping" mentions over time).            |

---

## 🚀 **Next Steps**
1. **Download the WARC files** (start with a small subset).
2. **Run the `extract_reviews.py` script** to get raw review data.
3. **Run the `process_reviews.py` script** to clean and structure the data.
4. **Train the sentiment model** using `train_sentiment.py`.
5. **Analyze trends** using `trend_analysis.py`.

---
**Let me know when you’re ready to start, and I’ll guide you through the first step!** 🚀