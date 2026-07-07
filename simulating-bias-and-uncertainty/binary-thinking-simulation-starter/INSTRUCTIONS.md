# When "Probably" Becomes "Definitely"

## Scenario

When a weather app shows **60% chance of rain**, most people round up mentally:
*"It's going to rain."* When it shows **40%**, they round down: *"It won't rain."*

This exercise simulates what happens when you treat probabilities as binary facts,
and quantifies how often that thinking leads you astray.

## What you will deliver

A completed Jupyter notebook that:

1. Simulates 1,000 days at 60% rain probability and shows how many stay dry —
   making binary thinking wrong.
2. Simulates 1,000 days at 40% and shows the symmetric error on the other side.
3. Sweeps all probability levels from 5% to 95% and plots the binary-thinking error
   rate as a curve.
4. Simulates a 30-day month with varied daily forecasts and visualizes which days
   trip up binary thinking.
5. Writes a takeaway identifying the key flaws in binary thinking, with specific
   numbers from steps 1–4.

## Requirements

- Steps 1 and 2 must use `RNG.binomial` to simulate outcomes and produce bar charts.
- Step 3 must produce a line chart of error rate vs. forecast probability with a
  vertical reference line at 50%.
- Step 4 must produce a two-panel chart: forecast probabilities (colored by error)
  in the top panel, actual outcomes vs. binary predictions in the bottom panel.
- The takeaway must cite specific numbers from at least two steps.
- The notebook must run top to bottom without errors.

## Resources you may find useful

- [NumPy: Generator.binomial](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.binomial.html)
- [NumPy: Generator.uniform](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.uniform.html)
- [Matplotlib: plt.subplots](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
