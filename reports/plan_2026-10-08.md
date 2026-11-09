# NFL Big Data Bowl 2027 — Game Plan

_Written 2026-10-08 (competition started 2026-10-06). Hard deadline: **2027-01-06 23:59 UTC**.
Our internal deadline: **2026-12-28** (9 days of buffer for illness, Kaggle outages, holidays)._

---

## 0. The competition in one screen

| Item | Detail |
|---|---|
| Type | **Analytics hackathon**, judged by humans (no leaderboard, no metric to optimise) |
| Theme | Link **10 Hz Combine tracking** to **future regular-season NFL performance**; find non-obvious, actionable signals |
| Deliverable | One Kaggle **Writeup** (≤ 2,000 words, **< 10** figures + tables) + an attached **public Kaggle notebook** |
| Hard gates (pass/fail) | (1) explicitly links Combine *tracking* to regular-season NFL performance; (2) readable markdown, embedded visuals, public notebook attached. A writeup that doesn't use tracking data is not scored. |
| Scoring | Football 30% · Data Science 30% · Writeup 20% · Data Viz 20% (each 0–10) |
| Judges | Analytics staff from NFL teams and tracking vendors |
| Prizes | Open track: 3 × $10k finalists + 3 × $5k runners-up. **University track (undergrads only): same $45k pool, separate.** Finalists present at the 2027 Combine for a $10k grand prize. |
| Submissions | **One** per team. Team size ≤ 5. |
| Data licence | CC BY-NC 4.0. Don't redistribute the raw data outside Kaggle. |

**Podium = top 6 of a track** (3 finalists + 3 runners-up). Typical BDB fields have hundreds of
serious submissions; the winners are almost always: *one sharp football question, one new metric,
airtight stats, and beautiful, self-explanatory visuals*. Not breadth. The host says so explicitly:
"focus on one small aspect of movement, a specific position group, or an individual drill."

---

## 1. What the data actually lets us do

| File | Rows | What it gives us |
|---|---|---|
| `players.csv` | 510 | position, draft year/round/pick (UDFA = null), college |
| `combine_results.csv` | 510 | measurables + stopwatch times + NGS athleticism/production scores |
| `combine_tracking.csv` | 463k frames, 6,310 drill attempts | x, y, s, a, dis, dir at 10 Hz for 40, 3-cone, shuttle and **position drills** (gauntlet, run-the-hoop, backpedal-and-transition, slot-strike routes, pass-pro mirror, OL pull…) |
| `player_play.csv` | 316k player-plays | NGS outcomes: **separation at throw, cushion, get-off, time-to-pressure, pressure allowed, peak pressure probability allowed, route run, EPA, coverage**… |
| `game_tracking_202{3,4,5}.csv` | 8.8M frames | 10 Hz in-game tracking (incl. **orientation `o`** and event tags) — **only for the 510 rookies**, not teammates/opponents |
| `player_career_successes.csv` | 510 | snaps, starts, All-Pro, Pro Bowl |

Cohort: WR 107 · TE 42 · DB 122 · OL 121 · DL 118 (draft classes 2023, 2024, 2025).

**Structural facts that shape the strategy:**

1. **n is small at the player level** (~100–120 per position group). Any "combine metric predicts career"
   claim lives or dies on statistical honesty. Most entrants will overfit or p-hack — that's our opening
   on the 30% Data Science score.
2. **Outcomes are play-level and plentiful** (316k player-plays). Modelling at the play level with player
   random effects gives far more power than correlating 100 career totals.
3. **Opportunity is confounded by draft capital.** High picks play more regardless of ability. Career
   totals (snaps, starts) are therefore partly *measuring the draft pick*, not the player. We must
   condition on draft position and use per-snap efficiency outcomes — and say so out loud (judges love this).
4. **We have the same player moving in both settings at 10 Hz.** This allows a
   *mechanism chain* most entries won't build:
   `Combine drill kinematics → the same movement signature in games → NFL outcome`.
   That middle link is what makes a finding believable and actionable rather than a correlation.
5. Classes have unequal follow-up (2023 class: 3 seasons; 2025: 1). Use that as a **natural holdout**:
   fit on 2023–24 classes, check the 2025 class out of sample.

---

## 2. The thesis (primary bet)

> **Update 2026-10-08 (after Combine EDA — see `reports/decisions.md`, `reports/eda.md`):** braking alone proved
> unreliable (≤ 0.38); *turning* (lateral g) and *burst* are the reliable traits (0.55–0.65 for WR/OL/DL), and
> they are largely independent of the 3-cone. The thesis below is therefore generalised to an
> **acceleration envelope (turning + burst)**; WR and OL/DL are front-runners, DB needs phase-specific features.
> The structure (Combine trait → same trait in games → outcome, beyond stopwatch + draft slot) is unchanged.

