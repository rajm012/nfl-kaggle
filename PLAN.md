# NFL Big Data Bowl 2027 — Plan for the next work

Updated **2026-11-11**, after the owner accepted the five priorities discussed following
the official Kaggle brief review. This is the active work plan. The previous plan is
preserved in [plan_before_wr_focus_2026-11-11.md](reports/plan_before_wr_focus_2026-11-11.md);
the original strategy remains in [plan_2026-10-08.md](reports/plan_2026-10-08.md).
Existing preregistrations, fitted models and stopping decisions remain in force.

## 1. Goal and competition requirements

Make the entry easier to understand and more useful to a football evaluator by centering
one concrete receiver question:

**Two receivers have similar sprint times but move differently. What does their turning
profile reveal, and what evidence would justify using that difference in scouting?**

Receiver turning is the central worked example. All nine primary comparisons remain
reported, with line findings providing supporting context. Narrative focus does not select
a new primary hypothesis from observed results.

The submission remains a **scouting evidence map**: can we measure the movement consistently,
does it carry into games, and does it improve regular-season performance prediction?
Current manuscript title: **“Beyond the Stopwatch: When Should Combine Tracking Change a
Scouting Decision?”** Refine wording only if it better describes the supported findings.

| Requirement | Current target |
|---|---|
| Competition | [NFL Big Data Bowl 2027](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027) |
| Track | University, ID 7289; every member must be an undergraduate; owner confirms eligibility |
| Judging | Football 30%, data science 30%, writeup 20%, visualization 20% |
| Required connection | Explicit Combine sensor-tracking link to regular-season NFL performance |
| Submission | At most 2,000 words, fewer than ten combined figures/tables, attached public Kaggle notebook |
| Visual target | Six figures and one table; improve existing assets before adding more |
| Claim lock | **November 20, 2026** |
| Internal submission | **December 28, 2026** |
| Hard deadline | **January 6, 2027, 23:59 UTC** |
| Incremental cash budget | **$0** |

The official description encourages a narrow movement aspect, position group or drill.
It emphasizes practical, novel insight; positive prediction improvement is not stated as
a requirement. All nine official page content hashes were unchanged in the November 11
recheck. Sources: [official_sources.md](reports/official_sources.md) and
[competition_recheck_2026-11-11.json](reports/competition_recheck_2026-11-11.json).
The $100,000 total pool includes a $45,000 University pool with three $10,000 finalists
and three $5,000 runners-up. Judging scores are not award probabilities.

## 2. Starting point: completed work and remaining gap

| Area | Verified starting state |
|---|---|
| Data and audits | Nine CSVs; 510 athletes, 22,654,290 game frames, 314,197 player-play rows; key/join/model audits complete |
| Historical associations | 0/9 two-sided Holm-significant primary associations; 0/3 player-clustered binary sensitivities |
| Cohort prediction | All 25 frozen pairs scored; none of nine primary marginal intervals supports improvement; all original-family simultaneous intervals include zero |
| WR movement | Development cross-drill TURN consistency 0.593 [0.373, 0.737], 70 WRs; descriptive game-movement transfer r=0.279 [0.107, 0.445], 98 WRs |
| DL movement | Burst transfer r=0.443, falling to 0.203 after weight adjustment; movement transfer is separate from added performance prediction |
| Study 3 | Adjusted route-family consistency 0.296 below frozen 0.40 gate; primary TURN interaction stopped without fitting or Study 3 evaluation |
| Reproduction | Clean raw-input local and Kaggle runs completed; 402 numeric checks, all 25 scores and 12 invariant tests pass |
| Notebook | Public version 4, ID 144208320; clean Kaggle execution version 3; API source/output verification complete |
| Materials | 1,926-word manuscript, six figures, one table, standalone previews and upload ZIP prepared |
| Submission | Owner browser rendering, Writeup upload/attachment, eligibility/terms, Submit and confirmation remain |

The strongest existing contribution is careful separation of movement information from
performance claims. The main gap is practical usefulness: the film-review aid is proposed
and has not been evaluated in actual scouting decisions. The tasks below improve that
contribution without claiming to have discovered a proven scouting advantage.

