# Planning feasibility — 2026-11-09

Read-only support inspection for the revised submission strategy. No new trait–outcome
associations, outcome means or fitted models were computed.

## Competition metadata

Command: `.venv/bin/python -m kaggle competitions list -s nfl --csv`.
The row for `nfl-big-data-bowl-2027` lists deadline **2027-01-06 23:59:00**, reward
**100,000 Usd** (total competition pool), `userHasEntered=True`, and 543 teams at inspection.
Team count is a point-in-time listing, not a number of eligible University-track entries.
This confirms listing/deadline/entry, not track eligibility or individual award allocation.

Public GET requests to overview/rules returned HTTP 404. The original rules notes are retained
as working requirements; official UI verification is still required before publication.

## Combine WR repetition

PLAYER rows only; join `combine_results` for WR; count distinct `event_id` per player/drill.
Canonicalise `SPEED_OUT_LEFT` to `SPEED_OUT_ROUTE_LEFT`.

| Drill | Players | Attempts | Players with ≥2 attempts |
|---|---:|---:|---:|
| SLANT_ROUTE_LEFT | 107 | 110 | 3 |
| SPEED_OUT_ROUTE_LEFT | 107 | 124 | 17 |
| GO_ROUTE_RIGHT | 98 | 105 | 7 |

Coverage does not establish test–retest reliability. Do not build a slant-only talent score
based on three repeated athletes.

## NFL performance support

Join `player_play`, `games`, `combine_results`, and `players`; filter WR, REG,
`play_nullified_by_penalty == 'N'`, recorded `separation_at_pass_forward` and requested routes.
Count plays per athlete/route or family without examining their outcome values.

| Class | ≥10 SLANT and ≥10 OUT, all recorded seasons | ≥10 BREAK and ≥10 GO, all recorded seasons | ≥10 BREAK and ≥10 GO, rookie season |
|---|---:|---:|---:|
| 2023 | 23 | 29 | 25 |
| 2024 | 17 | 20 | 17 |
| 2025 | 7 | 16 | 16 |

BREAK means pooled SLANT/OUT; rookie season means `season == draft_year`. The planned contrast
has **42 development + 16 evaluation** athletes before final feature checks. This is support
for a bounded experiment, not a power estimate or evidence it will succeed.

The route-specific ≥10 rookie-season supports are: SLANT 17/14/9, OUT 20/15/11,
GO 26/20/17 for classes 2023/2024/2025. The restricted route-pair design would lose many
athletes relative to pooling the predeclared family.

NFL labels include SLANT/OUT/GO but no explicit CURL/COMEBACK/POST_CORNER categories.
The revised primary study uses generic TURN and recorded NFL route contexts; it does not
claim an exact Combine-drill↔NFL-route talent match.
