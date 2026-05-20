# Solution Walkthrough — Presenting a Solar Decision Analysis

## Headline result

The three charts each answer a distinct decision question:
1. "Which package?" → grouped bar chart (scenario × package) showing Standard as the
   robust choice.
2. "Biggest risk?" → simplified 2-driver tornado with dollar labels.
3. "How close to the edge?" → annotated number line showing the $0.011/kWh margin.

The BLUF memo leads with the recommendation (Standard 8 kW), states the key financial
numbers, names the top risk (install cost), and specifies the exact condition that would
flip the recommendation.

## Key steps

1. **Given section runs as-is.** Learners should review it to understand what numbers
   they have available before building any charts.

2. **Chart 1** — Grouped bar chart with three scenario groups (Optimistic/Base/Pessimistic)
   and three bars per group (one per package). Key elements:
   - `ax.bar(x + offset, npvs, width, ...)` with offset per scenario
   - Data labels via `ax.text(bar.get_x() + width/2, height + padding, label)`
   - `ax.axhline(0)` for the zero reference
   - Title phrased as a question

3. **Chart 2** — Only the top 2 tornado rows (head(2) after sorting by range).
   - `ax.barh(i, hi - lo, left=lo, ...)` for horizontal bars
   - `ax.text(hi + offset, i, f"${range:,.0f} swing")` for direct labels
   - No legend needed — drivers are labeled on the y-axis

4. **Chart 3** — The creative chart. The solution uses an `annotate` number line with
   arrows. Other valid approaches: a simple gauge, a comparison bar ("need vs. have"),
   or even a bold text display ("$0.011/kWh cushion" in large font). What matters is
   that the margin is rendered visually, not just printed.

5. **BLUF memo** — Must fill in every bracketed field. The four fields map to:
   - Recommendation: which package and why in one sentence
   - Key numbers: base, optimistic, pessimistic NPV + break-even margin
   - Biggest risk: top tornado driver + dollar amount
   - What would change: the Pessimistic scenario's conditions, stated as a threshold

6. **Reflection** — Should name at least one specific chart and explain the question it
   answers. Learners who write "make the charts clearer" without naming a specific question
   have missed the point.

## Common mistakes to flag

- **Chart 1 not grouped by scenario** — Grouping by package (one group per package with
  three scenario bars) makes it harder to compare packages across scenarios. Grouping by
  package is the more natural academic layout but harder to read for a decision.
- **All 4 tornado drivers in Chart 2** — The instruction says top 2 only. Showing all 4
  adds clutter without adding insight; the CFO needs to know the main risk, not a ranked
  list.
- **Chart 3 as a table** — Printing the two numbers in a code cell is not a chart. The
  exercise specifically asks for a visual representation of the margin.
- **BLUF memo with no numbers** — Writing "the NPV is positive" without a dollar figure
  is not useful to a stakeholder. Every field must have a real number.
- **Reflection describes what the code does** — "Chart 1 uses bar charts" is not
  reflection. The question is: what decision question does each chart answer and why does
  the visual design make that answer easy to read?

## How this exercise feeds the project

**Project step this preps:** Step 9 — Recommendation memo (BLUF format, 1-pager).

**Skills the learner takes with them:**
- The BLUF structure: recommendation first, supporting numbers second, risks third,
  condition-for-changing-mind fourth.
- "Question-first" chart design: title the chart as the question it answers, then make
  the answer visually obvious.
- Simplifying analytical outputs: show only the top 2 drivers, not all 4; write one
  sentence per risk, not a paragraph.

**What's deliberately scoped out:**
- The full sensitivity and scenario analysis — that's the previous exercise. Here, the
  analysis is given and the skill is communication.
- Interactive dashboards — the exercise uses static matplotlib, same as the project.
- Multiple-page reports — the exercise targets a 1-pager, same as the project.