Current evidence: [submission_checklist.md](reports/submission_checklist.md),
[submission_handoff.md](reports/submission_handoff.md) and
[kaggle_execution.json](reports/kaggle_execution.json). Older next-stage paragraphs in
analysis reports are historical; they do not reopen completed work.

## 3. Work in order

### Step 1 — Make receiver turning the central story

**Target: November 12–14. Next task to start.**

Review the manuscript and notebook against the receiver question in section 1. Use the
already selected similar-stopwatch pair: 4.54 versus 4.52 seconds, with contrasting TURN
profiles. Selection remains based on Combine exposures, independent of NFL outcomes.
Map each proposed claim to its source and limitation. Keep the full nine-comparison table
and failed route gate visible; explain line results as supporting context.

**Output:** `reports/wr_story_review.md`, containing a revised outline, claim/source map,
and proposed changes to the opening, figure explanations and notebook. Prepare reviewable
wording before replacing the existing submission materials.

**Done when:** the question, actual result and proposed football use are clear in the first
minute of reading; all nine primary results are accounted for; the receiver focus does not
imply a new selected primary analysis.

### Step 2 — Explain what the movement difference means

**Target: November 14–16; builds on Step 1.**

Inspect existing receiver traces, feature definitions and size/speed-adjusted transfer
results. Explain how entry speed, path shape and acceleration contribute to the observed
TURN difference. High lateral acceleration must not automatically be described as efficient
cutting or intrinsic agility. One illustrated attempt does not by itself explain a profile
aggregated across drills.

Start with existing quantities and reusable kinematics. If extra descriptive trace
quantities are necessary, write their definition, segment rule, units, smoothing and quality
checks in `reports/wr_trace_measurement_protocol.md` before computing them. Apply the same
rule to the existing pair. They remain descriptive illustrations, with no new trait–outcome
tests, prospect rankings or outcome-based example selection. If a quantity cannot be measured
reliably, explain the limitation rather than inventing precision.

**Output:** `reports/wr_movement_explanation.md`, reproducible annotations for the existing
route-trace figure, and the descriptive measurement protocol if needed. Improve the existing
figure rather than expanding the main visual count.

**Done when:** readers understand what TURN captures, which speed/body-size effects are
addressed, and what remains unresolved. Cohort cross-drill consistency is not presented as
either example player's individual or single-route repeatability.

### Step 3 — Explain where the NFL evidence ends

**Target: November 16–18; uses the existing frozen results.**

Translate the nine prediction errors and gain intervals into yards, seconds or proportion
units. Use WR turning as the worked example: baseline separation RMSE 0.23572 yards versus
0.23577 with tracking, gain interval [−0.00903, 0.01267], 23 evaluation receivers. Distinguish
the point result, the reported interval and the limitations of that interval.

Explain athlete support, exposure noise, prior 2025 outcome exposure and uncertainty
conditional on training. Use already specified sample/season/cone sensitivities and
size/speed-adjusted transfer results; retain favourable and adverse findings. Do not diagnose
inadequate power solely from nonsignificance or introduce a post-results threshold to claim
equivalence or practical usefulness.

**Output:** `reports/uncertainty_interpretation.md`, covering all nine primary comparisons,
source references and candidate plain-language writeup/figure wording.

**Done when:** every performance claim traces to existing results; readers distinguish
movement transfer from added prediction and lack of supported improvement from proof of no
useful effect. Selected cone findings remain secondary.

### Step 4 — Make the proposed scouting action concrete

**Target: November 18–20; incorporates Steps 1–3.**

Build one receiver-evaluation conversation with a movement observation, a specific film
question, current NFL evidence and the evidence gap before a recommendation could change.
For example, review entry speed, break shape and reacceleration on comparable out routes,
interpreting coverage, cushion, motion and throw timing. This is a proposed workflow: no
film assessment or scouting intervention has been performed.

Revise the evidence card and worked example to identify the proposed action clearly.
Retain separate measurement, transfer and performance fields. Do not claim an automatic
draft upgrade, individual change threshold or benefit from training TURN.

**Output:** `reports/scouting_workflow_review.md`, revised example/card text and owner
readability feedback. External football/statistical feedback is optional if available.

**Done when:** readers can say what to inspect next and what evidence is missing before
acting on the draft board. Record final claims and sources by **November 20**; no new
hypothesis families afterward.

### Step 5 — Integrate, verify and submit

