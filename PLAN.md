# NFL Big Data Bowl 2027 — Submission plan

Updated **2026-11-09** after Studies 1–2 and the repository review. This supersedes the
original strategy, preserved in `reports/plan_2026-10-08.md`. Earlier preregistrations and
results remain in the research record.

## 1. Objective, budget and competition

Build the strongest defensible University-track entry using our existing data and machine.
Aim for a prize through a precise football question, credible validation and excellent
communication. A judged competition cannot provide guaranteed income or a reliable payout
date. Do not spend money assuming an award will arrive.

**Incremental cash budget: $0.** Use the installed environment, local CPU, existing Parquets
and available free Kaggle notebook resources. No paid datasets, cloud compute, new
subscriptions or large model search. Cache movement calculations. Work in resumable blocks
so the owner does not need to supervise continuously.

| Constraint | Working requirement |
|---|---|
| Competition | https://www.kaggle.com/competitions/nfl-big-data-bowl-2027 |
| Track | University; undergraduate status recorded in project memory |
| Hard deadline | **2027-01-06 23:59 UTC**, reconfirmed via Kaggle CLI on November 9 |
| Internal submission | **December 28**; public notebook ready by December 14 |
| Deliverable | Writeup ≤2,000 words, fewer than 10 combined figures/tables, attached public notebook |
| Rubric from original rules notes | Football 30%, Data Science 30%, Writeup 20%, Visualisation 20% |
| Prize information | API lists a **$100,000 total pool**, not an individual award. Earlier rules notes list $5k/$10k track awards; recheck allocation and eligibility before publication. |
| Required link | Combine **tracking** to regular-season **performance**, including a well-supported negative finding if warranted |

CLI confirms `userHasEntered=True`. Direct overview/rules HTTP requests returned 404 on
November 9 although the listing worked; the rules have not been newly reverified.
Check the official UI before publication. Changed legal terms and final Writeup submission
remain owner actions.

## 2. Existing evidence and limits

- All nine CSVs downloaded: 510 athletes, **22,654,290 game frames**, 314,197 player-play rows.
- Reusable pipeline: signed acceleration → drill-normalised Combine traits → game movement.
- Reported WR turning transfer r=0.28; DL burst r=0.45, attenuating to 0.21 after weight
  adjustment in prior notes. These are movement findings, not established performance gains.
- Six envelope tests and three first-step tests produced no Holm-significant added performance
  association. The original general-metric and first-step bets have ended.
- Held-out prediction, robust binary uncertainty and supporting reproduction checks remain
  unfinished. Audit the old nulls before presenting them as final evidence.
- Only the rookie cohort appears in game tracking. We cannot reconstruct opponent geometry,
  separation time series or ball-relative outcomes from these frames.
- Many plays improve performance measurement but do not create more independent athletes.

The final product will be a **scouting evidence map** separating measurement reliability,
game transfer and incremental performance value. A stronger signal headline is conditional
on validation; a complete submission will exist even if the next experiment fails.

## 3. One final bounded research question

**Working title: “Turning into Separation? What Combine Movement Can Tell a Scout.”**

**Does a receiver's Combine turning trait relate to better separation on slant/out routes
relative to go routes, after accounting for context and conventional measurables?**

This tests whether the earlier all-route null concealed a route-context relationship.
Use the existing TURN trait rather than inventing a score and searching for an outcome.

### Feasibility checked November 9

Counts below used eligibility/missingness only, with no new trait–outcome association:

| Draft class | ≥10 recorded plays on both SLANT and OUT, all available seasons | ≥10 on each of pooled SLANT/OUT and GO, rookie season only |
|---|---:|---:|
| 2023 | 23 | 25 |
| 2024 | 17 | 17 |
| 2025 | 7 | 16 |

All 107 WRs ran tracked slant and canonicalised speed-out drills. Only **3** repeated slant
and **17** repeated speed-out. A drill-specific route-talent score lacks convincing
test–retest evidence. The primary study uses the existing all-drill turning measurement.

### Fixed design

- Primary routes: **SLANT, OUT, GO**. Pool SLANT/OUT as the turning-route family for the
  interaction; retain separate route intercepts. These are distinct routes.
- Rookie-season REG, non-nullified plays with recorded separation; require ≥10 such plays
  in each family per athlete.
- One primary coefficient: **TURN × turning-route family**. Expected positive; two-sided
  test and 95% interval. This estimates a difference between route-family associations.
- Within-player comparison, context controls, and conventional-measurable family interactions.
  Player effects remove athlete-level intercept differences; they do not eliminate all
  context/selection confounding.
- Separate route slopes and coverage interactions are exploratory, not additional chances
  to declare a confirmatory success.
