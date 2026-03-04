# Automated Financial Benchmark & Reconciliation Pipeline

An enterprise-grade ETL pipeline designed to ingest daily time-series market data, simulate internal portfolio records, and run a daily reconciliation engine to flag pricing anomalies and SLA breaks.

## Tech Stack
- **Python**: Core ETL and Reconciliation logic (Pandas, NumPy)
- **SQLite**: Local database for storing market data and audit logs of data breaks.
- **yfinance**: Simulating a live Bloomberg/Refinitiv API feed.
- **Batch/Shell**: Automated daily scheduling.
