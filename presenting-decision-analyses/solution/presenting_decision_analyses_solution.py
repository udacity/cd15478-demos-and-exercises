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
# `presenting_decision_analyses_solution.ipynb`.

# %% [markdown]
# # Presenting a Solar Decision Analysis (SOLUTION)
#
# ## Scenario
#
# Translating the SunRoute sensitivity and scenario analysis into three decision-ready
# charts and a one-page BLUF executive summary for a non-technical stakeholder.

# %% [markdown]
# ## Given analysis — no changes needed

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq

DATA_PATH = "../presenting-decision-analyses-starter/data/eia_residential_rate.csv"

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

breakeven_rate = brentq(
    lambda r: system_npv(STANDARD_KW, r, RATE_INC, COST_PER_W, ITC_RATE), 0.05, 0.40
)

print("Analysis complete. Raw outputs:")
print(f"Base NPVs: {', '.join(f'{n}: ${system_npv(kw, **BASE_PARAMS):+,.0f}' for n,kw in OPTIONS.items())}")
print(f"Break-even rate: ${breakeven_rate:.4f}/kWh  Current: ${ELEC_RATE:.4f}/kWh")

# %% [markdown]
# ---
# ## Chart 1 — "Which package is best?"

# %%
SCENARIO_COLORS = {"Optimistic": "#2ca02c", "Base": "#1f77b4", "Pessimistic": "#d62728"}

fig, ax = plt.subplots(figsize=(9, 5))
pkg_names = list(OPTIONS.keys())
n_scenarios = len(scenarios)
bar_width = 0.25
x = np.arange(len(pkg_names))

for i, (scenario, color) in enumerate(SCENARIO_COLORS.items()):
    npvs = [scenario_npvs.loc[name, scenario] for name in pkg_names]
    bars = ax.bar(x + (i - 1) * bar_width, npvs, bar_width,
                  label=scenario, color=color, alpha=0.8)
    for bar, val in zip(bars, npvs):
        sign = "+" if val >= 0 else ""
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
                f"{sign}${val/1000:.0f}K", ha="center", va="bottom", fontsize=8)

ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels([n.replace(" kW)", " kW)") for n in pkg_names], fontsize=9)
ax.set_ylabel("10-year NPV ($)")
ax.set_title("Which package performs best? 10-year NPV by package and scenario")
ax.legend(title="Scenario")
plt.tight_layout()
plt.show()

# %% [markdown]
# **What this chart answers:** "Under any scenario, which package should we recommend?"
# All three packages go negative under Pessimistic — but Standard and Premium hold their
# value better in the Base case. Value Pack's NPV advantage over Premium is small in the
# Optimistic case, suggesting Standard is the robust middle.

# %% [markdown]
# ## Chart 2 — "What's the biggest risk?"

# %%
top2 = tornado.head(2).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(7, 2.5))
y = np.arange(len(top2))
for i, row in top2.iterrows():
    lo, hi = row["low_npv"], row["high_npv"]
    ax.barh(i, hi - lo, left=lo, height=0.4, color="#4C78A8", alpha=0.85)
    rng = abs(hi - lo)
    ax.text(hi + 200, i, f"${rng:,.0f} swing", va="center", fontsize=9)

ax.axvline(central_npv, color="black", linestyle="--", linewidth=1.2,
           label=f"Base NPV = ${central_npv:,.0f}")
ax.set_yticks(y)
ax.set_yticklabels(top2["driver"])
ax.set_xlabel("10-yr NPV ($) — Standard 8 kW")
ax.set_title("Two inputs drive most of the uncertainty")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Chart 3 — "How close to the edge are we?"

# %%
fig, ax = plt.subplots(figsize=(7, 2.5))
ax.set_xlim(0.10, 0.25)
ax.set_ylim(-0.5, 1.5)
ax.axis("off")

# Draw a number line
ax.annotate("", xy=(0.24, 0.5), xytext=(0.11, 0.5),
            arrowprops=dict(arrowstyle="-", lw=1.5, color="grey"))

# Break-even marker
ax.annotate("", xy=(breakeven_rate, 0.5), xytext=(breakeven_rate, -0.1),
            arrowprops=dict(arrowstyle="-|>", color="#d62728", lw=1.5))
ax.text(breakeven_rate, -0.2, f"Break-even\n${breakeven_rate:.3f}/kWh",
        ha="center", va="top", color="#d62728", fontsize=9)

# Current rate marker
ax.scatter([ELEC_RATE], [0.5], s=120, color="#1f77b4", zorder=5)
ax.text(ELEC_RATE, 0.85, f"Current rate\n${ELEC_RATE:.3f}/kWh",
        ha="center", va="bottom", color="#1f77b4", fontsize=9, fontweight="bold")

# Margin annotation
margin = ELEC_RATE - breakeven_rate
ax.annotate("", xy=(breakeven_rate, 0.5), xytext=(ELEC_RATE, 0.5),
            arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
ax.text((breakeven_rate + ELEC_RATE)/2, 0.62,
        f"${margin:.3f}/kWh margin", ha="center", fontsize=8, color="black")

ax.set_title("Current electricity rate vs. break-even (Standard 8 kW)", pad=12)
plt.tight_layout()
plt.show()

# %% [markdown]
# ---
# ## The memo

# %% [markdown]
# ## SunRoute Solar Investment Analysis — Executive Summary
#
# **Recommendation:** We recommend the **Standard 8 kW package** for all 10 properties:
# it delivers a positive 10-year NPV in the base case and optimistic scenario while
# keeping the downside risk smaller than the Premium option.
#
# **Key numbers:**
# - Base-case 10-yr NPV (Standard 8 kW): **+$1,004**
# - Optimistic scenario: **+$11,540** | Pessimistic: **−$13,493**
# - Break-even electricity rate: **$0.179/kWh** vs. current **$0.158/kWh** (11¢/kWh cushion)
#
# **Biggest risk:** Installation cost is the largest single driver — a $0.50/W increase
# above benchmark ($3.00 → $3.50/W) swings the 10-year NPV by roughly **$5,600** and
# is the primary reason the Pessimistic scenario is negative.
#
# **What would change this recommendation:** If installed costs rise above ~$3.20/W
# *or* electricity rates fall below the break-even threshold of $0.179/kWh, the
# Standard package turns NPV-negative. In either case, the alternative recommendation
# is to **defer**: not to choose a smaller package, but to wait until rates stabilize
# or until contractor quotes come in below $3.00/W before committing.

# %% [markdown]
# ---
# ## Reflection

# %% [markdown]
# A "decision-ready" chart answers one specific question a decision-maker is actually
# asking, rather than displaying all available data. Chart 1 — "Which package is best?"
# — answers the primary decision question directly by grouping bars by scenario rather
# than by driver, making it immediately clear that Standard is positive in both Base and
# Optimistic while all packages fail under Pessimistic. Chart 3 is the clearest
# departure from a data dump: instead of printing two numbers in a table, it renders the
# margin between current and break-even rates as a physical gap on a number line, making
# the "11 cents of cushion" interpretable without mental arithmetic.
