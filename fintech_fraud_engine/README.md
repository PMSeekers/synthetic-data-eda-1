# 💳 Fintech Fraud Detection Engine

This module generates and audits a high-fidelity synthetic dataset of 100,000 banking transactions. It is specifically designed to benchmark LLM reasoning capabilities in financial anomaly detection.

## 📊 Performance Metrics (N=100,000)
* **Recall (Sensitivity):** 88.8%
* **Total Value at Risk:** ~2,400,000 PLN
* **False Positives (FP):** High (By design, to test LLM deduction skills)

## 🔍 Simulated Scenarios
1. **Impossible Travel**: Transactions from the same user in distant cities (e.g., Warsaw and Dubai) within an impossible timeframe.
2. **Account Takeover (ATO)**: Detection of small "probe" transactions followed by a high-value theft attempt.
3. **Threshold Violations**: Automated flagging of transactions exceeding business-critical limits.

## 🤖 LLM Benchmark Usage
The generated `fintech_big_data.json` is ready for ingestion. Use the provided prompts to test if an AI agent can reduce False Positives compared to a traditional rule-based system.
