# Automated Financial Benchmark & Reconciliation Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Engineering-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Finance](https://img.shields.io/badge/Domain-Middle%20Office%20Operations-success)

## 📌 Project Overview
In asset management and corporate banking, relying on stale or missing market data to calculate Net Asset Value (NAV) can lead to massive regulatory fines and trading losses. 

This project simulates an enterprise-grade **Middle-Office Reconciliation Pipeline**. It automates the daily process of ingesting "Golden Source" market data, comparing it against an internal firm ledger, calculating pricing discrepancies, and flagging Service Level Agreement (SLA) breaks for root-cause analysis.

By leveraging vectorized Pandas operations, this pipeline replaces legacy, error-prone manual Excel VLOOKUP processes—reducing a task that typically takes hours into a sub-second automated background job.

## 🚀 Workflow & Architecture

1. **Golden Source Ingestion:** Connects to Yahoo Finance API (acting as a proxy for enterprise feeds like Bloomberg/Refinitiv) to pull daily closing prices and volumes for a basket of equities.
2. **Internal Ledger Simulation:** Dynamically generates a mock internal portfolio dump, intentionally injecting common data breaks (e.g., 5% stale pricing, null values).
3. **Reconciliation Engine:** Performs a rapid algorithmic merge of both datasets. It calculates the percentage discrepancy between the internal price and the market price.
4. **SLA Flagging:** Applies strict business logic to categorize breaks:
   * `CLEAN`: Prices match within a 1% tolerance.
   * `BREAK: Price Tolerance Exceeded`: Discrepancy > 1%.
   * `BREAK: Missing Internal/Market Price`: Null values detected.
5. **Audit Logging & Reporting:** Saves historical data to a local SQLite database and generates a timestamped Excel report for operational review.

## 🛠️ Tech Stack
* **Language:** Python
* **Data Processing:** Pandas, NumPy
* **Market Data Feed:** `yfinance` API
* **Database:** SQLite (Audit logs & historical tracking)
* **Automation:** Windows Batch Scripting

## 📊 Sample Output (Reconciliation Report)

When the pipeline runs, it generates an Excel report (`Recon_Report_YYYY-MM-DD.xlsx`) identifying the exact anomalies:

| date | ticker | internal_price | market_price | discrepancy_pct | status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-03-04 | AAPL | 250.56 | 263.75 | -5.00 | 🔴 BREAK: Price Tolerance Exceeded |
| 2026-03-04 | MSFT | *NaN* | 208.73 | *NaN* | 🔴 BREAK: Missing Internal Price |
| 2026-03-04 | GOOGL| 303.58 | 303.58 | 0.00 | 🟢 CLEAN |
| 2026-03-04 | AMZN | 655.08 | 655.08 | 0.00 | 🟢 CLEAN |

## 💻 Installation & Usage

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your machine.

### 2. Clone the Repository
```bash
git clone [https://github.com/your-username/Automated-Financial-Reconciliation-Pipeline.git](https://github.com/your-username/Automated-Financial-Reconciliation-Pipeline.git)
cd Automated-Financial-Reconciliation-Pipeline
