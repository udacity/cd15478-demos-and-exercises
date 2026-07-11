# Data: Job-Readiness Training Program Participants

## File

`program_participants.csv` — 614 participants from a job-readiness training program study,
combining treated participants who received the program and a comparison group.

## Columns

| Column | Description |
| --- | --- |
| `treat` | 1 = received job-readiness training program; 0 = control (comparison group) |
| `age` | Age in years |
| `educ` | Years of education |
| `race` | Race/ethnicity: `"black"`, `"hispan"`, `"white"` |
| `married` | 1 = married |
| `nodegree` | 1 = no high-school degree |
| `earnings_pre1` | Real earnings, pre-program year 1 ($) |
| `earnings_pre2` | Real earnings, pre-program year 2 ($) |
| `earnings_post` | Real earnings, post-program ($, outcome variable) |

## Dataset structure

The 614 rows combine:
- **185 treated participants** from a randomized experiment — they received the job-readiness training program.
- **429 comparison participants** drawn from a general population survey — not randomized into the program.

This mixture creates **confounding by baseline earnings**: comparison group participants have much higher
pre-program earnings (`earnings_pre1`, `earnings_pre2`) than the treated group, because the program
deliberately targeted workers with unstable employment histories. A naive comparison makes the
program appear harmful when it is not.

The known experimental estimate from the randomized portion of the study alone is approximately
**+$1,794** in annual earnings — this is the causal benchmark. IPW on the observational
mixture recovers a positive (though noisier) estimate.
