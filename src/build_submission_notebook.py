"""Build the complete standalone notebook; embeds source, not fitted-result substitutes."""
import hashlib
import json
from pathlib import Path

import nbformat

from src.submission_verify import selected_values

ROOT = Path(__file__).resolve().parents[1]
MODULES = ['__init__','kinematics','combine_features','game_features','sprint','audit_data',
           'join_audit','reliability','route_context','outcomes','study2','validation','evaluate',
           'cone_sensitivity','transfer_audit','audit_figures','evaluation_figures',
           'submission_pipeline','notebook_runtime','submission_figures','submission_verify','submission_replay']


def main():
    files = {'src/'+name+'.py':(ROOT/'src'/(name+'.py')).read_text() for name in MODULES}
    for name in ['requirements.txt','LICENSE','reports/evaluation_protocol.md','reports/study3_protocol.md',
                 'reports/prereg.md']:
        files[name] = (ROOT/name).read_text()
    for p in sorted((ROOT/'tests').glob('test_*.py')):
        files['tests/'+p.name] = p.read_text()
    reference = selected_values(ROOT)
    files['reports/reference_headlines.json'] = json.dumps(reference,indent=2)+'\n'
    cone = json.loads((ROOT/'reports/cone_sensitivity.json').read_text())
    solver_plan = [{'id':r['id'],'model':name,'columns':list(model['coefficients']),
                    'recorded_optimizer':model['optimizer'],
                    'method':'powell' if 'Powell' in model['optimizer'] else ['bfgs','lbfgs'],
                    'canonical_row_order':'Powell' not in model['optimizer']}
                   for r in cone['comparisons'] for name,model in r['models'].items()
                   if ('Powell' in model['optimizer'] or
                       ('Retrying MixedLM optimization with lbfgs' in model.get('initial_diagnostics', [])
                        and 'Retrying MixedLM optimization with cg' not in model.get('initial_diagnostics', [])))]
    files['reports/historical_solver_plan.json'] = json.dumps(solver_plan,indent=2)+'\n'
    frozen_source = json.loads((ROOT/'reports/evaluation_development.json').read_text())['provenance']
    for name in ['src/evaluate.py','src/route_context.py','requirements.txt','reports/evaluation_protocol.md']:
        if hashlib.sha256(files[name].encode()).hexdigest()!=frozen_source[name]:
            raise ValueError('Frozen specification changed: '+name)
    manifest = {name:hashlib.sha256(value.encode()).hexdigest() for name,value in files.items()}
    nb = nbformat.v4.new_notebook()
    nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                   'language_info': {'name': 'python'}, 'bdb_source_sha256': manifest,
                   'bdb_source_files': files, 'bdb_format_version': 2}
    md = nbformat.v4.new_markdown_cell

    def code(source, quiet=False):
        tags = ['hide-input', 'remove_input'] + (['remove_output'] if quiet else [])
        return nbformat.v4.new_code_cell(source, metadata={
            'jupyter': {'source_hidden': True, 'outputs_hidden': quiet},
            'hide_input': True, 'collapsed': True, 'tags': tags})

    nb.cells = [
        md('''# Beyond the stopwatch
### Combine movement to NFL decisions: an evidence map

**NFL Big Data Bowl 2027 · University Track**

Two prospects can post nearly identical 40-yard times and move differently through a route.
Does that difference carry into NFL games—and does it improve performance prediction?

We follow the evidence through three questions: **can we measure it, does it transfer,
and does it add predictive value?** The answer supports a scouting conversation, with clear limits
on what tracking can justify.'''),
        code('''# Load the source stored with this notebook, then prepare a fresh run.
import hashlib, json, os, sys, tempfile
from pathlib import Path

os.environ.update(OPENBLAS_NUM_THREADS='2', OMP_NUM_THREADS='2',
                  POLARS_MAX_THREADS='2', MPLBACKEND='Agg')
candidates = [Path(os.environ.get('BDB_NOTEBOOK_PATH', 'submission.ipynb')),
              Path('/kaggle/working/__notebook__.ipynb'),
              Path('notebooks/submission.ipynb'), *Path.cwd().glob('*.ipynb')]
for path in candidates:
    if path.is_file():
        metadata = json.loads(path.read_text()).get('metadata', {})
        if 'bdb_source_files' in metadata:
            break
else:
    raise FileNotFoundError('Open the complete notebook; its source metadata is required.')

output_base = Path('/kaggle/working') if Path('/kaggle/working').exists() else Path(tempfile.gettempdir())
run_root = Path(tempfile.mkdtemp(prefix='bdb_raw_rebuild_', dir=output_base))
for directory in ['src', 'tests', 'reports/figures', 'data/raw', 'data/interim']:
    (run_root/directory).mkdir(parents=True, exist_ok=True)
for name, source in metadata['bdb_source_files'].items():
    if hashlib.sha256(source.encode()).hexdigest() != metadata['bdb_source_sha256'][name]:
        raise ValueError('Source integrity check failed: '+name)
    (run_root/name).write_text(source)
sys.path.insert(0, str(run_root))
from src.notebook_runtime import prepare, rebuild, overview, figure, evaluation_table, evidence_notes, appendix, finish
prepare(run_root)''', quiet=True),
        code('''# Rebuild from the nine competition CSVs; detailed logs are saved in reports/.
rebuild()''', quiet=True),
        code('overview()'),
        md('''## 01 · What the stopwatch misses

The 40-yard dash captures straight-line speed. Route tracking adds the shape of movement:
how a player turns, accelerates and builds speed. Here, two development receivers have observed
40 times within **0.03 seconds**, but different turning profiles.'''),
        code("figure('combine_route_trace')"),
        md('''*Figure 1. Actual Combine route traces. The pair was chosen using Combine exposure only:
largest training-reference TURN difference among development WRs with comparable observed 40 times,
with deterministic athlete-ID ties. NFL outcomes played no part in selection.*

**TURN** summarises lateral acceleration through a drill. **BURST** summarises peak forward
acceleration. **A0** describes the early acceleration of the fitted 40-yard speed curve.
Positions are smoothed at 10 Hz; acceleration is decomposed into signed longitudinal and lateral
components. Standardisation for prediction uses 2023–24 athletes only.

These are descriptions of movement. A more distinctive trace alone does not establish a better player.'''),
        md('''## 02 · The sample behind the claim

The supplied tracking covers **510 rookie-cohort players**. Availability narrows as we require
a usable drill, an NFL outcome and enough repeated observations. Each comparison therefore
reports its own athlete count.'''),
        code("figure('evidence_support')"),
        md('''*Figure 2. Athlete support across the evidence chain. Primary cohort evaluation uses
20–37 athletes per comparison; cone subsets are smaller.*

The game coordinates contain the tracked rookies, without teammates, opponents or the ball.
We use provider-supplied performance outcomes rather than reconstructing opponent geometry.
Movement transfer uses PRE + REG and excludes POST; performance prediction uses rookie REG only.'''),
        md('''## 03 · Movement carries into games

Some Combine movement differences reappear in NFL tracking. Receiver TURN correlates with game
turning at **0.279 [0.107, 0.445]** across 98 athletes. Defensive-line BURST correlates with
game burst at **0.443 [0.289, 0.584]** across 115 athletes; after weight adjustment, the estimate
is **0.203 [0.044, 0.376]**.'''),
        code("figure('transfer_audited')"),
        md('''*Figure 3. Descriptive movement transfer, with athlete-bootstrap intervals and refitted
adjustment. These pooled PRE + REG estimates are separate from held-out performance prediction.*

Development WR cross-drill TURN consistency is **0.593 [0.373, 0.737]**, based on 70 receivers.
Cross-drill consistency supports measuring a trait, but does not by itself establish repeatability
of a particular route-performance outcome.'''),
        md('''## 04 · A measurement gate worth respecting

Before testing whether TURN predicts a route-specific performance advantage, we required a
stable SLANT/OUT-minus-GO contrast. The adjusted reliability was **0.296 [−0.257, 0.606]**
among 41 diagnostic receivers, below the predeclared **0.40** threshold.'''),
        code("figure('study3_measurement')"),
        md('''*Figure 4. The frozen measurement screen failed. The primary TURN interaction and its
2025 performance evaluation remain stopped.*

The data do not support turning this contrast into a talent score. Eligibility and route groups
were kept fixed after the result.'''),
        md('''## 05 · Does tracking improve performance prediction?

We trained conventional baselines on 2023–24 athletes and compared them with the same models
plus tracking on 2025 athletes. Both models score identical rows; each athlete contributes equal
weight to RMSE. Evaluation-player intercepts are never fitted.

**None of the nine primary marginal intervals supports an RMSE gain.** Every original-family
simultaneous interval includes zero. This is uncertainty about added value, not evidence of equivalence.'''),
        code("figure('cohort_prediction')"),
        md('''*Figure 5. All nine primary tracking additions, with athlete-bootstrap uncertainty.
Positive RMSE gain means better prediction. Intervals condition on the training fits.*'''),
        code('evaluation_table()'),
        md('''*Table 1. Equal-athlete RMSE in the original outcome units. Gain is baseline minus
tracking RMSE; the 95% intervals omit training-fit uncertainty.*

For WR TURN, the baseline RMSE is **0.23572 yd** and tracking RMSE is **0.23577 yd**
on 23 evaluation athletes. A secondary DL A0 comparison with observed cone times improves by
**0.00755 s [0.00443, 0.01080]**, but includes only **nine athletes**. The full appendix retains
this result, the positive historical DL TURN/pressure association, and uncertain/adverse subset findings.
Missing cone times are never imputed.

**Validation context:** earlier studies already used 2025 outcomes. This is a retrospective cohort
split, not a pristine holdout or a draft-time forecast. All 25 prescribed model pairs are refitted
before evaluation scoring, using training-only preprocessing. Binary outcomes use the disclosed
player-clustered linear-probability fallback without clipping.'''),
        md('''## 06 · A scout’s evidence card

Use tracking to make a specific film question: where does a player turn efficiently, build speed,
or lose momentum? Carry that question into game review. The evidence is stronger for describing
movement than for assigning an automatic draft upgrade.'''),
        code("figure('scout_evidence_card')"),
        md('''*Figure 6. A practical evidence map separating measurement, movement transfer and added
performance prediction. Film/practice review is a proposed use, not a validated intervention.*

The limits matter: small evaluation samples, prior 2025 exposure, omitted training uncertainty,
selection into NFL playing time and cone testing, observational context, and incomplete opponent
tracking. Supplied separation is measured at the pass-forward event, not a break-specific causal effect.'''),
        md('''---
## Reproduction and complete record

**Run All** rebuilds the six figures and table from all nine competition CSVs in a fresh directory.
On Kaggle, attach the competition data and enable Internet for the recorded dependencies.
Locally, set `BDB_INPUT_ROOT` to the raw CSV folder and `BDB_NOTEBOOK_PATH` to this notebook.
No private repository or fitted-coefficient cache is required.

The ordinary source files and their SHA-256 manifest are stored in notebook metadata, keeping
the setup cell readable. Detailed logs, fit warnings, sample attrition and full reports are saved
under the run’s `reports/` directory. The assertion references are checked only after refitting.
Recorded historical W1/W2 + cone retries are reproduced; W1 uses a stable row order to keep
numerical joins from changing its recorded BFGS → L-BFGS path.'''),
        code('evidence_notes()'),
        code('appendix()'),
        md('''**Attribution:** NFL / NFL Big Data Bowl 2027, competition data under CC BY-NC 4.0.
Prepared code: MIT, with the license included in the source metadata.
[Official competition data](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/data).'''),
        code('finish()', quiet=True),
    ]
    nbformat.write(nb,ROOT/'notebooks/submission.ipynb')
    metadata = {'id':'oppenheimer6th/combine-movement-to-nfl-decisions-an-evidence-map',
                'title':'Combine Movement to NFL Decisions: An Evidence Map',
                'code_file':'submission.ipynb','language':'python','kernel_type':'notebook',
                'is_private':json.loads((ROOT/'notebooks/kernel-metadata.json').read_text()).get('is_private',True)
                             if (ROOT/'notebooks/kernel-metadata.json').exists() else True,
                'enable_gpu':False,'enable_internet':True,
                'dataset_sources':[],'competition_sources':['nfl-big-data-bowl-2027'],
                'kernel_sources':[]}
    (ROOT/'notebooks/kernel-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    (ROOT/'reports/submission_source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Built {len(nb.cells)} standalone cells; {len(files)} embedded source/reference files.')


if __name__=='__main__':
    main()
