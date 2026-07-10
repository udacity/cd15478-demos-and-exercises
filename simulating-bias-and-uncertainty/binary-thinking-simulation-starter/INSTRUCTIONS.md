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
3. Derives the cost-aware decision threshold and plots the expected cost per day for
   binary thinking vs. the optimal threshold across all probability levels.
4. Models a forecaster's wet bias, simulates three decision strategies across all
   probability levels, and compares their expected daily cost.
5. Writes a takeaway identifying the key flaws in binary thinking, with specific
   numbers from steps 1–4.

## Requirements

- Steps 1 and 2 must use `RNG.binomial` to simulate outcomes and produce bar charts.
- Step 3 must derive the optimal threshold algebraically, simulate expected costs
  at each probability level, and plot both cost curves with the gap shaded.
- Step 4 must derive `biased_effective_threshold` algebraically, simulate all three
  strategies, and plot their cost curves with threshold lines marked.
- The takeaway must cite specific numbers from at least two steps.
- The notebook must run top to bottom without errors.

## Resources you may find useful

- [NumPy: Generator.binomial](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.binomial.html)
- [NumPy: Generator.uniform](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.uniform.html)
- [Matplotlib: plt.subplots](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
