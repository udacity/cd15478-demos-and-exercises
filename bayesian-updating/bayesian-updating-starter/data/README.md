# Data: Hobby & Book Industry Benchmarks and Pilot Scan Data

## Files

### `hobby_book_industry_benchmarks.csv`

Monthly US sporting goods, hobby, musical instrument, and book store retail sales
(in millions of dollars), January 2015 – December 2024.

| Column | Description |
| --- | --- |
| `date` | First day of each month (YYYY-MM-DD) |
| `sales_m` | Total US sporting goods/hobby/book store sales for that month ($M) |

**Source:** US Census Bureau / Federal Reserve Economic Data (FRED), series
[MRTSSM451USS](https://fred.stlouisfed.org/series/MRTSSM451USS) — Monthly Retail Trade Survey,
Sporting Goods, Hobby, Musical Instrument, and Book Stores (NAICS 451). US Government data,
public domain.

**How the prior is derived:** US sporting goods/hobby/book store monthly sales averaged
~$8.11B in 2022–2024 (from this dataset). With ~25,000 US stores in this category, this
implies ~$75.0K in weekly sales per store. Curated subscription boxes are estimated at
roughly 0.8% of category spend, giving ~$600/store/week in box-subscription revenue, or
~25.0 units/week at an average box price of $24. The exercise prior of 18.7 units reflects
that Chapter & Craft's new program is early-stage and targets a narrower audience than the
full category benchmark.

**How to refresh:**
```python
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MRTSSM451USS"
df = pd.read_csv(url)
df.columns = ["date", "sales_m"]
df[df["date"].str[:4].astype(int).between(2015, 2024)].to_csv("hobby_book_industry_benchmarks.csv", index=False)
```

### `pilot_scan_data_weeks1_4.csv` and `pilot_scan_data_weeks5_8.csv`

Weekly aggregate reservation counts reported from Chapter & Craft pilot stores, split into
two files by pilot week so each batch can be loaded only once it would actually be
available — `weeks1_4` first, `weeks5_8` only after the first Bayesian update is computed.

| Column | Description |
| --- | --- |
| `week` | Week number of the pilot (1–4 or 5–8, depending on file) |
| `mean_units_sold` | Average boxes reserved per store that week |
| `n_stores` | Number of stores reporting that week |

**Note:** These files were generated for this exercise to illustrate Bayesian belief
updating with realistic demand dynamics. The pilot started with 3 stores and grew to 8 as
the program expanded. Weekly means are plausible for a new curated-box program in a
specialty retail chain. The values are calibrated to converge toward a per-store demand
level moderately above the FRED-derived, discounted prior of ~18.7 units/week.
