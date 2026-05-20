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
# # Presenting a Solar Decision Analysis
#
# **Scenario.** SunRoute has finished its sensitivity and scenario analysis. The CFO of
# a regional property management firm wants a one-page summary: which solar package makes
# the most sense, and what could make that advice wrong? Your job is to translate the
# analysis into three decision-ready charts and a BLUF executive summary.
#
# The first section ("Given analysis") runs automatically — no changes needed there.
# Your work starts at "Chart 1."
#
# See `INSTRUCTIONS.md` for the full prompt.

# %% [markdown]
# ## Given analysis — no changes needed
#
# Review this section to understand the numbers you'll communicate.

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq

DATA_PATH = "data/eia_residential_rate.csv"

# Model constants
RATE_INC    = 0.030
COST_PER_W  = 3.00
ITC_RATE    = 0.30
DISC_RATE   = 0.05
PROD_KWH_KW = 1_300
YEARS       = 10
OPTIONS     = {"Value Pack (5 kW)": 5, "Standard (8 kW)": 8, "Premium (12 kW)": 12}

rates   = pd.read_csv(DATA_PATH, parse_dates=["date"])
recent  = rates[rates["date"].dt.year >= 2019]
ELEC_RATE = recent["rate_per_kwh"].mean()
ELEC_SD   = recent["rate_per_kwh"].std()


def system_npv(system_kw, elec_rate, rate_inc, cost_per_w, itc_rate):
    upfront    = system_kw * 1_000 * cost_per_w * (1 - itc_rate)
    pv_savings = sum(
        system_kw * PROD_KWH_KW * elec_rate * (1 + rate_inc) ** t / (1 + DISC_RATE) ** t
        for t in range(1, YEARS + 1)
    )
    return pv_savings - upfront


# Scenario table
BASE_PARAMS = {"elec_rate": ELEC_RATE, "rate_inc": RATE_INC,
               "cost_per_w": COST_PER_W, "itc_rate": ITC_RATE}
scenarios = {
    "Optimistic":  {"elec_rate": ELEC_RATE + 2*ELEC_SD, "rate_inc": 0.04, "cost_per_w": 2.50, "itc_rate": 0.35},
    "Base":        BASE_PARAMS,
    "Pessimistic": {"elec_rate": ELEC_RATE - 2*ELEC_SD, "rate_inc": 0.02, "cost_per_w": 3.50, "itc_rate": 0.25},
}
scenario_npvs = pd.DataFrame({
    scenario: {name: round(system_npv(kw, **params)) for name, kw in OPTIONS.items()}
    for scenario, params in scenarios.items()
})

# Tornado data (top drivers for Standard 8 kW)
STANDARD_KW = 8
central_npv = system_npv(STANDARD_KW, **BASE_PARAMS)
flex = [
    ("Electricity rate (±1 SD)",   ELEC_RATE + ELEC_SD,  ELEC_RATE - ELEC_SD,  "elec_rate"),
    ("Annual rate increase (±1pp)", RATE_INC + 0.01,      RATE_INC - 0.01,      "rate_inc"),
    ("Install cost (±$0.50/W)",    COST_PER_W - 0.50,    COST_PER_W + 0.50,    "cost_per_w"),
    ("Federal ITC (±5pp)",         ITC_RATE + 0.05,       ITC_RATE - 0.05,      "itc_rate"),
]
tornado_rows = []
for name, high_val, low_val, kw in flex:
    h = system_npv(STANDARD_KW, **{**BASE_PARAMS, kw: high_val})
    l = system_npv(STANDARD_KW, **{**BASE_PARAMS, kw: low_val})
    tornado_rows.append({"driver": name, "low_npv": l, "high_npv": h,
                         "range_npv": abs(h - l)})
tornado = pd.DataFrame(tornado_rows).sort_values("range_npv", ascending=False)

# Break-even electricity rate
breakeven_rate = brentq(
    lambda r: system_npv(STANDARD_KW, r, RATE_INC, COST_PER_W, ITC_RATE), 0.05, 0.40
)

print("=== Raw analysis outputs ===")
print(f"\nBase-case NPVs:")
print({name: f"${system_npv(kw, **BASE_PARAMS):+,.0f}" for name, kw in OPTIONS.items()})
print(f"\nBreak-even electricity rate: ${breakeven_rate:.4f}/kWh  (current: ${ELEC_RATE:.4f}/kWh)")
print(f"\nScenario table:")
print(scenario_npvs)
print(f"\nTop 2 tornado drivers:")
print(tornado.head(2)[["driver", "low_npv", "high_npv", "range_npv"]])

# %% [markdown]
# ---
# ## Chart 1 — "Which package is best?"
#
# The CFO needs to see at a glance which package wins under each scenario.
# Build a grouped bar chart: one group per package, one bar per scenario.
# Add data labels. Add a horizontal reference line at NPV = 0.
# Title the chart as a direct question or statement the CFO can read as a takeaway.

# %%
# TODO: Build the grouped bar chart.
# Hint: scenario_npvs.T is indexed by scenario with packages as columns — or use it as-is.

# %% [markdown]
# ## Chart 2 — "What's the biggest risk?"
#
# Show only the top 2 drivers from the tornado (sorted by range). Label each bar with
# the dollar amount of the swing in plain language (e.g., "$5,600 swing"). Don't use a
# legend — use direct axis labels or annotated text instead.

# %%
# TODO: Build the simplified 2-driver tornado.

# %% [markdown]
# ## Chart 3 — "How close to the edge are we?"
#
# Display the break-even electricity rate and the current rate on the same visual —
# make it clear how much cushion the Base scenario has. This could be a number line,
# an annotated horizontal bar, or a simple gauge. The CFO should be able to read the
# margin without parsing a table.

# %%
# TODO: Build the break-even margin visualization.

# %% [markdown]
# ---
# ## The memo
#
# *TODO: Fill in the BLUF memo using real numbers from the analysis above.
# Every bracketed field must have a number from the analysis.*

# %% [markdown]
# ## SunRoute Solar Investment Analysis — Executive Summary
#
# **Recommendation:** [One sentence]
#
# **Key numbers:**
# - Base-case 10-yr NPV (Standard 8 kW): $[X]
# - Optimistic scenario: $[X] | Pessimistic: $[X]
# - Break-even electricity rate: $[X]/kWh vs. current $[X]/kWh
#
# **Biggest risk:** [One sentence — top driver from tornado, quantified]
#
# **What would change this recommendation:** [One sentence — state the specific
# threshold condition (e.g., install cost above $X/W or electricity rate below
# $Y/kWh) that would flip the recommendation, AND what the alternative
# recommendation would be in that scenario. A well-grounded memo names the
# alternative, not just the risk.]

# %% [markdown]
# ---
# ## Reflection
#
# *TODO: Write 2–3 sentences. What makes a "decision-ready" chart different from a
# "data-dump" chart? Name at least one of your three charts and explain the specific
# question it answers.*
