# The Application Numbers Game

## Scenario

A friend of yours wants to break into sports journalism. After some research, you find
that candidates who apply to open roles at sports outlets have roughly a 3% chance of
receiving an offer. Your friend is discouraged: *"3% is basically zero — why bother
applying?"*

This is **binary thinking** — the tendency to treat probabilities below 50% as "won't
happen" and probabilities above 50% as "will happen." It is one of the most common ways
intuition fails when dealing with uncertain outcomes.

This exercise uses simulation to expose the gap between that intuition and actual outcomes.

## What you will deliver

A completed Jupyter notebook (start from `binary_thinking_simulation_starter.ipynb`) that:

1. Simulates 100 single applications at 3% and visualises how often binary thinking is wrong.
2. Mirrors the same test at 55% — showing the overconfidence side of the same bias.
3. Simulates 100 full job searches (30 applications each) and shows the distribution of offers received.
4. Computes P(at least one offer) analytically and from the simulation, then charts the
   before/after: 1 application vs 30 applications at 3%.
5. Solves analytically for the number of applications needed to reach 90% confidence,
   then verifies the result with simulation.
6. Writes a 2–3 sentence takeaway using specific numbers from the exercise.

## Requirements

- Steps 1–3 must use `RNG.binomial` to simulate outcomes.
- Steps 1 and 2 must each include a bar chart.
- Step 3 must include a histogram of offer counts.
- Step 4 must print both the simulation and analytical estimates before showing the chart.
- Step 5 must include both an analytical solution and a simulation verification.
- The takeaway must cite specific numbers from at least two steps.
- The notebook must run top to bottom without errors.

## Resources you may find useful

- [NumPy: Generator.binomial](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.binomial.html)
- [Python math.log](https://docs.python.org/3/library/math.html#math.log)
- [Python math.ceil](https://docs.python.org/3/library/math.html#math.ceil)
