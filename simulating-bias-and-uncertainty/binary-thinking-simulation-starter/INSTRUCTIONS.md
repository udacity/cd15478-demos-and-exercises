# When "Probably" Isn't the Same as "Definitely"

## Scenario

You're a decision analyst at **WaveForm**, a fictional music streaming platform. WaveForm's
Growth team runs genre-focused promotion campaigns each season — curating playlists, booking
in-app placements, and pushing tracks through the recommendation engine. Each campaign targets
one genre (Pop, Latin, R&B, Rap, Rock, or EDM) and has a measurable outcome: a promoted
track either breaks into regular listener rotation ("hits") or doesn't ("misses"). Each genre
targets a distinct listener audience, so a genre's 100 promotional slots can't be reallocated
to another — the decision per genre is simply whether to fill the slots it offers or leave
them empty.

A new analyst joining the team has a question: *why don't we just run campaigns for every
genre with a hit rate above 50%? Those are the likely winners.* It's an intuitive rule, and
she's not wrong that 54% sounds better than 37%. But the threshold that matters for a
profitable campaign isn't 50% — it's the break-even hit rate implied by the payoff structure.
You've been asked to show her why, using data.

Using track-level data from Spotify's catalog as an industry benchmark for real genre hit
rates, you'll simulate what the 50% rule actually produces, then compare it to a strategy
grounded in the payoff math. The data is real Spotify track data; WaveForm is fictional.

## What you'll deliver

A completed Jupyter notebook (start from `binary_thinking_simulation_starter.ipynb`) that:

1. Loads the Spotify track sample, computes `is_hit` (popularity ≥ 50), and reports each genre's
   real hit rate from the data.
2. Computes the break-even hit rate from the payoff structure below, and identifies the
   *disagreement zone* — genres that are profitable by the payoff math but skipped by the 50% rule.
3. **The certainty illusion:** simulates 100 Pop promotion campaigns (the only genre the binary
   rule runs, at a 54% hit rate). Counts the misses. Explains in one sentence what the miss count
   reveals about treating 54% as a near-certainty.
4. **The missed opportunity:** simulates 100 R&B campaigns (37% hit rate — a genre the binary rule
   skips). Counts the hits. Computes the average profit per R&B campaign (revenue from hits minus
   cost of misses) and the total profit left on the table by skipping 100 of them.
5. Implements `simulate_season(hit_rates)` and runs **one simulated season** per strategy,
   reporting the dollar difference for that draw.
6. Implements `average_season_profit(hit_rates)` — using the payoff formula directly, no
   randomness — and computes the **average profit** per strategy (revenue from hits minus
   cost of misses, multiplied by the number of campaigns). Reports the consistent gap.
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

- [NumPy: Generator.binomial](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.binomial.html) — `RNG.binomial(1, p, n)` draws `n` binary outcomes (1 = hit, 0 = miss) where each has probability `p` of being a hit; this is the core simulation tool for steps 3 and 4
- [pandas: DataFrame.groupby](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) — for computing genre-level hit rates
- [Spotify Web API: Audio Features](https://developer.spotify.com/documentation/web-api/reference/get-audio-features) — background on the danceability, energy, and valence fields
- [TidyTuesday 2020-01-21](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21) — original data source

## Note on the data

`data/spotify_tracks_sample.csv` contains 2,400 real tracks drawn from the
[TidyTuesday week 2020-01-21 Spotify dataset](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21),
originally sourced from the Spotify Web API via the spotifyr R package (CC0 1.0).
See `data/README.md` for the full citation and refresh instructions. The scenario company
**WaveForm** is fictional; the underlying track data is real.
