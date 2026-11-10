"""Quiet reproduction and readable displays for the submission notebook."""
from contextlib import redirect_stdout
from datetime import datetime, timezone
import html
from importlib.metadata import PackageNotFoundError, version
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

PACKAGES = ['duckdb', 'polars', 'numpy', 'pandas', 'scipy', 'statsmodels', 'matplotlib']
INPUTS = ['players.csv', 'combine_results.csv', 'combine_tracking.csv', 'games.csv',
          'player_play.csv', 'player_career_successes.csv', 'game_tracking_2023.csv',
          'game_tracking_2024.csv', 'game_tracking_2025.csv']
ROOT = None
PREVIEW = False
STARTED = None


def prepare(root):
    """Check dependencies and inputs; preview mode is local and explicitly labelled."""
    global ROOT, PREVIEW, STARTED
    STARTED = time.monotonic()
    ROOT = Path(root)
    os.environ.update(OPENBLAS_NUM_THREADS='2', OMP_NUM_THREADS='2',
                      POLARS_MAX_THREADS='2', MPLBACKEND='Agg')
    review = os.environ.get('BDB_REVIEW_ROOT')
    if review:
        if Path('/kaggle/working').exists():
            raise ValueError('Visual preview is unavailable on Kaggle; use the full raw rebuild.')
        ROOT = Path(review).resolve()
        record = json.loads((ROOT/'reports/submission_verification.json').read_text())
        if not _verified(record):
            raise ValueError('Preview requires a previously verified complete rebuild.')
        PREVIEW = True
        return
    required = dict(line.split('==') for line in (ROOT/'requirements.txt').read_text().splitlines()
                    if line and not line.startswith('#'))
    mismatches = []
    for package in PACKAGES:
        try:
            installed = version(package)
        except PackageNotFoundError:
            installed = None
        if installed != required[package]:
            mismatches.append(f'{package}=={required[package]}')
    if mismatches:
        with (ROOT/'reports/environment_setup.log').open('w') as log:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', *mismatches],
                           stdout=log, stderr=subprocess.STDOUT, check=True)
    input_base = Path(os.environ.get('BDB_INPUT_ROOT', '/kaggle/input'))
    for name in INPUTS:
        matches = sorted(input_base.rglob(name))
        if len(matches) != 1:
            raise ValueError(f'Expected one {name} under {input_base}; found {len(matches)}')
        (ROOT/'data/raw'/name).symlink_to(matches[0].resolve())


def rebuild():
    """Refit every model and verify results, with full logs saved outside the report."""
    if PREVIEW:
        return
    from src.submission_pipeline import run_stage
    stages = [('submission_pipeline', '--convert'), ('combine_features',), ('sprint',),
              ('game_features',), ('audit_data',), ('join_audit',), ('reliability',),
              ('route_context',), ('transfer_audit',), ('validation',),
              ('evaluate', '--stage', 'develop'), ('evaluate', '--stage', 'evaluate'),
              ('submission_replay',), ('submission_verify',), ('audit_figures',),
              ('evaluation_figures',), ('submission_figures',)]
    with (ROOT/'reports/rebuild_summary.log').open('w') as log:
        for module, *arguments in stages:
            try:
                with redirect_stdout(log):
                    run_stage(ROOT, 'src.'+module, arguments)
            except Exception:
                log.flush()
                raise RuntimeError(f'Rebuild stopped at {module}; see {ROOT}/reports/rebuild_*.log')
    with (ROOT/'reports/tests.log').open('w') as log:
        subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                       cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
    records = json.loads((ROOT/'reports/rebuild_stages.json').read_text())
    summary = {'source': 'nine raw competition CSVs', 'cohort_pipeline_rebuilt_in_notebook': True,
               'all_headlines_verified': True, 'figures': 6, 'tables': 1,
               'elapsed_seconds': round(time.monotonic()-STARTED, 2),
               'largest_stage_sampled_RSS_MiB': max(s['sampled_peak_RSS_MiB'] for s in records),
               'versions': {p: version(p) for p in PACKAGES}, 'output_root': str(ROOT),
               'presentation_format': 2, 'generated_utc': datetime.now(timezone.utc).isoformat()}
    (ROOT/'reports/full_notebook_execution.json').write_text(json.dumps(summary, indent=2)+'\n')


def _display_html(value):
    from IPython.display import HTML, display
    display(HTML(value))


