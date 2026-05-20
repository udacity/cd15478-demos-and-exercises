# Data: LaLonde Job Training Participants

## File

`lalonde_participants.csv` — 614 participants from the LaLonde (1986) job training study,
as curated in the MatchIt R package by Ho, Imai, King, and Stuart (2011).

## Columns

| Column | Description |
| --- | --- |
| `treat` | 1 = received job training program; 0 = control (comparison group from CPS) |
| `age` | Age in years |
| `educ` | Years of education |
| `race` | Race/ethnicity: `"black"`, `"hispan"`, `"white"` |
| `married` | 1 = married |
| `nodegree` | 1 = no high-school degree |
| `re74` | Real earnings in 1974 ($, pre-program) |
| `re75` | Real earnings in 1975 ($, pre-program) |
| `re78` | Real earnings in 1978 ($, post-program outcome) |

## Source and license

**Original study:** LaLonde, R.J. (1986). "Evaluating the Econometric Evaluations of Training
Programs with Experimental Data." *American Economic Review*, 76(4): 604–620.

**Dataset curated by:** Ho, D.E., Imai, K., King, G., and Stuart, E.A. (2011). "MatchIt:
Nonparametric Preprocessing for Parametric Causal Inference." *Journal of Statistical
Software*, 42(8): 1–28. [doi:10.18637/jss.v042.i08](https://doi.org/10.18637/jss.v042.i08)

**R package:** MatchIt, available on CRAN and via `statsmodels.datasets.get_rdataset("lalonde","MatchIt")`.  
**License:** CC0 (public domain). The MatchIt package is distributed under the GPL-2 license;
the LaLonde dataset it contains is in the public domain.

## Dataset structure

The 614 rows combine:
- **185 treated participants** from the National Supported Work (NSW) randomized experiment
  (LaLonde 1986) — they received the training program.
- **429 comparison participants** drawn from the Current Population Survey (CPS) — a general
  population survey, not randomized into the program.

This mixture creates **confounding by baseline earnings**: CPS controls have much higher
pre-program earnings (re74, re75) than the NSW treated group, because the NSW program
deliberately targeted economically disadvantaged workers. A naive comparison makes the
training program appear harmful when it is not.

The known experimental estimate from the randomized NSW study alone is approximately
**+$1,794** in annual earnings — this is the causal benchmark. IPW on the observational
mixture recovers a positive (though noisier) estimate.

## How to reproduce

```python
import statsmodels.api as sm
df = sm.datasets.get_rdataset("lalonde", "MatchIt").data
df.to_csv("lalonde_participants.csv", index=False)
```
