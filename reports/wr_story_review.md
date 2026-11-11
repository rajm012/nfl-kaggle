# Step 1 — Receiver story and claim review

Completed **2026-11-11** under [PLAN.md](../PLAN.md), Step 1. Internal narrative/source
review, not independent football validation. This report and the
[opening draft](../writeup/wr_story_opening_draft.md) are reviewable proposals for later
integration. Existing manuscript, notebook, figures and upload packet remain the tested
November 10 versions.

Evidence and source hashes: [wr_story_evidence.json](wr_story_evidence.json). This block
read existing results and checked their agreement; it did not fit models or extract features.

## 1. The central story

**Question:** two receivers have similar sprint times but different turning profiles.
What does tracking add to their evaluation, and what would justify acting on it?

**Finding:** turning profiles capture movement differences, and receiver turning has modest
descriptive transfer into games. The primary receiver comparison does not establish added
separation-prediction value. None of the nine primary comparisons supports improvement.

**Proposed action:** use the movement observation to frame a specific question for film
review, and identify the performance evidence missing before changing a recommendation.
The usefulness of this workflow has not been tested in scouting.

WR turning is the explanatory example, not a newly selected confirmatory hypothesis. Keep
the original nine-result table and prediction figure in the main submission. Line results
provide supporting context; all 25 comparisons remain available in the notebook record.

Keep the current title. It asks when tracking should affect a decision without asserting
that the study found a new talent detector. No athlete should be labelled a hidden star or
a draft mistake on the basis of this analysis.

## 2. What the existing materials need

| Observation | Proposed change | Reason |
|---|---|---|
| The manuscript opening starts with the receiver pair, then quickly becomes a general receiver/line summary | Ask the receiver question immediately; place W1's actual performance result before broadening to all nine | Readers encounter one question, its answer and the proposed use within the opening |
| The opening lists film, development and draft-board changes as possible decisions | Lead with a specific film question and the evidence gap before a recommendation | Development improvement and draft-ranking usefulness were not tested |
| The hero figure shows one speed-out attempt, while its headings show an across-drill profile | Distinguish the illustrated attempt from the composite profile in the caption and text | One attempt cannot explain or validate a trait averaged over several drills |
| The pair has the largest TURN contrast among qualifying similar-time development WRs | Explicitly call it an illustrative extreme contrast | Exposure-only selection avoids choosing by NFL success but does not make the pair representative |
| The notebook says “where does a player turn efficiently” | Ask how the player enters and exits comparable out cuts | Turning efficiency has not been measured or established |
| The notebook says cross-drill consistency “supports measuring a trait” | Describe population-level agreement across drill halves and its limits | This does not certify an individual's repeatability or a route-specific talent score |
| Supporting line and cone findings can compete with the receiver thread | Use brief labelled support paragraphs; retain all original rows and favourable/adverse results | Narrative focus must not hide the full evidence or promote selected subsets |
| Reliability, transfer and prediction use different cohorts and reference constructions | State their separate sample sizes, season windows and preprocessing | They are complementary checks, not one continuous validated prospect-ranking chain |

The original writeup already contains several of these cautions. The change is to carry
them consistently through the opening, hero explanation, notebook and practical conclusion.

## 3. First-minute opening

The exact proposed opening is saved in
[wr_story_opening_draft.md](../writeup/wr_story_opening_draft.md). It contains the question,
the receiver result, all-nine context and the proposed film question. It does not assert
individual repeatability, superior cutting or a demonstrated scouting benefit.

The error is **equal-athlete RMSE of athlete mean outcomes/predictions**, not average error
on an individual route. The full methods paragraph must define that distinction. The
comparison uses realised NFL contexts and is not a draft-time forecast of future roles.

This draft is a replacement for the opening, not an additional section to append. It is
not a complete revised submission; Steps 2–4 supply the movement explanation, fuller
uncertainty wording and practical workflow before integration in Step 5.

## 4. Revised manuscript outline

Keep six figures and one table. Use the existing assets and evidence, with these roles:

