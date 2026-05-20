# Presenting a Solar Decision Analysis

## Scenario

You are a decision analyst at **SunRoute**, a fictional residential solar installer.
A sensitivity and scenario analysis of three solar packages has already been run —
the full analysis code is in the notebook's **Given analysis** section, which runs
automatically. You have:

- A 10-year NPV model for three solar packages (Value Pack 5 kW, Standard 8 kW, Premium
  12 kW) with base-case numbers derived from real EIA electricity rate data.
- A tornado diagram showing which inputs drive the Standard package's NPV most.
- A three-scenario table (Optimistic, Base, Pessimistic) for all packages.
- A break-even electricity rate for the Standard package.

The CFO at a SunRoute customer — a regional property management firm considering solar
for 10 properties — has asked for a one-page summary. She is not a data scientist. She
wants to know: *Which package makes the most sense, why, and what could make that advice
wrong?* She has 5 minutes.

Your job is to translate the analysis into four decision-ready charts and a BLUF-format
executive summary. The emphasis is on making every chart answer a specific business
question, not on displaying all the analytical outputs.

## What you'll deliver

A completed Jupyter notebook (start from `presenting_decision_analyses_starter.ipynb`) that:

1. **(Given — no changes needed)** Runs the SunRoute analysis: loads EIA data, computes
   all NPVs and scenarios, and produces the raw tornado data. Review this section to
   understand the inputs.

2. **Chart 1 — "Which package is best?"** A bar chart showing base-case NPV for each
   package × scenario combination. Make it easy to read at a glance: use a single color
   per scenario (Optimistic / Base / Pessimistic), add data labels, and add a reference
   line at NPV = 0.

3. **Chart 2 — "What's the biggest risk?"** A simplified tornado diagram for the Standard
   package showing only the **top 2 drivers** (by sensitivity range). Label each bar with
   the dollar range it represents. Use direct labels rather than a legend.

4. **Chart 3 — "How close to the edge are we?"** A single number visualization: display
   the break-even electricity rate and the current rate on the same axis (e.g., a simple
   dot plot or annotated number line), making it clear how much cushion the Base scenario
   has.

5. **The memo** — A markdown cell structured as a BLUF 1-pager using the template below.

6. **Reflection** — A markdown cell with 2–3 sentences explaining what makes a "decision-
   ready" chart different from a "data-dump" chart, using your three charts as examples.

## BLUF memo template

Fill in the bracketed fields:

```
## SunRoute Solar Investment Analysis — Executive Summary

**Recommendation:** [One sentence — which package and why]

**Key numbers:**
- Base-case 10-yr NPV (Standard 8 kW): $[X]
- Optimistic scenario: $[X] | Pessimistic: $[X]
- Break-even electricity rate: $[X]/kWh vs. current $[X]/kWh

**Biggest risk:** [One sentence — top driver from tornado, quantified]

**What would change this recommendation:** [One sentence — the condition under which
the Pessimistic scenario becomes the base case, e.g., "If installed costs rise above
$X/W or electricity rates fall below $X/kWh, the Standard package's NPV turns
negative."]
```

## Requirements

- Notebook must run top to bottom without errors.
- Chart 1 must have data labels and a zero reference line.
- Chart 2 must show only the top 2 drivers (not all 4), with bar labels showing the
  dollar ranges.
- Chart 3 must visually communicate the margin between current rate and break-even rate
  (not just print the two numbers).
- The BLUF memo must fill in every bracketed field with a real number from the analysis.
- The reflection paragraph must name at least one specific chart and explain what question
  it answers.

## Resources

- [matplotlib: annotate](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.annotate.html) — for data labels
- [matplotlib: axhline / axvline](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axhline.html) — for reference lines
- [BLUF communication format](https://en.wikipedia.org/wiki/BLUF_(communication)) — structure and rationale

## Note on the data

Analysis is grounded in real EIA electricity rate data (BLS/FRED APU000072610, public
domain). Other parameters follow NREL benchmarks as documented in the sensitivity
analysis exercise's `data/README.md`. The scenario company **SunRoute** is fictional.
