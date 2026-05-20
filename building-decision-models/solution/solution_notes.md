# Solution Walkthrough — Building and Solving Decision Models Programmatically

This is the text companion to `building_decision_models_solution.ipynb`. It
summarizes the key steps, the numbers a learner should arrive at, and the most
common mistakes to flag.

## Headline result

| Decision rule | Selected option | Score |
| --- | --- | --- |
| EV-max | Full Launch | EV = $3.00M |
| Minimax regret | Regional Launch | Max regret = $6.50M |

**EV-max and minimax regret pick different options** — that disagreement is the
engineered teaching moment. Full Launch has the highest expected profit ($3.0M)
because the $12.0M High-demand upside outweighs the −$7.0M Low-demand loss on
average. Regional Launch wins on minimax regret because its worst-case "I wish I
had done something else" outcome ($6.5M) is just below Full Launch's ($7.0M).
The tradeoff is clear: more expected profit vs. less maximum regret.

The exercise stops at a defended choice of decision rule. It does not ask
learners to translate the comparison into a stakeholder-facing recommendation.

## Key steps

1. **Load data** — `pd.read_csv` with `parse_dates=["DATE"]` and `index_col="DATE"`.
   Result is a 120-row DataFrame with one column `MRTSSM45111USS`.

2. **YoY growth rate** — `sales["MRTSSM45111USS"].pct_change(12) * 100`.
   Drop NaN with `dropna(subset=["yoy"])`. Result: 108 rows, YoY range roughly
   −40% (COVID trough) to +102% (post-COVID recovery spike).

3. **Tertile binning** — `Q33 = sales["yoy"].quantile(1/3)` ≈ 1.07%;
   `Q67 = sales["yoy"].quantile(2/3)` ≈ 3.11%. `pd.cut` with
   `bins=[-inf, Q33, Q67, inf]` and `labels=["Low", "Base", "High"]`.
   Counts: Low ≈ 36, Base ≈ 37, High ≈ 35 (near-equal by construction).

4. **Probability vector** — `p = pd.Series({"Low": 1/3, "Base": 1/3, "High": 1/3})`.
   Use the exact fraction 1/3, not the empirical proportions, so that EV
   arithmetic is clean and the exercise is reproducible regardless of dataset
   length.

5. **Payoff matrix** — `pd.DataFrame` with options as rows (`Full Launch`,
   `Regional Launch`, `Hold`), states as columns (`Low`, `Base`, `High`).
   Pull values from module-level constants.

6. **Expected value** — `ev = (payoffs * p).sum(axis=1)`.
   Full Launch: **$3.00M**. Regional Launch: **$2.33M**. Hold: **$0.00M**.
   EV-maximizing option: **Full Launch**.

7. **Minimax regret** — `best_per_state = payoffs.max(axis=0)`;
   `regret = best_per_state - payoffs`; `max_regret = regret.max(axis=1)`.
   Max regret: Full Launch $7.0M, Regional Launch $6.5M, Hold $12.0M.
   Minimax-regret option: **Regional Launch** ($6.5M).

8. **Decision tree visualization** — root node at x=1, option nodes at x=4,
   state leaf nodes at x=8. Three state leaves per option, spread ±0.9 units
   in y. Each leaf labeled with state name and payoff. `boxstyle="round"`,
   three distinct fill colors (yellow root, blue options, green states).

9. **Comparison and defended rule** — the side-by-side table shows the
   disagreement. A learner leaning on EV-max should note that a $1M gap in
   expected profit and repeated decisions favor Full Launch. A learner leaning
   on minimax regret should note that Full Launch's $7M downside exposure is
   close to its max regret threshold, and Regional Launch provides meaningful
   downside protection for only $0.67M less in expected profit.

10. **Sensitivity flex** — under P(Low)=0.5, P(Base)=0.3, P(High)=0.2:
    Full Launch EV drops to **$0.10M** (nearly zero); Regional Launch holds
    at **$1.45M**. The EV-max choice **flips to Regional Launch**. This is
    the intended teaching takeaway: the EV-max recommendation is conditional
    on the probability assumption, and the baseline equal-1/3 case is
    relatively optimistic.

