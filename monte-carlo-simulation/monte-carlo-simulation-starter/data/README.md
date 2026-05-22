# Data: EIA US Residential Electricity Rate (Haul & Charge Co. Fleet Exercise)

## File

`eia_commercial_rate.csv` — monthly average US residential electricity retail price, 2015–2024.

| Column | Description |
| --- | --- |
| `date` | First day of each month (YYYY-MM-DD) |
| `rate_per_kwh` | Average US residential electricity retail price ($/kWh) |

**Note:** This is the residential rate series (BLS APU000072610). Commercial and fleet
rates are typically 10–20% lower than residential; the residential series is used here as
an upper-bound proxy when fleet-specific rate data is unavailable.

## Source

**BLS / FRED series [APU000072610](https://fred.stlouisfed.org/series/APU000072610)** —
Average Price: Electricity per Kilowatt-Hour in U.S. City Average. US Government, public domain.

## Other parameter benchmarks

The simulation uses the EIA rate for the electricity cost distribution. Other uncertain
inputs are calibrated to published fleet benchmarks:

| Parameter | Mean | SD | Source |
| --- | --- | --- | --- |
| Annual miles/truck | 30,000 | 4,000 | AFDC Fleet DNA Project (DOE, public domain) |
| Maintenance savings ($/truck/yr) | $2,500 | $400 | DOE "Costs and Benefits of EV Adoption" (2023) |
| Resale value (% of purchase price at yr 5) | 40% | 10% | NADA commercial vehicle market data (2023) |

**AFDC Fleet DNA Project:** US DOE Alternative Fuels Data Center (afdc.energy.gov), public domain.  
**DOE EV cost study:** US Department of Energy, "Reducing Fleet Costs with EVs," public domain.
