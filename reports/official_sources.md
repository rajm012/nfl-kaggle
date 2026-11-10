# Official source and field checks — 2026-11-10

Retrieved read-only through the authenticated official Kaggle API: competition metadata,
published competition pages and hackathon tracks. No rules acceptance or team change occurred.
Page hashes and concise rule excerpts: `official_source_snapshot.json`; exact track response:
`official_tracks.json`. These are source checks, not owner eligibility verification.

## Competition requirements

- [Submission requirements](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/overview/submission-requirements):
  no more than 2,000 words, fewer than ten figures/tables. Tracking must be used.
- [Evaluation](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/overview/evaluation):
  explicit Combine-to-regular-season-performance link, readable writeup with visuals, attached
  **Public Kaggle Notebook**. Football 30%, data science 30%, writeup 20%, visualization 20%.
- [Timeline](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/overview/timeline):
  Jan 6, 2027, 11:59 PM UTC; anticipated results Jan 26, subject to change.
- [Rules](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/rules): one submission per
  hackathon team, maximum five members. University pool $45,000: three $10,000 finalists and
  three $5,000 runners-up. Another $10,000 grand prize is reserved for invited finalists.
- Official track ID **7289**, University Track: “Open only to groups or individuals composed
  entirely of undergraduate students. Verification may be required to prove eligibility.”
  This matches the owner's recorded undergraduate status; the owner must select/confirm the
  track and supply any required evidence. Do not enter the Grand Prize track directly.
- Data CC BY-NC 4.0. Public competition code must use an OSI-approved license allowing commercial
  code use. Prepared code uses MIT; this does not change the data license. Public notebook
  output removes raw input links and intermediate row-level Parquets.

## Field interpretation

Source: [official data dictionary](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/data),
API page `data-description`.

| Field | Official definition | Interpretation used |
|---|---|---|
| `separation_at_pass_forward` | Distance in yards to the nearest defender at the moment the ball is thrown forward | Event-time separation; not necessarily receiver-break separation |
| `cushion` | Pre-snap distance in yards between receiver and primary coverage defender | Supplied pre-snap covariate; no opponent geometry inferred |
| `pressure_allowed` | True when OL allowed a QB hurry, hit or sack | Supplied binary outcome |
| `peak_pressure_probability_allowed` | Peak estimated pressure probability allowed by OL | Supplied model-derived outcome, in proportion units |
| `player_get_off` | Seconds from snap until defensive rusher moves forward across LOS | LOS-crossing time; not direct movement-onset latency |
| `time_to_pressure` | Seconds from snap until defender generated pressure on QB | Historical operational pressure flag: recorded time present on eligible rows |
| `dropback_duration` | Seconds from snap to pass release, sack or pressure | Realised NFL context; conditional retrospective prediction |

The dictionary does not exhaustively define every null's cause. Presence of `time_to_pressure`
is retained as the recorded operational proxy, not silently equated to an independently
verified pressure classification. Get-off need not equal first movement. Unavailable opponent
tracks prevent independently validating defender distances. Supplied game counts/season scope
differ from the dictionary's prose; source CSV audits, rather than prose, define the actual data.

## Resolved internal review issues

Route labels and event-time separation support the narrow wording in the writeup. TURN depends
on speed and curvature, so no intrinsic-agility or causal-training conclusion is made. Study 3
remains stopped at its frozen gate. All primary, subset and adverse results remain available;
no pristine-holdout, equivalence or automatic prospect-ranking claim.

Final account/track confirmation, terms and submission remain owner UI actions. Official
retrieval establishes the rules, not completion of those actions.
