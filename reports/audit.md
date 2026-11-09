# Data audit

Generated UTC: 2026-11-09T10:29:57.884783+00:00

Counts, integrity and eligibility only; no outcome associations or models fitted.

## Integrity checks

| check | value | expected | status |
| --- | --- | --- | --- |
| players: null primary keys | 0 | 0 | PASS |
| players: duplicate primary-key rows | 0 | 0 | PASS |
| combine_results: null primary keys | 0 | 0 | PASS |
| combine_results: duplicate primary-key rows | 0 | 0 | PASS |
| games: null primary keys | 0 | 0 | PASS |
| games: duplicate primary-key rows | 0 | 0 | PASS |
| player_play: null primary keys | 0 | 0 | PASS |
| player_play: duplicate primary-key rows | 0 | 0 | PASS |
| combine_traits: null primary keys | 0 | 0 | PASS |
| combine_traits: duplicate primary-key rows | 0 | 0 | PASS |
| combine_attempts: null primary keys | 0 | 0 | PASS |
| combine_attempts: duplicate primary-key rows | 0 | 0 | PASS |
| game_play_traits: null primary keys | 0 | 0 | PASS |
| game_play_traits: duplicate primary-key rows | 0 | 0 | PASS |
| combine_results → players: missing nfl_id | 0 | 0 | PASS |
| combine_traits → players: missing nfl_id | 0 | 0 | PASS |
| combine_attempts → players: missing nfl_id | 0 | 0 | PASS |
| player_play → players: missing nfl_id | 0 | 0 | PASS |
| player_play → games: missing game_id | 0 | 0 | PASS |
| game_play_traits → players: missing nfl_id | 0 | 0 | PASS |
| game_play_traits → games: missing game_id | 0 | 0 | PASS |
| Combine/player draft-year disagreements | 0 | 0 | PASS |
| Player-play rows before draft year | 0 | 0 | PASS |
| Game-trait/game season disagreements | 0 | 0 | PASS |
| Game-trait rows without player-play outcome/context row | 2496 | 0 | NOTE |
| Player-play rows without game-trait row | 2466 | 0 | NOTE |
| players: CSV versus Parquet row difference | 0 | 0 | PASS |
| combine_results: CSV versus Parquet row difference | 0 | 0 | PASS |
| games: CSV versus Parquet row difference | 0 | 0 | PASS |
| player_play: CSV versus Parquet row difference | 0 | 0 | PASS |
| Combine PLAYER frames: null keys | 0 | 0 | PASS |
| Combine PLAYER frames: duplicate keys | 0 | 0 | PASS |
| Game frames: null keys | 0 | 0 | PASS |
| Game frames: duplicate keys | 0 | 0 | PASS |

## Primary-key summaries

| table | rows | null_keys | duplicate_rows |
| --- | --- | --- | --- |
| players | 510 | 0 | 0 |
| combine_results | 510 | 0 | 0 |
| games | 1002 | 0 | 0 |
| player_play | 314197 | 0 | 0 |
| combine_traits | 510 | 0 | 0 |
| combine_attempts | 5517 | 0 | 0 |
| game_play_traits | 314227 | 0 | 0 |
| combine_tracking PLAYER | 431094 | 0 | 0 |
| game_tracking | 22654290 | 0 | 0 |

## Raw/Parquet counts

| table | csv_rows | parquet_rows |
| --- | --- | --- |
| players | 510 | 510 |
| combine_results | 510 | 510 |
| games | 1002 | 1002 |
| player_play | 314197 | 314197 |

## Game frames

| season | frames |
| --- | --- |
| 2023 | 3665443 |
| 2024 | 7827944 |
| 2025 | 11160903 |

## Player-play season types

| season_type | player_plays | players |
| --- | --- | --- |
| POST | 13169 | 161 |
| PRE | 51759 | 487 |
| REG | 249269 | 401 |

## Study 3 rookie-season eligibility

| draft_year | eligible_players |
| --- | --- |
| 2023 | 25 |
| 2024 | 17 |
| 2025 | 16 |

## Study 3 candidate context missingness

| draft_year | candidate_plays | missing_cushion | missing_required_context | missing_coverage | missing_alignment |
| --- | --- | --- | --- | --- | --- |
| 2023 | 2446 | 77 | 0 | 3 | 0 |
| 2024 | 1708 | 53 | 0 | 0 | 0 |
| 2025 | 1235 | 53 | 0 | 0 | 0 |

## Scope and interpretation

FAIL means an input-integrity violation. NOTE means join attrition requiring explanation, not automatic invalidity.

Study 3 eligibility precedes final feature/context checks and measurement reliability screening.

Raw/Parquet row checks cover the four named CSVs; equal counts do not prove cell-level equality.

Full game-frame primary keys were checked.
