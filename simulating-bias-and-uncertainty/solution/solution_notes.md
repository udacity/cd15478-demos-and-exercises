# Solution Notes — The Application Numbers Game

## Key results

- Step 1: A single 20% application succeeds ~20% of the time — binary thinking is wrong 1 in 5 times.
- Step 2: A single 75% application fails ~25% of the time — binary thinking is wrong 1 in 4 times.
- Step 3: 10 applications at 20% → P(at least one offer) ≈ 89%.
- Step 5: 11 applications needed for 90% confidence at 20% per application.

## Design notes

- No external data — all probabilities are stipulated constants. The exercise is about simulation mechanics and bias exposure, not data wrangling.
- `RNG.binomial(N_APPS, P_SINGLE, N_SIMS)` gives total offers per search directly; checking `>= 1` gives P(at least one).
- The analytical formula for step 5 is `math.ceil(math.log(1 - TARGET) / math.log(1 - P_SINGLE))`.