| Section | Approximate words | Main job | Evidence/visual |
|---|---:|---|---|
| Opening: the similar-time receiver question | 190 | State the question, primary receiver answer and proposed film-review use | Figure 1; W1 result |
| What the turning profile measures | 280 | Explain lateral acceleration, across-drill aggregation and the single-attempt illustration; define BURST/A0 briefly | Figure 1; existing kinematics; Step 2 output |
| How the NFL comparison was made | 290 | Describe baseline, samples, REG scope, train-only preprocessing, equal-athlete RMSE and conditional evaluation | Figure 2; frozen protocol |
| Movement transfer and the route measurement gate | 280 | Lead with WR evidence; summarize DL size adjustment; explain why the route primary stopped | Figures 3–4 |
| Added performance: receiver result and full comparison record | 390 | Explain W1, retain all nine errors/intervals, adverse D1 and secondary cone limits | Figure 5 and Table 1; Step 3 output |
| A concrete film-review question and limitations | 320 | Return to the same pair; describe the proposed next inspection and missing evidence; close with limitations | Figure 6; Step 4 output |

The prose allocation totals about **1,750 words**, leaving room for captions, attribution
and editor fields within 2,000. The conservative count of the integrated materials must
be checked; these allocations are not a completed word-limit verification.

Suggested bridges to keep the receiver thread connected:

- After measurement: “A movement difference is visible. The next question is whether it
  appears in games and improves prediction after conventional information is included.”
- After transfer: “Movement carryover does not establish an advantage in separation.
  We tested that performance question separately.”
- Before all-nine evidence: “The receiver example is one of nine prescribed comparisons.
  The complete set limits how broadly we can interpret it.”
- Before practical use: “For these two receivers, the next proposed output is a film
  question and an evidence gap before changing a recommendation.”

## 5. Claim-to-evidence map

| Proposed claim | Exact supporting record | Permitted interpretation and boundary |
|---|---|---|
| The selected pair has similar observed 40 times | [route_trace_selection.json](route_trace_selection.json): A 4.54 s, B 4.52 s; [audit_figures.py](../src/audit_figures.py), `route_trace` | Stopwatch results differ by 0.02 s; this is not a claim of equal speed during the illustrated drill |
| Their across-drill TURN profiles differ | Same selection record: A −1.78215, B +2.53314 development-WR athlete SD; `training_turn` in [reliability.py](../src/reliability.py) | Descriptive composite profile; the chosen pair maximizes the contrast within the exposure-only rule, so it is not typical-population evidence |
| The figure depicts actual speed-out motion | Selection record: first recorded speed-out event, 43/50 frames; [combine_route_trace.png](figures/combine_route_trace.png) | Start-relative translation only, common axes. Do not infer efficient cuts, defender leverage, matched drill-entry speed or future success |
| TURN summarizes lateral acceleration across non-40 drills | [combine_features.py](../src/combine_features.py): attempt 90th percentile of absolute lateral acceleration, player/drill means, drill standardization, average; [kinematics.py](../src/kinematics.py) | Lateral acceleration depends on speed and path shape. It is not a direct intrinsic-agility or cutting-efficiency score |
| Development WR profiles show cross-drill agreement | [reliability.json](reliability.json), `cross_drill`: development/training-reference WR TURN, n=70, SB=0.59258 [0.37274, 0.73694] | Across-drill composite consistency in a cohort, not individual or single-route test–retest reliability |
| Receiver turning transfers modestly into game movement | [transfer_audit.json](transfer_audit.json), corrected PRE+REG/WR/lat/raw: n=98, r=0.27885 [0.10723, 0.44453] | Descriptive pooled PRE+REG movement association, not REG performance prediction or untouched cohort validation |
| Adjusting for measured size and 40 leaves a similar WR transfer estimate | Same record, size+forty-adjusted: n=98, r=0.27828 [0.09236, 0.44969] | Does not account for drill-entry speed or all execution/context differences; no intrinsic-agility conclusion |
| DL burst provides supporting evidence about size effects | Same record, DL/burst: raw r=0.44338, weight-adjusted r=0.20350, n=115 | Smaller adjusted descriptive correlation; not a causal explanation or validated get-off advantage |
| The registered route-family primary stopped at measurement | [study3_measurement.json](study3_measurement.json): adjusted SB=0.29613 [−0.25661, 0.60620], n=41; [study3_protocol.md](study3_protocol.md), gate ≥0.40 | No primary TURN interaction or Study 3 evaluation fitted. Failure is not proof of no route-specific effect |
| WR TURN did not establish added separation prediction | [validation.json](validation.json), W1: RMSE 0.2357216 vs 0.2357681 yd; gain −0.0000465 [−0.0090258, 0.0126710], n=23 | Equal-athlete conditional prediction of means. Neither equivalence nor a player-specific prospect recommendation |
| No primary addition supports improvement | `validation.json`, all nine primary rows; [evaluation_table.csv](evaluation_table.csv) | 0/9 lower marginal gain bounds above zero; every original-family simultaneous interval includes zero. D1 has nominal deterioration, so do not say all marginal intervals include zero |
| Historical primary associations remain unsupported after correction | [model_audit.json](model_audit.json): original two-sided Holm significance count 0/9, separate binary sensitivity 0/3 | Association tests differ from prediction-gain intervals and are not the same evidence |
| A positive cone subset remains secondary | `validation.json`, F1_cone: gain 0.00754695 s [0.00442760, 0.01080184], n=9; [cone_sensitivity.md](cone_sensitivity.md) | Selected small cone cohort; retain alongside adverse/uncertain subset findings; no general DL ranking claim |
| A specific film question is a possible use | Proposed workflow in the opening and later Step 4 | A reasoned proposal only; no film review, coaching intervention or decision-utility evaluation was performed |
| Evaluation uses a disclosed retrospective cohort split | [evaluation_protocol.md](evaluation_protocol.md), [prereg.md](prereg.md), `validation.json` | Prior 2025 exposure disclosed; training-only preprocessing; realised context; intervals omit training-fit uncertainty |
| The record is reproducible | [kaggle_execution.json](kaggle_execution.json): tested version 3, public version 4; 402 checks/25 scores/12 tests | Saved version-specific evidence; future changes require relevant new checks. Owner browser/Writeup submission still pending |

