# Data: Grocery Industry Benchmarks and Pilot Scan Data

## Files

### `grocery_industry_benchmarks.csv`

Monthly US grocery store retail sales (in millions of dollars), January 2015 – December 2024.

| Column | Description |
| --- | --- |
| `date` | First day of each month (YYYY-MM-DD) |
| `sales_m` | Total US grocery store sales for that month ($M) |

**Source:** US Census Bureau / Federal Reserve Economic Data (FRED), series
[MRTSSM4451USS](https://fred.stlouisfed.org/series/MRTSSM4451USS) — Monthly Retail Trade Survey,
Grocery Stores (NAICS 4451). US Government data, public domain.

**How the prior is derived:** US grocery store monthly sales averaged ~$72.7B in 2022–2024
(from this dataset). With ~38,000 US grocery stores, this implies ~$442K in weekly sales per
store. Premium meal kits represent roughly 0.3% of grocery spend (USDA ERS Food Expenditure
Series, [ers.usda.gov](https://ers.usda.gov/data-products/food-expenditure-series/)), giving
~$1,326/store/week in meal-kit revenue, or ~110 units/week at an average price of $12.
The exercise prior of 80 units reflects that Grain & Gather Grocers's new program is early-stage and
targets a narrower premium segment than the full market benchmark.

**How to refresh:**
```python
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MRTSSM4451USS"
df = pd.read_csv(url)
df.columns = ["date", "sales_m"]
df[df["date"].str[:4].astype(int).between(2015, 2024)].to_csv("grocery_industry_benchmarks.csv", index=False)
```

### `pilot_scan_data.csv`

Weekly aggregate demand reported from Grain & Gather Grocers pilot stores, Weeks 1–8.

| Column | Description |
| --- | --- |
| `week` | Week number of the pilot (1–8) |
| `mean_units_sold` | Average units sold per store that week |
| `n_stores` | Number of stores reporting that week |

**Note:** This file was generated for this exercise to illustrate Bayesian belief
updating with realistic demand dynamics. The pilot started with 3 stores and grew to 8 as
the program expanded. Weekly means are plausible for a premium meal-kit program in mid-tier
grocery markets. The values are calibrated to converge toward the FRED-derived market estimate
of ~110 units/store/week.
