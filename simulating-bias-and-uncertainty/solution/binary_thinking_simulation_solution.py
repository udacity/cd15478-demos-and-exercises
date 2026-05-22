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
# # The Application Numbers Game (SOLUTION)
#
# **The bias.** When people encounter a probability below 50%, they tend to treat it as
# *"it won't happen."* Above 50%, they treat it as *"it will happen."* This is called
# **binary thinking** — collapsing a probability into a yes/no prediction before the
# outcome has occurred. It feels natural, but it leads to systematically wrong decisions.
#
# **The scenario.** A friend of yours wants to break into sports journalism. After some
# research, you find that candidates who apply to open roles at sports outlets have roughly
# a 3% chance of receiving an offer. Your friend is discouraged: *"3% is basically zero —
# why bother applying?"* This exercise will show, through simulation, exactly why that
# reasoning is wrong.
#
# ## What this notebook delivers
#
# 1. A simulation showing how often binary thinking is wrong at 3%.
# 2. A mirror showing how often it is wrong at 55%.
# 3. P(at least one offer) from a 30-application search.
# 4. A before/after chart: 1 application vs 30 at 3%.
# 5. The number of applications needed for 90% confidence, confirmed by simulation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import matplotlib.pyplot as plt
import math

P_SINGLE    = 0.03    # per-application offer probability (sports journalism)
P_HIGH      = 0.55    # per-application probability (in-demand role)
N_APPS      = 30      # applications in a full search
N_SIMS      = 100     # simulation runs
N_SIMS_MANY = 1_000   # simulation runs for the higher-probability scenario
TARGET      = 0.90    # target confidence of getting at least one offer

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. The bias in action — one application at 3%

# %%
single_outcomes = RNG.binomial(1, P_SINGLE, N_SIMS)
empirical_rate  = single_outcomes.mean()

print(f"Binary thinking: '3% < 50% — it won't happen'")
print(f"Simulation ({N_SIMS} tries): offer received {empirical_rate:.1%} of the time")
print(f"Binary thinking was wrong on roughly 1 in every {round(1/empirical_rate) if empirical_rate > 0 else 'N/A'} applications")

# %%
labels  = ['No offer', 'Offer']
counts  = [N_SIMS - single_outcomes.sum(), single_outcomes.sum()]

fig, ax = plt.subplots(figsize=(5, 3.5))
bars = ax.bar(labels, counts, color=['#cccccc', '#e07b54'], edgecolor='white', width=0.5)
ax.bar_label(bars, fmt=lambda v: f'{int(v):,}\n({v/N_SIMS:.1%})', padding=4, fontsize=10)
ax.set(title=f'{N_SIMS} single applications at {P_SINGLE:.0%}',
       ylabel='Number of simulations', ylim=(0, N_SIMS * 1.15))
ax.annotate('Binary thinking said\nthis bar was empty',
            xy=(1, counts[1]), xytext=(1.35, counts[1] + N_SIMS * 0.04),
            arrowprops=dict(arrowstyle='->', color='#e07b54'), color='#e07b54', fontsize=9)
plt.tight_layout()
plt.show()

# %% [markdown]
# A 3% hit rate means binary thinking is wrong roughly 1 in every 33 applications —
# but they never find out, because they already decided it wouldn't happen and didn't apply.

# %% [markdown]
# ## 2. The overconfidence mirror — spamming applications at 55%

# %%
high_outcomes = RNG.binomial(1, P_HIGH, N_SIMS_MANY)
failure_rate  = 1 - high_outcomes.mean()

print(f"Binary thinking: '55% > 50% — it will definitely work out'")
print(f"Simulation ({N_SIMS_MANY:,} tries): no offer {failure_rate:.0%} of the time")
print(f"Binary thinking was wrong roughly 1 in every {round(1/failure_rate):.0f} applications")

# %%
labels2 = ['Offer', 'No offer']
counts2 = [high_outcomes.sum(), N_SIMS_MANY - high_outcomes.sum()]

fig, ax = plt.subplots(figsize=(5, 3.5))
bars = ax.bar(labels2, counts2, color=['#cccccc', '#e07b54'], edgecolor='white', width=0.5)
ax.bar_label(bars, fmt=lambda v: f'{int(v):,}\n({v/N_SIMS_MANY:.0%})', padding=4, fontsize=10)
ax.set(title=f'{N_SIMS_MANY:,} single applications at {P_HIGH:.0%}',
       ylabel='Number of simulations', ylim=(0, N_SIMS_MANY * 1.15))
