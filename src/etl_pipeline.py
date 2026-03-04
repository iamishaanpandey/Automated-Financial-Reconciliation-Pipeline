import os
import sqlite3
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
DB_PATH = '../db/reconciliation.db'
OUTPUT_DIR = '../data/'

class FinancialPipeline:
    def __init__(self):
        self.today = datetime.today().strftime('%Y-%m-%d')
        self.yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        os.makedirs('../db', exist_ok=True)
        os.makedirs('../data', exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._setup_db()

    def _setup_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                date TEXT, ticker TEXT, closing_price REAL, volume INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recon_breaks (
                date TEXT, ticker TEXT, internal_price REAL, market_price REAL, discrepancy_pct REAL, status TEXT
            )
        ''')
        self.conn.commit()

    def fetch_market_data(self):
        print(f"[{datetime.now()}] Fetching market data...")
        data = yf.download(TICKERS, start=self.yesterday, end=self.today, progress=False)
        if data.empty:
            raise ValueError("No market data fetched. Market might be closed or dates are invalid.")
        prices = data['Close'].iloc[-1]
        volumes = data['Volume'].iloc[-1]
        market_df = pd.DataFrame({
            'date': self.today,
            'ticker': TICKERS,
            'closing_price': prices.values,
            'volume': volumes.values
        })
        market_df.to_sql('market_data', self.conn, if_exists='append', index=False)
        return market_df

    def generate_mock_internal_data(self, market_df):
        print(f"[{datetime.now()}] Generating internal portfolio data...")
        internal_df = market_df.copy()
        internal_df.loc[internal_df['ticker'] == 'AAPL', 'closing_price'] *= 0.95
        internal_df.loc[internal_df['ticker'] == 'MSFT', 'closing_price'] = np.nan
        internal_df = internal_df[['date', 'ticker', 'closing_price']]
        internal_df.rename(columns={'closing_price': 'internal_price'}, inplace=True)
        internal_file = os.path.join(OUTPUT_DIR, f'internal_portfolio_{self.today}.csv')
        internal_df.to_csv(internal_file, index=False)
        return internal_df

    def run_reconciliation(self, market_df, internal_df):
        print(f"[{datetime.now()}] Running Reconciliation Engine...")
        recon_df = pd.merge(internal_df, market_df[['ticker', 'closing_price']], on='ticker', how='left')
        recon_df.rename(columns={'closing_price': 'market_price'}, inplace=True)
        recon_df['discrepancy_pct'] = ((recon_df['internal_price'] - recon_df['market_price']) / recon_df['market_price']) * 100

        def determine_status(row):
            if pd.isna(row['internal_price']):
                return 'BREAK: Missing Internal Price'
            elif pd.isna(row['market_price']):
                return 'BREAK: Missing Market Price'
            elif abs(row['discrepancy_pct']) > 1.0:
                return 'BREAK: Price Tolerance Exceeded'
            else:
                return 'CLEAN'

        recon_df['status'] = recon_df.apply(determine_status, axis=1)
        breaks_df = recon_df[recon_df['status'] != 'CLEAN']
        breaks_df.to_sql('recon_breaks', self.conn, if_exists='append', index=False)
        report_path = os.path.join(OUTPUT_DIR, f'Recon_Report_{self.today}.xlsx')
        recon_df.to_excel(report_path, index=False, sheet_name='Recon_Summary')
        print(f"[{datetime.now()}] Reconciliation complete. Found {len(breaks_df)} breaks. Report saved to {report_path}")

    def execute_pipeline(self):
        try:
            market_data = self.fetch_market_data()
            internal_data = self.generate_mock_internal_data(market_data)
            self.run_reconciliation(market_data, internal_data)
        except Exception as e:
            print(f"PIPELINE FAILED SLA: {e}")
        finally:
            self.conn.close()

if __name__ == "__main__":
    pipeline = FinancialPipeline()
    pipeline.execute_pipeline()
