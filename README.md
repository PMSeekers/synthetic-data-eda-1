# 🚀 Operations-Driven Data Engineering Portfolio

Welcome! This repository demonstrates my transition from **Amazon Operations** to scalable **Data Engineering** solutions. I build tools inspired by real-world logistical challenges, focusing on synthetic data generation, risk modeling, and audit automation.

---

## 📂 Projects in this Repository

### 🛡️ [Cyber-Security Anomaly Detection](./cyber_security_eda/)
**Scenario-based synthetic log generation for AI security model evaluation.**
* **Core Logic:** Simulates a **Brute-Force attack** (Status 401) hidden within 2,000+ noisy web server logs.
* **Impact:** Provides "Ground Truth" datasets and specialized **LLM Task Definitions** to benchmark AI reasoning in threat detection.
* **Tech:** `Python`, `JSON` (Automated Reporting), `Seaborn` (Attack Timelines).

### 🌐 [Global Supply Chain Analytics](./supply_chain_analytics/)
**Predictive modeling of delivery delays across 50,000 international shipments.**
* **Core Logic:** Stochastic simulation of port congestion and maritime weather disruptions.
* **Business Impact:** Quantifies **"Total Value at Risk"** to prioritize high-value cargo during bottlenecks.
* **Tech:** `Python 3.12+`, `Pandas`, `Seaborn`.

### 💳 [Fintech Fraud Detection Engine](./fintech_fraud_engine/)
**High-fidelity simulation of 100,000 transactions to test anomaly detection patterns.**
* **Core Logic:** Simulates "Impossible Travel" and "Account Takeover" (ATO) scenarios.
* **Impact:** Identifies fraudulent signatures across **~2.4M PLN** of simulated transaction volume.
* **Tech:** `Python`, `NumPy`, `Seaborn`.

### 📦 [Inventory Quality Audit (ICQA) Logic](./inventory_quality_audit/)
**Automated anomaly detection for warehouse logistics, digitizing manual quality workflows.**
* **Core Logic:** Detects negative stock, bin inconsistencies, and "dirty data" patterns.
* **Context:** A Python-based automation of discrepancy identification processes observed during my time at **Amazon**.
* **Tech:** `Python`, `Pandas`, `XlsxWriter`.

---

## 🛠️ Technical Core & Quick Start

* **Languages:** Python 3.12+ (Managed via `uv`)
* **Data Tools:** Advanced Pandas (Vectorized operations, Time-series), NumPy.
* **Visualization:** Seaborn & Matplotlib (Heatmaps, Risk Density, Histograms).
* **AI/LLM Benchmarking:** Designing specialized prompt specifications for model evaluation.

### ⚙️ How to Run
⚙️ How to Run
Clone the repository:

Bash
git clone https://github.com/PMSeekers/synthetic-data-eda-1.git
Install all dependencies:

Bash
pip install -r requirements.txt
Run a specific module (example):

Bash
python cyber_security_eda/synthetic_security_eda.py
