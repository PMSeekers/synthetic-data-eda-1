# 🚀 Operations-Driven Data Engineering Portfolio

Welcome! This repository documents my transition from **Amazon Operations** to building scalable **Data Engineering** solutions. I develop tools inspired by real-world logistical challenges, focusing on synthetic data generation, risk modeling, and audit automation.

---

## 📂 Projects Overview

### 🛡️ [Cyber-Security Anomaly Detection](./cyber_security_eda/)
**Scenario-based synthetic log generation for AI security model evaluation.**
* **Business Logic:** Simulation of a **Brute-Force attack** (Status 401) hidden within 2,000+ noisy web server logs.
* **Impact:** Provides "Ground Truth" datasets and specialized LLM task definitions to benchmark AI reasoning in threat detection.
* **Stack:** `Python`, `JSON`, `Seaborn`.

### 🌐 [Global Supply Chain Analytics](./supply_chain_analytics/)
**Predictive modeling of delivery delays across 50,000 international shipments.**
* **Business Logic:** Stochastic simulation of port congestion and maritime weather disruptions.
* **Impact:** Quantifies **"Total Value at Risk"** (TVaR) to prioritize high-value cargo during supply chain bottlenecks.
* **Stack:** `Python 3.12+`, `Pandas`, `Seaborn`.

### 💳 [Fintech Fraud Detection Engine](./fintech_fraud_engine/)
**High-fidelity simulation of 100,000 transactions to test anomaly detection patterns.**
* **Business Logic:** Simulates "Impossible Travel" and Account Takeover (ATO) scenarios.
* **Impact:** Identifies fraudulent signatures across a simulated transaction volume of **~2.4M PLN**.
* **Stack:** `Python`, `NumPy`, `Seaborn`.

### 📦 [Inventory Quality Audit (ICQA) Logic](./inventory_quality_audit/)
**Automated anomaly detection for warehouse logistics (Digitalizing Quality Workflows).**
* **Business Logic:** Detects negative stock, bin inconsistencies, and "dirty data" patterns.
* **Context:** A Python-based automation of discrepancy identification processes based on firsthand experience at **Amazon**.
* **Stack:** `Python`, `Pandas`, `XlsxWriter`.

---

## 🛠️ Technical Stack & Competencies

| Category | Technologies |
| :--- | :--- |
| **Languages** | Python 3.12+ (Managed via `uv`) |
| **Data Processing** | Advanced Pandas (Vectorized operations, Time-series), NumPy |
| **Visualization** | Seaborn, Matplotlib (Risk Heatmaps, Density Plots) |
| **AI/LLM** | Prompt engineering and specification design for model evaluation |

---

## ⚙️ Quick Start

1. **Clone the repository:**
    ```bash
    git clone [https://github.com/PMSeekers/synthetic-data-eda-1.git](https://github.com/PMSeekers/synthetic-data-eda-1.git)
    cd synthetic-data-eda-1
    ```

2.  **Install all dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run a specific module (example):**
    ```bash
    python cyber_security_eda/synthetic_security_eda.py
    ```