Reference populations differ: development consistency and the hero profile use 2023–24
drill references. Historical movement transfer uses the recorded full-cohort drill-normalized
Combine traits. Cohort prediction rebuilds features and preprocessing from training athletes.
Do not silently describe historical transfer as a training-only held-out result.

The single illustrated attempts have raw 90th-percentile lateral acceleration **6.62008**
and **7.21783 yd/s²**. Those values have different units and aggregation from the −1.78/+2.53
composite headings. Keep the distinction explicit; Step 2 will examine the mechanics.

## 6. All nine primary comparisons retained

The ledger below is generated from `evaluation_table.csv` after checking every numeric field
against `validation.json`. Positive gain means improvement. Intervals are marginal 95%
evaluation-athlete bootstrap intervals, conditional on training fits; all original-family
simultaneous intervals include zero.

| ID | Comparison | Athletes | Unit | Baseline RMSE | + Tracking RMSE | Gain [95% interval] |
|---|---|---:|---|---:|---:|---|
| W1 | WR turning → separation | 23 | yards | 0.23572 | 0.23577 | -0.00005 [-0.00903, 0.01267] |
| W2 | WR burst → separation | 23 | yards | 0.23572 | 0.23651 | -0.00079 [-0.00641, 0.00416] |
| O1 | OL turning → pressure allowed | 28 | proportion | 0.09511 | 0.09446 | +0.00065 [-0.00114, 0.00171] |
| O2 | OL burst → pressure allowed | 28 | proportion | 0.09511 | 0.09800 | -0.00290 [-0.00728, 0.00382] |
| D1 | DL burst → get-off time | 37 | seconds | 0.07583 | 0.07981 | -0.00398 [-0.00705, -0.00049] |
| D2 | DL turning → pressure generated | 37 | proportion | 0.04370 | 0.04255 | +0.00115 [-0.00008, 0.00231] |
| F1 | DL first step → get-off time | 23 | seconds | 0.09281 | 0.09216 | +0.00065 [-0.00086, 0.00195] |
| F2 | OL first step → peak pressure allowed | 22 | proportion | 0.09364 | 0.09373 | -0.00009 [-0.00181, 0.00066] |
| F3 | WR first step → separation | 20 | yards | 0.21054 | 0.21062 | -0.00008 [-0.00779, 0.00875] |

W1 is the central worked example. W2/F3 retain the other receiver questions. O1/O2/D1/D2/F1/F2
retain all line evidence, including the adverse D1 point/nominal interval. None is removed
because of the new narrative focus. Historical associations and the stopped route interaction
are reported separately rather than merged into this prediction ledger.

The notebook's complete record retains 9 primary, 7 joint/no-10-yard secondary and 9 cone
comparisons. The positive F1_cone result cannot replace the uncertain primary F1 result.

## 7. Proposed figure explanations

These are replacements for existing explanations, not additional main visuals. Final
wording/length will be settled as Steps 2–4 finish.