def overview():
    preview = '<p style="color:#9c6200">Local visual preview · previously verified results</p>' if PREVIEW else ''
    _display_html('''<div style="padding:24px 28px;background:#eef5fa;border-left:5px solid #0072b2;
        border-radius:8px;color:#203746;font-family:system-ui,sans-serif">
        <p style="margin:0 0 10px;font-size:12px;letter-spacing:2px;color:#527184">THE FINDING</p>
        <h2 style="margin:0 0 14px;font-size:27px;line-height:1.3">Movement carries over.<br>
        Added performance prediction remains uncertain.</h2>
        <p style="margin:0;line-height:1.7"><b>510</b> rookie-cohort prospects &nbsp; · &nbsp;
        <b>10 Hz</b> tracking &nbsp; · &nbsp; <b>9</b> primary prediction comparisons</p>'''+preview+'</div>')


def figure(name):
    from IPython.display import Image, display
    display(Image(filename=str(ROOT/'reports/figures'/(name+'.png')), width=950))


def evaluation_table():
    import pandas as pd
    table = pd.read_csv(ROOT/'reports/evaluation_table.csv')
    rows = []
    for r in table.itertuples(index=False):
        unit = {'yards': 'yd', 'seconds': 's', 'proportion': 'proportion'}[r.units]
        cells = [html.escape(r.comparison), unit, str(r.evaluation_players),
                 f'{r.baseline_RMSE:.5f}', f'{r.tracking_RMSE:.5f}',
                 f'{r.RMSE_improvement:+.5f}',
                 f'[{r.improvement_95_lo:.5f}, {r.improvement_95_hi:.5f}]']
        background = '#f4f7fa' if len(rows) % 2 == 0 else '#ffffff'
        rows.append(f'<tr style="background:{background}">'+''.join(
            f'<td style="padding:10px 12px;border-bottom:1px solid #dce4eb;white-space:nowrap">{c}</td>'
            for c in cells)+'</tr>')
    heads = ['Comparison', 'Unit', 'Athletes', 'Baseline RMSE', '+ Tracking RMSE', 'Gain', '95% gain interval']
    _display_html('<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;'
                  'font:13px/1.5 system-ui,sans-serif;color:#253747"><thead><tr>'+''.join(
                  f'<th style="padding:12px;background:#203746;color:white;text-align:left;white-space:nowrap">{h}</th>'
                  for h in heads)+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>')


def evidence_notes():
    result = json.loads((ROOT/'reports/submission_verification.json').read_text())
    if not _verified(result):
        raise AssertionError('Verification must pass before displaying the evidence card.')
    _display_html('''<div style="padding:18px 22px;border:1px solid #dce4eb;border-radius:8px;
        font:14px/1.8 system-ui,sans-serif;color:#253747">
        <b>Reproduction checks passed</b><br>402 numeric comparisons · 25 athlete-weighted scores ·
        disjoint development/evaluation cohorts · frozen specification hashes<br>
        <b>Decision respected:</b> route-family measurement gate failed; primary TURN interaction stopped.
        </div>''')


def _verified(record):
    return (record.get('headline_numeric_checks') == 402
            and len(record.get('comparisons_verified', [])) == 25
            and record.get('raw_input_rebuild')
            and record.get('frozen_hashes_match')
            and record.get('no_player_overlap')
            and record.get('no_evaluation_player_effects'))


def appendix():
    import mistune
    # Keep Kaggle's renderer dependency intact; it can use the legacy Mistune API.
    markdown = (mistune.create_markdown(plugins=['table'])
                if hasattr(mistune, 'create_markdown') else mistune.markdown)
    labels = {'reliability': 'Measurement reliability', 'transfer_audit': 'Movement transfer',
              'model_audit': 'Historical model audit', 'study3_measurement': 'Route-family measurement screen',
              'validation': 'All cohort prediction comparisons', 'cone_sensitivity': 'All cone subset findings'}
    panels = []
    for name, title in labels.items():
        content = markdown((ROOT/'reports'/(name+'.md')).read_text())
        panels.append('<details style="margin:10px 0;padding:12px 16px;border:1px solid #dce4eb;'
                      'border-radius:6px"><summary style="cursor:pointer;font-weight:600;color:#0072b2">'
                      +title+'</summary><div style="overflow-x:auto;font-size:13px;line-height:1.65">'
                      +content+'</div></details>')
    _display_html(''.join(panels))


def finish():
    if Path('/kaggle/working').exists():
        shutil.rmtree(ROOT/'data')
