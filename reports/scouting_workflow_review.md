# Step 4 — A concrete receiver scouting conversation

Prepared **2026-11-11** using the receiver story, movement explanation and uncertainty review. Revised worked-example,
Figure 6 card and notebook text: [scouting_workflow_draft.md](../writeup/scouting_workflow_draft.md).
Source values, hashes and checks: [scouting_workflow_evidence.json](scouting_workflow_evidence.json).
This is an internal proposal. No film assessment or scouting intervention has been performed.

## The takeaway in simple words

The two receivers ran almost the same 40 time but showed different movement profiles.
That gives a scout a question to investigate: **how does each receiver approach an out
cut, change direction and build speed afterward in comparable football situations?**
The current results do not establish better NFL performance prediction from TURN. The
output today is a focused review question and a record of missing evidence. Changing a
draft recommendation would require repeatable individual measurements and independently
supported performance evidence beyond conventional information.

## One proposed evaluation meeting

| Stage | What the evaluator would do | What can be recorded now |
|---|---|---|
| Movement observation | Inspect A's and B's recorded speed-out paths, speed and lateral acceleration alongside their across-drill profiles | Observed Combine differences, selection rule and measurement limits |
| Film question | Request comparable out routes and ask how each receiver enters, turns and reaccelerates | The question and the context needed to interpret it; film answers remain unassessed |
| NFL evidence | Read movement transfer separately from the separation-prediction comparison | Cohort movement association; uncertain added performance prediction |
| Evidence before a recommendation | Seek repeatable individual measurements and independent evidence of useful NFL performance information | Neither requirement is established for this pair by this study |
| Meeting output | Write the question, source, uncertainty and next evidence needed | A review note; no TURN-based grade change is justified by these results |

### 1. Start with the same observed pair

A ran **4.54 s** and B **4.52 s**. Across-drill TURN is **−1.782** versus **+2.533**
development-WR standard deviations. Both profiles average the same **13 drills**. The
displayed speed-out attempts have lateral-acceleration 90th percentiles of **6.620** and
**7.218 yd/s²**; their difference contributes **5.9% arithmetically** to the composite gap.
One attempt therefore does not explain the whole profile.

At the separately selected interior reference peaks, B moves faster (**5.879** versus
**5.433 yd/s**) along a slightly wider local curve (**0.233** versus **0.249 1/yd**
curvature). Higher lateral acceleration here does not demonstrate a tighter or more
efficient cut. Speed² × curvature describes the same position-derived motion; it is not
independent validation or a causal decomposition of ability. Fixed pre/post-peak windows
are descriptive windows, not validated break-entry or exit phases.

The pair deliberately maximizes the TURN contrast among 2023–24 WRs with observed 40
times within 0.03 s. Ties and attempts follow the saved deterministic rule. No NFL outcomes
selected the pair, but it is an extreme illustration rather than a representative sample.
Sources: [route_trace_selection.json](route_trace_selection.json),
[wr_movement_metrics.json](wr_movement_metrics.json),
[wr_trace_measurement_protocol.md](wr_trace_measurement_protocol.md).

### 2. Ask a football question with context

**Proposed request:** “Show comparable out routes for each receiver. How does he approach
the break, redirect and build speed afterward? What does the coverage and throw timing
let us conclude about that movement?”

A reviewer would define the eligible film set by route and context before viewing its
results, then retain all eligible clips and log exclusions. Include unsuccessful and
untargeted eligible routes as well as successful plays. The supplied OUT label does not
guarantee the same route depth, speed-out technique or assignment; film must establish
whether the situations are comparable. If film access or context is missing, record the
question as unanswered.

| Context to record when visible or documented | Why it matters to this question |
|---|---|
| Route direction, depth and assignment; alignment and motion | Different starts and route demands change the approach and intended break |
| Man/zone coverage, initial cushion and defender leverage/contact | Space may reflect defensive positioning, contact or a zone opening |
| Approach pace, visible slowing, path through the turn and acceleration afterward | Describes execution; exact speed/curvature requires calibrated tracking |
| Defender response and quarterback release relative to the break | Throw-time space may develop before or after the direction change |
| Camera visibility and missing information | Prevents a hidden defender, guessed assignment or obscured break from becoming a confident conclusion |

These are proposed review fields, not covariates controlled in a completed film study.
Do not force unlike routes into a comparison or infer missing opponents from the rookie-only
tracking. Record visible actions separately from interpretations and unresolved alternatives.
There is no new numeric film score, prospect ranking or required clip-count threshold.

### 3. Bring the existing NFL evidence to the meeting

**Measurement:** Development-WR cross-drill TURN agreement is SB **0.593 [0.373, 0.737]**
in **70 receivers**. That cohort result does not establish either player's individual
repeatability. The separate speed-out repeat estimate is **r=0.012 [−0.442, 0.492]**,
**17 pairs**, and remains highly uncertain.

**Transfer:** Combine-to-game turning correlation is **r=0.279 [0.107, 0.445]**, **98 WRs**,
for pooled preseason and regular-season movement. After measured size and 40 adjustment,
it is **r=0.278 [0.092, 0.450]**. This describes cohort movement carryover, not out-route
success or an individual separation advantage. Historical full-cohort normalization differs
from the development references and training-only prediction processing.

**Performance:** W1 has **23 evaluation WRs**, **3,701 plays**, and athlete-mean separation
RMSE **0.23572 yd** at baseline versus **0.23577 yd** with TURN. Gain is baseline minus
tracking error; its marginal interval is **[−0.00903, +0.01267] yd**. It permits worsening
and improvement. The existing ≥30-play check retains **17 WRs** and remains uncertain.
The endpoint is supplied distance to the nearest defender **at throw**, rather than
separation caused specifically by an out cut. W1 pools eligible routes; it does not answer
the proposed out-route film question.

