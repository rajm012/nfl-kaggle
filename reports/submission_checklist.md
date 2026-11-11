# Submission checklist — started 2026-11-09
All unchecked items are pending. This file records evidence of completion, not assumed progress.

## Research and reproducibility
- [x] Revised plan, study protocol and eligibility counts saved; old plan archived.
- [x] Competition listing/deadline/entry reconfirmed through Kaggle CLI.
- [x] Reported remote RTX 5080/CPU resource and ranked help requests added to the plan.
- [ ] Verify remote host resources/access window and benchmark a bounded CPU job against local outputs.
- [x] Work allocated: assistant football/statistical review; owner Python/design; external review optional.
- [x] Preserve historical numerical reports before corrected reruns (`reports/history/2026-11-09/`).
- [x] Initial key/reference/count/season audit including full game-frame keys; report saved.
- [x] Explain unmatched game-trait/player-play rows and final model-specific attrition (`join_attrition.*`, `model_audit.json`).
- [x] Reproduce selected TURN/other published reliability, adjusted transfer and descriptive conventional-control checks (`reliability.*`, `transfer_audit.*`, `model_audit.json`).
- [x] Correct/document binary uncertainty, player-level Study 2 scaling and test direction (`model_audit.*`).
- [x] Record Study 3 measurement screens before exposure–outcome associations (`study3_measurement.*`; gate FAILED, primary claim stopped).
- [x] Save training-only preprocessing and development coefficients before 2025 evaluation (`evaluation_development.json`, `evaluation_models/`; Nov 10).
- [x] Finish baseline/augmented cohort evaluation, intervals and original prediction/cone sensitivities (`validation.*`, `cone_sensitivity.*`; Nov 10).
- [x] Choose narrative by Nov 20; retain null/uncertain findings and prior-outcome disclosure (`validation_findings.md`; evidence-map decision retained Nov 10, final wording review still pending).
  - Nov 9: follow the evidence-map path after the frozen measurement gate failed; final claims
    still depend on completing required Studies 1–2 evaluation/sensitivity work.
  - Nov 10: required cohort/cone work complete; none of nine primary intervals supports a prediction gain. Secondary subset findings retained; keep Nov 20 final-claim review.
- [x] Create starter notebook and record dependencies; local CSV/Parquet execution verified.
- [x] Run full notebook from clean inputs; record duration/memory; reproduce every headline number (`full_notebook_execution.json`, `submission_verification.json`; 523.08 s, sampled largest stage RSS 1,183 MiB, 402 checks and 25 scores).

## Football, figures and writeup
- [x] Explicit Combine-tracking→REG performance link with conventional baseline (`writeup/writeup.md`).
- [x] Six self-contained figures and one table; unique-player n, units and intervals agree (`submission_packet.json`).
- [x] Evidence card separates measurement, transfer and incremental prediction confidence (`figures/scout_evidence_card.png`).
- [x] Draft hero examples selected without reference to desired NFL outcomes (`route_trace_selection.json`).
- [x] Actual findings and limitations replace provisional titles/claims (`writeup/writeup.md`).
- [x] Football and statistical review issues recorded and resolved (`submission_review.md`, `official_sources.md`; internal review only).
- [x] ≤2,000 words and fewer than ten combined figures/tables (1,926 conservative manuscript words; title/description/body also checked together; 6 figures + 1 table).

- [x] Judging-focused writeup revision and concrete receiver film-review example (`writeup_judging_review.md`; internal review, no new models).
- [x] Exact Kaggle editor fields, numbered images and upload guide prepared (`writeup/kaggle_upload.zip`).
- [x] Optional external cold-read brief prepared (`writeup/reviewer_brief.md`; reviewers not yet arranged).

## Publication and submission
- [x] Official rules, University eligibility requirements, award allocation and citations rechecked (`official_sources.md`, `official_tracks.json`; owner personal/track confirmation separate).
- [x] Publication authorized by request to complete remaining steps; owner confirmed `oppenheimer6th`. Concrete local and Kaggle artifact tested before publication.
- [x] Redesigned notebook republished and public source/saved outputs verified (`kaggle_execution.json`; notebook 144208320, public version 4, full raw execution version 3). Ten clean report outputs and six figures; longest code cell 1,502 characters. Owner deleted the earlier oversized-source version; historical proof is archived.
- [ ] Owner confirms public notebook browser access/rendering (direct anonymous HTTP returned 404 from this workspace despite API public flag).
- [ ] Writeup embeds render correctly and notebook attachment works.
- [ ] Owner completes required terms/UI actions and submits by Dec 28.
- [ ] Submission confirmation and final artifact versions saved.

## Accepted improvement plan — November 11

The completed checks above refer to the existing November 10 materials. The owner accepted
the next work in [PLAN.md](../PLAN.md); these improvements have not yet been performed.

- [x] Active plan updated with WR focus, five ordered steps, outputs, completion checks and deadlines; prior plan archived (`plan_before_wr_focus_2026-11-11.md`).
- [ ] Step 1: receiver story/claim map reviewed; all nine results retained (`wr_story_review.md`).
- [ ] Step 2: movement explanation and trace annotation reviewed; any new descriptive quantities defined and checked before use (`wr_movement_explanation.md`).
- [ ] Step 3: plain-language interpretation of all nine primary prediction comparisons completed (`uncertainty_interpretation.md`).
- [ ] Step 4: proposed scouting workflow reviewed and final claims locked by Nov 20 (`scouting_workflow_review.md`).
- [ ] Step 5: revised manuscript, figures, notebook and packet integrated and verified as applicable; actual owner Kaggle UI checks/submission completed.

Remote-host verification remains optional under the revised plan; its unchecked historical
item is not a prerequisite for these steps or submission. New artifact revisions require
their own relevant checks before earlier completion evidence can be cited for them.

Append dated verification notes and links beneath each item as it is completed.
