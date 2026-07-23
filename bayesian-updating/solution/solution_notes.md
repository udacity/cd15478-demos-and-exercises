# Solution Walkthrough — Updating Demand Beliefs with Bayesian Methods

This is the text companion to `bayesian_updating_solution.ipynb`.

## Headline result

| Belief state | Mean (units) | SD (units) | Q recommended |
| --- | --- | --- | --- |
| Prior | ~19 | 7.0 | ~22 |
| Posterior 1 (after weeks 1–4) | ~24 | ~1.5 | ~25 |
| Posterior 2 (after weeks 5–8) | ~27 | ~0.7 | ~28 |

Q rises monotonically as data accumulates, and the safety buffer shrinks because the
posterior is tighter. The exercise stops at producing the updated Q — not a stakeholder
recommendation about whether to expand the program.

## Key steps

1. **Prior derivation from benchmark data** — Monthly sporting goods/hobby/book store sales
   averaged ~$8.11B in 2022–2024. Divided by ~25,000 US stores and 4.33 weeks
   gives ~$75.0K/store/week. At 0.8% box share and $24/box → ~25 units/week. Multiplied by
   0.75 (early-stage discount) → **prior_mu ≈ 18.7**. prior_sd = 7.0 is set wider than
   observed sales variability to reflect the genuine uncertainty of a new product launch.
   (This figure moves slightly as the benchmark dataset appends new monthly releases —
   re-run the notebook's derivation cell for the exact current value rather than treating
   18.7 as fixed.)

2. **Splitting batches** — `pilot[pilot["week"] <= 4]` and `pilot[pilot["week"] > 4]`.
   Straightforward; common mistake is using `< 4` and missing week 4.

3. **Likelihood parameters** — `lik_mu = batch["mean_units_sold"].mean()`;
   `lik_sd = batch["mean_units_sold"].std(ddof=1) / np.sqrt(len(batch))`.
   This is the standard error of the weekly means — treating each week as one observation.

4. **`normal_update`** — Precision-weighted arithmetic. The exact function the project uses:
   ```python
   prior_prec = 1 / prior_sd**2
   lik_prec   = 1 / lik_sd**2
   post_var   = 1 / (prior_prec + lik_prec)
   post_mu    = post_var * (prior_prec * prior_mu + lik_prec * lik_mu)
   return post_mu, np.sqrt(post_var)
   ```

5. **Two sequential updates** — Apply `normal_update` twice: once with the prior + batch-1
   likelihood, then with Posterior 1 + batch-2 likelihood. A common mistake is applying
   both batches to the prior simultaneously — that's not sequential updating.

6. **Three-distribution plot** — `scipy.stats.norm.pdf(xs, mu, sd)` for each belief state.
   Use a common x-axis range (0–50 covers all three distributions without clipping).

7. **Q = mean + 0.5 × sd** — Q rises from ~22 → 25 → 28; the buffer term (0.5 × sd)
   shrinks from 3.5 → 0.8 → 0.4. Both the center and the buffer move.

8. **Sensitivity check** — With doubled prior_sd (14), the prior contributes less precision,
   so Posterior 1 shifts closer to the batch-1 likelihood mean (~24.5). The numerics illustrate
   that a diffuse prior "gets out of the way" faster.

## Common mistakes to flag

- **Applying both batches to the prior at once** — compute a combined batch mean and
  standard error and run one update. This is mathematically different from two sequential
  updates and produces a different (less informative) posterior.
- **Using SEM incorrectly** — dividing by `sqrt(total_observations)` instead of
  `sqrt(n_weeks)`. Since each week's mean is one data point in the likelihood, the SE of
  those weekly means is `std(weekly_means) / sqrt(n_weeks)`.
- **Hardcoding prior_mu** — the requirement is to derive it from the benchmark data. Learners
  who write `prior_mu = 18.7` directly without the derivation lose the connection to the
  underlying data.
- **Not showing the distribution plot** — the three overlaid curves are the visual payoff
  of the exercise. Missing them means the learner hasn't seen belief sharpening visually.

## How this exercise feeds the project

**Project step this preps:** Step 3 — Bayesian updating (Normal-Normal conjugate updates).

**Code patterns the learner takes with them:**
- `normal_update(prior_mu, prior_sd, lik_mu, lik_sd)` — identical function signature used
  in the project. The project calls it twice: prior + pilot → Posterior 1, then
  Posterior 1 + survey → Posterior 2.
- Sequential application: the output of one update feeds the next as the new prior.
- Precision-weighted arithmetic: the exact formula the project uses.

**Conventions adopted from the project:**
- Module-level constants (`PRIOR_SD`, `Q_BUFFER`) rather than hardcoded values.
- `normal_update` returns a tuple `(mu, sd)`, unpacked immediately.

**What's deliberately scoped out:**
- Where the likelihood parameters come from (the IPW-corrected pilot estimate) — that's
  the causal estimates module.
- The survey adjustment (stated-to-revealed ratio) — that's specific to the Nimbus project
  scenario and doesn't need to appear in this exercise.
- PyMC — the course owner flagged this as too black-box for this audience. The exercise
  is intentionally closed-form only.
