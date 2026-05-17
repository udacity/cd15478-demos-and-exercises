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
# # [Exercise title]
#
# **Scenario.** [2–3 sentences mirroring the INSTRUCTIONS scenario — give
# enough context that someone opening the notebook directly knows what's going
# on, without making them switch tabs to the instructions.]
#
# You'll [briefly state the analytical work] and finish with a [comparison /
# defended choice / sensitivity check] — *not* a stakeholder-facing
# recommendation.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the
# dataset citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd

DATA_PATH = "data/[dataset].csv"

# %% [markdown]
# ## 1. [First step heading]
#
# [1–2 sentence description of what the learner should do in this cell.]

# %%
# TODO: [Concrete instruction — e.g., "Read the CSV into a DataFrame called `cities`."]
[variable_name] = ...

# %% [markdown]
# ## 2. [Second step heading]
#
# [Description.]

# %%
# TODO: [Concrete instruction.]

# %% [markdown]
# ## 3. [Third step heading — e.g., classify into discrete states]
#
# [Description.]

# %%
# TODO: [Concrete instruction. If the step needs constants, define them here
# at module level — see the CRRA-utility example below for the convention.]
[t_lower] = ...
[t_upper] = ...

# TODO: [Second concrete instruction.]

# %% [markdown]
# ## 4. [Fourth step — e.g., empirical probabilities]
#
# [Description.]

# %%
# TODO: [Concrete instruction.]
p = ...

# %% [markdown]
# ## 5. [Fifth step — e.g., payoff matrix]
#
# [Description. Reference the table in INSTRUCTIONS.md if the matrix is
# stipulated.]

# %%
# TODO: [Concrete instruction.]
payoffs = ...

# %% [markdown]
# ## 6. [Sixth step — primary metric]
#
# [Description.]

# %%
# TODO: [Concrete instruction.]
[primary_metric] = ...

# %% [markdown]
# ## 7. [Seventh step — secondary metric with helper function]
#
# [Description. If the helper function takes tunable parameters, define them
# as module-level constants and reference them as defaults — see below.]

# %%
[CONSTANT_A] = [default_value]
[CONSTANT_B] = [default_value]


# TODO: Implement the helper function.
def [helper_function](primary_arg, param_a: float = [CONSTANT_A], param_b: float = [CONSTANT_B]):
    """[One-sentence docstring describing what the function returns.]"""
    ...


# TODO: [Use the helper to compute the secondary metric.]
[secondary_metric] = ...

# %% [markdown]
# ## 8. [Eighth step — third metric]
#
# [Description.]

# %%
# TODO: [Concrete instruction.]

# %% [markdown]
# ## 9. Compare the [N] decision rules
#
# Produce a side-by-side comparison of what each rule selects. If the rules
# disagree, identify in 1–2 sentences which rule you would lean on and why.
#
# **Do not yet convert this comparison into a recommendation to a
# stakeholder.** The skill of translating analytical output into a
# stakeholder-facing recommendation is taught in separate modules. Today's
# deliverable is the comparison itself plus your defended choice of rule.

# %%
# TODO: Build a small comparison DataFrame.
comparison = ...

# %% [markdown]
# *TODO: write your 1–2 sentence defended-choice paragraph here.*

# %% [markdown]
# ## 10. Sensitivity flex
#
# [Description of the sensitivity flex — what assumption changes, what
# probability vector / parameter values to use.]

# %%
# TODO: [Concrete instruction.]
[alt_vector] = ...
[alt_metric] = ...