### "Brake to Break": deceleration quality is the hidden Combine signal

**Football claim:** Stopwatch drills (3-cone, shuttle) blend *acceleration*, *top speed* and *braking*
into one time. Tracking lets us separate them. Our hypothesis: **how fast a player kills speed
and re-accelerates out of a cut** — measured in the Combine's change-of-direction and position
drills — predicts NFL performance at the moments that require exactly that (route breaks for WRs,
backpedal-to-drive transitions for DBs), **beyond** what the 40, 3-cone, shuttle and draft slot
already tell you.

**Primary position groups:** WR + DB (229 players, mirrored skills, same events: the receiver's break
vs the defender's transition). TE added only if the WR result is strong.

**Metric (working name: *Brake-Burst Index*, BBI):** for each cut in a drill, from the speed/accel/dir
traces:
- peak deceleration (yd/s²) and *time from 90% speed to cut*,
- speed retained through the cut (min speed / entry speed),
- re-acceleration: time from cut to 80% of exit speed,
- path efficiency: actual path length vs ideal path around the cones.
Combined into one position-adjusted, interpretable number (z-scored components, weights from a
small hierarchical model, *not* a black box).

**The chain we'll show:**
1. *Combine BBI* — from 3-cone/shuttle + WR route drills / DB backpedal-transition drills.
2. *Game BBI* — the same quantity measured on the player's in-game route breaks / coverage
   transitions (detected from `dir` change + speed dip around `pass_forward`).
   → Shows the Combine trait **transfers** (test–retest across settings).
3. *Outcome* — WR: separation at throw, target share per route, YAC over expected.
   DB: opponents aren't in the tracking files, so outcome must come from `player_play` —
   candidates (confirmed in Week 1 EDA): separation / cushion fields if populated for defenders,
   completion & EPA on plays where they are the closest coverage defender, coverage assignment outcomes.
   → Play-level mixed model with controls: route type, coverage, down/distance, cushion, alignment,
   season, team, player random effect, draft pick.

**What a team does with it (Football score):** (a) draft: flag players whose BBI is far better/worse
than their 3-cone time suggests — "hidden talent / bust risk" lists; (b) development: BBI can be
computed weekly from practice GPS/tracking, so it becomes a **trainable KPI** with a target per
position. That answers the "week-to-week use" question directly.

### Backup thesis (decide by end of Week 2): "First Step" for the trenches
OL + DL (239 players). Combine first-step burst (accel in first 0.5 s of 40/10-yd split, lateral
burst in OL/DL drills like pass-pro mirror, pull, gauntlet-style) → in-game `player_get_off`,
time-to-pressure, pressure rate (DL) / pressure allowed, peak pressure probability allowed (OL).
Same chain structure. This becomes primary **only if** the WR/DB signal fails the go/no-go tests
below; otherwise it may feature as one figure showing the method generalises.

### Go / no-go rule (pre-registered, end of Week 3)
Primary thesis survives if BOTH:
- Combine→Game transfer correlation of the metric ≥ ~0.3 (players with enough in-game cuts), and
- adding the tracking metric to a model with {40, 3-cone, shuttle, size, draft pick} improves
  out-of-sample fit of the outcome model with a credible effect (posterior / CI excluding 0 or a
  clear cross-validated gain).
If not: switch to the backup. **A null result honestly reported ("the 3-cone already captures it")
is still a story, but a weaker podium story — we'll pivot rather than polish a null.**

---

## 3. Statistical design (the Data Science 30%)

- **Pre-declare features** in `reports/prereg.md` before looking at outcomes. Limits
  forking-paths; we cite it in the writeup as a credibility signal.
- **Play-level Bayesian / mixed models** (bambi/PyMC or statsmodels MixedLM): outcome ~ metric +
  traditional drill times + context + (1 | player) + (1 | team-season). Report effect sizes with
  intervals, not p-values only.
- **Incremental validity:** nested comparison vs a "stopwatch + draft slot" baseline. This is the
  single most important number in the writeup.
- **Selection / survivorship:** only players who play produce outcomes. Handle by (a) per-snap
  outcomes, (b) conditioning on draft pick, (c) a sensitivity check showing the result isn't driven
  by who got snaps.
- **Out-of-sample:** fit on 2023–24 classes, validate on 2025 class; plus leave-one-class-out.
- **Reliability:** attempt-to-attempt reliability of the metric within the Combine (ICC). A metric
  that isn't repeatable can't be a trait — judges from tracking vendors will check this.
- **Multiple comparisons:** one primary metric, one primary outcome per position; everything else
  labelled exploratory.

## 4. Visual plan (the Data Viz 20%) — max 9 figures/tables

1. Hero figure: animated or small-multiple trace of two players with the same 3-cone time but very
   different braking profiles (the "same stopwatch, different athlete" hook).
2. Metric anatomy: speed/accel curve through a cut, components annotated.
3. Combine → Game transfer scatter (with reliability band).
4. Effect plot: outcome vs BBI, with stopwatch-only baseline for comparison.
5. Incremental-value table (baseline vs +BBI, out-of-sample).
6. Player cards / leaderboard: top risers and fallers vs their 3-cone ranking (named players = football credibility).
7. Position-specific target bands ("development KPI" chart).
8. (Optional) trenches generalisation panel.
Colour-blind-safe palette, direct labels, no legends where avoidable, every chart readable alone.
Animation as a GIF in the writeup (counts as one figure).

## 5. Writeup plan (the Writeup 20%)

≈1,900 words. Structure: Hook (one player pair) → Why stopwatch times hide braking → Metric →
Does it transfer to games? → Does it predict performance beyond the stopwatch? → How a team uses it
(draft + development) → Limitations → Appendix link to notebook. Plain language first, maths in the
appendix. Final draft gets a "cold read" pass for a non-statistician NFL coach.

---

## 6. Timeline (13 weeks; illness-tolerant)

| Week | Dates | Deliverable | Needs you? |
|---|---|---|---|
| 0 | Oct 8–12 | Folder, env, plan (**this doc**); data download once token arrives | **Yes — 10 min (see §7)** |
| 1 | Oct 13–19 | Data loaded to parquet/duckdb; EDA report on drills, cut detection in combine traces; data-quirk log | No |
| 2 | Oct 20–26 | Combine metrics for WR/DB + OL/DL; reliability (ICC); choose primary thesis | Optional 5-min check-in |
| 3 | Oct 27–Nov 2 | In-game cut detection; Combine→Game transfer; **go/no-go** | Optional |
| 4–5 | Nov 3–16 | Outcome models, incremental validity, holdout, sensitivity checks | No |
| 6–7 | Nov 17–30 | All figures v1, hero animation, player cards | No |
| 8 | Dec 1–7 | Writeup draft v1 + Kaggle notebook (clean, runs top-to-bottom) | No |
| 9 | Dec 8–14 | Self-review against the rubric (I score it as a judge would), revise | Read draft (20 min) |
| 10 | Dec 15–21 | Polish, word/figure count check, notebook made public | No |
| 11 | Dec 22–28 | **Submit (you click)** — then only small edits | **Yes — 15 min** |
| 12 | Dec 29–Jan 6 | Buffer only | — |

Progress lives in `STATUS.md` (short, dated bullet log) so you can catch up in one minute whenever you check in.

---

## 7. What only you can do (≈ 30 minutes total over 3 months)

1. ✅ Done (token works). On Kaggle, open the competition page → **"Join Hackathon"** → accept the rules.
   (I must not accept legal terms on your behalf.)
2. ✅ Done — token at `~/.kaggle/access_token`. Kaggle → Settings → API → **"Create New Token"** → put the downloaded `kaggle.json` at
   `~/.kaggle/kaggle.json` (then `chmod 600 ~/.kaggle/kaggle.json`). With that I download the data and
   later push the public notebook myself.
3. ✅ Confirmed 2026-10-08: owner is an undergraduate (B.Tech Maths & Computing) → **University track**.
4. **Late December:** attach notebook + click **Submit** on the Writeup (Kaggle's writeup form is UI-only).

## 8. Risks and how we handle them

| Risk | Mitigation |
|---|---|
| Primary signal is weak | Pre-registered go/no-go in Week 3; trenches backup ready |
| 16 GB RAM (≈5 GB free) vs 2.2 GB of CSVs | Convert to parquet once; query with DuckDB/Polars lazily; never load all tracking into pandas |
| Kaggle notebook must reproduce | Build the public notebook in parallel from Week 6; keep heavy steps cached as a Kaggle dataset output |
| You're unavailable at submission time | Internal deadline Dec 28; 9-day buffer; everything ready so submission is a 2-click task |
| Overclaiming → judges dock Data Science | Intervals everywhere, limitations section, holdout class, reliability first |
| Data quirks (opt-outs, missing drills, ball frames) | Logged in `reports/data_quirks.md` in Week 1, handled explicitly |

## 9. Honest expectation

No one can guarantee a podium in a judged competition with hundreds of entrants and a subjective
rubric. What I can control: picking a sharp question, making the stats bulletproof, building
standout visuals, and submitting early. If you qualify for the University track, our odds improve
substantially.
