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
# # Sensitivity and Scenario Analysis for a Solar Installer
#
# **Scenario.** SunRoute, a fictional residential solar installer, wants to know how
# sensitive a homeowner's 10-year NPV is to key assumptions — electricity rates,
# installation costs, and policy incentives. You'll build a tornado diagram and
# break-even analysis to identify which inputs drive the recommendation, and run
# named scenarios (Optimistic / Base / Pessimistic) to stress-test the findings.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the data citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq

DATA_PATH   = "data/eia_residential_rate.csv"

# Stipulated constants — derive ELEC_RATE and ELEC_SD from the data in step 1
RATE_INC    = 0.030   # annual electricity price increase
COST_PER_W  = 3.00    # $/W installed system cost (NREL 2024 benchmark)
ITC_RATE    = 0.30    # federal solar ITC (Inflation Reduction Act)
DISC_RATE   = 0.05    # homeowner discount rate
PROD_KWH_KW = 1_300   # kWh produced per kW per year (US average)
YEARS       = 10      # planning horizon

OPTIONS = {"Value Pack (5 kW)": 5, "Standard (8 kW)": 8, "Premium (12 kW)": 12}

# %% [markdown]
# ## 1. Derive base-case electricity rate from EIA data

# %%
# TODO: Load the EIA rate CSV. Compute ELEC_RATE (mean 2019–2024) and ELEC_SD (SD same period).
rates = ...

ELEC_RATE = ...
ELEC_SD   = ...

print(f"Base-case electricity rate: ${ELEC_RATE:.4f}/kWh")
print(f"EIA rate SD (2019–2024):    ${ELEC_SD:.4f}/kWh")

# %% [markdown]
# ## 2. Implement the NPV model

# %%
# TODO: Implement system_npv(system_kw, elec_rate, rate_inc, cost_per_w, itc_rate).
#       Use the formula from INSTRUCTIONS.md. Pull DISC_RATE, PROD_KWH_KW, YEARS
#       from module scope; don't hardcode them.
def system_npv(system_kw: float, elec_rate: float, rate_inc: float,
               cost_per_w: float, itc_rate: float) -> float:
    """10-year NPV of a residential solar system ($)."""
    ...


# %% [markdown]
# ## 3. Base-case NPV for each package

# %%
# TODO: Compute base NPV for each option in OPTIONS and display as a DataFrame.
base_npv = {name: system_npv(kw, ELEC_RATE, RATE_INC, COST_PER_W, ITC_RATE)
            for name, kw in OPTIONS.items()}
base_npv_df = ...
base_npv_df

# %% [markdown]
# ## 4. Tornado diagram — Standard (8 kW) package
#
# Flex each of the four inputs one at a time, holding the others at base values.
# The flex range for electricity rate uses the EIA-derived SD.

# %%
STANDARD_KW = 8

# TODO: Define `flex` — a list of (driver_name, high_value, low_value, kwarg_name) tuples.
#       Use ELEC_SD for the electricity rate flex.
flex = [
    # ("Electricity rate (±1 SD)", ELEC_RATE + ELEC_SD, ELEC_RATE - ELEC_SD, "elec_rate"),
    # ...
]

# TODO: For each flex row, compute NPV at high_value and at low_value (all other params at base).
#       Build a tornado DataFrame: columns driver, low_npv, high_npv, range_npv.
#       Sort by range_npv ascending (largest range ends up at the top of the plot).
tornado = ...
tornado

# %% [markdown]
# ### Plot the tornado

# %%
# TODO: Plot horizontal bar chart. Each driver gets one bar from low_npv to high_npv.
#       Mark the central NPV with a vertical dashed line. Label axes and add a title.

# %% [markdown]
# ## 5. Break-even electricity rate

# %%
# TODO: Use brentq to find the electricity rate at which Standard (8 kW) NPV = 0.
#       Search over [0.05, 0.40].
STANDARD_KW = 8
breakeven_rate = brentq(...)

print(f"Break-even rate: ${breakeven_rate:.4f}/kWh")
print(f"Current base:    ${ELEC_RATE:.4f}/kWh")
print(f"Margin:          ${ELEC_RATE - breakeven_rate:.4f}/kWh")

# %% [markdown]
# ## 6. Named scenario analysis

# %%
scenarios = {
    "Optimistic":  {"elec_rate": ELEC_RATE + 2*ELEC_SD, "rate_inc": 0.04, "cost_per_w": 2.50, "itc_rate": 0.35},
    "Base":        {"elec_rate": ELEC_RATE,              "rate_inc": RATE_INC, "cost_per_w": COST_PER_W, "itc_rate": ITC_RATE},
    "Pessimistic": {"elec_rate": ELEC_RATE - 2*ELEC_SD, "rate_inc": 0.02, "cost_per_w": 3.50, "itc_rate": 0.25},
}

# TODO: For each scenario × option combination, compute NPV. Display as a wide DataFrame
#       with scenarios as columns and packages as rows.
scenario_results = ...
scenario_results

# %% [markdown]
# ## 7. Interpretation and conditional recommendation
#
# *TODO: Write 2–3 sentences covering:*
# - *Which input dominates the tornado and by how much.*
# - *The break-even margin and what it implies.*
# - *A conditional recommendation: under what specific conditions (e.g., if install
#   costs exceed $X/W or electricity rates fall below $Y/kWh) would you recommend
#   a different package — or defer the decision entirely? A well-supported
#   alternative recommendation is more valuable than unconsidered agreement with
#   the base-case result.*
