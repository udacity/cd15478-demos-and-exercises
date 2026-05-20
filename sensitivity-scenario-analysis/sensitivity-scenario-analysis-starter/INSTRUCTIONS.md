# Sensitivity and Scenario Analysis for a Coffee Chain

## Scenario

You are a decision analyst at **BrewPoint Coffee**, a fictional specialty coffee chain with
45 locations across the Pacific Northwest. The VP of Real Estate is evaluating entry into
a new metro market and has narrowed the choice to three store formats:

- **Flagship** — 2,000 sq ft street-level café, full menu, premium location. High buildout
  cost, high revenue potential, but more exposed to slow foot-traffic days.
- **Standard** — 1,200 sq ft neighborhood café, core menu. The team's working assumption
  for a typical new market entry.
- **Kiosk** — 400 sq ft kiosk in a transit hub, grab-and-go menu. Low buildout, capped
  upside, but predictable commuter traffic.

The decision is modeled as a 5-year lease NPV (Net Present Value): upfront buildout cost against the present
value of annual operating profits over the lease term.

To anchor the annual price growth assumption, `data/food_away_from_home_cpi.csv` contains
the US CPI for Food Away from Home (FRED series CUUR0000SEFV, US Census Bureau / BLS,
public domain). You'll compute the recent average annual growth rate from that series and
use it as the `ticket_growth` parameter in the NPV model.

## What you'll deliver

A completed Jupyter notebook (start from `sensitivity_scenario_analysis_starter.ipynb`) that:

1. Loads the food-away-from-home CPI data and computes the average annual price growth
   rate over the past five years. Uses that rate as `TICKET_GROWTH`.
2. Implements `cafe_npv(daily_customers, avg_ticket, op_margin, rent_annual, buildout)`
   — a function that returns the 5-year lease NPV in dollars. All parameters must be
   accepted as arguments; no hardcoded values inside the function body.
3. Computes the base-case NPV for all three formats using the stipulated parameters
   below. Identifies the highest-NPV format.
4. Produces a **tornado diagram** for the Standard format: flex each of the four
   drivers (daily customers, average ticket, operating margin, annual rent) one at a
   time by the amounts in the [Tornado flex amounts](#tornado-flex-amounts) table below.
   Plot the two-bar horizontal chart sorted by range, largest at the top.
5. Defines three **named scenarios** for the Standard format — Optimistic, Base,
   Pessimistic — using the parameters in the [Scenarios](#scenarios) table, and
   computes the NPV under each.
6. Computes the **break-even daily customer count** for the Standard format: the
   minimum number of daily customers at which NPV ≥ 0. Use `scipy.optimize.brentq`.
7. Plots a **break-even chart**: a horizontal bar with an "unprofitable" zone (red)
   and a "profitable" zone (green), marking the break-even count and the base-case
   assumption on the same axis.
8. Writes a 2–3 sentence interpretation: which format wins, what the dominant driver
   is, and what condition would flip the Standard recommendation.

## Base-case parameters

| Format | Daily customers | Avg ticket | Op margin | Annual rent | Buildout |
| --- | --- | --- | --- | --- | --- |
| Flagship | 420 | $9.00 | 17% | $110,000 | $470,000 |
| Standard | 250 | $8.50 | 20% | $60,000 | $250,000 |
| Kiosk | 130 | $7.50 | 23% | $42,000 | $75,000 |

Additional fixed parameters: `OPERATING_DAYS = 350`, `DISCOUNT_RATE = 0.08`,
`LEASE_YEARS = 5`. `TICKET_GROWTH` is derived from the CPI data in step 1.

## Tornado flex amounts

| Driver | Low value | High value |
| --- | --- | --- |
| Daily customers | −30 (220) | +30 (280) |
| Average ticket | −$0.50 ($8.00) | +$0.50 ($9.00) |
| Operating margin | −2pp (18%) | +2pp (22%) |
| Annual rent | +$10,000 ($70,000) | −$10,000 ($50,000) |

## Scenarios

| Scenario | Daily customers | Ticket growth | Buildout |
| --- | --- | --- | --- |
| Optimistic | 310 | 5.5% | $230,000 |
| Base | 250 | (from CPI data) | $250,000 |
| Pessimistic | 185 | 1.5% | $275,000 |

## Requirements

- `cafe_npv` must derive all annual revenues and profits from its arguments.
- `TICKET_GROWTH` must be computed from the CPI data — do not hardcode it.
- The tornado chart must be sorted by swing size (largest swing at the top).
- The break-even must use `brentq`, not a manual loop.
- The interpretation must cite specific numbers from the analysis.

## Note on the data

`data/food_away_from_home_cpi.csv` contains the US Consumer Price Index for Food Away
from Home (FRED series
[CUUR0000SEFV](https://fred.stlouisfed.org/series/CUUR0000SEFV)), published by the
US Bureau of Labor Statistics via the Federal Reserve Economic Data (FRED) system.
US Government data, public domain. The scenario company **BrewPoint Coffee** is
fictional; the underlying price index data is real.
