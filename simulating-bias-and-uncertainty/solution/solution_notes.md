# Solution Notes — When "Probably" Becomes "Definitely"

## Key results

- Step 1: ~400 out of 1,000 days at 60% stayed dry — binary thinking wrong ~40% of the time.
- Step 2: ~400 out of 1,000 days at 40% actually rained — same ~40% error rate on the other side.
- Step 3: The rounding curve peaks at 50% (maximum error) and decreases slowly; at 70%, binary thinking is still wrong ~30% of the time.
- Step 4: Over a 30-day month (forecasts 20%–80%), binary thinking gets roughly 10–12 days wrong — errors cluster near the 50% line.

## Design notes

- No external data — all probabilities are simulated. The exercise is about the mechanics of probability rounding, not data wrangling.
- The 60%/40% symmetry in steps 1–2 is the central insight: forecasts that feel opposite produce identical error rates under binary thinking.
- Step 3 uses a loop over probability levels; the branching on `p > 0.5` mirrors the exact rounding rule being critiqued.
- Step 4's two-panel chart makes the "clustering near 50%" insight visual: orange bars in the top panel consistently appear near the dashed 50% line.
- The exercise motivates why structured decision tools need to work with raw probabilities rather than rounded versions of them.
