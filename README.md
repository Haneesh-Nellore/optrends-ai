# 📊 OpTrends AI

> AI-enhanced retail performance and workforce insight dashboard — unified sales, inventory, and employee sentiment analytics in a single Power BI solution.

Built with **Power BI · Python · HuggingFace Transformers · pandas · NLP**

---

## 🎯 The Problem

Retail organizations suffer from fragmented reporting. Sales data lives in one system, inventory in another, and employee feedback in spreadsheets nobody reads. Leadership makes decisions without a complete picture — and problems like stockouts, delivery delays, or workforce burnout get caught too late.

**OpTrends fixes this by connecting all three into one AI-enhanced dashboard.**

---

## ✨ What It Does

### 📈 Sales Performance
- Real-time sales KPIs across regions, products, and time periods
- Revenue trends, top performers, and underperforming segments
- Key influencer analysis to surface what drives sales outcomes

### 📦 Inventory Health
- Stockout risk detection and low-inventory alerts
- Shipment delay tracking and supplier performance metrics
- Automated flags for inventory anomalies before they become problems

### 👥 Employee Sentiment (AI-Powered)
- NLP pipeline using **HuggingFace Transformers** to analyze open-text employee feedback
- Sentiment classification (Positive / Neutral / Negative) with confidence scores
- Connects employee experience metrics to operational outcomes

---

## 🏗️ Architecture

```
Raw Data (Excel/CSV)
        ↓
Python Data Pipeline
  ├── pandas — data cleaning and transformation
  ├── numpy — numerical processing
  └── HuggingFace Transformers — sentiment analysis on feedback text
        ↓
Enriched Dataset (with sentiment labels + confidence scores)
        ↓
Power BI Dashboard
  ├── Sales Performance Page
  ├── Inventory Health Page
  ├── Employee Sentiment Page
  └── Executive Summary Page
        ↓
AI Visuals (Smart Narrative, Q&A, Key Influencers)
```

---

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| Dashboard & Visualization | Power BI Desktop |
| Data Cleaning | Python (pandas, numpy) |
| NLP / Sentiment Analysis | HuggingFace Transformers |
| AI Visuals | Power BI Smart Narrative, Q&A, Key Influencers |
| Data Storage | Excel / CSV |
| Development | VS Code |

---

## 🤖 NLP Pipeline

The sentiment analysis pipeline processes raw employee feedback text and enriches it with AI-generated labels:

```python
from transformers import pipeline

# Load pre-trained sentiment model
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_feedback(feedback_text):
    """
    Analyze employee feedback and return sentiment + confidence score.
    """
    result = sentiment_analyzer(feedback_text[:512])  # truncate for model limit
    return {
        "sentiment": result[0]["label"],        # POSITIVE / NEGATIVE
        "confidence": round(result[0]["score"], 4)
    }

# Process feedback dataset
import pandas as pd

df = pd.read_csv("employee_feedback.csv")
df["sentiment"] = df["feedback"].apply(
    lambda x: analyze_feedback(x)["sentiment"] if pd.notna(x) else "NEUTRAL"
)
df["confidence_score"] = df["feedback"].apply(
    lambda x: analyze_feedback(x)["confidence"] if pd.notna(x) else 0.0
)

df.to_csv("employee_feedback_enriched.csv", index=False)
print(f"Processed {len(df)} feedback entries")
```

**Output:** Each feedback row gets a `sentiment` label and `confidence_score` that feeds directly into the Power BI dashboard.

---

## 📁 Project Structure

```
optrends-ai/
├── README.md
├── data/
│   ├── sample_sales_data.csv          # Sample sales dataset
│   ├── sample_inventory_data.csv      # Sample inventory dataset
│   └── sample_employee_feedback.csv   # Sample feedback (anonymized)
├── scripts/
│   ├── data_cleaning.py               # pandas data prep pipeline
│   ├── sentiment_analysis.py          # HuggingFace NLP pipeline
│   └── requirements.txt               # Python dependencies
└── dashboard/
    └── OpTrends_Dashboard.pbix        # Power BI dashboard file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Power BI Desktop (free from Microsoft)
- pip

### Run the Python Pipeline

```bash
git clone https://github.com/Haneesh-Nellore/optrends-ai.git
cd optrends-ai/scripts

pip install -r requirements.txt

# Clean and prepare data
python data_cleaning.py

# Run sentiment analysis on employee feedback
python sentiment_analysis.py
```

### Open the Dashboard

1. Open Power BI Desktop
2. File → Open → select `dashboard/OpTrends_Dashboard.pbix`
3. Refresh data sources to point to your enriched CSV files

---

## 📊 Dashboard Pages

**Page 1 — Sales Performance**
- Revenue by region, product category, and time period
- Top 10 products by revenue
- Key Influencers visual: what factors drive high sales?
- Smart Narrative: auto-generated summary of trends

**Page 2 — Inventory Health**
- Current stock levels vs. reorder thresholds
- Stockout risk heatmap by product and location
- Shipment delay tracker
- Low inventory alert table

**Page 3 — Employee Sentiment**
- Sentiment distribution (Positive / Neutral / Negative) over time
- Department-level sentiment breakdown
- Top themes in negative feedback
- Correlation: employee sentiment vs. sales performance

**Page 4 — Executive Summary**
- Single-page overview for leadership
- Key metrics: Revenue, Inventory Health Score, Employee Sentiment Score
- Month-over-month trends

---

## 💡 Key Insights Enabled

- Connect **employee morale dips** to **sales performance drops** in the same time period
- Identify **inventory stockouts** before they impact customers
- Surface **at-risk departments** based on recurring negative sentiment themes
- Give leadership a **single source of truth** instead of 3 separate reports

---

## 📦 Requirements

```
pandas==2.0.3
numpy==1.24.3
transformers==4.35.0
torch==2.0.1
scikit-learn==1.3.0
openpyxl==3.1.2
```

---

## 🔮 Roadmap

- [ ] Azure integration for real-time data refresh
- [ ] Automated email alerts for stockout risks
- [ ] Multi-language sentiment analysis
- [ ] Power BI Service deployment for cloud access
- [ ] REST API to serve sentiment scores to other systems

---

## 📄 License

MIT License — free to use and adapt.

---

## 👨‍💻 Author

Built by [Haneesh Nellore](https://github.com/Haneesh-Nellore) — Microsoft Externship Project

- 💼 [LinkedIn](https://linkedin.com/in/haneeshnellore)
- 🤖 [job-automation-pipeline](https://github.com/Haneesh-Nellore/job-automation-pipeline)
- 🩺 [VitalAI](https://github.com/Haneesh-Nellore/VitalAI)
- 🔧 [aws-serverless-patterns](https://github.com/Haneesh-Nellore/aws-serverless-patterns)
