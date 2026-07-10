# Solution Notes — When "Probably" Becomes "Definitely"

## Key results

- Step 1: ~400 out of 1,000 days at 60% stayed dry — binary thinking wrong ~40% of the time.
- Step 2: ~350 out of 1,000 days at 35% actually rained — ~35% error rate on the other side.
- Step 3: Optimal threshold is 25% (derived from $5/$20 cost ratio). Binary thinking overpays in the 25%–50% range by predicting "dry" when the cost-aware strategy would bring an umbrella.
- Step 4: Wet bias (inflation=0.15) shifts binary thinking's effective threshold from 50% to ~41% (true probability). Closes part of the 25–50% gap but leaves 25–41% uncovered. Three-curve chart makes the partial compensation visible.

## Design notes

- No external data — all probabilities are simulated. The exercise is about the mechanics of probability rounding, not data wrangling.
- The 60%/40% symmetry in steps 1–2 is the central insight: forecasts that feel opposite produce identical error rates under binary thinking.
- Step 3 derives the optimal threshold analytically (`cost_useless / (cost_wet + cost_useless) = 5/20 = 25%`) then verifies it via simulation. The two cost curves visually expose the gap in the 25%–50% range.
- Step 4's three-strategy chart is the payoff: it shows that the wet bias is a rational forecaster response to the same cost asymmetry users face, and that it partially (but not fully) compensates for binary thinking.
- The algebraic derivation of `biased_effective_threshold = (0.5 - inflation) / (1 - inflation)` is intentional — it mirrors the cost threshold derivation in section 3 and previews the course theme of using math to replace intuition.
- The exercise motivates why structured decision tools work with probabilities and costs together rather than a rounded rule of thumb.
