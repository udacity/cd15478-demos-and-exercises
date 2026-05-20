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
# # Presenting a Coffee Chain Expansion Analysis
#
# **Scenario.** BrewPoint Coffee has finished its sensitivity and scenario analysis.
# The VP of Real Estate wants a one-page summary: which store format makes the most
# sense, why, and what could make that advice wrong? She has 5 minutes.
#
# The **Given analysis** section below runs automatically — review it to understand
# the numbers before building your charts. Your job starts at Chart 1.
#
# See `INSTRUCTIONS.md` for the full prompt and `data/README.md` for the dataset citation.

# %% [markdown]
# ## Given analysis (run automatically — review but do not modify)

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq

DATA_PATH = "data/food_away_from_home_cpi.csv"

OPERATING_DAYS = 350
DISCOUNT_RATE  = 0.08
LEASE_YEARS    = 5

FORMATS = {
    "Flagship":  dict(daily_customers=420, avg_ticket=9.00,
                      op_margin=0.17, rent_annual=110_000, buildout=470_000),
    "Standard":  dict(daily_customers=250, avg_ticket=8.50,
                      op_margin=0.20, rent_annual=60_000,  buildout=250_000),
    "Kiosk":     dict(daily_customers=130, avg_ticket=7.50,
                      op_margin=0.23, rent_annual=42_000,  buildout=75_000),
}
STANDARD = FORMATS["Standard"]

cpi = pd.read_csv(DATA_PATH, parse_dates=["date"]).sort_values("date").dropna()
cpi["yoy"] = cpi["cpi_food_away"].pct_change(12)
TICKET_GROWTH = cpi[cpi["date"].dt.year >= cpi["date"].dt.year.max() - 5]["yoy"].dropna().mean()


def cafe_npv(daily_customers, avg_ticket, op_margin, rent_annual, buildout,
             ticket_growth=None, discount_rate=DISCOUNT_RATE,
             operating_days=OPERATING_DAYS, lease_years=LEASE_YEARS):
    """5-year lease NPV (Net Present Value): PV of operating profits minus buildout cost."""
    if ticket_growth is None:
        ticket_growth = TICKET_GROWTH
    annual_revenue = daily_customers * avg_ticket * operating_days
    annual_profit  = annual_revenue * op_margin - rent_annual
    pv = sum(annual_profit * (1 + ticket_growth)**t / (1 + discount_rate)**t
             for t in range(1, lease_years + 1))
    return pv - buildout


SCENARIOS = {
    "Optimistic":  dict(**{**STANDARD, "daily_customers": 310,
                           "ticket_growth": 0.055, "buildout": 230_000}),
    "Base":        dict(**STANDARD),
    "Pessimistic": dict(**{**STANDARD, "daily_customers": 185,
                           "ticket_growth": 0.015, "buildout": 275_000}),
}

FLEX = [
    ("Daily customers (±30)",   "daily_customers", 220, 280),
    ("Avg ticket (±$0.50)",     "avg_ticket",      8.00, 9.00),
    ("Op margin (±2pp)",        "op_margin",       0.18, 0.22),
    ("Annual rent (±$10K)",     "rent_annual",     70_000, 50_000),
]
CENTRAL_NPV = cafe_npv(**STANDARD)
tornado_rows = []
for label, kwarg, low_val, high_val in FLEX:
    lo = cafe_npv(**{**STANDARD, kwarg: low_val})
    hi = cafe_npv(**{**STANDARD, kwarg: high_val})
    tornado_rows.append({"driver": label, "low_npv": lo, "high_npv": hi,
                         "range_npv": abs(hi - lo)})
tornado = pd.DataFrame(tornado_rows).sort_values("range_npv")

breakeven_customers = brentq(
    lambda c: cafe_npv(c, STANDARD["avg_ticket"], STANDARD["op_margin"],
                       STANDARD["rent_annual"], STANDARD["buildout"]),
    10, 1_000
)
cushion = STANDARD["daily_customers"] - breakeven_customers

print("Given analysis complete.")
print(f"TICKET_GROWTH: {TICKET_GROWTH:.2%}")
print(f"Standard base NPV: ${CENTRAL_NPV:+,.0f}")
print(f"Break-even: {breakeven_customers:.0f} customers/day  (cushion: {cushion:.0f})")

# %% [markdown]
# ---
# ## Chart 1 — "Which format delivers the best return?"
#
# Build a grouped bar chart: one group per format, one bar per scenario (Optimistic /
# Base / Pessimistic). Use one color per scenario. Add a data label on each bar showing
# the NPV in $K (e.g. "+$141K"). Add a horizontal reference line at NPV = 0.
#
# **Hint:** For the Flagship and Kiosk under non-Base scenarios, scale their
# daily_customers and buildout by the same ratio as the Standard scenario parameters.

# %%
SCENARIO_COLORS = {"Optimistic": "#2ca02c", "Base": "#1f77b4", "Pessimistic": "#d62728"}

# TODO: Build and display Chart 1.

# %% [markdown]
# *TODO: 1–2 sentences. What does Chart 1 tell the VP about which format to open?*

# %% [markdown]
# ## Chart 2 — "What should we worry about most?"
#
# Show only the **top 2 drivers** from the tornado (largest range). For each driver,
# draw a horizontal bar from its low-NPV to its high-NPV value. Label the bar with
# the dollar swing. Mark the central NPV with a dashed line.

# %%
top2 = tornado.tail(2).reset_index(drop=True)

# TODO: Build and display Chart 2.

# %% [markdown]
# *TODO: 1–2 sentences. What does Chart 2 tell the VP about where to focus due diligence?*

# %% [markdown]
# ## Chart 3 — "How many customers do we need each day?"
#
# Draw a two-zone horizontal bar: red (unprofitable) to the left of break-even,
# green (profitable) to the right. Mark break-even and the base-case assumption
# as vertical lines. Put the break-even label to the LEFT of its line and the
# base-case label to the RIGHT so they don't overlap.

# %%
lo_chart, hi_chart = 50, 400

# TODO: Build and display Chart 3.

# %% [markdown]
# *TODO: 1–2 sentences. What does Chart 3 tell the VP about the risk of the recommendation?*

# %% [markdown]
# ---
# ## The memo
#
# Fill in every bracketed field with a real number from the analysis above.

# %% [markdown]
# ## BrewPoint Coffee — New Market Entry Format Analysis
#
# **Recommendation:** [One sentence — which format and why]
#
# **Key numbers:**
# - Standard base-case 5-year NPV: $[X]
# - Optimistic scenario: $[X] | Pessimistic: $[X]
# - Break-even: [X] customers/day vs. base assumption of [X]/day
#
# **Biggest risk:** [One sentence — top driver from tornado, quantified]
#
# **What would change this recommendation:** [One sentence — the specific condition
# that would flip the recommendation, e.g., "If daily foot traffic falls below X..."]
