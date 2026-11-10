"""Embed the conventional measurement screen in the existing portable notebook.

Run once after modifying the shared screen helpers. The generated notebook
contains their source and needs no unpublished src modules at runtime.
"""
import inspect
from pathlib import Path

import nbformat

from src.reliability import paired_reliability
from src.route_context import (baseline_design, independent_columns, measurement_screen,
                               plot_screen, preprocess_development)

ROOT = Path(__file__).resolve().parents[1]


def main():
    target = ROOT/'notebooks/submission.ipynb'
    nb = nbformat.read(target,as_version=4)
    # Keep the original input/eligibility starter, replacing any prior generated screen.
    nb.cells = nb.cells[:7]
    nb.cells[0].source = '''# What Combine movement can tell a scout — notebook in progress

This working version reproduces input integrity, receiver eligibility and the frozen
route-family separation measurement screen from four competition input tables.
It fits only the conventional baseline on 2023–24 rookie REG plays. No TURN–separation
association or 2025 performance evaluation is run here.

The adjusted measurement reliability failed the prespecified screen on November 9,
so the primary route-performance claim stops. Earlier Studies 1–2 included 2025 outcomes;
we do not describe that cohort as a pristine holdout. Their audited models and movement
reliability/transfer still need integration before this becomes the complete submission.

Local runs accept CSV or Parquet; Kaggle discovers the four competition CSVs. Only
development receiver rows enter pandas for the measurement model. No helper modules,
remote server or credentials are required at runtime.'''
    nb.cells[6].source = nb.cells[6].source.replace('\ncon.close()','')
    nb.cells.append(nbformat.v4.new_markdown_cell('''## Frozen outcome measurement screen

The screen asks whether a receiver's SLANT/OUT-minus-GO separation contrast repeats
across alternating rookie games. It does not test Combine TURN against separation.
Eligibility is ≥10 plays in each family; diagnostic halves require ≥3 in each family.

The conventional weighted model uses player intercepts, separate route/down/coverage/
alignment terms, yards-to-go, motion, cushion/missingness and conventional-measurable
family interactions. Every athlete/family gets equal total weight. Player scaling uses
unique development-class WRs; no 2025 outcomes enter the fit or diagnostic.

Subtracting this baseline shares estimated adjustments across halves, so adjusted
reliability is descriptive. The frozen gate requires ≥25 diagnostic athletes and
Spearman–Brown point reliability ≥0.40. Wide intervals remain relevant to interpretation.'''))
    functions = '\n\n'.join(inspect.getsource(f) for f in [
        paired_reliability,independent_columns,preprocess_development,
        baseline_design,measurement_screen,plot_screen])
    nb.cells.append(nbformat.v4.new_code_cell(
        'import numpy as np\nimport statsmodels.api as sm\nimport json\n'
        'SEED = 20261109\n'
        "CONVENTIONAL = ['weight_z', 'height_z', 'forty_z', 'pick_z', 'udfa', 'forty_missing']\n"
        "CATEGORICAL = ['route_ran', 'down', 'team_coverage_man_zone', 'receiver_alignment']\n\n"
        + functions))
    nb.cells.append(nbformat.v4.new_code_cell('''# Materialise only 2023–24 candidate WR outcomes and small conventional reference.
reference = con.sql("""SELECT c.*,p.draft_overall_pick FROM combine_results c
    JOIN players p USING(nfl_id)
    WHERE c.combine_position='WR' AND c.draft_year IN (2023,2024)""").df()
dev = con.sql("""SELECT pp.*,c.draft_year,c.combine_position,c.forty,
    c.combine_weight,c.combine_height,p.draft_overall_pick
    FROM player_play pp JOIN games g USING(game_id)
    JOIN combine_results c USING(nfl_id) JOIN players p USING(nfl_id)
    WHERE c.combine_position='WR' AND c.draft_year IN (2023,2024)
      AND g.season_type='REG' AND g.season=c.draft_year
      AND pp.play_nullified_by_penalty='N' AND pp.route_ran IN ('SLANT','OUT','GO')
      AND pp.separation_at_pass_forward IS NOT NULL""").df()
dev['BREAK'] = (dev.route_ran!='GO').astype(int)
counts = dev.groupby(['nfl_id','BREAK']).size().unstack(fill_value=0)
eligible = counts.index[(counts[0]>=10)&(counts[1]>=10)]
dev = dev[dev.nfl_id.isin(eligible)].dropna(subset=[
    'down','yards_to_go','combine_weight','combine_height']).copy()
counts = dev.groupby(['nfl_id','BREAK']).size().unstack(fill_value=0)
eligible = counts.index[(counts[0]>=10)&(counts[1]>=10)]
dev = dev[dev.nfl_id.isin(eligible)].copy()
assert dev.draft_year.isin([2023,2024]).all()
assert dev.nfl_id.nunique() >= 35
dev, metadata = preprocess_development(dev,reference,include_turn=False)
x, weights, dropped = baseline_design(dev,metadata)
rows, contrasts, baseline, passes = measurement_screen(dev,x,weights)
display(pd.DataFrame(rows))
summary = {'development_players':int(dev.nfl_id.nunique()),'development_plays':len(dev),
    'design_rank':x.shape[1],'dropped_columns':dropped,'diagnostic':rows,
    'screen_passes':bool(passes),'primary_TURN_association_fitted':False,
    'evaluation_outcomes_opened':False}
print('Measurement gate:', 'PASS' if passes else 'FAIL — stop primary route-performance claim')
Path('reports').mkdir(exist_ok=True)
Path('reports/notebook_measurement.json').write_text(json.dumps(summary,indent=2,allow_nan=False))
plot_screen(contrasts,rows,out/'study3_measurement.png')
from IPython.display import Image, display
display(Image(filename=str(out/'study3_measurement.png')))
con.close()'''))
    nb.cells.append(nbformat.v4.new_markdown_cell('''## Interpretation and remaining work

The local run gives 41 diagnostic development receivers. Adjusted correlation is
approximately 0.17 (95% bootstrap interval −0.11 to 0.43); Spearman–Brown is approximately
0.30, below the frozen 0.40 gate. The interval is wide. This failure limits the route-family
performance claim; it does not establish that Combine movement has no value.

The project now follows the planned evidence-map narrative: distinguish reproducible
movement, transfer into games and evidence of additional performance prediction.
Historical model audits still show no Holm-significant added associations, but held-out
prediction and the small 3-cone sensitivity must be completed before final claims.
Full feature rebuilding, audit integration, final figures and clean Kaggle execution remain
pending. This notebook is not ready for publication or submission.'''))
    for cell in nb.cells:
        if cell.cell_type=='code':
            cell.outputs = []
            cell.execution_count = None
            cell.metadata.pop('execution',None)
    nbformat.write(nb,target)
    print(f'Updated {target}')


if __name__=='__main__':
    main()
