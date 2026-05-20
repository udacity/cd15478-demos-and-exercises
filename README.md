# cd15478 — Decision Science Exercises

This repo contains all hands-on Python coding exercises for the Decision Science course
(cd15478). Each top-level folder is one implementation module.

## Course sequence

Exercises are listed below in the order they appear in the primary course build.
Folder names are not numbered so the modules can be repackaged into different programs
without breaking paths.

| # in primary build | Folder | Exercise title |
| --- | --- | --- |
| 3 | [simulating-bias-and-uncertainty](simulating-bias-and-uncertainty/) | When "Probably" Isn't the Same as "Definitely" |
| 5 | [expected-utility-and-comparing-decisions](expected-utility-and-comparing-decisions/) | Comparing Marketing Campaigns with Expected Utility |
| 7 | [building-decision-models](building-decision-models/) | Building and Solving a Decision Model Programmatically |
| 9 | [using-model-outputs](using-model-outputs/) | Using Model Outputs in Loan Approval Decisions |
| 11 | [bayesian-updating](bayesian-updating/) | Updating Demand Beliefs with Bayesian Methods |
| 13 | [causal-estimates-cost-benefit](causal-estimates-cost-benefit/) | From Causal Estimates to ROI |
| 15 | [sensitivity-scenario-analysis](sensitivity-scenario-analysis/) | Sensitivity and Scenario Analysis for a Solar Installer |
| 17 | [monte-carlo-simulation](monte-carlo-simulation/) | Stress-Testing Fleet Electrification with Monte Carlo Simulation |
| 19 | [presenting-decision-analyses](presenting-decision-analyses/) | Presenting a Solar Decision Analysis |

## Folder structure

Each module follows the same layout:

```
<module-name>/
├── <exercise-name>-starter/
│   ├── INSTRUCTIONS.md
│   ├── <exercise_name>_starter.py      # jupytext source
│   ├── <exercise_name>_starter.ipynb   # clean (no outputs)
│   └── data/
│       ├── <dataset>.csv
│       └── README.md                   # source + license
└── solution/
    ├── <exercise_name>_solution.py
    ├── <exercise_name>_solution.ipynb  # outputs baked in
    └── solution_notes.md
```

> **Do not number folders.** The modular build system allows exercises to be repackaged
> into different programs in different orders. Use the table above to communicate sequence
> within a specific program.

## Resources for Building Exercises

The [Exercise Creation Resources](Exercise%20Creation%20Resources/) folder contains essential guidelines and standards for creating high-quality, accessible, and engaging exercises. These resources ensure consistency and help you follow best practices when developing course content.

### [Exercise Guidance.md](Exercise%20Creation%20Resources/Exercise%20Guidance.md)

Comprehensive guide covering exercise design principles, instruction writing, starter and solution code best practices, and requirements for solution videos and text. This is your primary resource for understanding what makes an effective exercise.

### [Accessibility Standards.md](Exercise%20Creation%20Resources/Accessibility%20Standards.md)

Details the WCAG 2.1 AA accessibility standards that all content must meet, including guidelines for headings, alt text, hyperlinks, color contrast, and avoiding images of text. Ensures exercises are accessible to all learners regardless of their abilities or use of assistive technology.

### [Real-World Content Guidelines.md](Exercise%20Creation%20Resources/Real-World%20Content%20Guidelines.md)

Guidelines for using real-world examples, company logos, trademarks, and references to people and organizations in exercises. Covers when it's appropriate to use actual brands versus creating fictitious examples and how to avoid legal and ethical issues.

### [Third Party Images and Datasets.md](Exercise%20Creation%20Resources/Third%20Party%20Images%20and%20Datasets.md)

Requirements for using third-party content including licensing requirements (Creative Commons, public domain), attribution standards, and approved sources for images, coding libraries, and datasets. Lists acceptable and unacceptable license types for commercial educational use.
