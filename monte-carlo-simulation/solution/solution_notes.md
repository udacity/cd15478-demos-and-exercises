# Solution Walkthrough — Stress-Testing Fleet Electrification with Monte Carlo Simulation

## Headline result

| Strategy | Mean NPV | SD | P(NPV > 0) |
| --- | --- | --- | --- |
| Buy | ~$818K | ~$281K | ~99.8% |
| Lease | ~$899K | ~$250K | ~100% |
| Hold | $0 | $0 | — |

Lease has both higher mean NPV and lower variance. Buy wins only in ~26% of simulations
(high resale-value scenarios). Both EV options are robustly better than Hold.

## Key steps

1. **EIA rate derivation** — `rates[rates["date"].dt.year >= 2019]["rate_per_kwh"].mean()`
   and `.std()`. Same pattern as Module 5.

2. **`fleet_npv` function** — Pre-compute `_PV_FACTOR` and `_PV_RESALE_FACTOR` at module
   scope (avoids re-computing the sum inside every call). The function handles three string
   options with `if/elif/raise`.

3. **Monte Carlo draws** — Four `RNG.normal(mu, sd, N_SIMS).clip(lo, hi)` calls. The global
   `RNG = np.random.default_rng(42)` must be defined once at module scope; calling
   `np.random.default_rng(42)` inside the function makes every draw identical.

4. **`sim_profits` DataFrame** — Dict comprehension over OPTIONS with a `zip` loop. This is
   the exact pattern from the project's Step 5. Alternative: `pd.DataFrame.from_records`
   or vectorized numpy — but the zip-loop is most readable at this level.

5. **KDE plot** — `sns.kdeplot(..., fill=True, alpha=0.25)` for each non-Hold option;
   `ax.axvline(0)` for the zero reference; `ax.axvline(0, linestyle=":", label="Hold")`.

6. **Summary table** — `sim_profits.mean()`, `.std()`, `.quantile(0.05)`, `.quantile(0.95)`.
   Divide by 1e3 to display in $K.

7. **P(Buy > Lease)** — `(sim_profits["Buy"] > sim_profits["Lease"]).mean()`.

## Common mistakes to flag

- **Global RNG not used** — Creating a new `np.random.default_rng(42)` inside each draw
  call makes every simulation draw the same value. One RNG at module scope.
- **Resale not discounted** — `resale = N_TRUCKS × BUY_PRICE × resale_pct` without the
  time-value discount (`/ (1 + DISC_RATE)^YEARS`). The resale happens in year 5, not year 0.
- **Hold in the KDE** — Plotting Hold as a KDE of zeros produces a degenerate spike.
  Better to mark it as a vertical line at zero.
- **Sum inside the function** — Computing `sum(1/(1+r)^t for t in range(YEARS))` inside
  `fleet_npv` runs the sum 10,000 times per option. Pre-compute once at module scope.

## How this exercise feeds the project

**Project step this preps:** Step 5 — Monte Carlo simulation (NumPy-based, no PyMC).

**Code patterns the learner takes with them:**
- `RNG = np.random.default_rng(seed)` at module scope.
- `sim_input = RNG.normal(mu, sd, N_SIMS).clip(lo, hi)` for each uncertain input.
- Dict comprehension: `{opt: [f(opt, *args) for args in zip(...)]} for opt in OPTIONS}`.
- `sim_profits.quantile([0.05, 0.95])` for confidence bands.

**What's deliberately scoped out:**
- CRRA utility and Minimax regret (those are in the decision-theory module, already built).
- Tornado/break-even (that's Module 5).
- Correlated inputs — all four draws are independent here; the project also treats them
  as independent (POSTERIOR_MU is a single draw, not jointly sampled with MARGIN_PCT).