1. **Similar sprint times, different turning profiles.** “One recorded speed-out attempt
   per receiver, with start-relative positions and lateral acceleration. The headings show
   their across-drill TURN profiles. The pair maximizes that profile contrast among
   qualifying 2023–24 WRs with 40 times within 0.03 seconds; no NFL outcomes informed
   selection. It illustrates a difference, not a representative pair or superior talent.”
2. **Who supports the NFL comparison?** “Outcome and exposure availability leave 20–37
   evaluation athletes per primary comparison. WR TURN uses 23 receivers. More plays can
   improve an athlete's mean estimate but do not create more independent athletes.”
3. **Does movement carry over?** “WR turning has modest descriptive PRE+REG movement
   transfer. The DL panel shows how adjustment for measured body size changes burst
   transfer. These pooled movement findings are separate from added REG performance prediction.”
4. **Can the route contrast be measured consistently?** “Raw and adjusted SLANT/OUT-minus-GO
   contrasts across alternating games. Panel intervals describe correlations; the frozen
   gate uses adjusted Spearman–Brown consistency, 0.296 against 0.40. No primary TURN
   interaction or Study 3 evaluation was fitted.”
5. **Does tracking improve prediction?** “All nine primary RMSE comparisons, each with
   equal-athlete weighting. None supports a positive gain; D1 shows nominal deterioration.
   The figure uses relative reductions and Table 1 absolute errors/units. Intervals omit
   training-fit uncertainty; all original-family simultaneous intervals include zero.”
6. **What could a scout inspect next?** “A proposed receiver film-review aid. Keep movement
   observations, game carryover and performance evidence separate. A draft recommendation
   needs further support; decision usefulness has not been tested.”

## 8. Concrete notebook wording proposals

Use [build_submission_notebook.py](../src/build_submission_notebook.py) when integrating
later; do not hand-edit only the saved notebook and let the builder diverge. The current
Step 1 block does not rebuild or republish it.

| Location | Proposed replacement/addition |
|---|---|
| Opening markdown | “Two receivers can post similar 40-yard times and have different turning profiles. Does that difference justify a different scouting evaluation? We follow one receiver example through measurement, game-movement transfer and added separation prediction, while reporting all nine prescribed comparisons. None supports a primary prediction gain. The proposed output is a film question and an evidence gap before changing a recommendation.” |
| Section 01 and Figure 1 caption | Name the pair's 4.54/4.52-second times; use the Figure 1 wording above to distinguish composite profile, one attempt and extreme selection. Avoid claiming faster or more efficient cuts |
| Section 02 | Retain 510-player context and all-position support; state W1's n=23 directly. Preserve PRE+REG movement versus rookie-REG prediction scopes |
| Section 03 consistency paragraph | “Across 70 development receivers, drill-half agreement gives TURN composite consistency 0.593 [0.373, 0.737]. This is a cohort-level cross-drill estimate; it does not certify either illustrated receiver's repeatability or a single-route talent score.” |
| Section 04 | Retain the failed gate, its 41 diagnostic players and stopped primary. Do not change eligibility, threshold or route groups |
| Section 05 | Place W1's 0.23572/0.23577-yard RMSE comparison before the all-nine figure/table. Preserve all rows, negative/uncertain results, binary model disclosure, training-only processing and prior exposure |
| Section 06 | Replace “where does a player turn efficiently” with “how does each receiver enter and exit comparable out cuts?” Add “No film review or decision-utility test was performed; the question is a proposed next inspection.” |
| Reproduction appendix | Retain full methods, all 25 comparisons, historical audit, measurement gate and version-specific reproduction details |

The existing binary cohort prediction disclosure agrees with the frozen protocol: a
player-clustered linear-probability fallback is used for binary outcomes. Keep that detail
accurate rather than describing all cohort models as player random-intercept models.

## 9. Completion and handoff

Step 1's internal completion checks are satisfied:

- A concrete opening contains the question, W1 result, all-nine context and proposed use.
- Every quantitative claim above has a source and an interpretation limit.
- All nine primary rows and all 25 comparison IDs are accounted for; the stopped route
  primary remains unfitted and outcome-independent hero selection is recorded.
- Manuscript outline, all six figure explanations and notebook replacements are reviewable.
- Existing submission/frozen-source hashes match their preceding records. No source,
  protocol, manuscript, notebook, figure, upload packet or publication changed in this block.

Owner clarity/design feedback remains useful; these are internal source and narrative checks,
not an independent readability study or approval of a final manuscript. **Next: Step 2,
the movement explanation**, using the same selected pair and written definitions before
any extra descriptive quantities are calculated.
