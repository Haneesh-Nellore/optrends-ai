# clean_data.py
# Phase 2: Data Cleaning & Preparation for InsightSync

import pandas as pd
from pathlib import Path

# Base directory = project root (…\OpTrends_AI)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "Raw_Datasets"
DATA_CLEANED = BASE_DIR / "Clean_Datasets"

# 1️⃣ Load datasets
sales_path = DATA_RAW / "Sample - Superstore.csv"
inventory_path = DATA_RAW / "Inventory_Dataset.xlsx"
feedback_path = DATA_RAW / "Employee_Feedback.xlsx"

print("Loading files from:", DATA_RAW, "\n")
sales = pd.read_csv(sales_path, encoding="ISO-8859-1")
inventory = pd.read_excel(inventory_path)
feedback = pd.read_excel(feedback_path)

print("✅ Files loaded successfully!")
print("  Sales shape     :", sales.shape)
print("  Inventory shape :", inventory.shape)
print("  Feedback shape  :", feedback.shape, "\n")

# 2️⃣ Standardize column names (strip spaces, replace spaces with _)
for df in [sales, inventory, feedback]:
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

# 3️⃣ Handle nulls (basic safe defaults)
sales.fillna({"Profit": 0, "Discount": 0}, inplace=True)
inventory.fillna({"On_Hand": 0, "On_Order": 0}, inplace=True)
feedback.fillna({"Free_Text": "No comment"}, inplace=True)

# 4️⃣ Convert Date columns to proper datetime
# Sales may have Order_Date; if not, assume Date exists
if "Order_Date" in sales.columns:
    sales["Date"] = pd.to_datetime(sales["Order_Date"], errors="coerce")
else:
    sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")

inventory["Date"] = pd.to_datetime(inventory["Date"], errors="coerce")
feedback["Date"] = pd.to_datetime(feedback["Date"], errors="coerce")

# 5️⃣ Drop duplicate rows
sales_before = sales.shape[0]
inventory_before = inventory.shape[0]
feedback_before = feedback.shape[0]

sales.drop_duplicates(inplace=True)
inventory.drop_duplicates(inplace=True)
feedback.drop_duplicates(inplace=True)

print("Duplicates removed:")
print("  Sales     :", sales_before - sales.shape[0])
print("  Inventory :", inventory_before - inventory.shape[0])
print("  Feedback  :", feedback_before - feedback.shape[0], "\n")

# 6️⃣ Quick check of key columns
print("Unique city counts:")
print("  Sales     :", sales["City"].nunique())
print("  Inventory :", inventory["City"].nunique())
print("  Feedback  :", feedback["City"].nunique(), "\n")

# 7️⃣ Ensure output folder exists
DATA_CLEANED.mkdir(exist_ok=True)

# 8️⃣ Save cleaned versions as CSV (for Power BI)
sales.to_csv(DATA_CLEANED / "Sales_Cleaned.csv", index=False)
inventory.to_csv(DATA_CLEANED / "Inventory_Cleaned.csv", index=False)
feedback.to_csv(DATA_CLEANED / "Feedback_Cleaned.csv", index=False)

print("🎯 Cleaning complete! Cleaned files saved in:", DATA_CLEANED)
