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
           'submission_pipeline','submission_figures','submission_verify','submission_replay']


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
                    'recorded_optimizer':model['optimizer']}
                   for r in cone['comparisons'] for name,model in r['models'].items()
                   if 'Powell' in model['optimizer']]
    files['reports/historical_solver_plan.json'] = json.dumps(solver_plan,indent=2)+'\n'
    frozen_source = json.loads((ROOT/'reports/evaluation_development.json').read_text())['provenance']
    for name in ['src/evaluate.py','src/route_context.py','requirements.txt','reports/evaluation_protocol.md']:
        if hashlib.sha256(files[name].encode()).hexdigest()!=frozen_source[name]:
            raise ValueError('Frozen specification changed: '+name)
    manifest = {name:hashlib.sha256(value.encode()).hexdigest() for name,value in files.items()}
    nb = nbformat.v4.new_notebook()
    nb.metadata = {'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                   'language_info':{'name':'python'},'bdb_source_sha256':manifest}
    md,code = nbformat.v4.new_markdown_cell,nbformat.v4.new_code_cell
    nb.cells = [md('''# From Combine movement to NFL decisions: an evidence map

**Some movement transfers; added performance prediction remains uncertain.** This notebook
rebuilds every submission figure and the nine-primary-comparison table from the nine competition
CSVs. It includes the original source so no unpublished repository, cache, remote machine or
credential is needed. Every development model is refitted and frozen before evaluation scoring.

2025 outcomes were used in earlier studies. The cohort split below is retrospective conditional
validation, not a pristine holdout or a draft-time forecast. The route-family measurement gate
failed; no TURN interaction is fitted. Selected favourable and adverse cone findings remain secondary.

Code: MIT license (embedded in the source bundle). Data attribution: NFL / NFL Big Data Bowl 2027,
competition data (CC BY-NC 4.0). The code license does not relicense competition data.
Official source: https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/data .
Local use: set `BDB_INPUT_ROOT` to the raw CSV folder. Each Run All creates a fresh output directory.'''),
    code('''import os, sys, json, hashlib, tempfile, time, subprocess
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
os.environ.update(OPENBLAS_NUM_THREADS='2', OMP_NUM_THREADS='2', POLARS_MAX_THREADS='2', MPLBACKEND='Agg')
STARTED = time.monotonic()
INPUT_NAMES = ['players.csv','combine_results.csv','combine_tracking.csv','games.csv',
               'player_play.csv','player_career_successes.csv',
               'game_tracking_2023.csv','game_tracking_2024.csv','game_tracking_2025.csv']
input_base = Path(os.environ.get('BDB_INPUT_ROOT', '/kaggle/input'))
inputs = {}
for name in INPUT_NAMES:
    matches = sorted(input_base.rglob(name))
    if len(matches)!=1:
        raise ValueError(f'Expected one {name} under {input_base}; found {len(matches)}')
    inputs[name] = matches[0].resolve()
output_base = Path('/kaggle/working') if Path('/kaggle/working').exists() else Path(tempfile.gettempdir())
run_root = Path(tempfile.mkdtemp(prefix='bdb_raw_rebuild_', dir=output_base))
for directory in ['src','tests','reports/figures','data/raw','data/interim']:
    (run_root/directory).mkdir(parents=True, exist_ok=True)
for name,path in inputs.items():
    (run_root/'data/raw'/name).symlink_to(path)
print('Fresh raw-input rebuild:', run_root)
print('Input CSVs:', sorted(inputs))'''),
    md('''## Source and environment

The expandable source cell writes the frozen statistical modules and the bounded data pipeline
into the fresh working directory. The reference JSON is used only for assertions **after** all
fits and scores; it never supplies results or coefficients. CSV and source hashes are recorded.
Kaggle installs the recorded package versions when needed (Internet must be enabled).'''),
    code('SOURCE_FILES = json.loads('+repr(json.dumps(files))+')\n'
         'SOURCE_HASHES = json.loads('+repr(json.dumps(manifest))+')\n'
         '''for name,source in SOURCE_FILES.items():
    if hashlib.sha256(source.encode()).hexdigest()!=SOURCE_HASHES[name]:
        raise AssertionError('Embedded source integrity: '+name)
    (run_root/name).write_text(source)
runtime_packages = ['duckdb','polars','numpy','pandas','scipy','statsmodels','matplotlib']
required = dict(line.split('==') for line in SOURCE_FILES['requirements.txt'].splitlines()
                if line and not line.startswith('#'))
mismatches = []
for package in runtime_packages:
    try:
        installed = version(package)
    except PackageNotFoundError:
        installed = None
    if installed!=required[package]:
        mismatches.append(f'{package}=={required[package]}')
if mismatches:
    subprocess.run([sys.executable,'-m','pip','install','--quiet',*mismatches],check=True)
print({p:version(p) for p in runtime_packages})
sys.path.insert(0,str(run_root))
from src.submission_pipeline import run_stage
def run(module,*arguments):
    run_stage(run_root,'src.'+module,arguments)
'''),
    md('''## Raw data → movement measurements

Positions are smoothed at 10 Hz; signed acceleration is decomposed into longitudinal and lateral
components. TURN uses attempt 90th-percentile absolute lateral acceleration; BURST uses peak
longitudinal acceleration. Non-40 attempt means are standardised within drill, then averaged
within athlete. Prediction drill references use 2023–24 athletes only. A0 comes from the existing
40-yard speed-curve fit. Game traits use complete tracks for smoothing and a snap-to-three-second
window. Whole-game batches reduce memory without cutting any player track.'''),
    code("run('submission_pipeline','--convert')\nrun('combine_features')\nrun('sprint')"),
    code("run('game_features')\nrun('audit_data')\nrun('join_audit')"),
    md('''## Measurement and transfer

Cross-drill consistency is distinct from same-route test–retest. Movement transfer is descriptive
across available seasons, using PRE + REG and excluding POST; it is not performance prediction.
The frozen SLANT/OUT-minus-GO contrast screen uses 2023–24 rookie REG outcomes only. If it fails,
the primary TURN interaction remains stopped.'''),
    code("run('reliability')\nrun('route_context')\nrun('transfer_audit')\nrun('validation')"),
    md('''## Development freeze → cohort evaluation → cone sensitivity

All 25 prescribed baseline/augmented pairs are refitted before any evaluation score is calculated:
nine primary, seven original secondary, nine cone-subset comparisons. Primary outcomes are rookie
REG on 2025 athletes, with 2023–24 training-only preprocessing. Predictions use fixed components,
never evaluation-player intercepts, and each athlete receives equal weight in RMSE. Baseline and
tracking models score identical rows. Paired athlete-bootstrap intervals condition on trained
models and omit training-fit uncertainty. The latest trained calendar intercept is assumed to persist.

Binary outcomes use the disclosed player-clustered linear-probability fallback without clipping.
Historical associations use all available REG seasons and are reported separately from cohort
prediction. Cone checks compare identical rows and never invent missing cone times. The original
historical WR BURST + cone fit used a Powell retry; raw rebuilding replays that recorded solver
choice because unordered joins can alter the default retry path. No model, sample or prediction
solver is changed, and no cached coefficients are used.'''),
    code("run('evaluate','--stage','develop')"),
    code("run('evaluate','--stage','evaluate')\nrun('submission_replay')"),
    md('''## Verify every headline and athlete score

Recompute the 25 equal-athlete scores, verify disjoint training/evaluation players, frozen hashes,
context-adjustment identities and agreement with the reviewed results. Tolerances account for
floating-point/optimizer reproduction; they do not define football utility or change model choices.'''),
    code("run('submission_verify')\nsubprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=run_root,check=True)"),
    code("run('audit_figures')\nrun('evaluation_figures')\nrun('submission_figures')"),
    md('''## Six figures and one evaluation table

The hero pair is selected using Combine exposure only: development WRs within 0.03 seconds
in their observed 40, largest training-reference TURN difference, deterministic athlete-ID ties.
It illustrates measurement and carries no NFL-success ranking claim.'''),
    code('''from IPython.display import Image, display, Markdown
import pandas as pd
FIGURES = ['combine_route_trace','evidence_support','transfer_audited',
           'study3_measurement','cohort_prediction','scout_evidence_card']
for index,name in enumerate(FIGURES,1):
    display(Markdown(f'**Figure {index}**'))
    display(Image(filename=str(run_root/'reports/figures'/(name+'.png'))))
table = pd.read_csv(run_root/'reports/evaluation_table.csv')
display(table[['comparison','units','evaluation_players','baseline_RMSE','tracking_RMSE',
               'improvement_95_lo','improvement_95_hi']].round(5))'''),
    md('''## Complete record and decision

The evidence map supports describing repeatable movement and modest transfer while withholding
automatic draft upgrades. Nine primary marginal intervals do not support a prediction gain;
all original-family simultaneous intervals include zero. Uncertainty is not equivalence.
The route-family contrast failed the original measurement threshold before the interaction fit.

The full cone record retains the positive nine-athlete DL A0 cohort finding and the positive
historical DL TURN/pressure coefficient, as well as uncertain/adverse findings. These selected
subsets do not establish universal performance rankings. Rebuilt reports below include all tests,
sample attrition, context mappings, fit warnings and preprocessing metadata.

Limitations: prior 2025 exposure; small evaluation samples; training uncertainty omitted; selection
into NFL playing time and cone testing; observational context; incomplete opponent/ball tracking.
Player-only coordinates cannot reconstruct opponent geometry. Separation is the supplied
pass-forward-event field, not a break-specific causal effect. Practice/film review is a proposed use.'''),
    code('''for name in ['reliability','transfer_audit','model_audit','study3_measurement','validation','cone_sensitivity']:
    display(Markdown((run_root/'reports'/(name+'.md')).read_text()))
stages = json.loads((run_root/'reports/rebuild_stages.json').read_text())
summary = {'source':'nine raw competition CSVs','cohort_pipeline_rebuilt_in_notebook':True,
           'all_headlines_verified':True,'figures':6,'tables':1,
           'elapsed_seconds':round(time.monotonic()-STARTED,2),
           'largest_stage_sampled_RSS_MiB':max(s['sampled_peak_RSS_MiB'] for s in stages),
           'versions':{p:version(p) for p in runtime_packages},'output_root':str(run_root)}
(run_root/'reports/full_notebook_execution.json').write_text(json.dumps(summary,indent=2)+'\\n')
print(json.dumps(summary,indent=2))
# Public outputs contain summaries and figures, not redistributed source/row-level data.
if Path('/kaggle/working').exists():
    import shutil
    shutil.rmtree(run_root/'data')
    print('Removed input links and intermediate row-level data from Kaggle outputs.')''')]
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
