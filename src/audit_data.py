"""Audit input keys, joins, counts and Study 3 eligibility without fitting outcomes.

Run: .venv/bin/python -m src.audit_data
Add --tracking-keys for the full 22M-frame game-key check.
Writes reports/audit.md and reports/audit.json; never modifies input data.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import duckdb


KEYS = {
    "players": ["nfl_id"],
    "combine_results": ["nfl_id"],
    "games": ["game_id"],
    "player_play": ["game_id", "play_id", "nfl_id"],
    "combine_traits": ["nfl_id"],
    "combine_attempts": ["nfl_id", "drill", "event_id"],
    "game_play_traits": ["game_id", "play_id", "nfl_id"],
}


def sql_path(path: Path) -> str:
    return "'" + str(path).replace("'", "''") + "'"


def records(con, query: str) -> list[dict]:
    result = con.execute(query)
    names = [c[0] for c in result.description]
    return [dict(zip(names, row)) for row in result.fetchall()]


def key_counts(con, view: str, keys: list[str]) -> dict:
    columns = ", ".join(keys)
    nulls = " OR ".join(f"{k} IS NULL" for k in keys)
    return records(con, f"""
        SELECT count(*) AS rows,
               count(*) FILTER (WHERE {nulls}) AS null_keys,
               count(*) - count(DISTINCT ROW({columns})) AS duplicate_rows
        FROM {view}
    """)[0]


def audit(root: Path, tracking_keys: bool = False) -> dict:
    con = duckdb.connect()
    con.execute("SET memory_limit='1GB'")
    con.execute("SET threads=2")
    interim = root / "data" / "interim"
    for path in sorted(interim.glob("*.parquet")):
        con.execute(f"CREATE VIEW {path.stem} AS SELECT * FROM read_parquet({sql_path(path)})")

    checks = []
    def check(name, value, expected=0, blocking=True):
        checks.append(dict(check=name, value=value, expected=expected,
                           status="PASS" if value == expected else ("FAIL" if blocking else "NOTE")))

    counts = []
    for name, keys in KEYS.items():
        summary = key_counts(con, name, keys)
        counts.append(dict(table=name, **summary))
        check(f"{name}: null primary keys", summary["null_keys"])
        check(f"{name}: duplicate primary-key rows", summary["duplicate_rows"])

    for child, parent, key in (
        ("combine_results", "players", "nfl_id"),
        ("combine_traits", "players", "nfl_id"),
        ("combine_attempts", "players", "nfl_id"),
        ("player_play", "players", "nfl_id"),
        ("player_play", "games", "game_id"),
        ("game_play_traits", "players", "nfl_id"),
        ("game_play_traits", "games", "game_id"),
    ):
        missing = con.execute(f"""SELECT count(*) FROM {child} c
            WHERE NOT EXISTS (SELECT 1 FROM {parent} p WHERE p.{key}=c.{key})""").fetchone()[0]
        check(f"{child} → {parent}: missing {key}", missing)

    check("Combine/player draft-year disagreements", con.execute("""
        SELECT count(*) FROM combine_results c JOIN players p USING(nfl_id)
        WHERE c.draft_year IS DISTINCT FROM p.draft_year
    """).fetchone()[0])
    check("Player-play rows before draft year", con.execute("""
        SELECT count(*) FROM player_play pp JOIN games g USING(game_id)
        JOIN players p USING(nfl_id) WHERE g.season < p.draft_year
    """).fetchone()[0])
    check("Game-trait/game season disagreements", con.execute("""
        SELECT count(*) FROM game_play_traits t JOIN games g USING(game_id)
        WHERE t.season IS DISTINCT FROM g.season
    """).fetchone()[0])
    check("Game-trait rows without player-play outcome/context row", con.execute("""
        SELECT count(*) FROM game_play_traits t ANTI JOIN player_play pp
        USING(game_id, play_id, nfl_id)
    """).fetchone()[0], blocking=False)
    check("Player-play rows without game-trait row", con.execute("""
        SELECT count(*) FROM player_play pp ANTI JOIN game_play_traits t
        USING(game_id, play_id, nfl_id)
    """).fetchone()[0], blocking=False)

    raw_counts = []
    for name in ("players", "combine_results", "games", "player_play"):
        path = root / "data" / "raw" / f"{name}.csv"
        if not path.exists():
            raw_counts.append(dict(table=name, csv_rows=None, parquet_rows=None))
            continue
        n_raw = con.execute(f"SELECT count(*) FROM read_csv_auto({sql_path(path)}, nullstr='NA')").fetchone()[0]
        n_pq = con.execute(f"SELECT count(*) FROM {name}").fetchone()[0]
        raw_counts.append(dict(table=name, csv_rows=n_raw, parquet_rows=n_pq))
        check(f"{name}: CSV versus Parquet row difference", n_raw - n_pq)

    con.execute("CREATE VIEW combine_player_frames AS SELECT * FROM combine_tracking WHERE entity_type='PLAYER'")
    summary = key_counts(con, "combine_player_frames", ["event_id", "nfl_id", "time"])
    counts.append(dict(table="combine_tracking PLAYER", **summary))
    check("Combine PLAYER frames: null keys", summary["null_keys"])
    check("Combine PLAYER frames: duplicate keys", summary["duplicate_rows"])
    game_frames = records(con, "SELECT season, count(*) AS frames FROM game_tracking GROUP BY season ORDER BY season")
    if tracking_keys:
        summary = key_counts(con, "game_tracking", ["game_id", "play_id", "nfl_id", "time"])
        counts.append(dict(table="game_tracking", **summary))
        check("Game frames: null keys", summary["null_keys"])
        check("Game frames: duplicate keys", summary["duplicate_rows"])

    seasons = records(con, """
        SELECT g.season_type, count(*) AS player_plays, count(DISTINCT pp.nfl_id) AS players
        FROM player_play pp JOIN games g USING(game_id)
        GROUP BY g.season_type ORDER BY g.season_type
    """)
    con.execute("""CREATE VIEW wr_candidates AS
        SELECT pp.*, p.draft_year, g.season,
            CASE WHEN pp.route_ran='GO' THEN 'GO' ELSE 'BREAK' END AS family
        FROM player_play pp JOIN players p USING(nfl_id)
        JOIN combine_results c USING(nfl_id) JOIN games g USING(game_id)
        WHERE c.combine_position='WR' AND g.season_type='REG'
          AND pp.play_nullified_by_penalty='N' AND g.season=p.draft_year
          AND pp.route_ran IN ('SLANT','OUT','GO')
          AND pp.separation_at_pass_forward IS NOT NULL
    """)
    eligibility = records(con, """
        WITH family_counts AS (
            SELECT nfl_id, draft_year, family, count(*) AS n FROM wr_candidates
            GROUP BY nfl_id, draft_year, family
        ), eligible AS (
            SELECT nfl_id, draft_year FROM family_counts WHERE n>=10
            GROUP BY nfl_id, draft_year HAVING count(*)=2
        )
        SELECT draft_year, count(*) AS eligible_players FROM eligible
        GROUP BY draft_year ORDER BY draft_year
    """)
    missingness = records(con, """
        SELECT draft_year, count(*) AS candidate_plays,
            count(*) FILTER (WHERE cushion IS NULL) AS missing_cushion,
            count(*) FILTER (WHERE down IS NULL OR yards_to_go IS NULL) AS missing_required_context,
            count(*) FILTER (WHERE team_coverage_man_zone IS NULL) AS missing_coverage,
            count(*) FILTER (WHERE receiver_alignment IS NULL) AS missing_alignment
        FROM wr_candidates GROUP BY draft_year ORDER BY draft_year
    """)
    con.close()
    return dict(generated_utc=datetime.now(timezone.utc).isoformat(), checks=checks,
                table_keys=counts, raw_counts=raw_counts, game_frames=game_frames,
                season_types=seasons, study3_eligibility=eligibility,
                study3_missingness=missingness, full_game_tracking_keys_checked=tracking_keys)


def markdown_table(rows: list[dict]) -> str:
    if not rows:
        return "No rows.\n"
    columns = list(rows[0])
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    lines += ["| " + " | ".join(str(row[c]) for c in columns) + " |" for row in rows]
    return "\n".join(lines) + "\n"


def write_report(result: dict, reports: Path) -> None:
    reports.mkdir(parents=True, exist_ok=True)
    sections = ["# Data audit\n", f"Generated UTC: {result['generated_utc']}\n",
                "Counts, integrity and eligibility only; no outcome associations or models fitted.\n"]
    for title, key in (("Integrity checks", "checks"), ("Primary-key summaries", "table_keys"),
                       ("Raw/Parquet counts", "raw_counts"), ("Game frames", "game_frames"),
                       ("Player-play season types", "season_types"),
                       ("Study 3 rookie-season eligibility", "study3_eligibility"),
                       ("Study 3 candidate context missingness", "study3_missingness")):
        sections += [f"## {title}\n", markdown_table(result[key])]
    sections += ["## Scope and interpretation\n",
                 "FAIL means an input-integrity violation. NOTE means join attrition requiring explanation, not automatic invalidity.\n",
                 "Study 3 eligibility precedes final feature/context checks and measurement reliability screening.\n",
                 "Raw/Parquet row checks cover the four named CSVs; equal counts do not prove cell-level equality.\n",
                 "Full game-frame primary keys were checked.\n" if result["full_game_tracking_keys_checked"]
                 else "Full game-frame primary keys were not rescanned; rerun with `--tracking-keys` for that check.\n"]
    (reports / "audit.md").write_text("\n".join(sections))
    (reports / "audit.json").write_text(json.dumps(result, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--tracking-keys", action="store_true")
    args = parser.parse_args()
    result = audit(args.project_root.resolve(), args.tracking_keys)
    write_report(result, args.project_root / "reports")
    failures = [c for c in result["checks"] if c["status"] == "FAIL"]
    notes = [c for c in result["checks"] if c["status"] == "NOTE"]
    print(f"Audit: {len(failures)} failures, {len(notes)} join-attrition notes. Report: reports/audit.md")
    print("Study 3 eligibility:", result["study3_eligibility"])
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
