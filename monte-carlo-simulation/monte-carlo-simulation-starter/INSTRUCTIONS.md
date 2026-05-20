# Stress-Testing Fleet Electrification with Monte Carlo Simulation

## Scenario

You are a data analyst at **VoltRoute**, a fictional urban delivery company operating a
fleet of 20 diesel trucks in a major US metro. The fleet director is weighing two options
for transitioning to electric vehicles:

- **Buy** — purchase 20 Class 4 electric delivery trucks outright at $85,000 each.
  VoltRoute owns the residual value at year 5.
- **Lease** — lease the same trucks at $1,100 per truck per month for five years.
  No residual-value exposure at lease end.
- **Hold** — defer the decision; keep the diesel trucks running for another 5 years.
  This is the baseline (NPV = $0) against which the other options are measured.

Both electric options generate savings relative to Hold through lower fuel costs and
reduced maintenance. The question is which electric option is more attractive — and how
confident VoltRoute should be in that conclusion — given the real uncertainty in
electricity rates, fleet utilization, maintenance savings, and residual values.

To ground the simulation, `data/eia_commercial_rate.csv` contains real monthly US
residential electricity retail prices from FRED / BLS (public domain, see `data/README.md`).
VoltRoute's fleet-rate contract is based on this residential benchmark. The other uncertain
inputs (annual miles, maintenance savings, resale value) are calibrated to DOE and AFDC
fleet benchmarks, also cited in `data/README.md`.

## What you'll deliver

A completed Jupyter notebook (start from `monte_carlo_simulation_starter.ipynb`) that:

1. Loads the EIA rate data and derives the electricity rate distribution (mean and SD for
   2019–2024).
2. Implements `fleet_npv(option, elec_rate, annual_miles, maint_save, resale_pct)` using
   the constants below.
3. Draws 10,000 Monte Carlo samples for each of the four uncertain inputs using
   `np.random.default_rng(42)`. Clips each to a realistic range.
4. Evaluates `fleet_npv` for all three options across all 10,000 draws, producing a
   `pd.DataFrame` of shape (10,000 × 3).
5. Plots overlapping KDE curves for the three options on one axes (including a vertical
   line at NPV = 0).
6. Produces a summary table: mean, SD, 5th percentile, 95th percentile for each option.
7. Computes `P(Buy > Lease)` — the fraction of simulations where Buy beats Lease — and
   `P(NPV > 0)` for each option.
8. Writes a 2–3 sentence interpretation: which option the simulation favors, which is
   riskier, and under what condition Buy would outperform Lease.

## Model and constants

```
N_TRUCKS    = 20
BUY_PRICE   = 85_000   # $ per truck
LEASE_RATE  = 1_100    # $ per truck per month
DIESEL_GAL  = 4.50     # average diesel fuel price ($/gallon)
DIESEL_MPG  = 5.0      # urban delivery truck fuel economy (mpg)
EV_KWH_MILE = 1.2      # energy consumption of Class 4 EV delivery truck (kWh/mile)
DISC_RATE   = 0.06     # fleet hurdle rate
YEARS       = 5        # planning horizon
```

`fleet_npv` should compute, for a given `option`:

- **Buy:**
  `NPV = −N_TRUCKS × BUY_PRICE + PV(annual_savings) + PV(resale_value)`
  where `annual_savings = fuel_savings + maintenance_savings` and
  `resale_value = N_TRUCKS × BUY_PRICE × resale_pct` at year 5.

- **Lease:**
  `NPV = PV(annual_savings − N_TRUCKS × LEASE_RATE × 12)`

- **Hold:** `NPV = 0` (baseline).

`annual_savings = N_TRUCKS × annual_miles × (DIESEL_GAL/DIESEL_MPG − EV_KWH_MILE × elec_rate)
                + N_TRUCKS × maint_save`

## Uncertain inputs and their distributions

| Input | Distribution | Clip range |
| --- | --- | --- |
| `elec_rate` ($/kWh) | Normal(ELEC_MEAN, ELEC_SD) — from EIA data | [0.08, 0.40] |
| `annual_miles` (miles/truck/yr) | Normal(30,000, 4,000) | [10,000, 50,000] |
| `maint_save` ($/truck/yr) | Normal(2,500, 400) | [0, 5,000] |
| `resale_pct` (fraction of BUY_PRICE at yr 5) | Normal(0.40, 0.10) | [0.10, 0.70] |

## Requirements

- Notebook must run top to bottom without errors.
- `ELEC_MEAN` and `ELEC_SD` must be derived from the EIA data — don't hardcode them.
- Use `np.random.default_rng(42)` for all random draws. Use `RNG.normal(...)` clipped
  with `.clip(lo, hi)`.
- The simulation loop must use vectorized operations (one call to `fleet_npv` per option
  using `zip` over the four input arrays), not a pandas `apply` or four nested loops.
- `sim_profits` must be a `pd.DataFrame` with columns `["Buy", "Lease", "Hold"]`.
- The KDE plot must include a vertical line at NPV = 0 and a legend.
- The interpretation paragraph must quantify `P(Buy > Lease)` and state the condition
  under which Buy outperforms.

## Resources

- [FRED: APU000072610 — Residential Electricity Price](https://fred.stlouisfed.org/series/APU000072610)
- [DOE AFDC: Fleet DNA Project](https://afdc.energy.gov/data/)
- [NumPy: default_rng](https://numpy.org/doc/stable/reference/random/generator.html)
- [seaborn: kdeplot](https://seaborn.pydata.org/generated/seaborn.kdeplot.html)

## Note on the data

`data/eia_commercial_rate.csv` contains real monthly US electricity retail prices from
BLS / FRED (public domain). Other simulation parameters are calibrated to DOE and AFDC
fleet benchmarks cited in `data/README.md`. The scenario company **VoltRoute** is fictional.
