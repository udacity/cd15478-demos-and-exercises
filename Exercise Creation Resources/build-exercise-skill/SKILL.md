---
name: build-exercise
description: Build a hands-on Python coding exercise for a Udacity Decision Science / Applied Statistics course module in the cd15478-demos-and-exercises repo. Use whenever the user wants to create an exercise from a module dictionary entry, build a starter + solution notebook pair for a specific learning objective, set up a new `module-name/exercise-name-starter/` folder, write `INSTRUCTIONS.md` for a coding exercise, or asks for a Jupyter exercise tied to a real-world dataset. Trigger eagerly — for example, when the user mentions "build an exercise", "create an exercise", "make an exercise for [module name]", references a "module dictionary" or "implementation module", points at a PDF of modules, or asks for help writing a coding exercise with starter and solution. Also trigger when the user is working inside or near the cd15478-demos-and-exercises repo and the task involves exercise authoring, even if they don't say the word "skill".
---

# Build an Exercise

This skill captures the workflow, conventions, and pedagogical principles used to build hands-on Python coding exercises for the Udacity Decision Science course (`cd15478-demos-and-exercises` repo). Follow it when you're authoring a new exercise from a module dictionary entry.

## Why this skill exists

Authoring a course exercise looks straightforward but has a lot of subtle traps — wrong scenario framing, math that doesn't produce the intended teaching moment, robotic language, accidentally implying real companies are making fictional decisions, payoffs that students can't compute. This skill exists so the same lessons don't have to be relearned every time. It also exists so the exercises feel coherent across the course — same folder structure, same artifact set, same voice.

**Most importantly: every exercise in this course is preparation for one specific step of the capstone project** (`cd15478-project-solution/`). The skill the learner practices in an exercise should be the same skill they'll need to execute on the project — same shape of input, same code idioms, same kind of output. If the exercise teaches something that doesn't transfer to a project step, the exercise is in the wrong shape. See "Tying every exercise to the project" below for how to enforce this.

## Tying every exercise to the project

The project (`cd15478-project-solution/` and `cd15478-project-starter/`) is the integration point for the entire course. It's a single end-to-end analysis — the Nimbus Streaming pricing decision — that combines every skill the implementation modules teach: causal correction, Bayesian updating, cost-benefit modeling, Monte Carlo simulation, decision-tree construction, EV/utility/regret math, sensitivity analysis, and stakeholder communication.

Every implementation exercise should be designed as **deliberate preparation for one specific step of the project**.

### Read the project first

Open `cd15478-project-solution/solution/nimbus_decision_solution.py` (the jupytext `.py` is the most readable form, paired with the `.ipynb` learners actually run) and `cd15478-project-solution/README.md` before you sketch the exercise. Find the cells that correspond to the module you're teaching. Note:

- **Input shapes.** What data structures arrive at this step — a DataFrame, a Series, a fitted model, a scalar?
- **Function signatures.** What does `option_profit` take, in what order? How is the CRRA utility helper structured? What positional vs. keyword arguments?
- **Variable names.** `POSTERIOR_MU`, `LTV_MONTHS`, `OPTIONS`, `RECOMMENDED` — these are the names a learner will encounter on the project. Use the same conventions.
- **Visualization style.** Tornado diagrams, KDE plots, decision-tree sketches — adopt the same matplotlib/seaborn idioms so the exercise's plots look like the project's plots.

### Module-to-project-step mapping (approximate)

| Implementation module | Project step it preps |
| --- | --- |
| Simulating Bias and Uncertainty in Decision-Making | Motivational; no direct project step |
| Computing Expected Utility and Comparing Decisions | Step 7 — *Apply decision theory* (EV, CRRA, Minimax regret) |
| Building and Solving Decision Models Programmatically | Step 6 — *Decision tree* (options × posterior states, backward induction) |
| Using Model Outputs in Decision Calculations | Step 4 — *Cost-benefit model* (translating model outputs into payoffs) |
| Updating Decisions with Bayesian Methods in Python | Step 3 — *Bayesian updating* (Normal-Normal conjugate updates) |
| Using Causal Estimates in Cost-Benefit and ROI Analysis | Step 2 + Step 4 — *IPW correction* feeding into the cost-benefit model |
| Running Sensitivity and Scenario Analysis in Python | Step 8 — *Sensitivity & robustness* (tornado, break-even) |
| Stress-Testing Decisions with Simulation and Uncertainty | Step 5 — *Monte Carlo simulation* (NumPy-based, no PyMC) |
| Presenting Decision Analyses with Visuals and Narratives | Step 9 — *Recommendation memo* (BLUF format, 1-pager) |

