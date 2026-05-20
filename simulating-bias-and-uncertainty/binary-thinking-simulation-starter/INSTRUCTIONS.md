# When "Probably" Isn't the Same as "Definitely"

## Scenario

You're a data analyst at **WaveForm**, a fictional music streaming platform. WaveForm's editorial
team runs genre-focused promotion campaigns each season — curating playlists, booking in-app
placements, and pushing tracks through the platform's recommendation engine. Each campaign
targets one genre (Pop, Latin, R&B, Rap, Rock, or EDM) and has a measurable outcome: a promoted
track either breaks into regular listener rotation ("hits") or doesn't ("misses").

The editorial team currently uses a simple rule: if they think a genre's hit rate is above 50%,
they run a season-long campaign for it. Below 50%? They skip it. They call this approach "only
betting on likely winners."

You've been asked to stress-test that rule. Using track-level data from the Spotify catalog as an
industry benchmark for real genre hit rates, you'll simulate what happens when a promotion team
rounds every probability above 50% to "it'll work" and every probability below 50% to "it won't."
Then you'll compare that to a strategy that actually uses the hit rates to evaluate expected value.

The data is real Spotify track data; WaveForm is fictional. WaveForm's editorial team is *not*
managing Spotify's catalog — they're using Spotify's public track data as a benchmark to calibrate
their own genre hit-rate expectations.

## What you'll deliver

A completed Jupyter notebook (start from `binary_thinking_simulation_starter.ipynb`) that:

1. Loads the Spotify track sample, computes `is_hit` (popularity ≥ 50), and reports each genre's
   real hit rate from the data.
2. Computes the break-even hit rate from the payoff structure below, and identifies the
   *disagreement zone* — genres EV says run but the binary rule skips.
3. **The certainty illusion:** simulates 100 Pop promotion campaigns (the only genre the binary
   rule runs, at a 54% hit rate). Counts the misses. Explains in one sentence what the miss count
   reveals about treating 54% as a near-certainty.
4. **The missed opportunity:** simulates 100 R&B campaigns (37% hit rate — a genre the binary rule
   skips). Counts the hits. Computes the expected value of one R&B campaign and the total expected
   profit left on the table by skipping 100 of them.
5. Implements `simulate_season(hit_rates)` and runs **one simulated season** per strategy,
   reporting the dollar difference for that draw.
6. Implements `expected_season_profit(hit_rates)` — using the payoff formula directly, no
   randomness — and computes the **analytical expected profit** per strategy. Reports the
   systematic gap between strategies.
7. Writes a 2–3 sentence takeaway using specific numbers from steps 3–6: what the coin-flip
   simulations revealed, and why the analytical gap matters more than the single-season result.

## Payoff structure

Each promotion campaign costs WaveForm resources equivalent to **$8K** in lost opportunity if the
track misses. If the track hits, WaveForm nets **$15K** in incremental subscription and ad revenue
above the campaign cost.

| Outcome | Net payoff |
| --- | --- |
| Hit (track popularity ≥ 50) | +$15K |
| Miss | −$8K |

These numbers are stipulated so you can focus on the simulation mechanics. A separate module
covers how to build a cost-benefit model from first principles.

## Requirements

- Your notebook must run top to bottom without errors.
- Genre hit rates must be computed from the data — don't hardcode them.
- Break-even probability must be derived from the payoff table — don't hardcode it.
- Steps 3 and 4 must use `RNG.binomial` to simulate outcomes — don't compute them analytically.
- Step 6 must use the payoff formula directly — don't simulate. The distinction between a
  simulated result (one random draw) and an analytical result (always the same) is the point.
- The takeaway must cite specific numbers from at least two of steps 3–6.

## Resources you may find useful

- [NumPy: Generator.binomial](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.binomial.html) — for simulating campaign outcomes
- [pandas: DataFrame.groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) — for computing genre-level hit rates
- [Spotify Web API: Audio Features](https://developer.spotify.com/documentation/web-api/reference/get-audio-features) — background on the danceability, energy, and valence fields
- [TidyTuesday 2020-01-21](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21) — original data source

## Note on the data

`data/spotify_tracks_sample.csv` contains 2,400 real tracks drawn from the
[TidyTuesday week 2020-01-21 Spotify dataset](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21),
originally sourced from the Spotify Web API via the spotifyr R package (CC0 1.0).
See `data/README.md` for the full citation and refresh instructions. The scenario company
**WaveForm** is fictional; the underlying track data is real.
