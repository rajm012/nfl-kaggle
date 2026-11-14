# Step 3 — What the performance results allow us to conclude

Completed **2026-11-11**. Interpretation of existing frozen
results, not a new analysis specification. Evidence, unit conversions and checks are in
[uncertainty_evidence.json](uncertainty_evidence.json). Proposed results wording is in
[uncertainty_results_draft.md](../writeup/uncertainty_results_draft.md).

This is an internal explanation with several reference tables. It is not an additional
section or set of visuals to upload unchanged into the limited-word competition Writeup.
The tested manuscript, notebook, figures and packet remain their existing versions.

## 1. The answer in simple words

Some Combine movement differences appear again in NFL game movement. However, adding our
tracking measurements to conventional information did not establish better performance
prediction in any of the nine primary comparisons.

That answers a specific question about these traits, baselines, samples and scoring rules.
It does not establish that all tracking is useless or that every real improvement must be
zero. Several reported intervals allow both improvement and worsening. Small independent
player samples, noisy athlete means and omitted training-fit uncertainty limit the answer;
they do not prove that a useful effect is hiding in the data.

Three primary point gains are positive and six negative. None has a marginal interval
entirely above zero. One, DL burst/get-off, has a nominal interval entirely below zero;
its original-family simultaneous interval includes zero. Keep that adverse result visible.

## 2. What exactly was predicted?

The baseline includes conventional measurables, draft information and the supplied NFL
context for each position. First-step baselines also include the 10-yard split. Tracking
models add the prescribed feature on the same rows. Develop on 2023–24 rookie REG seasons,
evaluate 2025 rookie REG seasons, with fixed predictions and no evaluation-player effects.

Within each evaluation athlete, outcomes and predictions are averaged over that athlete's
realised NFL plays. RMSE is calculated across those athlete mean errors with equal athlete
weight. A player with two plays and one with hundreds each contribute one mean error.
Many plays can make an athlete's mean more precise; they do not create more independent
athletes. This score is not a per-route error, a ranking-success measure or draft-time
prediction of future routes, coverage or playing opportunity.

**Gain = baseline RMSE − tracking RMSE.** A positive gain means lower error. It does not
mean tracking improved the athlete's actual performance. A negative gain means higher
model prediction error, not that the movement trait physically harms players.

Binary pressure models use the recorded unclipped player-clustered linear-probability
fallback. Their errors are in proportion units; they are not calibrated risk forecasts.
Peak-pressure-probability is a supplied model-derived target, and recorded time-to-pressure
presence is an operational pressure proxy, with the disclosed eligibility filter.

Sources: [evaluation_protocol.md](evaluation_protocol.md), [evaluate.py](../src/evaluate.py),
[validation.json](validation.json), [official_sources.md](official_sources.md).

## 3. Receiver turning: the worked example

W1 evaluates **23 receivers** across **3,701 recorded plays**. Baseline RMSE is
**0.2357216 yards**, versus **0.2357681** with TURN. Both round to 0.24 yards. The point
gain is **−0.0000465 yards**: essentially unchanged at that rounded display precision,
with a slightly worse tracking point score. This rounding is not an equivalence test.

The marginal gain interval is **[−0.0090258, +0.0126710] yards**. Converting the same
interval to centimeters gives **[−0.825, +1.159] cm**: under the recorded conditional
bootstrap, it spans higher prediction error and lower prediction error. These are changes
in RMSE of athlete mean separation predictions, not changes in a receiver's separation
on an individual route. They are not bounds on that player's ability or on all possible
future applications of tracking.

The original six-comparison family interval is wider,
**[−0.0113788, +0.0174626] yards**. This comparison therefore has no supported prediction
gain under either reported interval. There is no justified automatic upgrade for the
higher-TURN illustrated profile, and no evidence here that the two illustrated players
must have equal football ability.

## 4. All nine primary results, in their original units

The table is generated from the saved results after checking the nine CSV rows against
the JSON. Intervals are marginal 95% paired evaluation-athlete bootstrap intervals,
conditional on the fitted training models.

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

Plain-language readings:

