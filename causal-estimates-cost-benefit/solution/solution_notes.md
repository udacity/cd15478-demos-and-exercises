# Solution Walkthrough — From Causal Estimates to ROI

This is the text companion to `causal_estimates_cost_benefit_solution.ipynb`.

## Headline result

| Estimate | Annual earnings lift | ROI (2-yr LTV, $250 cost) |
| --- | --- | --- |
| Naive | −$635 | −608% |
| IPW-corrected | +$223 | +78% |

The sign flip from the naive to the IPW estimate is the central teaching moment. A naive
analyst would recommend shutting down a program that genuinely helps participants.

## Key steps

1. **Naive estimate** — Simple `.mean()` difference. Result: −$635. The control group
   (CPS) has substantially higher pre-program earnings (earnings_pre1, earnings_pre2), making treated
   participants look worse even post-program.

2. **SMD check** — `earnings_pre1` (SMD ≈ −0.60) and `earnings_pre2` (SMD ≈ −0.29) show the largest
   imbalance. These are the primary confounders. `age` also shows imbalance (−0.24).

3. **Propensity model** — Logistic regression on age, educ, married, nodegree, earnings_pre1, earnings_pre2,
   plus race dummies. Clip propensity scores to [0.02, 0.98] to avoid extreme weights.

4. **Overlap check** — KDE plot shows two overlapping distributions; IPW is appropriate.
   Common mistake: not checking overlap before applying IPW.

5. **IPW estimate** — `ipw_estimate` function mirrors the project's implementation exactly.
   Weights: 1/ps for treated, 1/(1−ps) for control.

6. **Bootstrap CI** — 95% CI is wide: roughly [−$1,418, +$2,298]. This reflects the
   genuine difficulty of estimating the treatment effect from a CPS comparison group.
   The wide CI is not a bug — it's an honest statement of uncertainty.

7. **ROI translation** — `(lift × LTV_MULT − COST) / COST`. With LTV_MULT=2 and
   COST=$250, naive gives −608% ROI; IPW-corrected gives +78%.

## Common mistakes to flag

- **Not accounting for the sign flip** — Some learners expect IPW to produce a smaller
  positive estimate; instead it flips from negative to positive. The explanation is in
  the confounding direction: targeted-disadvantaged workers have lower baseline earnings
  than the CPS comparison group.
- **Using a single pooled weight** — Some learners write `w = 1/ps` for all observations
  instead of `1/ps` for treated and `1/(1-ps)` for control. The formula differs by group.
- **Not fitting a new propensity model on each bootstrap resample** — If you apply the
  original ps scores to resampled data, the CI is artificially narrow. Each resample needs
  its own propensity model.
- **Jumping to "expand the program" without CI caveat** — The wide CI means the program's
  ROI is uncertain. Learners should note the CI spans negative territory; the exercise

## How this exercise feeds the project

**Project step this preps:** Step 2 (IPW correction of pilot churn lift) + Step 4
(cost-benefit model translating the corrected lift into 12-month profit).

**Code patterns the learner takes with them:**
- `standardized_mean_diff(df, var, treat)` — identical to the project.
- `ipw_estimate(df, ps, outcome, treat)` — same signature, same weights formula.
- Bootstrap loop: `rng.integers(0, len(df), len(df))`, re-fit propensity model, call
  `ipw_estimate`, catch exceptions.
- ROI formula: `(lift × multiplier - cost) / cost` — a scaled version of what the
  project's `option_profit` function computes.

**Conventions adopted from the project:**
- Module-level constants for payoff parameters.
- `RNG = np.random.default_rng(42)` at module scope.
- `sm.Logit(...).fit(disp=0)` with propensity scores clipped to [0.02, 0.98].

**What's deliberately scoped out:**
- Doubly-robust estimation is not covered — IPW is the target skill.
- Translating the ROI into a memo is the communication module's job.
