"""Portable raw-input conversion and bounded subprocess execution for the notebook.

Statistical modules are embedded unchanged. No cached coefficients are used.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def convert(root):
    import duckdb
    from src.audit_data import sql_path
    raw, out = root/'data/raw', root/'data/interim'
    out.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='768MB'")
    con.execute('SET threads=2')
    con.execute('SET preserve_insertion_order=false')
    for csv in sorted(raw.glob('*.csv')):
        if csv.stem.startswith('game_tracking_'):
            continue
        target = out/(csv.stem+'.parquet')
        con.execute(f"COPY (SELECT * FROM read_csv_auto({sql_path(csv)}, sample_size=-1, nullstr='NA')) "
                    f"TO {sql_path(target)} (FORMAT parquet, COMPRESSION zstd)")
        print(f'{csv.name} converted', flush=True)
    seasons = [raw/f'game_tracking_{year}.csv' for year in [2023, 2024, 2025]]
    union = ' UNION ALL '.join(
        f"SELECT {year}::SMALLINT AS season,* FROM read_csv_auto({sql_path(csv)}, nullstr='NA')"
        for year, csv in zip([2023, 2024, 2025], seasons))
    con.execute(f"COPY ({union}) TO {sql_path(out/'game_tracking.parquet')} "
                '(FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 500000)')
    counts = {}
    for target in sorted(out.glob('*.parquet')):
        counts[target.stem] = con.execute(f'SELECT count(*) FROM read_parquet({sql_path(target)})').fetchone()[0]
    con.close()
    expected = {'players':510, 'combine_results':510, 'player_play':314197, 'game_tracking':22654290}
    for name, n in expected.items():
        if counts[name] != n:
            raise ValueError(f'{name}: expected {n}, received {counts[name]}')
    manifest = {'generated_utc':datetime.now(timezone.utc).isoformat(), 'source':'raw CSVs',
                'counts':counts, 'raw_sha256':{p.name:sha256(p) for p in sorted(raw.glob('*.csv'))}}
    (root/'reports/raw_input_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(counts, flush=True)


def process_memory_kib(pid):
    """Linux RSS of the stage and its children; return zero on other platforms."""
    try:
        status = Path(f'/proc/{pid}/status').read_text()
        rss = int(next(line.split()[1] for line in status.splitlines() if line.startswith('VmRSS:')))
        children = Path(f'/proc/{pid}/task/{pid}/children').read_text().split()
        return rss + sum(process_memory_kib(int(child)) for child in children)
    except (OSError, StopIteration):
        return 0


def run_stage(root, module, arguments=()):
    root = Path(root)
    label = module.rsplit('.',1)[-1] + ('_'+'_'.join(arguments).replace('--','') if arguments else '')
    logfile = root/'reports'/f'rebuild_{label}.log'
    environment = dict(os.environ, OPENBLAS_NUM_THREADS='2', OMP_NUM_THREADS='2',
                       POLARS_MAX_THREADS='2', MPLBACKEND='Agg', PYTHONUNBUFFERED='1')
    started, peak = time.monotonic(), 0
    command = [sys.executable, '-m', module, *arguments]
    with logfile.open('w') as log:
        process = subprocess.Popen(command, cwd=root, env=environment, stdout=log, stderr=subprocess.STDOUT)
        while process.poll() is None:
            peak = max(peak, process_memory_kib(process.pid))
            time.sleep(.25)
    elapsed = round(time.monotonic()-started, 2)
    print(f'{label}: {elapsed}s, sampled peak RSS {peak/1024:.0f} MiB', flush=True)
    tail = logfile.read_text().splitlines()[-5:]
    print('\n'.join(tail), flush=True)
    if process.returncode:
        raise RuntimeError(f'{label} failed ({process.returncode}); see {logfile}')
    target = root/'reports/rebuild_stages.json'
    records = json.loads(target.read_text()) if target.exists() else []
    records.append({'module':module, 'arguments':list(arguments), 'seconds':elapsed,
                    'sampled_peak_RSS_MiB':round(peak/1024,1), 'exit_code':process.returncode})
    target.write_text(json.dumps(records, indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--convert', action='store_true')
    args = parser.parse_args()
    if args.convert:
        convert(Path(__file__).resolve().parents[1])


if __name__ == '__main__':
    main()
