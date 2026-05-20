# Building and Solving Decision Models Programmatically

## Scenario

You are the lead decision scientist at **StrideWear**, a fictional athletic
apparel brand preparing to launch a new performance running shoe next season.
The launch commitment must be made now — 12 months before the shoe hits
shelves — so the team cannot wait to see how the market develops before
choosing a strategy. Three go-to-market options are on the table:

- **Full Launch** — broad multi-channel distribution with a $600K marketing
  spend. High upside if the athletic footwear retail market is strong, but a
  meaningful loss if the market turns out to be weak.
- **Regional Launch** — selective rollout in two key regions with a $200K
  marketing budget. Moderate upside and limited downside.
- **Hold** — delay the launch until the following season. Zero incremental
  cost, zero incremental gain.

What makes this decision hard is that the athletic footwear retail market is
uncertain over a 12-month horizon. Year-over-year demand growth can range from
sharply negative (macro slowdown, consumer spending pullback) to strongly
positive (category tailwinds, post-pandemic outdoor spending surge). StrideWear
can estimate the *distribution* of demand environments from historical data,
but cannot eliminate the uncertainty before committing.

To estimate that distribution, the team uses monthly US sporting goods store
sales data from the FRED economic database (series MRTSSM45111USS, NAICS
45111) as a benchmark for the range of demand conditions the athletic footwear
retail category can be in. The reasoning: 10 years of monthly data span a wide
range of year-over-year growth rates — from the COVID-era trough to the
post-pandemic surge — and that historical spread is a credible picture of what
a Low, Base, or High demand environment looks like in numbers. StrideWear's
own markets are not in the data; the data is a benchmark for what demand
conditions historically look like across this retail category.

The Head of Strategy has asked the team to build a decision model — a formal
decision tree with expected value and minimax regret — and to identify which
decision rule the team would lean on if forced to commit today. The deliverable
is the model output and a defended choice of rule. A stakeholder-facing
recommendation will be assembled separately; today's job is the numbers and a
defended analytical stance.

## What you'll deliver

A completed Jupyter notebook (start from
`building_decision_models_starter.ipynb`) that:

1. Loads the monthly sporting goods sales data and computes year-over-year
   growth rates.
2. Drops the initial NaN rows produced by the YoY computation.
3. Classifies each month into one of three demand states — **High**, **Base**,
   or **Low** — using the 33rd and 67th percentiles of the YoY growth rate as
   cut-points (tertile binning).
4. Derives the probability of each demand state (equal 1/3 each, by
   construction of tertile binning) and records the tertile boundaries.
5. Defines the stipulated payoff matrix (see the [Payoff matrix](#payoff-matrix)
   table below) as a `pd.DataFrame` with options as rows and demand states as
   columns.
6. Computes the **expected value (EV)** per option as `(payoffs * p).sum(axis=1)`
   and identifies the EV-maximizing option.
7. Computes the **minimax regret** per option (construct the regret matrix,
   take the row-wise maximum, identify the row-wise minimum) and identifies
   the minimax-regret option.
8. Builds a **decision tree visualization** using matplotlib: root node →
   option branches → demand-state leaves with payoffs labeled.
9. Produces a side-by-side comparison of what EV-max and minimax regret each
   select. If the two rules disagree, write 1–2 sentences identifying which
   rule you would lean on and why. Do not convert this into a stakeholder-facing
   recommendation — the deliverable stops at the defended-rule level.
10. Performs one **sensitivity flex**: recompute EV under pessimistic weights
    (P(Low) = 0.5, P(Base) = 0.3, P(High) = 0.2) and report whether the
    EV-max option changes.

## Payoff matrix

Twelve-month incremental contribution profit, in $M, relative to Hold = 0 in
every state. These numbers are stipulated so you can focus on the
decision-modeling mechanics. In a real engagement you would derive them from a
cost-benefit model.

| Option | Low demand | Base demand | High demand |
| --- | --- | --- | --- |
| Full Launch | -7.0 | +4.0 | +12.0 |
| Regional Launch | -0.5 | +2.0 | +5.5 |
| Hold | 0.0 | 0.0 | 0.0 |

These values are pre-calibrated so that the two decision rules pick different
options — uncovering that disagreement is one of the goals of this exercise.

## Requirements

- Your notebook must run top to bottom without errors.
- The YoY growth rates must be computed from the data; do not hardcode them.
- The demand-state probabilities must come from the tertile cut (1/3 each by
  construction); do not hardcode 0.333.
- Both decision rules (EV-max and minimax regret) must be computed from the
  payoff matrix and the probability vector — no hand-picked answers.
- The decision tree visualization must use matplotlib with `boxstyle="round"`
  annotations; options as branches off the root; demand states as leaf nodes
  with payoffs labeled.
- The defended-choice paragraph must name the decision rule, must explain the
  tradeoff in one to two sentences, and must not attempt a stakeholder-facing
  recommendation.
- The sensitivity flex must use the same payoff matrix and code path as the
  main analysis; only the probability vector changes.

## Resources you may find useful

- [pandas.DataFrame.pct_change — compute percentage change between rows](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html)
- [pandas.cut — bin continuous values into discrete intervals](https://pandas.pydata.org/docs/reference/api/pandas.cut.html)
- [pandas.DataFrame.max — column-wise or row-wise maximum](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.max.html)
- [matplotlib.axes.Axes.annotate — add text annotations with bounding boxes](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.annotate.html)
- [Wikipedia: Minimax regret](https://en.wikipedia.org/wiki/Minimax_regret) — short conceptual reference.

## Note on the data

`data/sporting_goods_sales.csv` contains monthly US sporting goods store
retail sales (FRED series MRTSSM45111USS, NAICS 45111), manually assembled
from published FRED figures. See `data/README.md` for the full source,
license, and refresh instructions. The scenario company **StrideWear** is
fictional; only the underlying retail sales data is real.
