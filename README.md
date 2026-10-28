# Apparel & Textiles Trend Analysis and Forecasting

A reproducible Python project studying historical apparel retail demand, comparing forecasting methods, visualizing trends, and translating findings into business recommendations.

## Research question
What can historical monthly apparel-retail sales tell us about demand direction and seasonality, and which simple forecasting approach performs best on a recent holdout period?

## Data: real public data, not invented sales
The project uses the U.S. Census Bureau retail-sales series distributed by the Federal Reserve Bank of St. Louis (FRED):

- Series: Retail Sales: Clothing and Clothing Accessory Stores
- FRED ID: MRTSSM448USS (seasonally adjusted; millions of current U.S. dollars)
- Source: https://fred.stlouisfed.org/series/MRTSSM448USS
- CSV download: https://fred.stlouisfed.org/graph/fredgraph.csv?id=MRTSSM448USS

This is a transparent retail-demand proxy, not a complete measure of the global apparel and textiles industry. It measures U.S. clothing-store sales in nominal dollars, so inflation, store-channel changes, and U.S.-specific conditions affect interpretation. It does not directly measure units sold, textile production, exports, or global market size.

The script downloads the latest available public observations when you run it. It does not commit made-up historical values or pretend a forecast is an observed fact.

## What the analysis does
1. Downloads and validates the public monthly series.
2. Saves a local raw-data copy for reproducibility.
3. Plots historical sales and a 12-month rolling average.
4. Measures year-over-year changes and monthly seasonal patterns.
5. Compares seasonal-naive, 12-month moving average, and Holt-Winters additive seasonal forecasting on the final 12 months.
6. Reports MAE, RMSE, and MAPE on the holdout period and exports month-by-month actual/predicted values.
7. Exports descriptive statistics, worked month-over-month/year-over-year calculations, and clearly labelled illustrative business sensitivity scenarios.\n8. Selects the lowest-MAE method and refits it on all available data to create a 12-month forecast.
8. Exports charts, metrics, forecast values, and a plain-language summary.

## Quick start
Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python src/analysis.py
```

Generated files are written to data/raw/ and outputs/, including `model_comparison.csv`, `holdout_predictions.csv`, `descriptive_statistics.csv`, `business_scenarios.csv`, `summary.md`, and charts including `holdout_actual_vs_predicted.png`. Internet access is required for the initial data download.

## Repository structure
- data/raw/ — created by the script; downloaded source data
- outputs/ — created by the script; charts, metrics, and forecast
- research/market_context.md — qualitative context and interpretation limits
- src/analysis.py — end-to-end data and forecasting workflow
- requirements.txt — Python dependencies

## Interpretation and limitations
A forecast is a conditional estimate, not a guarantee. The chronological holdout is better suited to time-series data than random shuffling, but one holdout period is not enough to establish universal model superiority. For stronger evaluation, repeat the comparison using rolling-origin backtesting.

The series is nominal, so a rise can reflect higher prices as well as more purchases. This covers one U.S. retail category, not the global market; it does not directly measure units sold or textile-mill output. Structural breaks, inflation, channel shifts, and promotions can weaken historical relationships. Combine with inflation-adjusted sales, inventory, returns, fibre costs, and company-level data where available.

## Sources
- FRED series documentation and data: https://fred.stlouisfed.org/series/MRTSSM448USS
- U.S. Census Bureau Monthly Retail Trade Survey: https://www.census.gov/retail/index.html
- Market context and further reading: research/market_context.md

Educational analysis only. Check the source series, download date, model metrics, and assumptions before using outputs in a business decision or academic submission.