**Target: November 21–December 28, with the existing January buffer.**

Integrate the reviewed explanation into the manuscript, figures and notebook. Preserve
all primary, secondary and adverse results in the reproducible record. Keep six main figures
and one table; count intended editor fields conservatively and remain under the limits.

Regenerate affected artifacts and check source/asset hashes, numeric claims, captions,
sample counts, previews and ZIP contents. If notebook source or its embedded bundle changes,
rebuild with `src.build_submission_notebook`, complete a clean raw-input execution and verify
the corresponding Kaggle version before updating publication evidence. A saved execution
record proves its tested version; it does not certify later changed code. For manuscript-only
changes, regenerate/check the affected packet and previews without repeating unchanged fits.

Owner checks public browser access and actual Kaggle Writeup rendering, uploads images and
the manuscript/table, attaches the exact notebook, confirms University eligibility and
presented terms, and performs Submit. Save the Writeup URL, confirmation and final artifact/
notebook versions. Update [submission_handoff.md](reports/submission_handoff.md) as materials
change and follow its UI instructions.

**Done when:** final materials agree and render on Kaggle, the attachment works, and owner
submission confirmation is saved by **December 28**. Keep December 29–January 6 for genuine
fixes and submission issues.

## 4. Work tracker and responsibility

All five improvement steps are pending; the starting artifacts in section 2 are complete.
Start Step 1 in the next work block and update this table as outputs are produced.

| Step | Dates | Lead | Status |
|---|---|---|---|
| 1. Receiver story and claim map | Nov 12–14 | Assistant; owner reviews clarity | Pending — next |
| 2. Movement explanation | Nov 14–16 | Assistant; owner checks code/figures | Pending |
| 3. Prediction uncertainty explanation | Nov 16–18 | Assistant; owner reviews plain language | Pending |
| 4. Scouting workflow and claim lock | Nov 18–20 | Assistant draft; owner design/writeup review | Pending |
| 5. Final integration and submission | Nov 21–Dec 28 | Assistant prepares/verifies; owner UI/Submit | Pending |

Owner handles Python/notebook checks and design/writeup review; assistant leads football
interpretation and statistical explanation. These are internal reviews, not independent
expert validation. External reviewers are unavailable unless the owner arranges them.

## 5. Scientific and execution boundaries

- Preserve frozen sources/protocols and prediction samples. Do not tune models after
  evaluation, fit the stopped Study 3 primary interaction, weaken its gate, or select
  favourable subsets for a headline. Genuine error corrections must be documented separately.
- Keep [prereg.md](reports/prereg.md), [study3_protocol.md](reports/study3_protocol.md) and
  [evaluation_protocol.md](reports/evaluation_protocol.md) as the scientific record. This plan
  covers explanation and bounded descriptive measurement, not a new outcome study.
- Preserve 2023–24 training-only processing and disclosed prior 2025 exposure. No pristine
  holdout, causal-training, universal-ranking or unsupported equivalence claims.
- Game tracking contains only rookie-cohort players. Opponent/ball geometry and independent
  defender-distance validation are unavailable. Event-time separation is not separation
  caused specifically by the break; get-off is LOS-crossing time.
- Use `.venv/bin/python`, existing Parquets and bounded local threads. Never load all game
  tracking into pandas. No extra hardware or paid services are needed for these priorities.
- Owner chose local execution after remote SSH trouble. Professor-provided RTX 5080 access
  remains optional and unverified; it is not a required milestone. Additional compute does
  not increase independent-player support.
- Raw data stay unedited in `data/raw/`, excluded from Git and non-Kaggle redistribution.
  Data are CC BY-NC 4.0; code is MIT. Never expose credentials or push Git without authorization.
- Check changed numerical/kinematic behavior with meaningful invariants; reuse the existing
  12 tests as appropriate. Documentation-only blocks need consistency/link/diff checks, not
  model runs. Update [submission_checklist.md](reports/submission_checklist.md) as evidence is
  produced; do not mark planned work complete prematurely.
- End each block with a dated `STATUS.md` entry and durable `CLAUDE.md` updates. Resume from
  completed artifacts and the next pending step.

If time tightens, drop optional new descriptive quantities, animation and outside reviews
first. Preserve honest claims, readable football explanation, reproduction and submission.
