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
# # Stress-Testing Fleet Electrification with Monte Carlo Simulation
#
# **Scenario.** VoltRoute, a fictional urban delivery company, is deciding whether to
# buy or lease 20 electric trucks — or keep the diesel fleet for another 5 years (Hold).
# Both electric options beat diesel on average, but uncertain electricity rates,
# utilization, maintenance savings, and resale values change the picture. You'll run a
# 10,000-draw Monte Carlo simulation to quantify how often each option wins and what
# the worst-case outcomes look like.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the data citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/eia_commercial_rate.csv"

# Fleet constants
N_TRUCKS    = 20
BUY_PRICE   = 85_000
LEASE_RATE  = 1_100     # $/truck/month
DIESEL_GAL  = 4.50      # $/gallon
DIESEL_MPG  = 5.0       # urban delivery mpg
EV_KWH_MILE = 1.2       # kWh/mile
DISC_RATE   = 0.06
YEARS       = 5

N_SIMS = 10_000
RNG    = np.random.default_rng(42)

OPTIONS = ["Buy", "Lease", "Hold"]

# %% [markdown]
# ## 1. Derive electricity rate distribution from EIA data

# %%
# TODO: Load EIA rate CSV. Compute ELEC_MEAN and ELEC_SD for the 2019–2024 period.
rates = ...

ELEC_MEAN = ...
ELEC_SD   = ...

print(f"Electricity rate: mean=${ELEC_MEAN:.4f}/kWh, SD=${ELEC_SD:.4f}/kWh")

# %% [markdown]
# ## 2. Implement the fleet NPV model

# %%
# TODO: Implement fleet_npv(option, elec_rate, annual_miles, maint_save, resale_pct).
#       - "Buy": upfront cost + PV(savings) + PV(resale)
#       - "Lease": PV(savings - annual_lease_payments)
#       - "Hold": 0
#       Pull all constants from module scope; don't hardcode them in the function body.
def fleet_npv(option: str, elec_rate: float, annual_miles: float,
              maint_save: float, resale_pct: float) -> float:
    """5-year fleet NPV relative to keeping the diesel fleet ($)."""
    ...


# %% [markdown]
# ## 3. Draw Monte Carlo samples

# %%
# TODO: Draw N_SIMS samples for each uncertain input using RNG.normal(...).clip(...).
#       Use the distributions from INSTRUCTIONS.md.
sim_elec_rate    = ...
sim_annual_miles = ...
sim_maint_save   = ...
sim_resale_pct   = ...

# %% [markdown]
# ## 4. Evaluate all three options across all draws

# %%
# TODO: For each option, evaluate fleet_npv across all 10,000 draws using zip().
#       Store results in sim_profits — a pd.DataFrame with columns ["Buy","Lease","Hold"].
sim_profits = pd.DataFrame({
    opt: [fleet_npv(opt, e, m, s, r)
          for e, m, s, r in zip(sim_elec_rate, sim_annual_miles, sim_maint_save, sim_resale_pct)]
    for opt in OPTIONS
})
sim_profits.head()

# %% [markdown]
# ## 5. Plot profit distributions

# %%
# TODO: Plot KDE curves for Buy and Lease (Hold is always 0 — add as a vertical line or note).
#       Add a vertical line at NPV = 0. Label axes and add a legend.
#       Hint: sns.kdeplot(data, label="...", fill=True, ax=ax) draws one distribution.
#             ax.axvline(0) adds the zero reference line.

# %% [markdown]
# ## 6. Summary statistics

# %%
# TODO: Compute mean, SD, 5th percentile, 95th percentile for each option.
#       Display as a DataFrame.
summary = ...
summary

# %% [markdown]
# ## 7. P(Buy > Lease) and P(NPV > 0)

# %%
# TODO: Compute and print the fraction of simulations where Buy beats Lease,
#       and P(NPV > 0) for each EV option.

# %% [markdown]
# ## 8. Interpretation
#
# *TODO: Write 2–3 sentences. State which option the simulation favors (higher mean,
# lower risk, or both). Quantify P(Buy > Lease). State the condition under which Buy
# would outperform Lease (hint: resale value).*
