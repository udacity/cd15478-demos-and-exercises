# Solution Walkthrough — When "Probably" Isn't the Same as "Definitely"

This is the text companion to `binary_thinking_simulation_solution.ipynb`. It summarizes
the key steps, the numbers a learner should arrive at, and the most common mistakes to flag.

## Headline result

| Strategy | Genres run | Mean seasonal profit | Std |
| --- | --- | --- | --- |
| Binary (> 50% threshold) | Pop only | ~$444K | ~$117K |
| EV-aware (> break-even) | R&B, Rap, Rock, Latin, Pop | ~$1,216K | ~$252K |
| Gap | — | ~$772K per season | — |

The $772K gap is the cost of binary thinking over one season of 100 campaigns per genre.
It comes entirely from skipping four genres (R&B at 37.2%, Rap at 41.5%, Rock at 46.2%,
Latin at 48.0%) that are all EV-positive under the payoff structure — not because they're
high-probability, but because the asymmetric payoff ($15K gain vs. $8K loss) makes
anything above a 34.8% hit rate worth running.

This exercise stops at a simulated comparison. It does not produce a stakeholder recommendation.

## Key steps

1. **Load data and compute genre hit rates** — `tracks.groupby("playlist_genre")["is_hit"].agg(...)`.
   After setting `is_hit = track_popularity >= 50`, the six genre hit rates are:
   EDM 18.8%, R&B 37.2%, Rap 41.5%, Rock 46.2%, Latin 48.0%, Pop 54.0%.
   Only Pop clears the 50% binary threshold.

2. **Break-even hit rate** — `COST_K / (COST_K + NET_GAIN_K) = 8 / 23 ≈ 34.8%`.
   Four genres sit between 34.8% and 50.0%: R&B, Rap, Rock, Latin.
   These are the disagreement-zone genres — EV-positive but skipped by binary thinking.

3. **Simulate one season** — `simulate_season(hit_rates)` uses `RNG.binomial(N_PER_GENRE, hit_rates)`
   to draw hits per genre in a single vectorized call, then computes
   `(hits * NET_GAIN_K - misses * COST_K).sum()`. This is the pattern to reinforce:
   vectorized binomial draws, not a Python loop over individual campaigns.

4. **Monte Carlo** — 2,000 calls to `simulate_season` for each strategy.
   Binary mean ≈ $444K, EV-aware mean ≈ $1,216K. The distributions barely overlap.
   The EV-aware distribution is shifted right by ~$770K and has higher variance
   (it runs more campaigns, so there's more variance — but the mean is far superior).

5. **Certainty illusion** — Pop has a 54% hit rate; binary thinking treats it as near-certain.
   Reality: ~46 out of every 100 Pop campaigns miss. Even the strategy's "sure thing" fails
   almost half the time.

6. **Takeaway** — The key insight to look for: the 50% threshold has no connection to the
   payoff math. The economically correct threshold is 34.8%. Any probability above that
   is worth acting on; any probability below it is not worth acting on — regardless of
   whether it's above or below 0.50.

## Code snippets

```python
# Break-even derivation — must come from payoff constants, never hardcoded
BREAK_EVEN = COST_K / (COST_K + NET_GAIN_K)  # 8 / 23 ≈ 0.348
```

```python
# Vectorized simulate_season — hits across all genres in one binomial draw
def simulate_season(hit_rates: np.ndarray, n_per_genre: int = N_PER_GENRE) -> float:
    hits = RNG.binomial(n_per_genre, hit_rates)
    misses = n_per_genre - hits
    return float((hits * NET_GAIN_K - misses * COST_K).sum())
```

```python
# Monte Carlo loop — simple list comprehension is sufficient; no PyMC needed
binary_profits = np.array([simulate_season(binary_hit_rates) for _ in range(N_SIMS)])
ev_profits     = np.array([simulate_season(ev_hit_rates)     for _ in range(N_SIMS)])
```

## Common mistakes to flag

- **Hardcoding the break-even** — Writing `BREAK_EVEN = 0.35` instead of
  `COST_K / (COST_K + NET_GAIN_K)`. The requirement says to derive it from the payoff
  constants. Hardcoding breaks if the payoff structure changes.

- **Looping over individual campaigns instead of using binomial** — Writing a Python
  `for i in range(N_PER_GENRE)` loop inside `simulate_season` works but is slow and
  harder to read. The vectorized pattern `RNG.binomial(n_per_genre, hit_rates)` where
  `hit_rates` is an array produces all genre outcomes in one call.

- **Not sorting genre_stats before displaying** — Hit rates are more readable in
  ascending order (EDM at the bottom, Pop at the top). Sort before displaying.

- **Forgetting that `simulate_season` uses the shared RNG** — The global `RNG` advances
  its state with each call. Learners who create a new `np.random.default_rng(42)` inside
  the function will get the same result every call, which produces a degenerate "simulation"
  where all 2,000 seasons are identical. The RNG must be defined once at module scope and
  shared across calls.

- **Treating the simulation as the final recommendation** — The exercise asks for a
  simulation and a takeaway, not a recommendation to WaveForm's stakeholders. Learners
  who end with "WaveForm should switch to the EV strategy" are jumping ahead; framing it
  as "the simulation shows that binary thinking costs X" is the right level.

## How this exercise feeds the project

**Project step this preps:** This exercise is motivational groundwork — it has no direct
counterpart in the Nimbus project step list. Its purpose is to establish the intuition
that probability estimates are not verdicts, and that treating them as binary is
economically costly. Every subsequent implementation module assumes the learner has
internalized this lesson.

**Concepts the learner takes with them:**
- **Break-even probability as a decision threshold.** The project's cost-benefit model
  (Step 4) uses a similar calculation to determine which price option clears the
  revenue hurdle. The formula `cost / (cost + gain)` will reappear.
- **Monte Carlo simulation via NumPy.** The project's Monte Carlo step (Step 5) uses
  `np.random.default_rng(seed).normal(...)` draws in the same loop pattern. The
  `simulate_season` function here is structurally identical to the project's
  `simulate_outcome` function — different inputs, same idiom.
- **The shared global RNG pattern.** The project defines one `RNG` at module scope and
  passes it (or relies on module-level state) throughout. This exercise establishes
  that pattern.

**Conventions adopted from the project:**
- Module-level constants (`HIT_THRESHOLD`, `NET_GAIN_K`, `COST_K`, `N_SIMS`) rather
  than hardcoded values inside functions.
- `np.random.default_rng(seed)` for reproducibility, not `np.random.seed()`.

**What's deliberately scoped out:**
- Building a cost-benefit function from first principles is covered in a separate module;
  here the payoff structure is stipulated.
- Translating the analytical comparison into a stakeholder memo is taught in the
  communication modules.
- The project's Bayesian updating, IPW correction, and CRRA utility are not previewed
  here — this exercise is purely about the simulation of probability rounding bias.

This section is for the SME reviewing the exercise, not for the learner. It documents
the connection between this motivational exercise and the capstone so the connection
survives across course revisions and module reorderings.
