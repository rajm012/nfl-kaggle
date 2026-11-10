# Game-trait / player-play join attrition

Generated UTC: 2026-11-09T14:35:18.359900+00:00.

These tables have different source support. Player-play metadata does not guarantee a usable tracking window, and tracking can exist without player-play context.

## Player-play rows without derived movement traits

| reason | player_plays |
| --- | --- |
| no ball_snap event | 715 |
| no game tracking key | 1750 |
| track shorter than 15 frames | 1 |

Mutually exclusive reasons follow the extractor: absent tracking key, track <15 frames, no snap, post-snap window <10 frames. Every unmatched row is accounted for.

| play_nullified_by_penalty | rows |
| --- | --- |
| N | 1028 |
| Y | 1438 |

## Derived movement rows without player-play context

| traits_without_player_play | confirmed_in_tracking | play_has_other_player_context |
| --- | --- | --- |
| 2496 | 2496 | 2287 |

These keys exist in supplied tracking. The reason the provider omitted player-play context is unknown; do not label them as extraction errors or fabricate outcomes. Inner joins appropriately exclude them from context/outcome models.

| direction | season_type | rows | players |
| --- | --- | --- | --- |
| missing_traits | POST | 244 | 77 |
| missing_traits | PRE | 1182 | 325 |
| missing_traits | REG | 1040 | 248 |
| missing_pp | POST | 79 | 30 |
| missing_pp | PRE | 185 | 75 |
| missing_pp | REG | 2232 | 110 |

## Frozen Study 3 sample

| candidate_rows | without_game_trait |
| --- | --- |
| 5389 | 3 |

Study 3 links Combine TURN directly to supplied NFL separation/context; it does not require a derived game movement trait. Do not introduce an unnecessary game-trait join that removes otherwise eligible performance rows.
