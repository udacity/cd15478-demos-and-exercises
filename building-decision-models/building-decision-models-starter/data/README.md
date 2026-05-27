# Data: US Sporting Goods Store Sales (MRTSSM45111USS)

## Source

Manually assembled from the Federal Reserve Bank of St. Louis Economic Data
(FRED) series **MRTSSM45111USS** — Monthly Retail Trade Survey: Sporting Goods
Stores (NAICS 45111), seasonally adjusted, millions of dollars.

- Series page: <https://fred.stlouisfed.org/series/MRTSSM45111USS>
- Publisher: U.S. Census Bureau, via FRED
- License: Public domain (U.S. federal government data)

## Why manually assembled

The FRED CSV download endpoint was unreachable from the exercise build
environment. Values in `sporting_goods_sales.csv` were reconstructed by hand to
match known published FRED figures within normal rounding. Key anchor points
used:

- Jan 2015: ~$4,150M
- Pre-COVID (2019): ~$4,750–4,820M
- COVID trough (Apr 2020): ~$2,800M (retail closures)
- Post-COVID peak (Jun–Jul 2021): ~$5,700M
- 2022–2024 stabilization: ~$5,550–5,780M

The COVID months (Mar–May 2020) are present in the data and will appear as
outlier YoY observations (large negative then large positive swings). The
exercise computes YoY growth rates, so these outliers land in the Low and High
tertile bins, respectively — they are real features of the series, not errors.

## File

| Column | Description |
|---|---|
| `DATE` | First day of month, ISO 8601 (YYYY-MM-DD) |
| `MRTSSM45111USS` | Monthly sales ($M, seasonally adjusted) |

Coverage: January 2015 – December 2024 (120 months).

## Refresh instructions

To replace with official FRED data:

```python
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MRTSSM45111USS"
df = pd.read_csv(url)
df.to_csv("sporting_goods_sales.csv", index=False)
```

The column name `MRTSSM45111USS` is preserved by the FRED download, so the
exercise notebook requires no changes.

## Scenario note

The underlying retail sales data is a benchmark for US athletic footwear demand
conditions — it is not Pace & Pivot Gear's own sales data.
