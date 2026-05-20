# Solution Walkthrough — Sensitivity and Scenario Analysis for a Solar Installer

## Headline result

| Input | Sensitivity range | NPV swing (Standard 8 kW) |
| --- | --- | --- |
| Install cost (±$0.50/W) | $2.50 – $3.50/W | ~$5,600 |
| Federal ITC (±5pp) | 25% – 35% | ~$2,400 |
| Electricity rate (±1 SD) | ±$0.02/kWh | ~$3,700 |
| Annual rate increase (±1pp) | 2% – 4% | ~$1,850 |

Install cost is the top driver; electricity rate is second. Break-even rate ≈ $0.179/kWh
vs. base-case $0.158/kWh — tight margin.

| Scenario | Value Pack 5kW | Standard 8kW | Premium 12kW |
| --- | --- | --- | --- |
| Optimistic | +$7,200 | +$11,500 | +$17,300 |
| Base | +$627 | +$1,004 | +$1,506 |
| Pessimistic | −$8,400 | −$13,500 | −$20,200 |

All packages flip negative in the Pessimistic scenario — the recommendation is
market-condition-dependent.

## Key steps

1. **EIA rate derivation** — `rates[rates["date"].dt.year >= 2019]["rate_per_kwh"].mean()`
   gives ELEC_RATE; `.std()` gives ELEC_SD. Both must come from the data, not be hardcoded.

2. **`system_npv`** — Sum discounted annual savings over `range(1, YEARS+1)`, subtract
   upfront cost net of ITC. Common mistake: off-by-one (`range(YEARS)` instead of
   `range(1, YEARS+1)`, losing year 1).

3. **Tornado** — The `flex` list structure mirrors the project exactly:
   `(driver_name, high_value, low_value, kwarg_name)`. For each row: compute NPV twice
   (one for high, one for low), build a DataFrame, sort by range. Higher cost per watt
   is the "pessimistic" direction for install cost, so `low_val` > `high_val` for that
   input (it makes NPV lower).

4. **Break-even** — `brentq(lambda r: system_npv(STANDARD_KW, r, ...), 0.05, 0.40)`.
   Must bracket a sign change. Verify by printing `system_npv` at a rate below and above
   break-even before calling brentq.

5. **Scenarios** — Named scenarios combine multiple simultaneous inputs changing at once
   (unlike one-at-a-time tornado). The pessimistic scenario NPV is strongly negative,
   which is the intended teaching signal: the base-case recommendation is conditional.

## Common mistakes to flag

- **Hardcoding ELEC_RATE** — The requirement is to derive it from the EIA data. Writing
  `ELEC_RATE = 0.16` directly violates the exercise requirement.
- **Tornado not sorted** — The bars must be sorted by range (smallest at bottom, largest
  at top) so the most impactful driver is at the top of the chart.
- **`brentq` bracket error** — If the search interval doesn't bracket a sign change,
  brentq raises `ValueError`. Common fix: check that `f(0.05) < 0 < f(0.40)`.
- **Scenario table axes swapped** — The scenario table should have packages as rows and
  scenarios as columns for easy comparison.

## How this exercise feeds the project

**Project step this preps:** Step 8 — Sensitivity & robustness (tornado, break-even,
robustness check).

**Code patterns the learner takes with them:**
- The `flex` list-of-tuples structure and the loop that calls `profit_at` twice per row.
  The project uses `profit_at(lift, margin, cac, ltv)` with `**{kw: val}` unpacking.
- `pd.DataFrame(rows).sort_values("range_npv")` — same pattern.
- `brentq(lambda lift: option_profit(RECOMMENDED, lift, ...), 0.0, 0.5)` — same idiom.
- Tornado matplotlib code with `ax.barh` and `ax.axvline` for the central value.

**Conventions from the project:**
- Module-level constants; no hardcoded values inside functions.
- `RECOMMENDED` constant pointing to the strategy being analyzed.

**What's deliberately scoped out:**
- Monte Carlo simulation of simultaneous uncertainty (that's Module 6).
- Recommendation memo formatting (that's Module 7).
