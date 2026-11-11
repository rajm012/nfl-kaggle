# Writeup judging review — 2026-11-11

Internal editorial, football and statistical review. This is not independent expert feedback
or a prediction of the competition result. Steps 1–4 are integrated into the manuscript,
Figures 1/6 and notebook. Models, samples, frozen prediction specifications and measurement
definitions remain unchanged. A documented historical-solver memory-layout reproduction
fix preserves matrix values and the original acceptance checks; see
[step5_reproduction_findings.json](step5_reproduction_findings.json).

## Rubric review

| Criterion | Weight | Revision and evidence | Remaining limitation |
|---|---:|---|---|
| Football relevance | 30% | Opens with the observed 4.54/4.52-second WR pair. The scout conversation specifies drill checks, out-cut film questions and the performance evidence needed for a recommendation. Explains that get-off is LOS-crossing time. | Film review and decision usefulness are proposed; no film assessment or scouting intervention was performed. |
| Data science | 30% | Retains the failed measurement gate, all nine primary comparisons, conservative historical inference, equal-athlete scoring, training-only processing and conditional evaluation limits. | Small samples, earlier 2025 exposure, selection and omitted training-fit uncertainty remain. |
| Writing | 20% | Replaces a generic introduction and repeated abstract advice with a specific football question and a three-part worked conversation. Reduces audit detail while preserving necessary corrections. | External cold-read feedback remains unavailable until arranged. |
| Visualization | 20% | Keeps six figures and one generated table; Figure 1 adds speed/reference-window explanations, while Figure 6 specifies the next film question and missing evidence. Relative plot gains remain distinct from absolute table errors. | Actual Kaggle Writeup image upload and editor rendering remain owner checks. |

## Issues found and resolved

1. **Generic scouting advice.** The original advice asked broadly how movement appears in
   games. The revised example asks about entry speed, break geometry and reacceleration on
   comparable out cuts, with coverage, cushion, motion and throw timing as interpretation context.
2. **Cohort-to-player overreach.** The prior phrase “a receiver with repeatable TURN” implied
   an individual reliability conclusion. The revision says cross-drill consistency is estimated
   across 70 development receivers and does not certify either example player's repeatability.
3. **Implied validation of a scouting aid.** “Calibrated scouting aid” could suggest tested
   decision performance. The introduction now calls the map a proposed review aid and states
   that its usefulness in actual scouting decisions has not been tested.
4. **Point estimate versus equivalence.** Removed “effectively no point improvement.” The
   WR baseline/tracking errors and gain interval are stated directly; no equivalence claim follows.
5. **Pressure outcome wording.** The methods preserve the recorded-time operational pressure
   proxy; the results call it the recorded pressure proxy rather than an independently validated
   pressure classification.
6. **Drill-mix claim.** Replaced the unverified assertion that scaling reduces mix effects
   with the narrower statement that standardisation puts drill measurements on comparable scales.
7. **Upload friction.** The generated `writeup/kaggle_upload/` folder supplies exact title,
   description, body, notebook attachment details and six numbered PNGs. Local image paths still
   need replacing with editor-generated links. The package checks the combined editor-field word count.
8. **Packet omission.** Added the actual nine-row evaluation CSV to the ZIP and asset manifest;
   the earlier packet description promised it but the generator omitted it.
9. **Single-attempt/profile confusion.** Both profiles average the same 13 drills; the
   illustrated speed-out contributes 5.9% arithmetically to their gap. Separate reference
   peaks show B faster along a wider local curve. Higher TURN is not cutting efficiency.
10. **Repeatability on the card.** Replaced “Observe repeatable movement” with cohort
    agreement and explicit absence of individual repeatability validation. The uncertain
    n=17 speed-out repeat result is retained in the manuscript and notebook.
11. **Prediction endpoint and deployment.** W1 scores athlete means over realised NFL
    contexts, rather than route-level errors or a draft-time role forecast. Throw-time
    separation and the pooled-route W1 test do not answer the proposed out-cut film question.
