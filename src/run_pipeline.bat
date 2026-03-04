@echo off
title Daily Financial Reconciliation Pipeline
echo ==========================================
echo Starting Financial Recon Batch Job...
echo ==========================================
:: Move to the script's current directory
cd /d "%~dp0"
python etl_pipeline.py
echo.
pause
