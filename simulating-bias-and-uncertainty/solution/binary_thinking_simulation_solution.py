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
# **The scenario.** You have just finished a data analytics program and you are job searching.
# Each application has roughly a 20% chance of converting to an offer. Binary thinking says:
# *"20% is below 50% — it probably won't work."* This exercise will show you, through
# simulation, exactly how wrong that reasoning is.
#
# ## What this notebook delivers
#
# 1. A simulation showing how often binary thinking is wrong at 20%.
# 2. A mirror showing how often it is wrong at 75%.
# 3. P(at least one offer) from a 10-application search — the number that surprises people.
# 4. A plot of how confidence grows with each additional application.
# 5. The exact number of applications needed to hit 90% confidence, confirmed by simulation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import matplotlib.pyplot as plt
import math

P_SINGLE = 0.20    # per-application offer probability
P_HIGH   = 0.75    # per-application probability in a strong-candidate scenario
N_APPS   = 10      # applications in a typical search
N_SIMS   = 10_000  # simulation runs
TARGET   = 0.90    # target confidence of getting at least one offer

RNG = np.random.default_rng(42)

# %% [markdown]
# ## 1. The bias in action — one application at 20%

# %%
single_outcomes = RNG.binomial(1, P_SINGLE, N_SIMS)
empirical_rate  = single_outcomes.mean()

print(f"Binary thinking: '20% < 50% — it won't happen'")
print(f"Simulation ({N_SIMS:,} tries): offer received {empirical_rate:.1%} of the time")
print(f"Binary thinking was wrong on roughly 1 in every {round(1/empirical_rate):.0f} applications")

# %% [markdown]
# A 20% hit rate means the binary thinker is wrong 1 in 5 times on average — but they
# never find out, because they already decided it wouldn't happen and didn't apply.

# %% [markdown]
# ## 2. The overconfidence mirror — one application at 75%

# %%
high_outcomes = RNG.binomial(1, P_HIGH, N_SIMS)
failure_rate  = 1 - high_outcomes.mean()

print(f"Binary thinking: '75% > 50% — it will happen'")
print(f"Simulation ({N_SIMS:,} tries): no offer {failure_rate:.1%} of the time")
print(f"Binary thinking was wrong roughly 1 in every {round(1/failure_rate):.0f} applications")

# %% [markdown]
# A 75% hit rate fails 1 in 4 times. That is not rare — it is the expected outcome
# for roughly every fourth strong application. Treating it as a certainty and sending
# only one application is a real risk.

# %% [markdown]
# ## 3. Stack the applications

# %%
search_outcomes = RNG.binomial(N_APPS, P_SINGLE, N_SIMS)
p_at_least_one  = (search_outcomes >= 1).mean()
analytical      = 1 - (1 - P_SINGLE) ** N_APPS

print(f"Binary thinking: '20% x {N_APPS} applications — none will pan out'")
print(f"Simulation:  P(at least one offer) = {p_at_least_one:.1%}")
print(f"Analytical:  1 - (1 - {P_SINGLE})^{N_APPS} = {analytical:.1%}")

# %% [markdown]
# Ten applications at 20% yields at least one offer roughly 89% of the time.
# Binary thinking about each individual application would have you send one, feel
# pessimistic, and stop — leaving an 89% chance on the table.

# %% [markdown]
# ## 4. The full picture

# %%
ns     = np.arange(1, 21)
p_low  = 1 - (1 - P_SINGLE) ** ns
p_high = 1 - (1 - P_HIGH)   ** ns

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(ns, p_low,  '-o', label=f'p = {P_SINGLE:.0%} per application')
ax.plot(ns, p_high, '-s', label=f'p = {P_HIGH:.0%} per application')
ax.axhline(TARGET, ls='--', color='gray', label=f'{TARGET:.0%} confidence target')
ax.set(xlabel='Applications sent', ylabel='P(at least one offer)',
       title='How the odds stack up with each application', ylim=(0, 1.05))
ax.legend()
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
# You need 11 applications to hit 90% confidence at 20% per application. The arithmetic
# is simple; the bias is what makes the answer feel surprising.

# %% [markdown]
# ## 6. Takeaway

# %% [markdown]
# Binary thinking treats 20% as "won't happen" — but a single application succeeds
# 20% of the time, and 10 applications yield at least one offer roughly 89% of the time.
# The bias cuts both ways: it leads people to under-apply because 20% feels like zero,
# and to over-rely on a single strong application because 75% feels like a guarantee.
# Simulation makes both errors visible by replacing intuition with counts.
