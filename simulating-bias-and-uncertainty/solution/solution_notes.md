# Solution Notes — Is Your Friend Actually Good at This?

## Key results

- Step 1: 455 out of 1,000 people lost following one pick at 55% — binary thinking was wrong 45% of the time.
- Step 2: 414 out of 1,000 random guessers hit 55%+ over a 20-game season by pure chance (41.4%).
- Step 3: That drops to 176 out of 1,000 (17.6%) over a 100-game season — still not convincing.
- Step 4: Your friend needs ~170 games for their 55% to be more likely skill than luck (< 10% chance it's random).

## Design notes

- No external data — all probabilities are stipulated. The exercise is about simulation mechanics and bias exposure.
- Step 2 and 3 use `RNG.binomial(n, 0.50, 1_000)` to simulate coin flippers; `>= math.ceil(0.55 * n)` checks for 55%+.
- Step 4 uses a loop over season lengths with 5,000 simulations each for stable estimates.
- The two-claim structure (single game + skill question) mirrors the two directions binary thinking fails: overconfidence on a single outcome, and overconfidence in a small sample.
