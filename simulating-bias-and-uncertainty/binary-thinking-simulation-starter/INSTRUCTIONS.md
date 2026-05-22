# The Application Numbers Game

## Scenario

You have just finished a data analytics program and you are job searching. Each application
has roughly a 20% chance of converting to an offer.

Most people's gut reaction: *"20% — that's low. It probably won't work."* This is
**binary thinking** — the tendency to treat probabilities below 50% as "won't happen"
and probabilities above 50% as "will happen." It is one of the most common ways intuition
fails when dealing with uncertain outcomes.

This exercise uses simulation to expose the gap between that intuition and actual outcomes.

## What you will deliver

A completed Jupyter notebook (start from `binary_thinking_simulation_starter.ipynb`) that:

1. Simulates 10,000 single applications at 20% and shows how often binary thinking is wrong.
2. Mirrors the same test at 75% — showing the overconfidence side of the same bias.
3. Simulates a 10-application search and computes P(at least one offer).
4. Plots P(at least one offer) vs. applications sent for two per-application rates.
5. Solves analytically for the number of applications needed to reach 90% confidence,
   then verifies the result with simulation.
6. Writes a 2–3 sentence takeaway using specific numbers from the exercise.

## Requirements

- Steps 1–3 must use `RNG.binomial` to simulate outcomes.
- Step 5 must include both an analytical solution and a simulation verification.
- The takeaway must cite specific numbers from at least two steps.
- The notebook must run top to bottom without errors.

## Resources you may find useful

- [NumPy: Generator.binomial](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.binomial.html)
- [Python math.log](https://docs.python.org/3/library/math.html#math.log)
- [Python math.ceil](https://docs.python.org/3/library/math.html#math.ceil)