## Code snippets

```python
# The EV calculation — the most important snippet
p = pd.Series({"Low": 1/3, "Base": 1/3, "High": 1/3})
ev = (payoffs * p).sum(axis=1)
```

```python
# Minimax regret — easy to get the axis directions wrong
best_per_state = payoffs.max(axis=0)   # axis=0: max across options per state
regret = best_per_state - payoffs      # elementwise subtraction
max_regret = regret.max(axis=1)        # axis=1: max across states per option
```

```python
# Sensitivity flex — only the probability vector changes
p_pess = pd.Series({"Low": 0.5, "Base": 0.3, "High": 0.2})
ev_pess = (payoffs * p_pess).sum(axis=1)
```

## Common mistakes to flag

- **Hardcoding probabilities as 0.333.** The requirement is to derive them from
  the tertile binning by construction (exact 1/3), not to hardcode a rounded
  approximation. `pd.Series({"Low": 1/3, "Base": 1/3, "High": 1/3})` is the
  correct form.

- **Swapping axis=0 and axis=1 in the regret computation.** `payoffs.max(axis=0)`
  gives the best payoff *across options* for each state (a Series indexed by
  state). `payoffs.max(axis=1)` would give the best payoff across states for
  each option — wrong. Then `regret.max(axis=1)` gives the worst-case regret
  across states for each option — that is correct.

- **Using `print(df)` instead of `display(df)`.** The `display()` function
  renders the DataFrame as a rich HTML table in the notebook. `print(df)` gives
  a plain-text representation and suppresses the rendered output.

- **Interpreting regret as the payoff, not the gap.** Regret for option A in
  state S = (best payoff in S) − (A's payoff in S). A learner who confuses
  regret with the payoff itself will produce a nonsensical regret matrix.

- **Jumping past the defended rule to a stakeholder recommendation.** The
  exercise deliberately stops at naming a decision rule and explaining the
  tradeoff. Translating the output into a recommendation memo — with caveats,
  risk appetite discussion, and strategic context — is taught in separate
  modules.

## How this exercise feeds the project

**Project step this preps:** Step 6 — Decision tree (options × posterior states,
backward induction).

**Code patterns the learner takes with them:**

- `p = pd.Series({"Low": 1/3, "Base": 1/3, "High": 1/3})` — the probability
  vector as a named Series. The project uses the same structure, with
  probabilities derived from tertile-binning posterior draws.
- `payoffs = pd.DataFrame({"Low": {...}, "Base": {...}, "High": {...}})` with
  options as the index — the project uses this exact layout for its 4 × 3
  matrix.
- `ev = (payoffs * p).sum(axis=1)` — the EV formula is identical in the
  project.
- The minimax regret three-liner (`best_per_state`, `regret`, `max_regret`)
  is reused verbatim.
- The matplotlib decision tree with `boxstyle="round"` annotations is the same
  rendering approach used in the project solution.

**Conventions adopted from the project:**

- Module-level constants for all tunable payoff values.
- Probability vector as `pd.Series` indexed by state name.
- Payoff matrix as `pd.DataFrame` with options as rows.
- `display()` for all DataFrames.
- No CRRA utility (that belongs to the expected-utility module, already built).

**What's deliberately scoped out:**

- Building the payoff matrix from a cost-benefit model — the matrix is
  stipulated here; the project derives it from Nimbus's revenue and cost
  assumptions.
- CRRA expected utility — covered in the prior exercise
  (`comparing-marketing-campaigns`); not repeated here to avoid overlap.
- Translating the comparison into a stakeholder recommendation — taught in the
  communication-focused modules.

This section is for the SME reviewing the exercise — not for the learner. It
documents the intentional connection between this exercise and the capstone
project so the connection survives across exercise revisions and course
re-orderings.