| ID | What the result says |
|---|---|
| W1 | Nearly identical point errors for separation; interval allows both improvement and worsening. No established added prediction value |
| W2 | Slightly worse separation point score; uncertainty crosses zero. No established burst-based improvement |
| O1 | Slightly better pressure-allowed point score; uncertainty crosses zero. No validated OL upgrade |
| O2 | Worse pressure-allowed point score; uncertainty crosses zero. Neither benefit nor general harm established |
| D1 | Worse get-off point score and adverse nominal interval. Family and ≥30-play checks include zero; do not turn this into a universal claim that burst is harmful |
| D2 | Better recorded-pressure-proxy point score; interval crosses zero. A positive point estimate is not validated pressure prediction |
| F1 | Better first-step/get-off point score; interval crosses zero. The positive cone subset cannot replace this uncertain primary |
| F2 | Almost unchanged, slightly worse peak-pressure point score; interval crosses zero. No established first-step gain |
| F3 | Almost unchanged, slightly worse separation point score; interval crosses zero. No established receiver first-step gain |

Every original-family simultaneous interval includes zero. Historical coefficient tests
used two-sided Holm correction within their six/three families. Prediction intervals use
Bonferroni-adjusted bootstrap percentiles within the six/three prediction families. These
are different calculations; do not call prediction intervals Holm-adjusted coefficient tests.

### The same prediction changes in familiar units

Conversions are exactly **1 yard = 91.44 cm**, **1 second = 1,000 ms**, and **1 proportion
unit = 100 percentage points**. They change the display, not the analysis or conclusion.

| ID | Display unit | Baseline RMSE | + Tracking RMSE | Gain [95% interval] |
|---|---|---:|---:|---|
| W1 | cm | 21.554 | 21.559 | -0.004 [-0.825, 1.159] |
| W2 | cm | 21.554 | 21.627 | -0.072 [-0.586, 0.380] |
| O1 | percentage points | 9.511 | 9.446 | +0.065 [-0.114, 0.171] |
| O2 | percentage points | 9.511 | 9.800 | -0.290 [-0.728, 0.382] |
| D1 | ms | 75.828 | 79.809 | -3.982 [-7.046, -0.486] |
| D2 | percentage points | 4.370 | 4.255 | +0.115 [-0.008, 0.231] |
| F1 | ms | 92.806 | 92.158 | +0.648 [-0.864, 1.954] |
| F2 | percentage points | 9.364 | 9.373 | -0.009 [-0.181, 0.066] |
| F3 | cm | 19.252 | 19.259 | -0.008 [-0.713, 0.800] |

For pressure targets, a 9.51-percentage-point RMSE is the size of prediction error on
athlete mean pressure fractions, not a predicted 9.51% event probability. A reduction in
that error is not a reduction in the player's actual pressure rate. Millisecond errors
similarly describe prediction of athlete mean LOS-crossing times, not measured reaction
latency or a coaching improvement.

## 5. What the intervals include and leave out

The recorded procedure resamples evaluation athletes as paired baseline/tracking errors
10,000 times. It measures how the error comparison varies with that evaluation sample,
**holding the fitted training models fixed**. The interval is not a statement that there
is a 95% probability the trait is useful or that a prospect will succeed.

Important boundaries are:

- Training-fit uncertainty is omitted: training coefficients, preprocessing and sample
  selection are not refitted within these intervals. Do not describe them as full uncertainty
  for a future prospect's forecast. No new training-bootstrap refits were performed here.
- Earlier studies already used 2025 outcomes. The choices were frozen for this cohort
  evaluation, but that history prevents an untouched-holdout claim.
- Prediction conditions on realised NFL context. The 2025 calendar level uses the latest
  trained intercept (2024); that persistence assumption and unknown-context encoding are fixed.
- Primary samples contain 20–37 athletes. Some have few plays, and selection into playing
  time or recorded outcomes can limit generalization. Small samples do not by themselves
  prove that the true gain is absent or present.
- Numerical boundary warnings and recorded optimizer retries remain part of the development
  diagnostics. Passing reproduction checks verifies the computation, not every model assumption.
- The reported simultaneous intervals account for the original prediction families; they
  do not convert a selected secondary/subset finding into an independently validated discovery.

No new utility threshold was introduced. The older route-interaction planning band of
0.10 yard per SD concerns a different, stopped coefficient question; it is not an RMSE
equivalence band. Neither a small point estimate nor an interval that crosses zero proves
that tracking gains are negligible for football decisions.

## 6. Sample support and the prespecified ≥30-play sensitivity

Primary exposure counts and the already specified evaluation-only ≥30-play restriction:

