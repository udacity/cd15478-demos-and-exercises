# Presenting a Coffee Chain Expansion Analysis

## Scenario

You are a decision analyst at **Cup & Ledger Coffee**, a fictional specialty coffee chain.
A sensitivity and scenario analysis for three store formats has already been run —
the full analysis code is in the notebook's **Given analysis** section, which runs
automatically. You have:

- A 5-year lease NPV (Net Present Value) model for three formats (Flagship, Standard,
  Kiosk) with base-case numbers derived from real US food-away-from-home CPI data.
- A tornado diagram showing which inputs drive the Standard format's NPV most.
- Three named scenarios (Optimistic, Base, Pessimistic) across all formats.
- A break-even daily customer count for the Standard format.

The VP of Real Estate has asked for a one-page summary. She is not a data scientist.
She wants to know: *Which format should we open, why, and what could make that advice
wrong?* She has 5 minutes.

Your job is to translate the analysis into three decision-ready charts and a BLUF-format
executive summary. Every chart should answer one specific business question — not display
all the available data.

## What you'll deliver

A completed Jupyter notebook (start from `presenting_decision_analyses_starter.ipynb`) that:

1. **(Given — no changes needed)** Runs the Cup & Ledger Coffee analysis: loads CPI data, computes
   NPVs and scenarios, builds the tornado, and finds the break-even. Review this section
   to understand the numbers before building the charts.

2. **Chart 1 — "Which format delivers the best return?"** A grouped bar chart showing
   NPV for each format × scenario combination. Use one color per scenario, add data
   labels on each bar, and add a reference line at NPV = 0.

3. **Chart 2 — "What should we worry about most?"** A simplified tornado showing only
   the **top 2 drivers** for the Standard format. Label each bar with the dollar swing.

4. **Chart 3 — "How many customers do we need each day?"** A two-zone horizontal bar
   (red = unprofitable, green = profitable) showing the break-even customer count and
   the base-case assumption on the same axis. Put break-even label to the left of its
   line and the base-case label to the right.

5. **The memo** — A markdown cell structured as a BLUF 1-pager using the template below.

## BLUF memo template

Fill in the bracketed fields with real numbers from the analysis:

```
## Cup & Ledger Coffee — New Market Entry Format Analysis

**Recommendation:** [One sentence — which format and why]

**Key numbers:**
- Standard base-case 5-year NPV: $[X]
- Optimistic scenario: $[X] | Pessimistic: $[X]
- Break-even: [X] customers/day vs. base assumption of [X]/day

**Biggest risk:** [One sentence — top driver from tornado, quantified]

**What would change this recommendation:** [One sentence — the condition under which
the recommendation flips, e.g., "If foot traffic falls below X customers/day..."]
```

## Requirements

- Notebook must run top to bottom without errors.
- Chart 1 must have data labels and a NPV = 0 reference line.
- Chart 2 must show only the top 2 tornado drivers with dollar-swing labels.
- Chart 3 must use the two-zone bar design — not just two printed numbers.
- Every bracketed field in the memo must be filled with a real number.

## Resources

- [matplotlib: axhline / axvline](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axhline.html) — reference lines
- [matplotlib: barh](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.barh.html) — horizontal bars for Chart 3
- [BLUF communication format](https://en.wikipedia.org/wiki/BLUF_(communication)) — memo structure

## Note on the data

`data/food_away_from_home_cpi.csv` contains the US Consumer Price Index for Food Away
from Home (FRED series
[CUUR0000SEFV](https://fred.stlouisfed.org/series/CUUR0000SEFV), US Bureau of Labor
Statistics, public domain). The scenario company **Cup & Ledger Coffee** is fictional;
the underlying price data is real.
