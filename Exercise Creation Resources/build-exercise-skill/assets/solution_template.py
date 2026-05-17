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

# This file is a jupytext-paired Python script export of
# `[exercise_name]_solution.ipynb`. The canonical artifact for learners is
# the notebook (.ipynb); this script is provided for code review and `git diff`
# readability. Run `jupytext --sync` to keep the two in lockstep after edits.

# %% [markdown]
# # [Exercise title] (SOLUTION)
#
# ## Scenario
#
# [Full scenario from INSTRUCTIONS.md, copied so the solution notebook is
# self-contained. Reviewers and learners should be able to read the solution
# .ipynb top-to-bottom without flipping to other files.]
#
# ## What this notebook delivers
#
# [List of deliverables, matching the INSTRUCTIONS scenario's "what you'll
# deliver" framing. State that this stops at the analytical layer and does
# not produce a stakeholder-facing recommendation.]

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "../[starter-folder]/data/[dataset].csv"

# %% [markdown]
# ## 1. [First step heading]

# %%
[variable_name] = pd.read_csv(DATA_PATH)
[variable_name].head()

# %% [markdown]
# ## 2. [Second step heading]
#
# [Short markdown commentary on the choice you're making — what the derived
# metric represents and why it's the right one.]

# %%
[variable_name]["[derived_column]"] = ...  # actual computation
[variable_name].head()

# %% [markdown]
# ## 3. [Third step — classify into discrete states]
#
# [Commentary on the binning choice.]

# %%
t_lower, t_upper = [variable_name]["[derived_column]"].quantile([1 / 3, 2 / 3])
print(f"33rd percentile cutoff: {t_lower:.2f}")
print(f"67th percentile cutoff: {t_upper:.2f}")


def classify(value: float) -> str:
    if value >= t_upper:
        return "Strong"
    if value >= t_lower:
        return "Average"
    return "Weak"


[variable_name]["[state_column]"] = [variable_name]["[derived_column]"].apply(classify)
[variable_name]

# %% [markdown]
# ## 4. [Empirical probabilities]

# %%
counts = [variable_name]["[state_column]"].value_counts()
p = (counts / counts.sum()).reindex(["Strong", "Average", "Weak"])
p

# %% [markdown]
# By construction, the tertile bins each contain ~1/3 of the rows. This
# gives a simple baseline distribution.

# %% [markdown]
# ## 5. [Payoff matrix]

# %%
payoffs = pd.DataFrame(
    {
        "Strong":  {"[Option A]": ..., "[Option B]": ..., "[Hold]": 0.0},
        "Average": {"[Option A]": ..., "[Option B]": ..., "[Hold]": 0.0},
        "Weak":    {"[Option A]": ..., "[Option B]": ..., "[Hold]": 0.0},
    }
)
payoffs

# %% [markdown]
# ## 6. [Primary metric — e.g., expected value]

# %%
ev = (payoffs * p).sum(axis=1)
ev

# %% [markdown]
# ## 7. [Secondary metric — e.g., expected utility with risk aversion]
#
# [Conceptual commentary — why this metric, what its parameters represent,
# why the wealth baseline / constants are set the way they are.]

# %%
[CONSTANT_A] = [value]
[CONSTANT_B] = [value]


def [helper_function](primary_arg, param_a: float = [CONSTANT_A], param_b: float = [CONSTANT_B]):
    """[Docstring.]"""
    ...


utility_table = payoffs.map([helper_function])
expected_utility = (utility_table * p).sum(axis=1)
expected_utility

# %% [markdown]
# [Inverted-back-to-dollars step or other secondary computation.]

# %% [markdown]
# ## 8. [Third metric — e.g., minimax regret]

# %%
best_per_state = payoffs.max(axis=0)
regret = best_per_state - payoffs
max_regret = regret.max(axis=1)
max_regret

# %% [markdown]
# ## 9. Compare the [N] decision rules

# %%
comparison = pd.DataFrame(
    {
        "Selected option": [ev.idxmax(), expected_utility.idxmax(), max_regret.idxmin()],
        "Score": [f"EV = ...", f"CE = ...", f"Max regret = ..."],
    },
    index=["EV-max", "[Utility-max]", "Minimax regret"],
)
comparison

# %% [markdown]
# **The [N] rules [agree / disagree].** [If they disagree: state the real
# tradeoff behind the disagreement in 1–2 sentences.]
#
# **The decision rule I would lean on is [X]** because [brief justification].
#
# This deliverable stops at *defending a decision rule*. Translating the
# comparison into a stakeholder-facing recommendation is taught in separate
# modules.

# %% [markdown]
# ## 10. Sensitivity flex

# %%
[alt_vector] = pd.Series({"Strong": ..., "Average": ..., "Weak": ...})
[alt_metric] = (payoffs * [alt_vector]).sum(axis=1)
[alt_metric]

# %% [markdown]
# [1–2 sentence interpretation. Headline takeaway should be that the
# analytical output is conditional on the assumption being flexed — any
# downstream recommendation inherits that conditionality.]
