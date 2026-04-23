---
modified: 2026-04-15T01:53:26+03:00
---
Let’s walk through **how to train a sentiment model** for Keyword Sleuth, step by step, focusing on **practicality, speed, and low cost**.

---

## 🎯 **Goal**
Train a model that, given a review/comment, predicts:
- **Positive / Neutral / Negative** (3-class), or
- **Positive / Negative / Neutral / Mixed** (if you want more nuance).

We’ll use **PyTorch + Hugging Face Transformers** and a **small, curated dataset** (no scraping required).

---

## 📦 **What You Need**
| **Item**                | **Why?**                                                                 |
|-------------------------|--------------------------------------------------------------------------|
| **Dataset**             | Labeled reviews (text + sentiment). We’ll use **Hugging Face datasets**. |
| **Model**               | A pre-trained BERT model (e.g., `bert-base-uncased`).                   |
| **Hardware**            | CPU is fine for small datasets; GPU speeds up training.                 |
| **Libraries**           | `transformers`, `datasets`, `torch`, `pandas`.                          |

---

## 🚀 **Step-by-Step Process**

---

### **1. Get a Labeled Dataset (No Scraping)**
We’ll use the **Yelp Polarity dataset** (public, labeled reviews).

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("yelp_polarity")

# It has:
# dataset['train']  -> 640,000 reviews (label 0=negative, 1=positive)
# dataset['test']   -> 50,000 reviews
```

> **Note**: This dataset is **binary** (positive/negative). We’ll convert it to **3-class** later.

---

### **2. Preprocess the Data**
We’ll:
- Tokenize the text.
- Convert labels to 3 classes (optional: map negative=0, neutral=1, positive=2).
- Split into train/validation sets.

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

# Tokenize the dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Rename label: 0 -> Negative, 1 -> Positive (we’ll add Neutral later)
# For now, we keep binary. We’ll convert to 3-class in next step.
```

---

### **3. Convert to 3-Class Sentiment (Optional)**
If you want **Negative / Neutral / Positive**:
- Use a **confidence threshold**:
  - Label 0 (negative) with score < 0.4 → **Negative**
  - Label 1 (positive) with score > 0.6 → **Positive**
  - Everything in between → **Neutral**

But for **training**, we need labeled data. Let’s use a **simple rule**:
- Take the existing binary dataset.
- For **50% of positives**, relabel as **Neutral** (to simulate uncertainty).

```python
import numpy as np

def add_neutral(dataset):
    positives = dataset.filter(lambda x: x["label"] == 1)
    negatives = dataset.filter(lambda x: x["label"] == 0)

    # Relabel 50% of positives as Neutral (label=2)
    indices = np.random.choice(positives["label"], size=int(0.5 * len(positives)), replace=False)
    # (In practice, you'd relabel based on indices; this is a sketch)

    # For simplicity, we’ll just keep binary for now.
    return dataset
```

> **Tip**: If you don’t have neutral labels, **start with binary** and expand later.

---

### **4. Fine-Tune the Model**
We’ll use **`Trainer`** from Hugging Face (simplest way).

```python
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2  # Change to 3 if using Neutral class
)

training_args = TrainingArguments(
    output_dir="./sentiment_model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    save_strategy="epoch",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"].shuffle(seed=42).select(range(10000)),  # Subset for speed
    eval_dataset=tokenized_datasets["test"].shuffle(seed=42).select(range(2000)),
)

trainer.train()
```

> **Why a subset?**  
> Training on 640K reviews takes time. We use **10K for training, 2K for validation** to prototype quickly.

---

### **5. Save the Model**
```python
trainer.save_model("./sentiment_model")
tokenizer.save_pretrained("./sentiment_model")
```

Now you have a **fine-tuned sentiment model** ready to use.

---

### **6. Use the Model in Your API**
Load the model in your FastAPI app:

```python
from transformers import pipeline

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="./sentiment_model",
    tokenizer="./sentiment_model"
)

@app.post("/analyze")
async def analyze_sentiment(text: str):
    result = sentiment_analyzer(text)[0]
    return {"label": result["label"], "score": result["score"]}
```

---

## 🧠 **Understanding the Process**

| **Step**               | **What Happens**                                                                 |
|------------------------|----------------------------------------------------------------------------------|
| **Data Loading**       | We use a pre-labeled dataset (no scraping).                                      |
| **Tokenization**       | Convert text to BERT-readable tokens (e.g., "hello" → [101, 7592, 102]).        |
| **Fine-Tuning**        | Adjust BERT’s weights to predict sentiment on our data.                          |
| **Evaluation**         | Check accuracy on a validation set (e.g., 85% accuracy).                         |
| **Deployment**         | Load the model in an API and call it with new text.                              |

---

## ⚡ **Speed & Cost Tips**

| **Tip**                                | **Why It Helps**                                                                 |
|----------------------------------------|----------------------------------------------------------------------------------|
| **Use a small subset**                 | Faster training, lower cost.                                                     |
| **Use `bert-base-uncased`**            | Smaller than `bert-large`, still accurate.                                      |
| **Train on CPU**                       | No GPU needed (slower but free).                                                 |
| **Use Hugging Face Inference API**     | Skip training altogether for a small fee.                                        |
| **Quantize the model**                 | Reduce model size (e.g., `optimize_model.py`).                                   |

---

## 📊 **Expected Results**
| **Metric**          | **Value (Example)** |
|---------------------|---------------------|
| Training Time       | 10-30 minutes (CPU) |
| Model Size          | ~400 MB             |
| Accuracy (binary)   | ~85-90%             |
| Inference Speed     | ~100 ms per review  |

---

## 🔄 **Next Steps**
1. **Train a binary sentiment model** (Positive/Negative) first.
2. **Test it** on real reviews (e.g., from Common Crawl).
3. **Expand to 3-class** (add Neutral) once binary works.
4. **Deploy** in FastAPI and integrate with your keyword search.

---

**Would you like me to:**
- Provide the **full training script** (with data loading, fine-tuning, saving)?
- Show how to **convert to 3-class sentiment**?
- Help **deploy the model** in your FastAPI?

Let me know which step you want to dive into next! 🚀