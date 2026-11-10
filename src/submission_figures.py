"""Final support figure and scout evidence card from regenerated artifacts only."""
import json
from pathlib import Path

import duckdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd

from src.audit_data import sql_path

ROOT = Path(__file__).resolve().parents[1]
BLUE, ORANGE, GREEN, INK = '#0072B2', '#D55E00', '#009E73', '#253747'


def support():
    con = duckdb.connect()
    con.execute("SET memory_limit='256MB'")
    for name in ['combine_results', 'combine_traits', 'sprint_traits']:
        con.execute(f'CREATE VIEW {name} AS SELECT * FROM read_parquet('
                    f'{sql_path(ROOT/"data/interim"/(name+".parquet"))})')
    cohorts = con.sql('''SELECT c.combine_position AS position,c.draft_year,
        count(*) AS total,count(t.nfl_id) AS movement,count(s.nfl_id) AS sprint
        FROM combine_results c LEFT JOIN combine_traits t USING(nfl_id)
        LEFT JOIN sprint_traits s USING(nfl_id)
        WHERE c.combine_position IN ('WR','OL','DL')
        GROUP BY c.combine_position,c.draft_year ORDER BY c.combine_position,c.draft_year''').df()
    con.close()
    validation = json.loads((ROOT/'reports/validation.json').read_text())
    lookup = {r['id']:r for r in validation['results']}
    fig, axes = plt.subplots(1,3, figsize=(11.5,4.4), layout='constrained', sharey=True)
    values = []
    for ax,pos,primary,first in zip(axes,['WR','OL','DL'],['W1','O1','D1'],['F3','F2','F1']):
        d = cohorts[(cohorts.position==pos)&(cohorts.draft_year==2025)].iloc[0]
        counts = [int(d.total),int(d.movement),lookup[primary]['metrics']['players'],
                  lookup[first]['metrics']['players']]
        labels = ['Combine cohort','Non-40 movement','Primary REG outcome','Sprint + REG outcome']
        ax.barh(range(3,-1,-1),counts,color=[INK,BLUE,BLUE,ORANGE],height=.58)
        for y,n in zip(range(3,-1,-1),counts):
            ax.text(n+.6,y,str(n),va='center',fontsize=12,fontweight='bold',color=INK)
        ax.set(yticks=range(3,-1,-1),yticklabels=labels,xlim=(0,max(cohorts.total.max()+5,44)),
               xlabel='Unique athletes')
        ax.set_title(pos,loc='left',fontweight='bold',color=INK)
        ax.spines[['top','right','left']].set_visible(False)
        values.append({'position':pos,'counts':dict(zip(labels,counts))})
    fig.suptitle('The independent evaluation sample is athletes, not plays\n2025 rookie cohort; outcome and exposure availability determine support',
                 fontsize=14,x=.01,ha='left',color=INK)
    fig.supxlabel('Displayed outcome: WR separation, OL pressure allowed, DL get-off.\n'
                  'First-step samples require sprint tracking; comparisons use the same rows within each test.',fontsize=9)
    fig.savefig(ROOT/'reports/figures/evidence_support.png',dpi=200)
    plt.close(fig)
    (ROOT/'reports/evidence_support.json').write_text(json.dumps(values,indent=2)+'\n')


def evidence_card():
    reliability = json.loads((ROOT/'reports/reliability.json').read_text())
    turn = next(r for r in reliability['cross_drill'] if r['position']=='WR'
                and r['feature']=='TURN' and r['sample']=='development, training reference')
    transfer = json.loads((ROOT/'reports/transfer_audit.json').read_text())
    move = next(r for r in transfer['rows'] if r['position']=='WR' and r['trait']=='lat'
                and r['scope']=='corrected, PRE+REG' and r['adjustment']=='raw')
    validation = json.loads((ROOT/'reports/validation.json').read_text())
    score = next(r for r in validation['results'] if r['id']=='W1')['metrics']
    measurement = json.loads((ROOT/'reports/study3_measurement.json').read_text())
    adjusted = next(r for r in measurement['diagnostic'] if r['contrast']=='adjusted')
    fig,ax = plt.subplots(figsize=(10.8,6.8))
    fig.subplots_adjust(left=.025,right=.975,top=.96,bottom=.03)
    ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
    ax.text(.02,.96,'WR turning: a scout’s evidence card',fontsize=21,fontweight='bold',color=INK)
    rows = [
        ('MEASUREMENT','Cross-drill consistency',
         f"SB {turn['SB']:.2f} [{turn['SB_lo']:.2f}, {turn['SB_hi']:.2f}] · {turn['n']} development WRs",
         'Observe repeatable movement; this is not single-route test–retest.',BLUE),
        ('TRANSFER','Modest movement carryover',
         f"r {move['r']:.2f} [{move['lo']:.2f}, {move['hi']:.2f}] · {move['n']} WRs · PRE + REG",
         'Use as movement context alongside film; size/speed adjustment is shown separately.',GREEN),
        ('PERFORMANCE','Added prediction remains uncertain',
         f"RMSE gain {score['improvement']:+.5f} yd [{score['improvement_lo']:.5f}, {score['improvement_hi']:.5f}] · {score['players']} WRs",
         'No automatic draft upgrade or validated separation ranking.',ORANGE),
    ]
    for y,(label,title,stat,use,color) in zip([.72,.49,.26],rows):
        ax.add_patch(FancyBboxPatch((.015,y-.055),.97,.20,boxstyle='round,pad=.008',
                                    facecolor='#F3F6F8',edgecolor='#DDE4E9'))
        ax.text(.035,y+.102,label,fontsize=9,fontweight='bold',color=color)
        ax.text(.035,y+.058,title,fontsize=15,fontweight='bold',color=INK)
        ax.text(.035,y+.015,stat,fontsize=11,color=INK)
        ax.text(.035,y-.023,use,fontsize=10,color=INK)
    ax.text(.025,.11,f"Route-family screen: adjusted SB {adjusted['SB']:.2f} < frozen 0.40 gate; primary interaction not fitted.",
            fontsize=10,color=INK)
    ax.text(.025,.065,'Intervals: 95% athlete bootstrap. Prediction is conditional on trained models and realised NFL contexts.\n'
            'Prior 2025 exposure disclosed. Observational evidence does not establish a causal training benefit.',fontsize=9,color=INK)
    fig.savefig(ROOT/'reports/figures/scout_evidence_card.png',dpi=200)
    plt.close(fig)


def main():
    (ROOT/'reports/figures').mkdir(exist_ok=True)
    support()
    evidence_card()
    print('Saved evidence_support.png and scout_evidence_card.png; no new model fits.')


if __name__=='__main__':
    main()
