"""Exposure-only explanation of the frozen WR hero pair; see the descriptive protocol.

Run: .venv/bin/python -m src.wr_movement
Writes descriptive artifacts and an explained trace; the notebook runtime uses it as Figure 1.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import polars as pl

from src.kinematics import decompose

ROOT = Path(__file__).resolve().parents[1]
COLORS = ['#0072B2', '#D55E00']
KINEMATICS = ['sp', 'a_lon', 'a_lat', 'curv']


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def summarize_trace(frame):
    """Apply the written peak/window rules; reject irregular time or cached derivatives."""
    f = frame.sort_values('time').reset_index(drop=True)
    elapsed = (f.time - f.time.iloc[0]).dt.total_seconds().to_numpy()
    if len(f) < 13 or not np.allclose(np.diff(elapsed), .1, rtol=0, atol=1e-6):
        raise ValueError('Insufficient samples or non-10-Hz cadence; no local summaries.')
    if not np.isfinite(f[['x', 'y', *KINEMATICS]].to_numpy(float)).all():
        raise ValueError('Nonfinite coordinates or kinematics; no local summaries.')
    rebuilt = decompose(f.x.to_numpy(), f.y.to_numpy())
    for name in KINEMATICS:
        np.testing.assert_allclose(f[name], rebuilt[name], rtol=1e-10, atol=1e-10)
    interior = np.arange(len(f))
    eligible = (interior >= 3) & (interior < len(f)-3) & (f.sp.to_numpy() >= 1.)
    ids = np.flatnonzero(eligible)
    if not len(ids):
        raise ValueError('No eligible interior motion; no local summaries.')
    # np.argmax uses the first maximum; time sorting resolves ties.
    peak = int(ids[np.argmax(np.abs(f.a_lat.to_numpy()[ids]))])
    row = f.iloc[peak]
    curvature = float(abs(row.curv))
    identity = np.abs(f.a_lat.to_numpy()[ids]) - f.sp.to_numpy()[ids]**2 * np.abs(f.curv.to_numpy()[ids])
    np.testing.assert_allclose(identity, 0., atol=1e-10, rtol=0)
    windows = {}
    for name, lower, upper in [('pre_peak', -.3, -.1), ('post_peak', .1, .3)]:
        mask = eligible & (elapsed >= elapsed[peak]+lower-1e-8) & (elapsed <= elapsed[peak]+upper+1e-8)
        windows[name] = {'samples': int(mask.sum()), 'available': bool(mask.sum() >= 3),
                         'median_speed': float(f.loc[mask, 'sp'].median()) if mask.sum() >= 3 else None,
                         'start_seconds': float(elapsed[peak]+lower),
                         'end_seconds': float(elapsed[peak]+upper)}
    a, b = windows['pre_peak']['median_speed'], windows['post_peak']['median_speed']
    return {'frames': len(f), 'elapsed_span_seconds': float(elapsed[-1]),
            'full_attempt_turn': float(pl.Series(f.a_lat.abs()).quantile(.9)),
            'eligible_interior_samples': len(ids), 'peak_frame': peak,
            'peak_seconds': float(elapsed[peak]), 'peak_speed': float(row.sp),
            'peak_absolute_lateral_acceleration': float(abs(row.a_lat)),
            'peak_absolute_curvature': curvature,
            'peak_local_radius': 1/curvature if curvature > 1e-6 else None,
            'windows': windows, 'post_minus_pre_speed': b-a if a is not None and b is not None else None,
            'quality': {'cadence_passed': True, 'finite_passed': True,
                        'cached_kinematics_match': True,
                        'max_identity_absolute_error': float(np.max(np.abs(identity)))}}


def profiles(attempts, players, traits, reference, selection):
    """Explain existing composites using the recorded drill references, without refitting."""
    refs = pd.DataFrame(reference['drill_reference']).set_index('drill')
    dev = traits.merge(players[['nfl_id', 'draft_year', 'combine_position']], validate='one_to_one')
    dev = dev[(dev.combine_position == 'WR') & dev.draft_year.isin([2023, 2024])]
    mean, sd = float(dev.TURN.mean()), float(dev.TURN.std(ddof=1))
    result = []
    for selected in selection['players']:
        a = attempts[attempts.nfl_id == selected['nfl_id']]
        d = a.groupby('drill').lat.agg(['mean', 'count']).rename(columns={'mean': 'raw_attempt_mean', 'count': 'attempts'})
        d = d.join(refs[['mean', 'std']], how='inner').sort_index()
        d['z'] = (d.raw_attempt_mean-d['mean'])/d['std']
        d['composite_contribution'] = d.z/len(d)
        original = float(traits.loc[traits.nfl_id == selected['nfl_id'], 'TURN'].iloc[0])
        np.testing.assert_allclose(d.z.mean(), original, rtol=1e-10, atol=1e-10)
        athlete_z = (original-mean)/sd
        np.testing.assert_allclose(athlete_z, selected['TURN_z'], rtol=1e-10, atol=1e-10)
        result.append({'label': selected['label'], 'drills': len(d), 'raw_composite': original,
                       'development_WR_z': athlete_z, 'rows': d.reset_index().to_dict('records')})
    same_drills = [r['drill'] for r in result[0]['rows']] == [r['drill'] for r in result[1]['rows']]
    contrasts = None
    if same_drills:
        contrasts = [{'drill': a['drill'], 'B_minus_A_drill_z': b['z']-a['z'],
                      'B_minus_A_composite_contribution': b['composite_contribution']-a['composite_contribution']}
                     for a, b in zip(result[0]['rows'], result[1]['rows'])]
        np.testing.assert_allclose(sum(r['B_minus_A_composite_contribution'] for r in contrasts),
                                   result[1]['raw_composite']-result[0]['raw_composite'], atol=1e-10, rtol=1e-10)
    return {'development_WR_reference_n': len(dev), 'mean': mean, 'sd': sd,
            'same_drill_sets': same_drills, 'players': result, 'drill_contrasts': contrasts}


def plot_trace(frames, selection, summaries, target):
    fig, axes = plt.subplots(3, 2, figsize=(10, 10), layout='constrained')
    for col, (selected, summary, color) in enumerate(zip(selection['players'], summaries, COLORS)):
        f = frames[frames.event_id == selected['event_id']].sort_values('time').reset_index(drop=True)
        t = (f.time-f.time.iloc[0]).dt.total_seconds()
        x, y = f.x-f.x.iloc[0], f.y-f.y.iloc[0]
        axes[0, col].plot(x, y, color=color, lw=2)
        axes[0, col].scatter(x.iloc[0], y.iloc[0], color=color, s=25)
        axes[0, col].set(title=f"{selected['label']} · 40: {selected['forty']:.2f} s\n"
                        f"Across-drill TURN: {selected['TURN_z']:+.2f} WR SD",
                        xlabel='Start-relative x (yards)', ylabel='Start-relative y (yards)', aspect='equal')
        axes[1, col].plot(t, f.sp, color=color, lw=1.8)
        axes[1, col].set(xlabel='Recorded attempt time (s)', ylabel='Speed (yd/s)')
        axes[2, col].plot(t, f.a_lat.abs(), color=color, lw=1.8)
        axes[2, col].axhline(selected['attempt_turn'], color=color, ls='--', lw=1,
                            label=f"Full-attempt 90th percentile: {selected['attempt_turn']:.2f}")
        axes[2, col].set(xlabel='Recorded attempt time (s)', ylabel='Absolute lateral acceleration (yd/s²)')
        if 'error' not in summary:
            k, peak = summary['peak_frame'], summary['peak_seconds']
            axes[0, col].scatter(x.iloc[k], y.iloc[k], s=60, marker='x', color='#253747')
            axes[0, col].annotate('Reference peak', (x.iloc[k], y.iloc[k]), xytext=(-65, 12),
                                 textcoords='offset points', fontsize=9)
            for row in [1, 2]:
                ax = axes[row, col]
                ax.axvline(peak, color='#253747', ls=':', lw=1)
                ax.axvspan(0, float(t.iloc[3]), color='#777777', alpha=.12)
                ax.axvspan(float(t.iloc[-4]), float(t.iloc[-1]), color='#777777', alpha=.12)
            for name, shade in [('pre_peak', '#0072B2'), ('post_peak', '#009E73')]:
                window = summary['windows'][name]
                axes[1, col].axvspan(window['start_seconds'], window['end_seconds'], color=shade, alpha=.17)
            pre = summary['windows']['pre_peak']['median_speed']
            post = summary['windows']['post_peak']['median_speed']
            message = f'Pre/post-peak speed: {pre:.2f} / {post:.2f} yd/s' if pre is not None and post is not None else 'Local window comparison unavailable'
            axes[1, col].set_title(message, fontsize=10)
        else:
            axes[1, col].set_title('Local summaries unavailable: quality gate failed', fontsize=9)
        axes[2, col].legend(frameon=False, fontsize=8, loc='upper left')
    for row in range(3):
        pair = axes[row]
        xlim = min(ax.get_xlim()[0] for ax in pair), max(ax.get_xlim()[1] for ax in pair)
        ylim = min(ax.get_ylim()[0] for ax in pair), max(ax.get_ylim()[1] for ax in pair)
        for ax in pair:
            ax.set(xlim=xlim, ylim=ylim)
            ax.spines[['top', 'right']].set_visible(False)
    fig.suptitle('Similar sprint times do not fix drill speed or path shape\n'
                 'Across-drill headings; one recorded speed-out attempt below', fontsize=14)
    fig.supxlabel('Dotted line / ×: interior lateral-acceleration peak, not detected cut onset.\n'
                  'Shaded speed windows: fixed pre/post-peak samples; gray: derivative edges.\n'
                  'Illustrative extreme profile contrast; no efficiency or talent ranking.', fontsize=9)
    fig.savefig(target, dpi=200)
    plt.close(fig)


def report(record):
    lines = ['# Step 2 — What the receiver movement difference means', '',
             'Descriptive review of the existing pair, using the written [measurement protocol](wr_trace_measurement_protocol.md). '
             'Rebuild with `.venv/bin/python -m src.wr_movement`. Values and hashes: [wr_movement_metrics.json](wr_movement_metrics.json).', '',
             '## The plain-language explanation', '',
             'TURN measures lateral acceleration: how strongly the direction of movement changes while a player is moving. '
             'A faster player on the same curved path has more lateral acceleration. At the same speed, a tighter path also '
             'has more lateral acceleration. A larger TURN value therefore does not by itself mean better or more efficient cutting.', '',
             'For motion above the written speed floor, **absolute lateral acceleration = speed² × absolute path curvature**. '
             'This identity describes these same position-derived quantities; it is not independent validation or a causal '
             'breakdown of talent. Forty times measure a different task and do not hold these drill speeds constant.', '',
             '## The two recorded attempts', '',
             '| Quantity | WR A | WR B |', '|---|---:|---:|']
    selected = record['selection']['players']
    stats = record['traces']
    specifications = [('Observed 40 time (s)', [s['forty'] for s in selected]),
                      ('Across-drill profile (development WR SD)', [s['TURN_z'] for s in selected]),
                      ('Full-attempt 90th-percentile lateral acceleration (yd/s²)', [s['attempt_turn'] for s in selected])]
    for label, key in [('Recorded elapsed span (s)', 'elapsed_span_seconds'), ('Interior reference peak (s)', 'peak_seconds'),
                       ('Speed at reference peak (yd/s)', 'peak_speed'),
                       ('Lateral acceleration at reference peak (yd/s²)', 'peak_absolute_lateral_acceleration'),
                       ('Local curvature at reference peak (1/yd)', 'peak_absolute_curvature'),
                       ('Approximate local radius at reference peak (yd)', 'peak_local_radius')]:
        specifications.append((label, [s.get(key) for s in stats]))
    for label, values in specifications:
        formatted = ['unavailable' if value is None else f'{value:.3f}' for value in values]
        lines.append(f'| {label} | {formatted[0]} | {formatted[1]} |')
    if all('error' not in s for s in stats):
        a, b = stats
        lines += ['', f"At the separately selected reference peaks, B has higher lateral acceleration "
                  f"({b['peak_absolute_lateral_acceleration']:.2f} versus {a['peak_absolute_lateral_acceleration']:.2f} yd/s²) "
                  f"and higher speed ({b['peak_speed']:.2f} versus {a['peak_speed']:.2f} yd/s). "
                  f"Its local curvature is lower ({b['peak_absolute_curvature']:.3f} versus {a['peak_absolute_curvature']:.3f} 1/yd), "
                  'corresponding to a slightly wider local radius. This illustrates why larger lateral acceleration cannot '
                  'be equated with a tighter turn. It does not assign causal credit to speed or identify the better receiver.']
    lines += ['', 'These peaks are chosen separately by the same written rule. They are not matched football situations, '
              'validated break events, reaction times or a causal comparison. The recorded span is not timed drill completion. '
              'The full-attempt percentile and the interior peak summarize different samples.', '',
              '### Fixed windows around the reference peak', '', '| Athlete | Pre-peak speed | Post-peak speed | Post minus pre | Available samples |',
              '|---|---:|---:|---:|---|']
    for chosen, summary in zip(selected, stats):
        if 'error' in summary:
            lines.append(f"| {chosen['label']} | unavailable | unavailable | unavailable | {summary['error']} |")
            continue
        windows = summary['windows']
        values = [windows['pre_peak']['median_speed'], windows['post_peak']['median_speed'], summary['post_minus_pre_speed']]
        values = ['unavailable' if x is None else f'{x:.3f}' for x in values]
        lines.append(f"| {chosen['label']} | {' | '.join(values)} | {windows['pre_peak']['samples']} / {windows['post_peak']['samples']} |")
    lines += ['', 'Speeds are yd/s in fixed 0.3-to-0.1-second windows before/after the peak. '
              'These are descriptive local windows, not verified drill-entry/exit phases or a new reacceleration score. '
              'Do not read a speed difference as proof that one receiver cuts more efficiently.', '',
              '## Why one attempt does not explain the headline profile', '',
              'The headings summarize several non-40 drills, after averaging attempts within each drill and standardizing '
              'against the saved development reference. The selected speed-out attempt is only one illustration. '
              'A large across-drill gap does not imply the same-sized difference in this one drill.', '']
    profile = record['profiles']
    lines.append(f"The athletes have {'identical' if profile['same_drill_sets'] else 'different'} available drill sets. "
                 'Every available referenced drill is retained below; missing drills are not imputed.')
    for player in profile['players']:
        lines += ['', f"### {player['label']}: {player['drills']} drills", '',
                  '| Drill | Attempts | Raw percentile mean (yd/s²) | Reference mean | Reference SD | Drill z | Contribution to composite |',
                  '|---|---:|---:|---:|---:|---:|---:|']
        for r in player['rows']:
            lines.append(f"| {r['drill']} | {r['attempts']} | {r['raw_attempt_mean']:.3f} | {r['mean']:.3f} | {r['std']:.3f} | {r['z']:.3f} | {r['composite_contribution']:.3f} |")
        lines.append(f"\nThe drill z values average to {player['raw_composite']:.5f}; expressed in development-WR athlete SD units, "
                     f"this is {player['development_WR_z']:+.5f}, matching the historical heading.")
    if profile['drill_contrasts'] is not None:
        lines += ['', '### Arithmetic contribution to the composite difference', '',
                  '| Drill | B minus A drill z | Contribution to B minus A composite |',
                  '|---|---:|---:|']
        for r in profile['drill_contrasts']:
            lines.append(f"| {r['drill']} | {r['B_minus_A_drill_z']:+.3f} | {r['B_minus_A_composite_contribution']:+.3f} |")
        gap = profile['players'][1]['raw_composite']-profile['players'][0]['raw_composite']
        speed_out = next(r['B_minus_A_composite_contribution'] for r in profile['drill_contrasts'] if r['drill']=='SPEED_OUT_ROUTE_LEFT')
        if abs(gap) > 1e-10:
            lines += ['', f"The speed-out difference contributes {speed_out:.5f} of the {gap:.5f} raw composite gap "
                      f"({100*speed_out/gap:.1f}% arithmetically). The across-drill contrast is broader than the single "
                      'illustrated speed-out. These equal-weight contributions are accounting identities, not causal '
                      'explanations of talent or performance.']
    lines += ['', 'The training drill reference uses 2023–24 athletes across positions; the final display uses development '
              'WR mean/SD. Standardizing drills puts values on comparable scales; it does not remove speed dependence or '
              'prove that each drill measures the same talent.', '', '## Reliability and size/speed adjustments', '']
    repeat = record['existing_speed_out_repeat']
    lines.append(f"The existing same-drill report has {repeat['n']} WR speed-out repeat pairs: r={repeat['r']:.3f} "
                 f"[{repeat['r_lo']:.3f}, {repeat['r_hi']:.3f}], two-attempt composite SB={repeat['SB']:.3f}. "
                 'This wide, uncertain repeat result does not establish an individual speed-out score. The development '
                 'cross-drill SB of 0.593 is a different measurement across tasks and athletes.')
    for r in record['existing_WR_transfer']:
        lines.append(f"\nExisting PRE+REG WR movement transfer, {r['adjustment']}: r={r['r']:.3f} "
                     f"[{r['lo']:.3f}, {r['hi']:.3f}], n={r['n']}. This is population-level descriptive transfer, "
                     'not an adjustment for the entry speed of these two attempts or improved separation prediction.')
    lines += ['', '## Explained Figure 1 and writeup wording', '',
              'The [explained route figure](figures/combine_route_trace_explained.png) adds the speed curve, reference '
              'peak and fixed local windows to the original path/acceleration view. It keeps the original pair, common '
              'axes and separately labelled across-drill profile. The standalone notebook rebuild uses it to replace '
              'Figure 1, keeping six main figures.', '',
              '**Proposed methods wording:** “TURN summarizes the upper range of lateral acceleration across non-40 drills. '
              'Lateral acceleration increases with both speed and path curvature, so a higher profile can reflect drill '
              'execution as well as movement ability. The illustrated speed-out attempts show path, speed and acceleration; '
              'the headings summarize multiple drills. Neither view establishes cutting efficiency or an individual talent ranking.”', '',
              '**Proposed caption:** “Same selected receivers, one recorded speed-out attempt each. Headings show their '
              'across-drill TURN profiles. Dotted lines/crosses mark an interior lateral-acceleration peak using identical '
              'rules; speed-window shading is descriptive and does not identify a verified cut phase. Derivative-edge '
              'samples are shaded gray. The pair was selected for an extreme profile contrast, without NFL outcomes.”', '',
              '## Quality, reproduction and limits', '',
              'Full-attempt percentiles, composite headings and cached kinematics were checked against the recorded values. '
              'Local summaries require 10-Hz cadence, finite values, an interior speed floor and fixed window support. '
              'Failures remain unavailable; the saved metrics record each gate. Seven-sample quadratic derivatives span '
              '0.6 seconds between endpoints and can blur brief movements; estimates are not direct measurements of forces.', '',
              'The four physics checks run with `.venv/bin/python -m unittest discover -s tests -p wr_movement_checks.py -v`. '
              'They cover straight motion, circular motion at a known radius, quadratic speed dependence, rigid-coordinate '
              'invariance and rejection of irregular cadence. The standalone notebook includes this module, written '
              'protocol and explicit check file, and runs all four checks alongside the twelve pipeline tests.', '',
              'No NFL outcomes enter these new summaries. No new outcome models, efficiency rankings, causal attribution, '
              'individual repeatability claims, route-gate changes or fitted-reference changes were made. '
              'Performance uncertainty is assessed separately in the nine prescribed comparisons.']
    return '\n'.join(lines)+'\n'


def main():
    reports, interim = ROOT/'reports', ROOT/'data/interim'
    protocol = reports/'wr_trace_measurement_protocol.md'
    if not protocol.exists():
        raise ValueError('Write the descriptive protocol before calculating summaries.')
    selection = json.loads((reports/'route_trace_selection.json').read_text())
    if selection['outcome_information_used']:
        raise ValueError('Outcome-independent frozen selection required.')
    events = [p['event_id'] for p in selection['players']]
    frames = (pl.scan_parquet(interim/'combine_frames.parquet')
              .filter(pl.col('event_id').is_in(events))
              .select(['nfl_id', 'event_id', 'drill', 'time', 'x', 'y', *KINEMATICS]).collect().to_pandas())
    summaries = []
    for chosen in selection['players']:
        f = frames[frames.event_id == chosen['event_id']]
        if (len(f) != chosen['frames'] or set(f.nfl_id) != {chosen['nfl_id']}
                or set(f.drill) != {'SPEED_OUT_ROUTE_LEFT'} or f.time.duplicated().any()):
            raise ValueError('Frozen event identity or frame counts changed.')
        try:
            summary = summarize_trace(f)
            np.testing.assert_allclose(summary['full_attempt_turn'], chosen['attempt_turn'], rtol=1e-10, atol=1e-10)
        except (ValueError, AssertionError) as exc:
            summary = {'error': str(exc), 'quality': {'passed': False}}
        summaries.append(summary)
    profile = profiles(pd.read_parquet(interim/'combine_attempts.parquet'),
                       pd.read_parquet(interim/'combine_results.parquet', columns=['nfl_id', 'draft_year', 'combine_position']),
                       pd.read_parquet(interim/'study3_turn.parquet'),
                       json.loads((reports/'study3_turn_reference.json').read_text()), selection)
    reliability = json.loads((reports/'reliability.json').read_text())
    repeat = next(r for r in reliability['same_drill_turn'] if r['position']=='WR' and r['drill']=='SPEED_OUT_ROUTE_LEFT')
    transfer = json.loads((reports/'transfer_audit.json').read_text())
    sources = ['src/wr_movement.py', 'src/kinematics.py', 'reports/wr_trace_measurement_protocol.md',
               'reports/route_trace_selection.json', 'reports/study3_turn_reference.json',
               'reports/reliability.json', 'reports/transfer_audit.json',
               'data/interim/combine_frames.parquet', 'data/interim/combine_attempts.parquet',
               'data/interim/combine_results.parquet', 'data/interim/study3_turn.parquet']
    record = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'scope': 'Exposure-only descriptive explanation',
              'source_sha256': {p: sha256(ROOT/p) for p in sources}, 'selection': selection, 'traces': summaries,
              'profiles': profile, 'existing_speed_out_repeat': repeat,
              'existing_WR_transfer': [r for r in transfer['rows'] if r['scope']=='corrected, PRE+REG'
                                      and r['position']=='WR' and r['trait']=='lat'],
              'nfl_outcomes_used': False, 'frozen_features_changed': False,
              'candidate_replaces_figure': 1, 'all_local_quality_gates_pass': all('error' not in r for r in summaries)}
    plot_trace(frames, selection, summaries, reports/'figures/combine_route_trace_explained.png')
    (reports/'wr_movement_metrics.json').write_text(json.dumps(record, indent=2, allow_nan=False)+'\n')
    (reports/'wr_movement_explanation.md').write_text(report(record))
    print(json.dumps({'quality_passes': record['all_local_quality_gates_pass'],
                      'same_drill_sets': profile['same_drill_sets'], 'traces': summaries}, indent=2))


if __name__ == '__main__':
    main()
