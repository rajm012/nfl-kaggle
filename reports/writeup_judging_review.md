# Writeup judging review — 2026-11-10

Internal editorial, football and statistical review. This is not independent expert feedback
or a prediction of the competition result. Models, samples, frozen specifications and notebook
version 4 remain unchanged. The revision uses existing verified results only.

## Rubric review

| Criterion | Weight | Revision and evidence | Remaining limitation |
|---|---:|---|---|
| Football relevance | 30% | Opens with the observed 4.54/4.52-second WR pair. The scout conversation specifies drill checks, out-cut film questions and the performance evidence needed for a recommendation. Explains that get-off is LOS-crossing time. | Film review and decision usefulness are proposed; no film assessment or scouting intervention was performed. |
| Data science | 30% | Retains the failed measurement gate, all nine primary comparisons, conservative historical inference, equal-athlete scoring, training-only processing and conditional evaluation limits. | Small samples, earlier 2025 exposure, selection and omitted training-fit uncertainty remain. |
| Writing | 20% | Replaces a generic introduction and repeated abstract advice with a specific football question and a three-part worked conversation. Reduces audit detail while preserving necessary corrections. | External cold-read feedback remains unavailable until arranged. |
| Visualization | 20% | Preserves six verified figures and one generated table; explains the illustrated receiver pair and distinguishes relative plot gains from absolute table errors. Improves preview spacing and mobile table scrolling. | Actual Kaggle Writeup image upload and editor rendering are unverified. |

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
| Reproduction | `kaggle_execution.json`: public notebook 144208320/version 4; clean raw execution version 3; 402 checks, 25 scores, 12 tests pass. |

## Actual open work

Numerical/asset checks are recorded in `writeup_verification.json`. The six full-resolution
figures and the published notebook match their preceding verified hashes; frozen prediction
source/protocol hashes remain unchanged. Counts and headline values were checked against the reports.

- Owner review of the revised preview, followed by any corrections it identifies.
- Optional external football/statistical cold reads; a brief is prepared in `writeup/reviewer_brief.md`.
- Competition Writeup draft creation, image upload, notebook attachment and actual editor preview.
  The installed SDK offers read-only Hackathon/Writeup methods and this session has no browser
  editing tool, so no Kaggle Writeup draft was created.
- Owner confirmation of University eligibility, presented terms and final Submit. The public
  notebook is published; it is not the final competition Writeup submission.