| ID | Primary athletes | Plays per athlete: min / median / max | ≥30-play athletes | Restricted gain [95% interval], original unit |
|---|---:|---|---:|---|
| W1 | 23 | 2 / 162 / 401 | 17 | -0.00092 [-0.01094, 0.00894] |
| W2 | 23 | 2 / 162 / 401 | 17 | -0.00251 [-0.00684, 0.00286] |
| O1 | 28 | 1 / 263.5 / 632 | 23 | +0.00062 [-0.00072, 0.00183] |
| O2 | 28 | 1 / 263.5 / 632 | 23 | -0.00386 [-0.01141, 0.00313] |
| D1 | 37 | 7 / 119 / 415 | 29 | -0.00263 [-0.00742, 0.00127] |
| D2 | 37 | 5 / 111 / 389 | 29 | +0.00091 [-0.00046, 0.00249] |
| F1 | 23 | 7 / 71 / 344 | 18 | -0.00015 [-0.00169, 0.00170] |
| F2 | 22 | 1 / 248 / 617 | 18 | -0.00179 [-0.00317, -0.00028] |
| F3 | 20 | 13 / 176 / 401 | 16 | -0.00128 [-0.00901, 0.00859] |

The retained athletes are scored with the same frozen fits; this is not a refit that chooses
better coefficients. W1 drops from 23 to 17 receivers, with gain **−0.0009245 yards**,
marginal interval **[−0.0109361, +0.0089366]**. Removing sparse observations does not reveal
a supported receiver gain in this check. It also removes athletes, so it does not resolve
selection or training uncertainty.

D1's ≥30-play gain is **−0.0026316 seconds**, with interval
**[−0.0074162, +0.0012711]**, 29 athletes. F2's ≥30-play sensitivity has nominal deterioration
on 18 athletes; its family interval includes zero. Retain these adverse findings instead
of describing every sensitivity as nearly unchanged. All nine ≥30-play original-family
intervals include zero, and none has a supported marginal positive gain.

MAE is a recorded secondary score. W1 MAE improves from **0.1695908** to **0.1669505 yards**,
but its primary RMSE does not improve at the point estimate. MAE penalizes large errors less
than RMSE. No MAE-gain interval was recorded; do not switch the main criterion after seeing
this favourable point score or call it validated benefit.

## 7. Retain the favourable and adverse secondaries

All 16 secondary/cone comparisons remain in the record. Their intervals are marginal;
their displayed family size is one, so they should not be described as nine-cone-family
simultaneous intervals.

| ID | Family | Athletes | Gain [95% interval], original unit | Reading |
|---|---|---:|---|---|
| W1_joint | joint secondary | 23 | -0.00021 [-0.00857, 0.00870] yards | Interval spans improvement and worsening |
| O1_joint | joint secondary | 28 | -0.00179 [-0.00564, 0.00373] proportion | Interval spans improvement and worsening |
| D1_joint | joint secondary | 37 | -0.00514 [-0.01033, -0.00068] seconds | Adverse marginal interval; secondary |
| D2_joint | joint secondary | 37 | +0.00067 [-0.00117, 0.00243] proportion | Interval spans improvement and worsening |
| F1_no10 | no-10yd secondary | 23 | +0.00041 [-0.00058, 0.00122] seconds | Interval spans improvement and worsening |
| F2_no10 | no-10yd secondary | 22 | -0.00150 [-0.00330, -0.00014] proportion | Adverse marginal interval; secondary |
| F3_no10 | no-10yd secondary | 20 | +0.00064 [-0.00559, 0.00761] yards | Interval spans improvement and worsening |
| W1_cone | cone sensitivity | 7 | +0.03276 [-0.04748, 0.09115] yards | Interval spans improvement and worsening |
| W2_cone | cone sensitivity | 7 | -0.25493 [-0.39734, -0.12727] yards | Adverse marginal interval; secondary |
| O1_cone | cone sensitivity | 13 | -0.00047 [-0.00116, 0.00075] proportion | Interval spans improvement and worsening |
| O2_cone | cone sensitivity | 13 | -0.00286 [-0.00523, 0.00038] proportion | Interval spans improvement and worsening |
| D1_cone | cone sensitivity | 13 | -0.01668 [-0.04755, 0.01432] seconds | Interval spans improvement and worsening |
| D2_cone | cone sensitivity | 13 | -0.00032 [-0.00598, 0.00569] proportion | Interval spans improvement and worsening |
| F1_cone | cone sensitivity | 9 | +0.00755 [0.00443, 0.01080] seconds | Positive marginal interval; selected secondary |
| F2_cone | cone sensitivity | 12 | -0.00012 [-0.00140, 0.00040] proportion | Interval spans improvement and worsening |
| F3_cone | cone sensitivity | 6 | +0.10993 [-0.01557, 0.21656] yards | Interval spans improvement and worsening |