ax.annotate('Binary thinking said\nthis bar was empty',
            xy=(1, counts2[1]), xytext=(1.35, counts2[1] + N_SIMS_MANY * 0.04),
            arrowprops=dict(arrowstyle='->', color='#e07b54'), color='#e07b54', fontsize=9)
plt.tight_layout()
plt.show()

# %% [markdown]
# Even at 55% — above the binary threshold — a single application fails 45% of the time.
# Binary thinking treats 'above 50%' as a guarantee, but nearly half the time it produces nothing.

# %% [markdown]
# ## 3. Stack the applications

# %%
search_outcomes = RNG.binomial(N_APPS, P_SINGLE, N_SIMS)
p_at_least_one  = (search_outcomes >= 1).mean()
analytical      = 1 - (1 - P_SINGLE) ** N_APPS

print(f"Binary thinking: '3% × {N_APPS} applications — none will pan out'")
print(f"Simulation:  P(at least one offer) = {p_at_least_one:.1%}")
print(f"Analytical:  1 - (1 - {P_SINGLE})^{N_APPS} = {analytical:.1%}")

# %%
bins = range(0, 8)

fig, ax = plt.subplots(figsize=(7, 3.5))
n, _, patches = ax.hist(search_outcomes, bins=bins, align='left', rwidth=0.7,
                         color='#cccccc', edgecolor='white')
patches[0].set_facecolor('#e07b54')
ax.set(title=f'Offers from {N_APPS} applications at {P_SINGLE:.0%} — {N_SIMS} searches',
       xlabel='Offers received', ylabel='Number of searches')
ax.annotate('Binary thinking\npredicted only this',
            xy=(0.45, n[0] * 0.5), xytext=(2, n[0] * 0.75),
            arrowprops=dict(arrowstyle='->', color='#e07b54'), color='#e07b54', fontsize=9, ha='left')
plt.tight_layout()
plt.show()

# %% [markdown]
# Thirty applications at 3% yields at least one offer roughly 60% of the time.
# Binary thinking about each individual application would have your friend give up
# before the numbers have a chance to work in their favour.

# %% [markdown]
# ## 4. The full picture

# %%
p_one  = P_SINGLE
p_many = 1 - (1 - P_SINGLE) ** N_APPS

labels4 = ['Send 1 application', f'Send {N_APPS} applications']
probs4  = [p_one, p_many]

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(labels4, probs4, color=['#cccccc', '#e07b54'], edgecolor='white', width=0.5)
ax.bar_label(bars, fmt=lambda v: f'{v:.0%}', padding=6, fontsize=13, fontweight='bold')
ax.set(title='P(at least one offer) — sports journalism role at 3%',
       ylabel='Probability of at least one offer', ylim=(0, 1.0))
ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(xmax=1))
ax.axhline(0.5, ls='--', color='gray', lw=1, label='50% threshold')
ax.legend(fontsize=9)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 5. Find your number

# %%
n_needed = math.ceil(math.log(1 - TARGET) / math.log(1 - P_SINGLE))
print(f"Analytical: {n_needed} applications for {TARGET:.0%} confidence at p = {P_SINGLE:.0%}")

sim_probs     = [(RNG.binomial(n, P_SINGLE, N_SIMS) >= 1).mean() for n in range(1, n_needed + 3)]
sim_crossover = next(n for n, p in enumerate(sim_probs, 1) if p >= TARGET)
print(f"Simulation confirms: {TARGET:.0%} confidence reached at {sim_crossover} applications")

# %% [markdown]
# Your friend needs roughly 76 applications to hit 90% confidence at 3% per application.
# That sounds like a lot — but it is exactly what the math requires, and binary thinking
# is the only reason it feels surprising.

# %% [markdown]
# ## 6. Takeaway

# %% [markdown]
# Binary thinking treats 3% as "won't happen" — but 30 applications yield at least one
# offer roughly 60% of the time, and 76 applications get your friend to 90% confidence.
# The same bias cuts the other way: 55% per application sounds like a sure thing, but a
# single submission still fails 45% of the time. Simulation makes both errors visible
# by replacing intuition with counts.
