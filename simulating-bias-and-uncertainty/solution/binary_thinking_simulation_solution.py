# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # When "Probably" Becomes "Definitely"
# ## Simulating the Cost of Probability Rounding
#
# When a weather app says **60% chance of rain**, most people round up mentally: *"It's going to rain."*
# When it says **40%**, they round down: *"It won't rain."*
#
# This feels like common sense — it turns a messy number into a clear action. But rounding comes with a hidden, predictable cost.
#
# This exercise simulates what happens when you treat probabilities as binary facts, and shows how the error rate follows directly from the math.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import matplotlib.pyplot as plt

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. Rounding up: "60% means it will rain"
#
# The app shows **60% chance of rain**. Binary thinking rounds up: *"It's going to rain — I'll cancel the picnic."*
#
# Simulate 1,000 days where the true rain probability is 60%.
# How many of those days stay dry — making binary thinking wrong?

# %%
n_days = 1_000
p_rain = 0.60

outcomes = RNG.binomial(1, p_rain, n_days)
rainy = outcomes.sum()
dry   = n_days - rainy

print(f"Forecast: {p_rain:.0%} chance of rain")
print(f"Binary thinking predicts: rain every single day")
print()
print(f"Rainy days: {rainy:,}  ({rainy/n_days:.0%})")
print(f"Dry days:   {dry:,}  ({dry/n_days:.0%})  ← binary thinking is wrong here")

# %%
fig, ax = plt.subplots(figsize=(5, 3.5))
bars = ax.bar(['Rainy\n(binary right)', 'Dry\n(binary wrong)'],
              [rainy, dry],
              color=['#cccccc', '#e07b54'], edgecolor='white', width=0.5)
ax.bar_label(bars, fmt=lambda v: f'{int(v):,}\n({v/n_days:.0%})', padding=4, fontsize=10)
ax.set(title=f'1,000 days at {p_rain:.0%} rain probability',
       ylabel='Number of days', ylim=(0, 1_200))
plt.tight_layout()
plt.show()

# %% [markdown]
# Binary thinking is wrong **~40% of the time** — even though the forecast was 60%.
# The error rate is exactly the complement of the probability: `1 - 0.60 = 0.40`.
#
# This is not a flaw in the app. The app was right. The rounding was the mistake.

# %% [markdown]
# ## 2. Rounding down: "40% means it won't rain"
#
# Now the app shows **40% chance of rain**. Binary thinking rounds down: *"It probably won't rain — no need for an umbrella."*
#
# Simulate 1,000 days at 40% true rain probability.
# How many of those days actually rain — leaving you without an umbrella?

# %%
p_rain_low = 0.40

outcomes_low = RNG.binomial(1, p_rain_low, n_days)
rainy_low = outcomes_low.sum()
dry_low   = n_days - rainy_low

print(f"Forecast: {p_rain_low:.0%} chance of rain")
print(f"Binary thinking predicts: dry every single day")
print()
print(f"Dry days:   {dry_low:,}  ({dry_low/n_days:.0%})")
print(f"Rainy days: {rainy_low:,}  ({rainy_low/n_days:.0%})  ← caught without an umbrella")

# %%
fig, ax = plt.subplots(figsize=(5, 3.5))
bars = ax.bar(['Dry\n(binary right)', 'Rainy\n(binary wrong)'],
              [dry_low, rainy_low],
              color=['#cccccc', '#e07b54'], edgecolor='white', width=0.5)
ax.bar_label(bars, fmt=lambda v: f'{int(v):,}\n({v/n_days:.0%})', padding=4, fontsize=10)
ax.set(title=f'1,000 days at {p_rain_low:.0%} rain probability',
       ylabel='Number of days', ylim=(0, 1_200))
plt.tight_layout()
plt.show()

# %% [markdown]
# Rounding down causes just as many errors: about **40% of the time**, it rains anyway.
#
# The two cases are symmetric:
# - 60% forecast → round up → wrong ~40% of the time
# - 40% forecast → round down → wrong ~40% of the time
#
# A 60% forecast and a 40% forecast *feel* completely different. Under binary thinking, they produce the same error rate.