12. **Workflow specificity.** The revised example records comparable routes, coverage,
    timing, contradictory clips and missing context. It identifies repeatable individual
    measurements and independent performance information as evidence needed before a grade
    change. No film assessment or decision-utility test is represented as completed.

## Claim and source checks

| Manuscript claim | Source and reviewed values |
|---|---|
| Illustrative receivers | `route_trace_selection.json`: A=4.54 s, TURN −1.78; B=4.52 s, TURN +2.53. The display uses development-WR athlete SD units (`audit_figures.py`), after training drill standardisation. Selection used Combine exposures only; profiles summarise multiple drills, not only the illustrated speed-out attempt. |
| Cohort support | `evidence_support.json`: WR/OL/DL primary support 23/28/37; first-step support 20/22/23. Other primary outcomes use the displayed corresponding samples. |
| WR cross-drill consistency | `reliability.json`: development training-reference TURN SB 0.593 [0.373, 0.737], 70 WRs. |
| Movement transfer | `transfer_audit.json`: corrected PRE+REG WR TURN 0.279 [0.107, 0.445], n=98; DL burst 0.443 [0.289, 0.584], n=115; weight-adjusted 0.203 [0.044, 0.376]. |
| Route gate | `study3_measurement.json`: adjusted SB 0.296 [−0.257, 0.606], below 0.40; 41 diagnostic WRs. Primary interaction stopped. |
| Primary added prediction | `validation.json` and `evaluation_table.csv`: zero of nine marginal intervals supports improvement; all original-family simultaneous intervals include zero. DL BURST has nominal deterioration, not a supported improvement. |
| WR TURN prediction | Baseline 0.23572 yd, tracking 0.23577 yd; gain interval [−0.00903, 0.01267], n=23. The full nine-row table is generated rather than manually maintained. |
| Selected cone finding | `validation.json`: DL A0 cone gain 0.00755 s [0.00443, 0.01080], nine evaluation athletes. Secondary, selected sample; broader primary uncertain. |
| Trace explanation | `wr_movement_metrics.json` and the written trace protocol: speed 5.433/5.879 yd/s, curvature 0.249/0.233 1/yd; fixed interior peaks/windows, no efficiency claim. |
| Repeat and adjusted transfer | `reliability.json`: speed-out r=0.012 [−0.442, 0.492], n=17. `transfer_audit.json`: size/40-adjusted WR r=0.278 [0.092, 0.450], n=98. |
| Adverse/secondary findings | `validation.json`: D1 nominal deterioration, F2 adverse ≥30-play nominal result, selected F1_cone positive n=9 and W2_cone adverse n=7. All 16 secondaries retained. |
| Reproduction | `step5_integration_verification.json` and `kaggle_execution.json` hold current version-specific proof: 402 original checks, 25 scores, 241 descriptive numeric checks, 12 pipeline tests and 4 physics checks. The public notebook ID remains 144208320. |

## Actual open work

Numerical/asset checks are recorded in `writeup_verification.json` and
`step5_integration_verification.json`. The manuscript is 1,687 conservative words; title,
description and body total 1,720, with six figures and one table. Frozen scientific
sources and reports are preserved. Publication is verified against the corresponding
source bundle and execution record, rather than relying on the preceding version's hashes.

- Owner review of the revised preview, followed by any corrections it identifies.
- Optional external football/statistical cold reads; a brief is prepared in `writeup/reviewer_brief.md`.
- Competition Writeup draft creation, image upload, notebook attachment and actual editor preview.
  The installed SDK offers read-only Hackathon/Writeup methods and this session has no browser
  editing tool, so no Kaggle Writeup draft was created.
- Owner confirmation of University eligibility, presented terms and final Submit. The public
  notebook is published; it is not the final competition Writeup submission.
