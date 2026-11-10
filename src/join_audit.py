"""Explain unmatched game-trait/player-play keys from their tracking inputs.

Run: .venv/bin/python -m src.join_audit
Writes reports/join_attrition.{md,json}, without changing source data.
"""
from datetime import datetime, timezone
import json
from pathlib import Path

import duckdb

from src.audit_data import markdown_table, records, sql_path

ROOT = Path(__file__).resolve().parents[1]


def main():
    c = duckdb.connect()
    c.execute("SET threads=2")
    c.execute("SET memory_limit='1GB'")
    for name in ['game_tracking', 'game_play_traits', 'player_play', 'games']:
        c.execute(f'CREATE VIEW {name} AS SELECT * FROM read_parquet('
                  f'{sql_path(ROOT/"data/interim"/f"{name}.parquet")})')
    c.execute('CREATE VIEW missing_traits AS SELECT p.* FROM player_play p '
              'ANTI JOIN game_play_traits USING(game_id, play_id, nfl_id)')
    c.execute('CREATE VIEW missing_pp AS SELECT t.* FROM game_play_traits t '
              'ANTI JOIN player_play USING(game_id, play_id, nfl_id)')
    c.execute('''CREATE TEMP TABLE frame_summary AS
        SELECT t.game_id, t.play_id, t.nfl_id, count(*) AS frames,
               count(*) FILTER(WHERE event='ball_snap') AS snaps,
               min(time) FILTER(WHERE event='ball_snap') AS snap_time
        FROM game_tracking t SEMI JOIN missing_traits USING(game_id,play_id,nfl_id)
        GROUP BY ALL''')
    c.execute('''CREATE TEMP TABLE windows AS
        SELECT t.game_id,t.play_id,t.nfl_id,count(*) AS window_frames
        FROM game_tracking t JOIN frame_summary f USING(game_id,play_id,nfl_id)
        WHERE t.time >= f.snap_time AND t.time <= f.snap_time + INTERVAL '3 seconds'
        GROUP BY ALL''')
    reasons = records(c, '''SELECT
        CASE WHEN f.frames IS NULL THEN 'no game tracking key'
             WHEN f.frames<15 THEN 'track shorter than 15 frames'
             WHEN f.snaps=0 THEN 'no ball_snap event'
             WHEN coalesce(w.window_frames,0)<10 THEN 'fewer than 10 post-snap window frames'
             ELSE 'unexplained' END AS reason, count(*) AS player_plays
        FROM missing_traits p LEFT JOIN frame_summary f USING(game_id,play_id,nfl_id)
        LEFT JOIN windows w USING(game_id,play_id,nfl_id) GROUP BY reason ORDER BY reason''')
    # The source tracking confirms traits without context rows, but cannot explain
    # why the competition provider omitted those rows. Check play-level availability.
    source = records(c, '''WITH keys AS (
        SELECT DISTINCT game_id,play_id,nfl_id FROM game_tracking
        SEMI JOIN missing_pp USING(game_id,play_id,nfl_id))
        SELECT count(*) AS traits_without_player_play,
        count(*) FILTER(WHERE EXISTS (SELECT 1 FROM keys k WHERE
          k.game_id=t.game_id AND k.play_id=t.play_id AND k.nfl_id=t.nfl_id)) AS confirmed_in_tracking,
        count(*) FILTER(WHERE EXISTS (SELECT 1 FROM player_play p WHERE
          p.game_id=t.game_id AND p.play_id=t.play_id)) AS play_has_other_player_context
        FROM missing_pp t''')
    seasons = []
    for name in ['missing_traits', 'missing_pp']:
        seasons.extend([dict(direction=name, **row) for row in records(c, f'''
            SELECT season_type,count(*) AS rows,count(DISTINCT nfl_id) AS players
            FROM {name} JOIN games USING(game_id) GROUP BY season_type ORDER BY season_type''')])
    nullified = records(c, '''SELECT play_nullified_by_penalty,count(*) AS rows
        FROM missing_traits GROUP BY 1 ORDER BY 1''')
    study3 = records(c, '''SELECT count(*) AS candidate_rows,
        count(*) FILTER(WHERE t.nfl_id IS NULL) AS without_game_trait
        FROM player_play p JOIN games g USING(game_id)
        JOIN read_parquet('data/interim/combine_results.parquet') cr USING(nfl_id)
        LEFT JOIN game_play_traits t USING(game_id,play_id,nfl_id)
        WHERE cr.combine_position='WR' AND g.season_type='REG' AND g.season=cr.draft_year
          AND p.play_nullified_by_penalty='N' AND p.route_ran IN ('SLANT','OUT','GO')
          AND p.separation_at_pass_forward IS NOT NULL''')
    c.close()
    result = dict(generated_utc=datetime.now(timezone.utc).isoformat(), reasons=reasons,
                  source_confirmation=source, by_season=seasons, nullified=nullified,
                  study3=study3)
    unexplained = sum(r['player_plays'] for r in reasons if r['reason']=='unexplained')
    if unexplained:
        raise ValueError(f'{unexplained} missing traits lack an extraction explanation')
    reports = ROOT/'reports'
    (reports/'join_attrition.json').write_text(json.dumps(result, indent=2)+'\n')
    (reports/'join_attrition.md').write_text(
        '# Game-trait / player-play join attrition\n\n'
        f"Generated UTC: {result['generated_utc']}.\n\n"
        'These tables have different source support. Player-play metadata does not guarantee '
        'a usable tracking window, and tracking can exist without player-play context.\n\n'
        '## Player-play rows without derived movement traits\n\n'
        + markdown_table(reasons)
        + '\nMutually exclusive reasons follow the extractor: absent tracking key, track <15 '
        'frames, no snap, post-snap window <10 frames. Every unmatched row is accounted for.\n\n'
        + markdown_table(nullified)
        + '\n## Derived movement rows without player-play context\n\n'
        + markdown_table(source)
        + '\nThese keys exist in supplied tracking. The reason the provider omitted player-play '
        'context is unknown; do not label them as extraction errors or fabricate outcomes. '
        'Inner joins appropriately exclude them from context/outcome models.\n\n'
        + markdown_table(seasons)
        + '\n## Frozen Study 3 sample\n\n'
        + markdown_table(study3)
        + '\nStudy 3 links Combine TURN directly to supplied NFL separation/context; it does '
        'not require a derived game movement trait. Do not introduce an unnecessary '
        'game-trait join that removes otherwise eligible performance rows.\n')
    print(markdown_table(reasons), flush=True)
    print(markdown_table(source), flush=True)


if __name__ == '__main__':
    main()
