# 📦 Inventory Quality Audit (ICQA) & Anomaly Detection

### 🎯 Project Overview
This project is an automated warehouse inventory audit system, inspired by **Amazon ICQA** (Inventory Control & Quality Assurance) standards. The script translates operational expertise into a scalable Python solution that identifies technical errors in logistics data and ensures data integrity.

---

## 🚀 Key Features

* **🔍 Automated Anomaly Detection**: Statistical outlier detection using **Z-Score** and immediate flagging of negative stock values.
* **🛠️ Missing Data Recovery**: Automatic imputation of missing records based on category medians to maintain dataset consistency.
* **📊 Business Intelligence**: Inventory classification using the **ABC (Pareto) method** and stock depletion forecasting (**DOH - Days on Hand**).
* **📈 Excel Automation**: Generation of professional audit reports with conditional formatting for urgent operational actions.

---

## 💼 Business Context: From Amazon to Code
During **2025-2026 at Amazon**, I was responsible for identifying technical discrepancies in warehouse management software. This project represents a digital transformation of those processes:

1. **Manual Logic → Python Script**: Manual filtering is replaced by an algorithm that performs a full audit in milliseconds.
2. **Scalability**: The tool efficiently processes thousands of records, preparing "clean" data for downstream AI/ML models.

---

## 🛠️ Tech Stack
* **Language**: `Python 3.x`
* **Core Libraries**: `Pandas` (Data Manipulation), `NumPy` (Statistics), `XlsxWriter` (Reporting).
* **Tools**: `VS Code`.

---

## ⚙️ How to Run
1. Install dependencies:
   ```bash
   pip install pandas numpy xlsxwriter openpyxl