Treat this mapping as approximate — modules may be repackaged or reordered between programs. The principle is what's important: every exercise should mirror something the project asks for, and the exercise's code should be portable into the project notebook as one cell.

### Use the project's idioms

A non-exhaustive list of conventions the project establishes that exercises should follow:

- **Probability vectors** as `pd.Series` indexed by state name (`p["Strong"]`, not `p[0]`).
- **Payoff matrices** as `pd.DataFrame` with options as rows, states as columns.
- **Cost-benefit functions** named `option_profit(option, lift, margin, cac, ltv_months)` — take the option as a string and the uncertain inputs as keyword args, return a single dollar number.
- **CRRA utility** as a standalone helper with `GAMMA` and `WEALTH` as module-level constants, function signature `crra_utility(profit, gamma=GAMMA, wealth_baseline=WEALTH)`.
- **Monte Carlo sampling** via NumPy (`np.random.default_rng(seed).normal(...)`), no PyMC. The course owner has flagged PyMC as too "black box" for this audience.
- **Bayesian updates** as closed-form Normal-Normal conjugate (precision-weighted means), not MCMC.
- **Decision-tree visualization** as a hand-drawn matplotlib sketch with `boxstyle="round"` labels (see the project's tree cell).
- **Tornado diagrams** with `±1 SD` flexes per driver, sorted by range.

When the exercise uses these same APIs, the learner doesn't have to learn new conventions when they hit the project — they extend what they already know.

### Don't spoil the project

The exercise should never use:

- The project's scenario (Nimbus Streaming, video subscriptions, the $12.99 → $14.99 price increase, 4M subscribers).
- The project's data files (`pilot_data.csv`, `industry_pricing_history.csv`, etc.).
- The project's specific numerical answers (the $15M expected profit, the 3.7 pp churn lift, the Full-rollout recommendation).

Use a different industry, a different company, a different dataset. The *skill* being practiced is what transfers; the *scenario* should be fresh. (The course owner explicitly flagged this in the module dictionary: "Ideally a new scenario for each module.")

### Leave the learner with portable code

A well-designed exercise produces functions or patterns the learner could literally copy-paste into the project notebook as one cell. The exercise's `crra_utility` function should work for the project unchanged; its sensitivity-flex loop should adapt to the project by swapping the input vector; its tree-solving routine should generalize to the project's option set.

If the exercise's code is so tied to its scenario that nothing transfers, the exercise hasn't done its job — even if the scenario is engaging and the math is correct.

## The canonical workflow

Build exercises in this order. The order matters: most pitfalls come from skipping the early steps and discovering downstream that the math doesn't land or the framing is off.

1. **Read the four guidance docs in `Exercise Creation Resources/`.** They're authoritative — if anything in this skill conflicts with them, the guidance docs win. The relevant files are:
   - `Exercise Guidance.md` — what makes a good exercise, instruction-writing principles, starter vs. solution code conventions, solution video/text requirements.
   - `Real-World Content Guidelines.md` — when you can name real companies, how to use logos/trademarks, the *fictional-company-with-real-data* pattern.
   - `Third Party Images and Datasets.md` — license rules for data and images.
   - `Accessibility Standards.md` — WCAG 2.1 AA requirements (headings, alt text, hyperlinks, contrast).

2. **Find the target module in the module dictionary.** The user will typically point to a PDF or a row in a module dictionary table. Pay attention to:
   - The module type — only build for `Implementation (new)` modules. Conceptual modules are quiz-based and aren't this skill's job.
   - The module description (one sentence — the learning objective).
   - The topics or exercises list (the parenthetical sometimes contains hand-written notes from the course owner about what they want the exercise to feel like — read those carefully).
   - Where the module sits in the dictionary, which tells you what came before (it may stipulate that prior modules' outputs are available as inputs).

3. **Read the project to find the step this exercise prepares the learner for.** Open `cd15478-project-solution/solution/nimbus_decision_solution.py` (the paired `.py` is the most readable form) and `cd15478-project-solution/README.md`. Locate the section(s) of the project that exercise this module's skill. Note the input shapes, function signatures, variable names, and visualization patterns used there. *Your exercise should produce code that mirrors those idioms* — so when the learner reaches the corresponding project step, the transfer is mechanical. See "Tying every exercise to the project" below for the full rationale and the module-to-project-step mapping.

4. **Get the scope right by asking the user a few questions before building.** Use `AskUserQuestion`. Don't guess — the user has opinions about scenario direction, company choice, and data source that aren't in the module dictionary. See "Questions to ask before building" below.

5. **Pick real data + a fictional scenario company.** Real, well-known data sources with acceptable licenses; fictional scenario company per `Real-World Content Guidelines.md`. See "Sourcing the data" and "Naming the company". **Do not reuse the project's industry, company, or data files** — pick a different sector and a different dataset so the exercise practices the skill without spoiling the project's scenario.

6. **Calibrate the math first — before writing any prose.** Write a quick verification script in the sandbox that computes the exercise's outputs end-to-end. Confirm the numbers produce the intended teaching outcome (e.g., three rules disagree the way the module wants them to disagree). If they don't, adjust the payoffs or the data until they do. *Never write the instructions before the math is locked in* — it's tempting, but if the math has to change later the instructions need to change too, and you'll waste effort.

7. **Build the artifacts.** Five files, in this order:
   - `data/<dataset>.csv` plus `data/README.md` (data + attribution).
   - `<exercise-name>_starter.py` (jupytext source).
   - `<exercise-name>_solution.py` (jupytext source).
   - `INSTRUCTIONS.md` (the user-facing prompt — write this *after* the notebooks so it accurately describes what they ask for).
   - `solution_notes.md` (text walkthrough companion to the solution notebook). Include the "How this exercise feeds the project" section so the SME reviewing the solution knows which project step it preps the learner for.

8. **Convert .py to .ipynb via jupytext and execute the solution.** Use `jupytext --to ipynb` to produce both notebooks, then `jupyter nbconvert --to notebook --execute --inplace` on the solution so its outputs bake into the file. Reviewers and learners should be able to read the solution `.ipynb` top-to-bottom without running it.

9. **Sanity-check.** Read back the INSTRUCTIONS, run a final end-to-end of the solution, eyeball the artifacts as a learner would. Verify the exercise's outputs *use the same data structures and function signatures* as the corresponding project step. See the checklist at the bottom of this file.

## Questions to ask before building

Use `AskUserQuestion`. Pick the questions that fit the situation; don't ask all of them every time.

- **Scenario direction.** "There are several reasonable scenarios for this module — which industry/decision should we use?" Offer 2–3 concrete options. The course owner has typically expressed a preference (marketing-related scenarios are fine, *each implementation exercise should use a different scenario* — don't reuse the project's company or industry).
- **Real-data source.** "Which real-company / real-dataset should the data come from?" Offer 2–3 specific options. The course owner usually wants something well-known and currently-existing — *Tesla quarterly deliveries*, *Inside Airbnb city stats*, *Spotify quarterly subscribers* are all fine; *Pan Am 1949 airline passengers* is real but not currently-existing, which has been pushed back on.
- **Data delivery mechanism.** "Should the data be bundled as a small pre-aggregated CSV in the repo, or should the learner download it themselves?" Default to bundling.

You can sometimes skip the questions if the module dictionary already nails the scenario and the user has previously expressed strong preferences — but don't make the user push back twice.

## Sourcing the data

Per `Third Party Images and Datasets.md`, acceptable licenses are CC0, CC BY, CC BY-ND, ODC-PDDL / ODC-By / ODbL, U.S. Government open data, and MIT/ISC/Apache 2.0 for code. **NC** (non-commercial) and **SA** (share-alike) are not acceptable for Udacity content.

A few sources that work reliably for this course's exercises:

- **Inside Airbnb** (insideairbnb.com) — per-city short-term-rental snapshots, CC0. Great for marketing/pricing decisions.
- **U.S. Census Bureau, BLS, BEA, FRED** — public domain U.S. government economic data. Good for macro-flavored uncertainty.
- **NYC TLC trip data** — public domain rideshare/taxi trips.
- **Tesla quarterly Production & Deliveries press releases** — factual financial data, reproducible with attribution to Tesla Investor Relations and SEC EDGAR.
- **Spotify quarterly Letter to Shareholders** — same pattern.

When you bundle data in the repo, two things must be true:

1. **`data/README.md` cites the source, license, and any rounding/aggregation choices.** It also tells the SME how to refresh from the live source.
2. **The values in the CSV are real or rounded-real.** Don't fabricate. If you've rounded for legibility, say so. If you're using a published per-city/per-quarter number, attribute it.

### When the sandbox blocks the source

The Cowork sandbox has a restrictive network allowlist. FRED, raw.githubusercontent.com, Yahoo Finance, and most government data portals are typically blocked. Workarounds:

- **Use a Python package that bundles the data.** `statsmodels.datasets` ships real FRED-sourced macro data; `seaborn.load_dataset()` would ship the classic airline dataset but its loader also hits the network. Worth checking.
- **Hand-build the CSV from publicly disclosed, factual numbers** you're confident in (rounded). This is the right move for things like Tesla's quarterly delivery counts — they're factual financial data (not copyrightable), widely cited, and easily attributable.
- **Document the network limitation in your response** to the user and offer them the option of dropping the real data file into the repo themselves before publication.

## Naming the company

Per `Real-World Content Guidelines.md`: real companies as **data sources** are fine (cite them properly); real companies as the **scenario company making the decision** are not (that would fictionalize them). Pick a plausible fictional name — *BlueDoor Hosts*, *VoltStop*, *Solstice Coffee Roasters*, *UdaciCola* — and use it consistently. State up-front in the scenario that the company is fictional and the data is real.

## Calibrating the math first

This is the single highest-leverage step. Before writing any prose:

1. Sketch the exercise's payoff/outcome structure on paper or in a notepad cell.
2. Write a one-shot Python script that loads the data, computes every output the exercise asks for, and prints the answers.
3. Confirm the numbers produce the *intended teaching outcome* — usually some version of "the three decision rules disagree" or "the sensitivity flex changes the answer". If they don't, adjust the payoffs (or the data, or both) until they do. The teaching outcome is the point of the exercise; everything else is in service of it.
4. Only when the numbers land, write the INSTRUCTIONS and notebooks.

For decision-theory exercises specifically, the rule of thumb is: **three options × three states is the goldilocks size**. Smaller and the rules don't have room to disagree; bigger and the matrix gets unwieldy for a 60-minute exercise. Use tertile-binning of a continuous variable to get clean 1/3-1/3-1/3 probabilities by construction.

## Folder structure and file conventions

Exercises live under the repo root in a folder named after the module's content (never numbered — see `Exercise Guidance.md`):

```
<module-name>/
├── <exercise-name>-starter/
│   ├── INSTRUCTIONS.md
│   ├── <exercise_name>_starter.py        # jupytext source
│   ├── <exercise_name>_starter.ipynb     # generated from .py
│   └── data/
│       ├── <dataset>.csv
│       └── README.md                      # source + license + rounding notes
└── solution/
    ├── <exercise_name>_solution.py        # jupytext source
    ├── <exercise_name>_solution.ipynb     # generated, with outputs baked in
    └── solution_notes.md                  # text walkthrough companion
```

A few specifics:

- **Don't number the module folder or the exercise folder.** Module ordering changes between programs; numbering breaks that.
- **Jupytext pairs `.py` ↔ `.ipynb`.** Author the `.py` (cleaner diffs, easier to edit), then `jupytext --to ipynb foo.py -o foo.ipynb` to generate the notebook. For the solution, follow with `jupyter nbconvert --to notebook --execute --inplace foo.ipynb` to bake in outputs.
- **The starter `.ipynb` has TODOs and no outputs.** The solution `.ipynb` has full code and baked-in outputs.
- **Templates for all five artifacts live in `assets/`** — copy them, fill in the gaps. See `assets/INSTRUCTIONS_template.md`, `assets/starter_template.py`, `assets/solution_template.py`, `assets/data_README_template.md`, `assets/solution_notes_template.md`.

## Writing style rules

These rules came from real review feedback on exercises in this repo. Following them keeps the voice consistent across the course.

### Avoid sequencing language

The course is modular — exercises may be repackaged into different programs and reordered. Don't write phrases that assume a specific surrounding sequence:

- ❌ "In the next module..." / "Up next..." / "Later in the course..." / "As you saw in the previous exercise..."
- ✅ "In a later step..." / "In other modules..." / "When you build a payoff function (covered separately)..."

Skip-references that depend on order also need to be neutralized. Instead of "the next implementation module covers X," write "a separate module covers X" or just drop the forward reference entirely.

### Use natural, plain language; avoid robotic words

A few words show up in early drafts and consistently sound robotic. Replace them:

- ❌ *defensible* → ✅ *reasonable*, *solid*, or drop entirely
- ❌ *empirical* → ✅ *from the data*, *observed*, or drop
- ❌ *operationally* → ✅ *in practice*
- ❌ *utilize* / *leverage* → ✅ *use*
- ❌ *thereby* / *consequently* / *furthermore* → ✅ *so*, *and*

Use contractions ("don't" not "do not") and active voice. The voice you're aiming for is *competent practitioner explaining to a smart colleague who's new to the topic*, not *textbook*.

### `display(df)` instead of `print(df)`

In notebooks, display a DataFrame by writing `df` on its own line (or `from IPython.display import display; display(df)` when you need it mid-cell). Don't wrap DataFrames in `print()` — the rendered HTML output is much more readable than the str representation. The same rule applies to Series and to multi-cell summaries.

### Constants at the top of the cell

When a function takes a parameter that's also conceptually a tunable constant (like `gamma = 2.0` or `wealth_m = 50.0` in CRRA utility), define the constants at module-level and reference them as defaults in the function signature:

```python
GAMMA = 2.0
WEALTH_M = 50.0

def crra_utility(profit_m, gamma: float = GAMMA, wealth_m: float = WEALTH_M):
    ...
```

This makes the constants easy to find and easy to change in one place. Avoid hardcoding them inside the function signature alone (`def crra_utility(profit_m, gamma=2.0, wealth_m=50.0)`) — that hides them.

## Pedagogical principles

These shape *what* the exercise asks the learner to do, separate from *how* it's written.

### Build for transferability to the project

Every analytical pattern in the exercise — function signatures, data structures, helper utilities, visualization style — should match what the project uses for the same kind of work. If the learner finishes the exercise and then opens the project, the cognitive jump should be *"oh, different scenario, same code shape"* — not *"wait, do I need to relearn this?"* When you're tempted to invent a clever new abstraction for the exercise, ask first whether the project does the same thing differently, and prefer the project's convention. (See "Tying every exercise to the project" above for the catalogue of conventions to follow.)

### Scope tightly to one module's skill

Each exercise teaches the skill described in its module's one-sentence description. Don't try to teach adjacent skills, even if they're tempting and natural. If an adjacent skill (cost-benefit modeling, Bayesian updating, simulation) would be useful as an *input* to this exercise, **stipulate it** — give the learner the input pre-computed, with a one-line note that says *"a separate module covers how this was derived"*. That keeps the cognitive load focused on the target skill and respects the modular course structure.

### Intermediate analytical deliverables, not stakeholder recommendations

Implementation exercises produce *analytical artifacts* (a probability table, an EV/utility comparison, an optimal strategy, a sensitivity tornado). They should **not** end with a "deliver a recommendation to the stakeholder" step. That skill is taught explicitly in the communication-focused modules of the course; loading it into every implementation exercise creates an overconfident "always-recommend" reflex that has to be unlearned later.

If a step naturally produces something that *looks* like a recommendation, frame it as "produce the comparison" or "defend a decision rule" instead of "make a recommendation." See the BlueDoor exercise's step 9 for a canonical example.

### Real-world content, framed cleanly

When using real-company data as a benchmark for a fictional scenario, make the modeling assumption explicit. Don't let the reader confuse the data layer (real cities, real quarters, real listings) with the scenario layer (fictional company's decision). One paragraph of scenario framing usually fixes this — say where the data comes from, why it's relevant, what it's a stand-in for, and what the fictional company is actually deciding.

### Tertile (or quantile) binning over invented probabilities

When the exercise needs a probability distribution, derive it from the data via quantile binning rather than asking the learner to invent one. Tertiles (33rd, 67th percentile cuts) give clean 1/3-each probabilities by construction and read naturally as Strong / Average / Weak. The point isn't the specific numerical probabilities — it's that they came from data, which makes the sensitivity-flex step land properly later.

## Verification before you ship

After the artifacts are written, run this sequence:

1. **Solution executes top-to-bottom with zero errors.**
   ```bash
   jupyter nbconvert --to notebook --execute --inplace solution/<solution>.ipynb
   ```
   If anything fails, fix it before moving on.

2. **Outputs are baked into the solution `.ipynb`.** A learner opening the solution should see every printed/displayed value inline without having to run it. The `--inplace` flag above handles this.

3. **Starter `.ipynb` has TODOs and no outputs.** It should NOT execute cleanly — TODOs are intentional placeholders.

4. **The math produces the intended teaching outcome.** Re-confirm by reading the solution outputs against what the module dictionary asks for. If the module says *"my decision depends heavily on this assumption"*, the sensitivity-flex output should visibly change the recommendation.

5. **INSTRUCTIONS accurately describes the deliverables.** Read it as a learner. Every requirement listed should be something the starter actually asks for. No hidden requirements.

6. **Data README cites source + license + any rounding.** No fabricated values.

7. **Accessibility quick check.** Headings start at H2 and don't skip levels. Hyperlinks have descriptive titles, not "click here." Tables are markdown, not images.

## Common pitfalls

- **Building the exercise without reading the project first.** The exercise then uses a different function signature, different variable names, or a different data structure than the project does, and the learner has to re-learn the convention when they hit the capstone. Always start by reading the corresponding section of the project solution and adopt its idioms.
- **Reusing the project's industry, scenario company, or data files.** That spoils the project. Use a different sector and a different dataset every time.
- **Writing INSTRUCTIONS before the math is calibrated.** Then the math turns out wrong and the prose has to be rewritten. Always math first.
- **Hardcoding probabilities the learner should derive.** If the exercise's lesson is "your decision depends on this probability assumption," the learner needs to compute the probability from data — not read it off a stipulation.
- **Asking the learner to "make a recommendation" in step N.** Reframe as "produce the comparison" or "defend a decision rule." The recommendation lives later.
- **Forgetting to bake outputs into the solution `.ipynb`.** Use `nbconvert --execute --inplace` after `jupytext --to ipynb`.
- **Numbering the module folder or exercise folder.** Never do this; module ordering changes between programs.
- **Using a real company as the scenario company.** Fictional only. Real companies appear as data sources with attribution.
- **Sequencing language ("later in the course")** sneaks into solution-notes and instructions easily. Re-read for it before shipping.
- **`print(df)` instead of `display(df)` or just `df`.** Especially in solution notebooks where the rendered HTML is much nicer.
- **Constants hidden in function signatures.** Pull them out to module scope.
- **Skipping the four guidance docs.** They're authoritative and they catch things this skill doesn't.

## Templates

All five artifacts have templates in `assets/`. Copy them to the new exercise's folder and fill in the gaps. Each template has clearly-marked sections and TODO placeholders. The templates encode the conventions described above — folder structure, jupytext frontmatter, section ordering, citation format — so following them keeps you aligned with the rest of the course.

- `assets/INSTRUCTIONS_template.md`
- `assets/starter_template.py`
- `assets/solution_template.py`
- `assets/data_README_template.md`
- `assets/solution_notes_template.md`
