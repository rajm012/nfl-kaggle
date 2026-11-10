"""Export the frozen cohort-evaluation table and a review figure, without refitting."""
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

from src.evaluate import ROOT

LABELS = {
    'W1':'WR turning → separation', 'W2':'WR burst → separation',
    'O1':'OL turning → pressure allowed', 'O2':'OL burst → pressure allowed',
    'D1':'DL burst → get-off time', 'D2':'DL turning → pressure generated',
    'F1':'DL first step → get-off time', 'F2':'OL first step → peak pressure allowed',
    'F3':'WR first step → separation',
}


def main():
    result = json.loads((ROOT/'reports/validation.json').read_text())
    rows = [r for r in result['results'] if r['family']=='primary']
    table = []
    fig,ax = plt.subplots(figsize=(10.5,6.4),layout='constrained')
    for y,row in zip(range(8,-1,-1),rows):
        m = row['metrics']
        point = m['relative_improvement_percent']
        color = '#0072B2' if row['study']==1 else '#D55E00'
        ax.errorbar(point,y,xerr=[[point-m['relative_lo']],[m['relative_hi']-point]],
                    fmt='o',color=color,capsize=3,lw=1.6)
        ax.text(10.5,y,f"n={m['players']} · {point:+.2f}%",va='center',fontsize=9)
        unit = 'yards' if row['position']=='WR' else (
            'seconds' if row['outcome']=='player_get_off' else 'proportion')
        table.append(dict(test=row['id'],comparison=LABELS[row['id']],units=unit,
            training_players=row['training_players'],evaluation_players=m['players'],
            baseline_RMSE=m['rmse0'],tracking_RMSE=m['rmse1'],RMSE_improvement=m['improvement'],
            improvement_95_lo=m['improvement_lo'],improvement_95_hi=m['improvement_hi'],
            family_interval_lo=m['simultaneous_lo'],family_interval_hi=m['simultaneous_hi'],
            baseline_MAE=m['mae0'],tracking_MAE=m['mae1']))
    ax.set(yticks=range(8,-1,-1),yticklabels=[LABELS[r['id']] for r in rows],
           xlabel='Relative reduction in equal-player RMSE (%) · positive is better',
           xlim=(-19,17),ylim=(-.7,8.7))
    ax.axvline(0,color='#666666',lw=1,ls='--')
    ax.spines[['top','right']].set_visible(False)
    ax.set_title('No primary tracking addition shows a supported prediction gain\n'
                 '2025 rookie REG; fixed 2023–24 development models',loc='left',fontsize=12)
    fig.supxlabel('Bars: marginal 95% paired athlete-bootstrap intervals, conditional on training fits.\n'
                   'Prior studies used 2025 outcomes; this is not a pristine holdout.',fontsize=9)
    fig.savefig(ROOT/'reports/figures/cohort_prediction.png',dpi=200)
    plt.close(fig)
    pd.DataFrame(table).to_csv(ROOT/'reports/evaluation_table.csv',index=False)
    print('Saved cohort_prediction.png and evaluation_table.csv; no model refits.')


if __name__=='__main__':
    main()
