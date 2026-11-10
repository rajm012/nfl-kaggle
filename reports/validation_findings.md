# Validation decision — 2026-11-10

**Retain the scouting evidence-map narrative. No primary tracking addition has a
supported cohort prediction gain, and the route-family primary claim remains stopped.**

All nine original prediction comparisons and 16 prespecified secondary/cone comparisons
were evaluated after development preprocessing and coefficients were frozen. Primary
evaluation samples contain 20–37 distinct 2025 athletes, depending on outcome/exposure
availability. These are conditional predictions on the receivers'/linemen's realised NFL
contexts, not draft-time forecasts of future roles or rankings.

## What the primary prediction results support

- WR TURN adds essentially no point improvement in separation prediction: baseline
  RMSE 0.23572 yards versus 0.23577 with TURN; improvement −0.00005 yards, 95% interval
  [−0.00903, 0.01267], 23 evaluation receivers. WR BURST and first-step additions are
  also uncertain, with point improvements slightly negative.
- DL TURN has a small positive pressure-generation point gain (0.00115 proportion
  units), but its interval crosses zero [−0.00008, 0.00231], n=37. This does not validate
  a pressure-generation ranking claim.
- Adding DL agility-drill BURST worsens get-off prediction by about 0.00398 seconds
  (nominal gain interval [−0.00705, −0.00049], n=37). Its family-adjusted interval and
  ≥30-play sensitivity include zero. Report the deterioration without calling it a
  definitive general harm from the measurement.
- All nine primary family-adjusted intervals include zero. Three point gains are positive,
  six negative; no primary marginal 95% interval supports improvement. These statements
  describe uncertainty in improvement, not equivalence or proof every true effect is zero.

## Cone sensitivity: retain interesting exceptions without promoting them

- Historical all-REG cone-observed samples contain 23–43 athletes. On identical rows,
  DL TURN's pressure-generation coefficient remains positive after cone adjustment
  (0.01521 [0.00682,0.02359], n=37). Its cone-subset cohort prediction gain is slightly
  negative/uncertain (−0.00032 [−0.00598,0.00569], n=13). The association has not translated
  into validated incremental cohort prediction.
- The DL first-step cone-subset cohort comparison improves RMSE by 0.00755 seconds
  [0.00443,0.01080], but evaluates just **nine athletes**. This is one of nine cone
  sensitivities, conditional on the fitted training model and selected cone participation;
  its broader primary comparison is uncertain. Treat it as a secondary finding, not a
  general performance claim or a reason to reopen hypothesis selection.
- Historical WR first-step/cone association is negative (−0.08328 yards per SD
  [−0.15586,−0.01069], n=23), opposite the original expected positive direction. Its
  six-player cone cohort improvement interval crosses zero. Other cone comparisons
  generally remain uncertain, and WR BURST cone prediction deteriorates substantially.
- Cone availability differs by position/draft status and does not identify a random sample.
  No times were imputed. Tables retain all findings, not only favourable subset results.

## Practical claim and limitations

The defensible entry separates reasonably repeatable Combine movement, modest movement
transfer, and uncertain added performance prediction beyond draft slot/body size/stopwatch
and NFL context. These results justify calibrated evidence cards, not an automatic draft
upgrade, hidden-star ranking or causal training recommendation.

Prior 2025 outcome exposure prevents an untouched-holdout claim. Paired bootstrap intervals
condition on training models; they omit training-fit uncertainty. Small/player-sparse
targets, selection into NFL participation and cone testing, assumed persistence of the
latest trained calendar intercept, and numerical boundary fits limit certainty. The
prediction window is rookie-only; historical association sensitivities use all REG seasons.

Evidence: `validation.md`, `validation.json`, `cone_sensitivity.md`, `cone_sensitivity.json`,
`evaluation_development.json`, `evaluation_table.csv`, `figures/cohort_prediction.png`.
No new Study 3 interaction, model tuning after evaluation or new hypothesis family.

## Next stage

The requested cohort/cone validation block is complete. Next is submission production:
integrate raw-input rebuilding of these results into the public notebook, settle final
figure selection/evidence-card design, and draft the writeup. Current notebook execution
checks cover the earlier conventional measurement screen; full Kaggle reproduction is
still pending. Keep the November 20 final-claim checkpoint and December 14/28 deadlines.