- Full protocol: `reports/study3_protocol.md`, appended to the preregistration record.

### Required validation

1. Reproduce TURN reliability; inspect actual movement traces. Cross-drill reliability is
   not proof of reliability for a single-route score.
2. Measure repeatability of the adjusted route-family separation contrast across games,
   using outcomes alone. Report uncertainty and who is missing.
3. Develop on **2023–24 rookie seasons** with training-only preprocessing.
4. Evaluate on **2025 athletes**, comparing baseline versus TURN-augmented prediction of
   each athlete's route-family separation contrast. Give every athlete equal evaluation weight.
5. Use player-aware uncertainty and game clustering; check influential athletes, route weights,
   missingness and the small 3-cone-observed subset without redefining the primary test.

**History matters:** 2025 outcomes already appeared in Studies 1–2. Reserve them from
further Study 3 development, but do not call this a pristine untouched holdout. Disclose
prior outcome exposure, frozen choices and the limits of a 16-athlete evaluation sample.

Prediction using realised NFL context is retrospective conditional validation. It does not
directly establish a pre-draft forecast of a prospect's future route tree.

### Research limits and narrative decision

- **November 12:** audit and frozen protocol in place before associations.
- **November 16:** measurement/support checks and development fits complete.
- **November 20:** cohort evaluation complete and final story selected. No new hypothesis
  families after this date; later work corrects errors or supplies prespecified sensitivities.
- Do not lower eligibility thresholds after viewing an effect or change route groups until
  significance appears. Do not revive unreliable braking features.
- Stop the performance-signal claim if measurement, support or replication fails.

| Evidence by November 20 | Story and permitted football use |
|---|---|
| Positive development interval excludes zero; stable direction; improved cohort prediction with uncertainty supporting improvement | Limited route-context signal; propose targeted film/practice evaluation with prospect uncertainty |
| Development association but uncertain/worse cohort prediction | Exploratory association; no validated ranking claim |
| Reliable movement transfer but absent/uncertain added performance gain | Evidence map showing where Combine movement carries over and where scouting claims lack support |
| Audit materially changes prior results | Correct reports transparently; reassess against the same evidence requirements |

Use **0.10 yard per SD** as a predeclared planning band for the route interaction, with
0.05/0.20-yard sensitivity bands. This is not an established NFL utility threshold.
Absence of significance does not establish negligible effect. Use equivalence wording only
with an appropriate interval/test against a predeclared band. No universal “tracking is useless” claim.

## 4. Repair the evidence before polishing it

Preserve numerical reports as dated historical outputs. Save corrected reruns separately;
explain amendments and discrepancies rather than overwriting unfavourable results.

| Work | Concrete output | Acceptance condition |
|---|---|---|
| Data/key audit | `src/audit_data.py`, `reports/audit.md` | Unique joins, counts, REG/PRE/POST treatment, retained/dropped players, missingness |
| Model audit | `src/validation.py`, corrected Study 1/2 reports | Actual fitted n; robust player-clustered binary LPM sensitivity; player-table Study 2 SDs; directional-test deviation; convergence |
| Supporting findings | `reports/reliability.md`, adjusted-transfer and positive-control tables | Saved code regenerates all selected numbers, intervals and adjustment definitions |
| Transfer specification | Player-season and pooled traits; season-type sensitivity | Explicit POST exclusion for REG/PRE measurement; code/report alignment; no evaluation leakage |
| Incremental validity | `src/evaluate.py`, `reports/validation.md` | Baseline vs tracking; train-only imputation/scaling; no held-out player effects fitted from evaluation outcomes |
| 3-cone sensitivity | Same-sample nested comparison table | Show small sample/opt-outs; do not fabricate cone times |

A separate player-clustered linear-probability model is a documented sensitivity analysis,
not silently described as the original mixed model. Show changes in coefficients and
intervals. Study 3 remains continuous.

Prioritise checks used in the submission. Use small meaningful tests for keys, season
filters, player-level scaling and evaluation leakage. Reuse cached tracking; installed
Bayesian/ML packages do not require a new model suite.

## 5. Earn points in all four rubric categories

### Football — 30%

Explain the difference between moving well and creating separation against NFL coverage.
Ask when tracking justifies additional evaluation beyond the conventional baseline.
The scout-facing evidence card has separate measurement, transfer and prediction fields.
Reliable movement without added performance evidence does not justify a draft upgrade.

Show practice monitoring as a proposed use only. Observational associations cannot prove
that training this metric improves performance. Do not label athletes busts or hidden stars.
Explain limitations from absent opponents, changing route usage and selection into playing time.

### Data Science — 30%

