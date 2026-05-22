# From Causal Estimates to ROI: Evaluating a Career Skills Program

## Scenario

You are a data scientist at **Lift & Launch Works**, a fictional nonprofit workforce development
organization. Over the past several years, Lift & Launch Works has run an online career skills
program designed to boost participants' long-term earnings. The program was offered
primarily to economically disadvantaged workers — people with low pre-program earnings who
needed a boost most. That targeting decision, though well-intentioned, creates a problem:
because participants started out with lower baseline earnings than non-participants, a simple
comparison makes the program look *harmful*.

The dataset comes from the LaLonde (1986) job training study — a classic observational
causal inference benchmark used in economics and data science education — curated by Ho,
Imai, King, and Stuart (2011) and available as the `lalonde` dataset in the MatchIt R
package (public domain). Lift & Launch Works is fictional; the underlying data and research design
are real. The treated participants received a real training program; the comparison group
is drawn from the CPS general population survey.

Your job: correct for the confounding, translate the corrected estimate into a
cost-benefit calculation, and report a defensible ROI figure.

## What you'll deliver

A completed Jupyter notebook (start from `causal_estimates_cost_benefit_starter.ipynb`) that:

1. Loads the data and computes the **naive difference-in-means** between treated and control
   groups on the `re78` earnings outcome.
2. Checks **covariate imbalance** using standardized mean differences for `age`, `educ`,
   `re74`, and `re75`. Identifies which features show the largest imbalance.
3. Fits a **propensity score model** (logistic regression on the four features plus race
   dummies) and produces trimmed propensity scores.
4. Verifies **overlap** with a KDE plot of propensity scores by treatment group.
5. Implements `ipw_estimate(df, ps, outcome, treat)` and computes the IPW-corrected earnings lift.
6. Runs a **bootstrap confidence interval** (500 replicates) to quantify uncertainty.
7. Prints a side-by-side comparison: naive lift vs. IPW lift.
8. Translates the IPW estimate into a **cost-benefit model**:
   - Cost per participant: `COST_PER_PARTICIPANT` (see constants below)
   - Effect persists for `LTV_MULT` years
   - Compute corrected ROI and compare to the ROI implied by the naive estimate.
9. **Validation**: compare the naive estimate, IPW-corrected estimate, and the known
   experimental benchmark ($1,794) side by side. Explain what the gap between them
   implies for the business decision.

## Constants (stipulated)

```
COST_PER_PARTICIPANT = 250   # $ to deliver the online program to one participant
LTV_MULT             = 2     # effect on earnings is assumed to persist for 2 years
```

These are pre-set so you can focus on the causal estimation and ROI mechanics. A cost-benefit
module covers how to build these inputs from first principles.

## Requirements

- Notebook must run top to bottom without errors.
- IPW estimate must use the same precision-weighted inverse-probability formula as described
  in the resources below — don't substitute a regression adjustment.
- Bootstrap must use `numpy.random.default_rng(42)` with integer resampling
  (`rng.integers(0, n, n)`), fitting a new propensity model on each resample.
- The naive vs. IPW comparison must be printed numerically (not just shown in a plot).
- The validation step must quantify the difference between the IPW-based ROI and
  the experimental-benchmark ROI.

## Resources you may find useful

- [Inverse Probability Weighting — Stanford Encyclopedia](https://plato.stanford.edu/entries/causation-probabilistic/) — conceptual overview
- [statsmodels Logit](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.html) — for the propensity model
- [seaborn.kdeplot](https://seaborn.pydata.org/generated/seaborn.kdeplot.html) — for the overlap check
- [LaLonde (1986)](https://www.jstor.org/stable/1806062) — original study
- [MatchIt package documentation](https://cran.r-project.org/package=MatchIt) — dataset source

## Note on the data

`data/lalonde_participants.csv` contains the LaLonde (1986) observational job training
dataset as curated in the MatchIt R package (Ho et al. 2011, CC0). The treated group
received a real job training program; the comparison group is drawn from the CPS general
population survey. The scenario company **Lift & Launch Works** is fictional; the underlying
causal structure and data are real. See `data/README.md` for the full citation.