The DL first-step cone result (F1_cone) has gain **0.00754695 seconds**, or **7.547 ms**,
interval **[4.428, 10.802] ms**, on **nine athletes**. It is a positive result in a selected
small sample. Cone participation is not random, the interval conditions on training, and
the broader primary F1 interval includes zero. This is a secondary signal for future
verification, not a general DL ranking claim or justification to retune the primary.

For balance, W2_cone worsens separation prediction by **0.2549318 yards**, interval
**[−0.3973438, −0.1272694]**, seven athletes. D1_joint and F2_no10 also have adverse marginal
intervals. W1_cone and F3_cone have positive point gains but uncertain intervals, on seven
and six athletes respectively. No subset result is silently omitted or promoted to primary.

The historical all-REG cone association is a separate question. D2 has positive adjusted
TURN coefficient **0.01521 [0.00682, 0.02359]**, 37 athletes, while its rookie cone prediction
gain is **−0.0003186 [−0.0059792, +0.0056919]**, 13 athletes. An association interval is not
an RMSE-gain interval. F3's historical cone coefficient is negative,
**−0.08328 [−0.15586, −0.01069] yards per SD**, opposite the expected positive direction;
its six-athlete cone prediction remains uncertain. Sources:
[cone_sensitivity.json](cone_sensitivity.json) and [validation.json](validation.json).

## 8. Movement transfer is a separate piece of evidence

The recorded receiver movement correlation is **0.279 [0.107, 0.445]**, 98 athletes,
in pooled PRE+REG data. The size-plus-40-adjusted estimate is **0.278 [0.092, 0.450]**.
The saved REG-only sensitivity is **0.322 [0.122, 0.503]**, 74 athletes. These are descriptive
movement associations with their own normalizations/samples, not added-performance gains.

The DL raw burst correlation is **0.443**, falling to **0.203** after weight adjustment
in PRE+REG. REG-only, weight-adjusted transfer is **0.178 [−0.013, 0.377]**, 92 athletes.
Retaining the season sensitivity makes the scope of the movement claim clear. Neither
adjustment controls the entry speeds of the illustrated attempts or establishes causal
training usefulness. Source: [transfer_audit.json](transfer_audit.json).

The original historical families have **0/9 Holm-significant associations** and **0/3**
player-clustered binary sensitivities. The stopped route-family measurement gate has
adjusted SB **0.296 [−0.257, 0.606]**, below 0.40. That gate failure did not test the primary
TURN interaction and does not establish that all route-specific effects are zero.

## 9. Proposed figure/notebook explanations

For Figure 5: “All nine primary comparisons of prediction error. Positive gain means lower
equal-athlete RMSE. None has a marginal interval entirely above zero; DL burst/get-off has
nominal deterioration. Every original-family simultaneous interval includes zero.
Intervals resample evaluation athletes and hold training fits fixed.”

For Table 1: “Errors predict each athlete's mean outcome over realised NFL contexts;
they are not per-play errors or changes in actual performance. Units are yards, seconds
or outcome proportions. Gain is baseline minus tracking error.”

For the notebook receiver paragraph: “Both WR TURN point errors round to 0.24 yards.
The marginal gain range [−0.00903, +0.01267] yards permits improvement and worsening.
The ≥30-play check remains uncertain. Movement transfer and the proposed film question
do not establish an added separation-prediction benefit or an automatic draft upgrade.”

Use the [candidate results draft](../writeup/uncertainty_results_draft.md) as replacement
wording during later integration, rather than appending this internal report to the Writeup.
Keep all primary rows and the adverse/secondary findings in the notebook record.

## 10. Checks and handoff

All nine CSV rows agree with saved primary results. Equal-athlete RMSE and MAE were
recomputed from saved errors for all 25 comparisons; athlete counts, cohort disjointness
and development-before-evaluation order were checked. This did not refit models, recalculate
bootstrap intervals or tune thresholds. Unit conversions and preserved source/asset hashes
are recorded in `uncertainty_evidence.json`.

Step 3's explanation/source checks are complete. **Next: Step 4 — make the proposed scouting
action concrete**, using the receiver movement explanation and these performance limits.
The tested submission materials and frozen scientific protocols remain their existing versions.
