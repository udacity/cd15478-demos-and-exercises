# Data: EIA US Residential Electricity Rate

## File

`eia_residential_rate.csv` — monthly average US residential electricity retail price, 2010–2024.

| Column | Description |
| --- | --- |
| `date` | First day of each month (YYYY-MM-DD) |
| `rate_per_kwh` | Average US residential electricity retail price ($/kWh) |

## Source and license

**Source:** US Bureau of Labor Statistics / Federal Reserve Economic Data (FRED), series
[APU000072610](https://fred.stlouisfed.org/series/APU000072610) — *Average Price: Electricity
per Kilowatt-Hour in U.S. City Average.* Collected by the BLS Consumer Price Index program
as part of the Consumer Expenditure Survey.

**License:** US Government data, public domain.

## How to refresh

```python
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=APU000072610"
df = pd.read_csv(url)
df.columns = ["date", "rate_per_kwh"]
df[df["date"].str[:4].astype(int) >= 2010].to_csv("eia_residential_rate.csv", index=False)
```

## How the data is used

The exercise uses this real rate history to:
1. Derive the **base-case electricity rate** (recent average, ~$0.19/kWh).
2. Justify the **sensitivity flex range** (±$0.02/kWh ≈ ±1 SD of recent monthly rates).
   Note: state-level variation is much larger — Hawaii exceeds $0.40/kWh while several
   states are below $0.12/kWh — so the exercise flips in value proposition across
   realistic US markets.
3. Calibrate the **break-even rate** relative to historical context.

System cost benchmarks (NREL Annual Solar Cost Benchmark Report, 2024 edition,
[nrel.gov/solar](https://www.nrel.gov/solar/market-research-analysis/solar-cost-data.html)):
average US residential installed system cost ≈ $3.00/W before incentives.
Federal solar tax credit (ITC): 30% under the Inflation Reduction Act (26 U.S.C. § 48(a)).
