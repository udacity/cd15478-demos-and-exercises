# Is Your Friend Actually Good at This?

## Scenario

Your friend claims they correctly predicted 55% of football games last season and made
good money doing it. They have a pick for this weekend and want you to follow it.

Binary thinking says: *"55% is above 50% — they know what they're doing, and I'll
probably win."* This exercise runs the numbers on both claims.

## What you will deliver

A completed Jupyter notebook that:

1. Simulates 1,000 people following one pick at 55% and shows how many lose.
2. Simulates 1,000 random guessers over a 20-game season and shows how many hit 55%+
   by pure chance.
3. Repeats the same simulation over a 100-game season to show the effect of sample size.
4. Plots how often a coin flipper hits 55%+ across season lengths from 10 to 300 games,
   and finds the point where it drops below 10%.
5. Writes a takeaway identifying the two flaws in the original reasoning.

## Requirements

- Steps 1–3 must use `RNG.binomial` to simulate outcomes.
- Steps 2 and 3 must each include a histogram with the 55%+ zone highlighted.
- Step 4 must include a line chart with a 10% reference line and the threshold marked.
- The takeaway must cite specific numbers from at least two steps.
- The notebook must run top to bottom without errors.

## Resources you may find useful

- [NumPy: Generator.binomial](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.binomial.html)
- [Python math.ceil](https://docs.python.org/3/library/math.html#math.ceil)
