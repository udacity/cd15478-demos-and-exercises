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
# # Sensitivity and Scenario Analysis for a Coffee Chain
#
# **Scenario.** BrewPoint Coffee is evaluating three store formats for a new metro
# market entry: a Flagship café, a Standard café, and a transit-hub Kiosk. Each
# format is modeled as a 5-year lease NPV (Net Present Value). You'll identify the highest-return format,
# find what drives the most uncertainty, define three named scenarios, and compute
# the break-even daily customer count for the recommended format.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the dataset citation.

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq

DATA_PATH = "data/food_away_from_home_cpi.csv"

# Fixed model parameters
OPERATING_DAYS = 350
DISCOUNT_RATE  = 0.08
LEASE_YEARS    = 5

# Base-case format parameters
FORMATS = {
    "Flagship (2 000 sq ft)": dict(daily_customers=420, avg_ticket=9.00,
                                   op_margin=0.17, rent_annual=110_000, buildout=470_000),
    "Standard (1 200 sq ft)": dict(daily_customers=250, avg_ticket=8.50,
                                   op_margin=0.20, rent_annual=60_000,  buildout=250_000),
    "Kiosk (400 sq ft)":      dict(daily_customers=130, avg_ticket=7.50,
                                   op_margin=0.23, rent_annual=42_000,  buildout=75_000),
}
STANDARD = FORMATS["Standard (1 200 sq ft)"]

# %% [markdown]
# ## 1. Derive `TICKET_GROWTH` from real CPI data
#
# Load the food-away-from-home CPI, compute year-over-year % change, and take the
# mean of the past five years as the annual ticket price growth assumption.

# %%
# TODO: Load the CPI CSV. Columns are `date` (parse as datetime) and `cpi_food_away`.
cpi = ...

# TODO: Compute year-over-year % change (12-month lag). Drop NaN rows.

# TODO: Filter to the past 5 years and compute the mean annual growth rate.
#       Store it as TICKET_GROWTH.
TICKET_GROWTH = ...

print(f"TICKET_GROWTH derived from CPI data: {TICKET_GROWTH:.2%}")

# %% [markdown]
# ## 2. Implement `cafe_npv`
#
# 5-year lease NPV: present value of annual operating profits minus upfront buildout.
# Annual profit = (daily_customers × avg_ticket × OPERATING_DAYS) × op_margin − rent_annual
# Each year's profit grows at `ticket_growth`; discount at `discount_rate`.

# %%
def cafe_npv(daily_customers: float, avg_ticket: float, op_margin: float,
             rent_annual: float, buildout: float,
             ticket_growth: float = None,
             discount_rate: float = DISCOUNT_RATE,
             operating_days: int = OPERATING_DAYS,
             lease_years: int = LEASE_YEARS) -> float:
    """Return 5-year lease NPV ($) for a BrewPoint café format."""
    if ticket_growth is None:
        ticket_growth = TICKET_GROWTH
    # TODO: implement the NPV formula described above
    ...


# Sanity check — uncomment once implemented:
# print(f"Standard base NPV: ${cafe_npv(**STANDARD):+,.0f}")   # should be ~+$141,000

# %% [markdown]
# ## 3. Base-case NPV for all three formats

# %%
# TODO: Compute base-case NPV for each format in FORMATS.
#       Print results and identify the highest-NPV format.

# %% [markdown]
# ## 4. Tornado diagram — Standard format
#
# Flex each driver one at a time using the amounts in the INSTRUCTIONS table.
# Compute the NPV at the low and high value of each driver, holding all others at
# their base-case values. Sort rows by swing (high NPV − low NPV), largest at top.

# %%
# Flex definitions: (driver_label, kwarg_name, low_value, high_value)
FLEX = [
    ("Daily customers (±30)",       "daily_customers", 220, 280),
    ("Average ticket (±$0.50)",     "avg_ticket",      8.00, 9.00),
    ("Operating margin (±2pp)",     "op_margin",       0.18, 0.22),
    ("Annual rent (±$10K)",         "rent_annual",     70_000, 50_000),
]
CENTRAL_NPV = cafe_npv(**STANDARD)

# TODO: Build a DataFrame `tornado` with columns:
#   driver | low_npv | high_npv | range_npv
# Sort descending by range_npv.
tornado = ...

# TODO: Plot the tornado diagram (horizontal bars, sorted largest at top).
#       Mark the central NPV with a dashed vertical line.

# %% [markdown]
# ## 5. Named scenarios — Standard format

# %%
SCENARIOS = {
    "Optimistic":  dict(**{**STANDARD, "daily_customers": 310, "ticket_growth": 0.055, "buildout": 230_000}),
    "Base":        dict(**STANDARD),
    "Pessimistic": dict(**{**STANDARD, "daily_customers": 185, "ticket_growth": 0.015, "buildout": 275_000}),
}

# TODO: Compute the NPV for each scenario and display the results.

# %% [markdown]
# ## 6. Break-even daily customer count

# %%
# TODO: Use brentq to find the minimum daily_customers at which cafe_npv = 0
#       for the Standard format (hold all other parameters at base-case values).
breakeven_customers = ...

print(f"Break-even daily customers: {breakeven_customers:.0f}")
print(f"Base-case assumption:       {STANDARD['daily_customers']}")
print(f"Cushion:                    {STANDARD['daily_customers'] - breakeven_customers:.0f} customers/day")

# %% [markdown]
# ## 7. Break-even chart

# %%
# TODO: Plot a horizontal two-zone bar:
#   - Red zone from 0 (or a sensible minimum) to break-even
#   - Green zone from break-even to a sensible maximum
#   - Mark break-even and base-case assumption as vertical lines
#   - Label each clearly; put break-even label to the LEFT and
#     base-case label to the RIGHT so they don't overlap

# %% [markdown]
# ## 8. Interpretation
#
# *TODO: 2–3 sentences. Which format has the highest base-case NPV? What single driver
# dominates the tornado? Under what specific condition does the Standard recommendation
# flip negative?*