# %% [markdown]
# ## 3. The rounding curve — error rate at every probability
#
# Sections 1 and 2 showed two specific points. Now let's see the full picture.
#
# For any forecast probability `p`:
# - If `p > 0.50` → binary thinking predicts rain → wrong when it stays dry, probability `1 - p`
# - If `p ≤ 0.50` → binary thinking predicts dry → wrong when it rains, probability `p`
#
# Simulate 1,000 days at each probability level from 5% to 95%.
# Plot the binary-thinking error rate across the full range.

# %%
probabilities = [p / 100 for p in range(5, 96, 5)]
error_rates   = []

for p in probabilities:
    sim = RNG.binomial(1, p, 1_000)
    if p > 0.5:
        errors = (1_000 - sim.sum()) / 1_000   # predicted rain, wrong when dry
    else:
        errors = sim.sum() / 1_000              # predicted dry, wrong when rainy
    error_rates.append(errors)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot([p * 100 for p in probabilities], [e * 100 for e in error_rates],
        '-o', color='#e07b54', ms=5)
ax.axvline(50, ls='--', color='gray', lw=1, label='50% — true coin flip')
ax.set(title='Binary-thinking error rate across all forecast probabilities',
       xlabel='Forecast probability (%)', ylabel='Error rate (%)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))
ax.legend(fontsize=9)
plt.tight_layout()
plt.show()

# %% [markdown]
# The error rate peaks at 50% and drops toward the extremes — but slowly. At **70% chance of rain**, binary thinking is still wrong **~30% of the time**.
#
# Forecasts in the 30%–70% range — exactly where weather predictions often land — are far more uncertain than they feel.

# %% [markdown]
# ## 4. A month of forecasts — where does rounding go wrong?
#
# Real forecasts change day to day. Simulate a 30-day month where each day's true rain probability is drawn uniformly between 20% and 80%.
#
# For each day:
# 1. Simulate whether it actually rains.
# 2. Record what a binary thinker would predict (rain if forecast > 50%, dry otherwise).
# 3. Count and visualize the binary thinker's errors.

# %%
n_forecast_days = 30

true_probs      = RNG.uniform(0.20, 0.80, n_forecast_days)
actually_rained = RNG.binomial(1, true_probs)

binary_predictions = (true_probs > 0.50).astype(int)
binary_errors      = (binary_predictions != actually_rained).sum()

print(f"Over {n_forecast_days} days (forecasts ranging {true_probs.min():.0%}–{true_probs.max():.0%}):")
print(f"  Days where binary thinking was wrong: {binary_errors} ({binary_errors/n_forecast_days:.0%})")

# %%
days   = range(1, n_forecast_days + 1)
colors = ['#e07b54' if err else '#cccccc'
          for err in (binary_predictions != actually_rained)]

fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)

axes[0].bar(days, true_probs * 100, color=colors, edgecolor='white', width=0.7)
axes[0].axhline(50, ls='--', color='gray', lw=1)
axes[0].set(ylabel='Forecast probability (%)',
            title='30-day forecast — orange bars are days binary thinking got wrong')
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))

axes[1].bar(days, actually_rained, color='steelblue', alpha=0.6,
            edgecolor='white', width=0.7, label='Actually rained')
axes[1].step(list(days), binary_predictions, where='mid',
             color='#e07b54', lw=1.5, label='Binary prediction')
axes[1].set(xlabel='Day of month', ylabel='Rain (1) / Dry (0)', ylim=(-0.1, 1.4))
axes[1].legend(fontsize=9)

plt.tight_layout()
plt.show()

# %% [markdown]
# The orange bars cluster near the 50% dashed line — the forecasts that *feel* most decisive ("just above" or "just below" the midpoint) are exactly where rounding is most likely to backfire.

# %% [markdown]
# ## 5. Takeaway
#
# Probability rounding is one of the most common intuitive shortcuts in everyday reasoning — and one of the most predictably costly.
#
# Three things this simulation showed:
#
# 1. **A 60% forecast is not a prediction of rain.** It stays dry ~40% of the time. Treating it as a certainty means you're wrong nearly as often as you're right.
#
# 2. **The rounding error is symmetric.** Whether you round up from 40% or down from 60%, the error rate is the complement of the probability — and both sides feel like they "should" be obvious calls.
#
# 3. **Errors cluster near 50%.** The forecasts that trip up binary thinking most often are the ones closest to the midpoint — exactly the range where weather (and most real-world predictions) typically lands.
#
# This is why good decision-making works with probabilities directly, not rounded versions of them. The rest of this course builds tools that use the full uncertainty in service of better choices.