One predeclared follow-up, corrected uncertainty, unique-player n, reliability, a conventional
baseline, route/context adjustment, grouped evaluation and explicit prior outcome exposure.
Show effect sizes in real units. All headline numbers must regenerate from saved code.

### Visualisation — 20%

Target **six figures and one table**. Every chart must stand alone at writeup width,
with colour-blind-safe colours, direct labels, units and sample sizes.

| Visual | Purpose |
|---|---|
| 1. Hero route trace | Show actual Combine movement and what TURN measures; comparable-stopwatch pair selected by an exposure-only rule |
| 2. Evidence funnel | Show unique athletes with drills, movement and REG outcomes |
| 3. Transfer panel | WR turning and DL burst; raw/size-adjusted estimates and intervals |
| 4. Performance effect plot | Audited effect sizes with practical-size bands and study labels |
| 5. Route-context result | The within-player interaction, including honest uncertainty/null display |
| 6. Scout evidence card | Separate confidence in measurement, transfer and prediction |
| Table 1. Evaluation | Baseline vs tracking, equal-player error, gain interval and evaluation n |

Never select the hero pair because their NFL outcomes tell the desired story. Animation is
optional. Build an interactive product only if it improves the judged submission enough
to justify the time; static figures are sufficient for the current plan.

### Writeup — 20%

Target **1,850–1,950 words**: question/hook 180; data/measurement 300; validation 300;
results 500; football use 350; limitations 220. Lead with the actual primary finding.
Every conclusion should connect to a visual or table.

Summarise earlier studies in the evidence map and link the complete record from the notebook.
Do not narrate every abandoned approach in the main writeup.

## 6. Reproduction begins during the audit week

Create `notebooks/submission.ipynb` now in the next execution block. Its first working
version should regenerate at least one verified table and figure from Kaggle input paths.

- Version project dependencies; avoid paid/network services at runtime.
- Do not rely on local interim files, secrets or unpublished helper modules.
- Rebuild required features from competition inputs. If using a permitted Kaggle output
  cache, disclose/version it and retain the rebuilding procedure.
- A small smoke-run is for development only, clearly distinct from submission results.
- Run the complete notebook in a clean Kaggle session, save outputs and record memory/runtime.
- Prepare exact notebook metadata and the writeup before requesting any necessary publication
  authorization. Do not publicly publish/push unless authorization is already provided.
- Never include token values or raw data in Git; do not push without authorization.
  Changed terms and final Submit are owner actions.

## 7. Schedule from today

| Dates | Required output |
|---|---|
| Nov 9 | Revised strategy and bounded protocol; feasibility recorded |
| Nov 10–12 | Data/model audit; reliability reproduction; notebook skeleton and first table/figure |
| Nov 13–16 | Corrected models; Study 3 measurement/development; two prototype figures |
| Nov 17–20 | Frozen cohort evaluation, sensitivities, **final story decision** |
| Nov 21–30 | Complete seven visuals/table, notebook v1 and draft v1 |
| Dec 1–7 | Football/statistical cold reads; clean-input rerun; revise explanations and figures |
| Dec 8–14 | Full Kaggle execution; public notebook ready with authorization; writeup v2 |
| Dec 15–21 | Official rules/track verification; access, citations, rendering and count checks; packet ready |
| Dec 22–28 | Owner attaches notebook and submits; save confirmation and artifact versions |
| Dec 29–Jan 6 | Buffer for genuine fixes/submission issues; no new hypothesis search |

If work slips, remove optional animation and analyses first. Preserve validation, readable
writeup, public reproduction and the internal submission date.

## 8. Review and execution discipline

Review from two perspectives: a football reader asking what a scout can do, and a statistical
reader checking the evidence for every claim. These are review perspectives, not a requirement
to pay reviewers or launch more agents.

Maintain `reports/submission_checklist.md`. Self-assigned rubric scores diagnose weaknesses;
they are not prize probabilities. Final checks:

- Explicit Combine-tracking→REG performance link and conventional baseline.
- Every headline number regenerates; intervals, athlete counts and study labels agree.
- Prior 2025 exposure and current evaluation boundaries disclosed.
- No unsupported causal training effects, universal rankings or claims that p>0.05 proves zero.
- ≤2,000 words, fewer than ten figures/tables, public notebook runs and is attached.
- Eligibility/terms and owner submission complete before the hard deadline.

End each work block with `STATUS.md` and durable `CLAUDE.md` updates. Resume from saved
artifacts instead of repeating orientation or adding more study families.

**Next work block:** preserve historical reports, audit keys/season filters, reproduce TURN
reliability, and create the notebook skeleton. No new trait–outcome fit before the frozen
follow-up protocol and measurement checks.
