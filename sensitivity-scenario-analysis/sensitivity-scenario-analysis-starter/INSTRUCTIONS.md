# Sensitivity and Scenario Analysis for a Solar Installer

## Scenario

You are a decision analyst at **SunRoute**, a fictional residential solar installation
company. SunRoute offers homeowners three package options — Value Pack (5 kW), Standard
(8 kW), and Premium (12 kW) — and earns its margin from the installation contract. Before
recommending a package, SunRoute wants to know: *how sensitive is the homeowner's
10-year net present value (NPV) to the assumptions we're making about electricity rates,
installation costs, and policy incentives?*

The financial case for solar depends on a handful of key inputs, none of which is known
with certainty: electricity rates fluctuate by season, geography, and policy; installed
system costs have been falling for a decade; the federal solar tax credit could be revised;
and each home's actual production depends on orientation, shading, and local climate. If
the financial case is robust to realistic variation in those inputs, that's a strong
signal. If the NPV flips sign under a modest pessimistic flex, the recommendation needs
a caveat.

To anchor the sensitivity ranges, `data/eia_residential_rate.csv` contains real monthly
US residential electricity retail prices from the Bureau of Labor Statistics via
[FRED](https://fred.stlouisfed.org/series/APU000072610) (public domain). You'll use this
real rate history to set the base-case electricity rate and justify the sensitivity flex.

## What you'll deliver

A completed Jupyter notebook (start from `sensitivity_scenario_analysis_starter.ipynb`) that:

1. Loads the EIA electricity rate data, computes the base-case rate (mean of 2019–2024)
   and the flex range (±1 SD over the same period).
2. Implements `system_npv(system_kw, elec_rate, rate_inc, cost_per_w, itc_rate)` —
   the 10-year NPV of a residential solar system — using the constants below.
3. Computes base-case NPV for each of the three package options.
4. Builds a **tornado diagram**: flex each of the four inputs (electricity rate, annual
   rate increase, install cost, federal ITC) one at a time while holding the others at
   their base values. Show which input moves the Standard package's NPV the most.
5. Identifies the **break-even electricity rate**: the rate at which the Standard
   package's NPV equals zero. Use `scipy.optimize.brentq`.
6. Computes NPV under three named scenarios (Optimistic, Base, Pessimistic) for all
   three packages and produces a comparison table.
7. Writes a 2–3 sentence interpretation: which input dominates the sensitivity, and what
   does the break-even rate imply about the robustness of SunRoute's value proposition?

## NPV model and constants (stipulated)

```
ELEC_RATE   = [derived from EIA data]   # $/kWh, base-case
RATE_INC    = 0.030   # annual electricity rate increase (3%/yr)
COST_PER_W  = 3.00    # $/W installed cost (NREL 2024 benchmark)
ITC_RATE    = 0.30    # federal solar tax credit (Inflation Reduction Act)
DISC_RATE   = 0.05    # homeowner discount rate
PROD_KWH_KW = 1300    # kWh produced per kW-installed per year (US average)
YEARS       = 10      # planning horizon
```

`system_npv` should compute:
- `upfront_cost = system_kw × 1000 × cost_per_w × (1 − itc_rate)`
- `annual_savings_year_t = system_kw × PROD_KWH_KW × elec_rate × (1 + rate_inc)^t`
- `NPV = Σ(annual_savings_t / (1 + DISC_RATE)^t for t=1..YEARS) − upfront_cost`

## Named scenarios

| Scenario | `elec_rate` | `rate_inc` | `cost_per_w` | `itc_rate` |
| --- | --- | --- | --- | --- |
| Optimistic | base + 2 × SD | 0.04 | 2.50 | 0.35 |
| Base | base | 0.030 | 3.00 | 0.30 |
| Pessimistic | base − 2 × SD | 0.02 | 3.50 | 0.25 |

(Use the SD you derive from the EIA data; 2 × SD approximates the range of rate environments
SunRoute operates in across different US regions.)

## Requirements

- Notebook must run top to bottom without errors.
- `ELEC_RATE` must be derived from the EIA data — don't hardcode it.
- The sensitivity flex ranges must reference the EIA-derived SD — don't hardcode them.
- The tornado diagram must be sorted by sensitivity range (largest at top) and show the
  central NPV as a vertical dashed line.
- `brentq` must be used for the break-even calculation; don't solve it analytically.
- The interpretation paragraph must name the top driver and quantify the break-even margin.

## Resources you may find useful

- [FRED: APU000072610 — Residential Electricity Price](https://fred.stlouisfed.org/series/APU000072610) — data source
- [NREL: Solar Market Research & Analysis](https://www.nrel.gov/solar/market-research-analysis/solar-cost-data.html) — system cost benchmarks
- [scipy.optimize.brentq](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html) — root-finding for break-even
- [IRS: Residential Clean Energy Credit](https://www.irs.gov/credits-deductions/residential-clean-energy-credit) — ITC details

## Note on the data

`data/eia_residential_rate.csv` contains real monthly US residential electricity retail
prices from the BLS/FRED (APU000072610, public domain). System cost benchmarks come from
NREL's publicly available Annual Solar Cost Benchmark Report. The scenario company
**SunRoute** is fictional; the rate history and cost benchmarks are real.
