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
# `monte_carlo_simulation_solution.ipynb`.

# %% [markdown]
# # Stress-Testing Fleet Electrification with Monte Carlo Simulation (SOLUTION)
#
# ## Scenario
#
# Haul & Charge Co., a fictional urban delivery company, evaluates three strategies for its
# 20-truck fleet over a 5-year horizon: Buy electric trucks outright, Lease them, or
# Hold (keep diesel as baseline). A 10,000-draw Monte Carlo simulation across uncertain
# electricity rates, utilization, maintenance savings, and resale values quantifies the
# distribution of outcomes and identifies which strategy is more robust.
#

# %% [markdown]
# ## Setup

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "../monte-carlo-simulation-starter/data/eia_commercial_rate.csv"

N_TRUCKS    = 20
BUY_PRICE   = 85_000
LEASE_RATE  = 1_100
DIESEL_GAL  = 4.50
DIESEL_MPG  = 5.0
EV_KWH_MILE = 1.2
DISC_RATE   = 0.06
YEARS       = 5

N_SIMS = 10_000
RNG    = np.random.default_rng(42)

OPTIONS = ["Buy", "Lease", "Hold"]

# %% [markdown]
# ## 1. Electricity rate distribution from EIA data

# %%
rates = pd.read_csv(DATA_PATH, parse_dates=["date"])
rates

# %%
recent    = rates[rates["date"].dt.year >= 2019]
ELEC_MEAN = recent["rate_per_kwh"].mean()
ELEC_SD   = recent["rate_per_kwh"].std()

print(f"Electricity rate: mean=${ELEC_MEAN:.4f}/kWh, SD=${ELEC_SD:.4f}/kWh")

# %% [markdown]
# ## 2. Fleet NPV model

# %%
_PV_FACTOR       = sum(1 / (1 + DISC_RATE) ** t for t in range(1, YEARS + 1))
_PV_RESALE_FACTOR = 1 / (1 + DISC_RATE) ** YEARS


def fleet_npv(option: str, elec_rate: float, annual_miles: float,
              maint_save: float, resale_pct: float) -> float:
    """5-year fleet NPV relative to keeping the diesel fleet ($)."""
    if option == "Hold":
        return 0.0

    fuel_save_annual  = N_TRUCKS * annual_miles * (DIESEL_GAL / DIESEL_MPG - EV_KWH_MILE * elec_rate)
    maint_save_annual = N_TRUCKS * maint_save
    annual_savings    = fuel_save_annual + maint_save_annual

    if option == "Buy":
        upfront = N_TRUCKS * BUY_PRICE
        resale  = N_TRUCKS * BUY_PRICE * resale_pct * _PV_RESALE_FACTOR
        return -upfront + annual_savings * _PV_FACTOR + resale

    if option == "Lease":
        lease_annual = N_TRUCKS * LEASE_RATE * 12
        return (annual_savings - lease_annual) * _PV_FACTOR

    raise ValueError(f"Unknown option: {option}")

# %% [markdown]
# ## 3. Monte Carlo draws

# %%
sim_elec_rate    = RNG.normal(ELEC_MEAN, ELEC_SD, N_SIMS).clip(0.08, 0.40)
sim_annual_miles = RNG.normal(30_000, 4_000, N_SIMS).clip(10_000, 50_000)
sim_maint_save   = RNG.normal(2_500, 400, N_SIMS).clip(0, 5_000)
sim_resale_pct   = RNG.normal(0.40, 0.10, N_SIMS).clip(0.10, 0.70)

# %% [markdown]
# ## 4. Evaluate across all draws

# %%
sim_profits = pd.DataFrame({
    opt: [fleet_npv(opt, e, m, s, r)
          for e, m, s, r in zip(sim_elec_rate, sim_annual_miles, sim_maint_save, sim_resale_pct)]
    for opt in OPTIONS
})
sim_profits.head()

# %% [markdown]
# ## 5. Distribution plot

# %%
fig, ax = plt.subplots(figsize=(9, 5))
for opt, color in [("Buy", "steelblue"), ("Lease", "salmon"), ("Hold", "grey")]:
    if opt == "Hold":
        ax.axvline(0, color=color, linestyle=":", linewidth=1.5, label="Hold (NPV = $0)")
    else:
        sns.kdeplot(sim_profits[opt] / 1e6, label=opt, fill=True, alpha=0.25, color=color, ax=ax)

ax.axvline(0, color="black", linewidth=0.8)
ax.set(title="Monte Carlo: 5-year fleet NPV by strategy",
       xlabel="NPV ($M)", ylabel="density")
ax.legend(title="Strategy")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 6. Summary statistics

# %%
summary = pd.DataFrame({
    "Mean ($K)":  (sim_profits.mean() / 1e3).round(0),
    "SD ($K)":    (sim_profits.std()  / 1e3).round(0),
    "P5 ($K)":    (sim_profits.quantile(0.05) / 1e3).round(0),
    "P95 ($K)":   (sim_profits.quantile(0.95) / 1e3).round(0),
})
summary

# %% [markdown]
# ## 7. P(Buy > Lease) and P(NPV > 0)

# %%
p_buy_gt_lease = (sim_profits["Buy"] > sim_profits["Lease"]).mean()
p_buy_pos      = (sim_profits["Buy"]   > 0).mean()
p_lease_pos    = (sim_profits["Lease"] > 0).mean()

print(f"P(Buy > Lease):    {p_buy_gt_lease:.1%}")
print(f"P(Buy NPV > 0):   {p_buy_pos:.1%}")
print(f"P(Lease NPV > 0): {p_lease_pos:.1%}")

# %% [markdown]
# ## 8. Interpretation

# %% [markdown]
# **Lease is the stronger strategy** on both mean NPV (~$899K vs. ~$818K for Buy) and
# downside risk (lower SD, never goes negative in the simulation). Buy wins in only
# ~26% of simulations — specifically in scenarios where the year-5 resale value is
# high enough to offset the larger upfront capital commitment. If Haul & Charge Co. expects
# resale value to exceed roughly 50% of purchase price (above the mean assumption of
# 40%), Buy becomes competitive; below that, Lease dominates. Both EV options are
# robustly better than Hold across essentially all simulated conditions.