The baseline includes conventional measurables, draft information and realised NFL context.
This is conditional retrospective prediction of athlete means, not a draft-time forecast
of a future role. Intervals hold trained models fixed and omit training-fit uncertainty;
earlier studies already used 2025 outcomes. Similar rounded errors do not establish equivalence.
Sources: [reliability.json](reliability.json), [transfer_audit.json](transfer_audit.json),
[validation.json](validation.json), [evaluation_protocol.md](evaluation_protocol.md),
[official_sources.md](official_sources.md), [uncertainty_interpretation.md](uncertainty_interpretation.md).

### 4. Write a review note without inventing observations

Use this blank structure if the owner later arranges film review. **No entries have been
filled from film in this work block.**

| Field | Entry to make during an actual review |
|---|---|
| Receiver and evidence source | Athlete ID; game/play or drill attempt; source and review date |
| Eligibility and comparability | Route/context rule; included/excluded and reason; limitations of matching |
| Direct observation | What is visible or measured, with its source |
| Interpretation | Possible explanation, separated from the observation |
| Competing explanation or uncertainty | Coverage, throw timing, route assignment, visibility or measurement noise |
| Contradictory clips | Retain observations that challenge the initial explanation |
| Next evidence needed | Unanswered question and appropriate measurement/review source |
| Recommendation implication | What the evidence supports; the present study supplies no TURN-based upgrade |

If differences vary with approach pace or coverage, record that dependence. If a similar
pattern recurs, record it as an observation that needs measurement validation. If the
clips disagree or are incomparable, retain the uncertainty. None of those outcomes alone
establishes incremental NFL prediction or a benefit from training TURN.

### 5. Evidence needed before TURN changes a recommendation

An individual movement claim needs repeated, comparably executed measurements with
documented measurement error and stability. The existing cross-drill coefficient and
single illustrated attempts do not supply that evidence for A or B.

A performance claim needs independent, relevant regular-season evidence that movement adds
useful information beyond the conventional evaluation, with football context, player
support and uncertainty addressed. A future study would define its decision target and
evaluation rules before observing outcomes. For a draft-time tool, inputs must be available
at draft time; the present realised-context comparison cannot certify that use.

Claiming the workflow improves scouting decisions would additionally require testing its
use with evaluators and an independently judged decision outcome. No such test exists here.
These are evidence requirements for future work, not a new protocol or authorization to
fit models. The failed Study 3 measurement gate remains closed.

## Final narrative claims and sources for the November 20 checkpoint

This is the **assistant's proposed final claim set, recorded November 11**. It is ready
for the scheduled November 20 owner checkpoint; owner readability feedback and final
review are pending. No new hypothesis family is introduced by these proposals.

| ID | Claim to retain | Source and boundary |
|---|---|---|
| C1 | Similar 40 times can accompany differing measured TURN profiles | Pair selection and movement metrics; deliberately extreme, outcome-independent illustration |
| C2 | TURN depends on speed and curvature; the single attempt is distinct from the multi-drill profile | Written trace protocol, metrics and kinematics; no efficiency or causal-talent conclusion |
| C3 | Cohort cross-drill agreement does not certify individual repeatability | Reliability JSON: n=70 development SB; uncertain n=17 speed-out repeats |
| C4 | WR movement carries modestly into pooled PRE+REG movement, including after size/40 adjustment | Corrected transfer rows; descriptive, full-cohort normalization, not added performance prediction |
| C5 | W1 does not establish added separation prediction | Validation W1 and ≥30-play rows; athlete-mean error, conditional interval, supplied throw-time endpoint |
| C6 | None of all nine primary marginal intervals supports improvement; all original-family intervals include zero | Validation primary rows and evaluation table; three positive and six negative point gains |
| C7 | Retain adverse and selected secondary results | D1 nominal deterioration, F2 adverse ≥30-play nominal result, F1_cone positive n=9 and W2_cone adverse n=7; all 16 secondaries in the uncertainty report |
| C8 | Historical associations and prediction comparisons are separate | Model audit: 0/9 two-sided Holm-significant original associations and separate binary sensitivity 0/3 |
| C9 | Route-family primary stopped at the frozen measurement gate | Study 3 adjusted SB 0.296 [−0.257, 0.606] below 0.40; no TURN interaction or Study 3 evaluation fitted |
| C10 | A targeted film question is a proposed use, with further evidence needed before a grade change | This workflow; no film review, decision-utility test, ranking or training intervention performed |
| C11 | Prior outcome exposure and conditional uncertainty limit generalization | Evaluation protocol, preregistration and validation; no pristine holdout, equivalence or draft-ready predictor claim |
| C12 | Reproduction evidence is version-specific | Saved Kaggle execution: clean version 3, public version 4; candidate drafts await Step 5 integration and verification |

The official brief calls for actionable Combine-to-regular-season insights. This workflow
answers what an evaluator could inspect next and why the current evidence stops short of
a scouting upgrade. It remains a proposal whose usefulness has not been demonstrated.
Official context: [official_sources.md](official_sources.md) and the unchanged November 11
[competition recheck](competition_recheck_2026-11-11.json).

## Integration handoff

The draft supplies replacement worked-example text, Figure 6 title/three fields/action/
caption, and concise notebook wording. Replace “Observe repeatable movement” with explicit
cohort-agreement wording. Keep the original card/figure, manuscript, notebook and packet
as their tested versions until Step 5. Use six main figures and one table; the internal
tables here are not extra submission visuals. Step 5 will reconcile this copy with the
Step 1 opening, Step 2 movement candidate and Step 3 results within the word limit.
