"""Draft figures from audited outputs and an exposure-only route-trace rule."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def transfer_panel():
    rows = json.loads((ROOT/'reports/transfer_audit.json').read_text())['rows']
    fig,axes = plt.subplots(1,2,figsize=(9,3.8),layout='constrained')
    for ax,pos,trait,label in zip(axes,['WR','DL'],['lat','burst'],['Receiver turning','Defensive-line burst']):
        data = [r for r in rows if r['scope']=='corrected, PRE+REG'
                and r['position']==pos and r['trait']==trait]
        for y,row,color in zip([2,1,0],data,['#0072B2','#D55E00','#009E73']):
            ax.errorbar(row['r'],y,xerr=[[row['r']-row['lo']],[row['hi']-row['r']]],
                        fmt='o',color=color,capsize=3)
            ax.text(.66,y,f"{row['r']:.2f}",va='center',fontsize=10)
        ax.set(yticks=[2,1,0],yticklabels=['Unadjusted','Weight adjusted','Size + 40 adjusted'],
               xlim=(-.05,.73),ylim=(-.5,2.5),xlabel='Correlation (95% athlete-bootstrap interval)')
        ax.set_title(f"{label} · n={data[0]['n']} athletes",fontsize=11)
        ax.axvline(0,color='#888888',lw=.8)
        ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Movement carries over; body size explains part of DL burst\nPRE + REG games; 2,000 athlete bootstrap resamples',fontsize=12)
    fig.savefig(ROOT/'reports/figures/transfer_audited.png',dpi=200)
    plt.close(fig)


def route_trace():
    path = ROOT/'data/interim'
    p = pd.read_parquet(path/'combine_results.parquet')
    turn = pd.read_parquet(path/'study3_turn.parquet')
    p = p.merge(turn,validate='one_to_one')
    p = p[(p.combine_position=='WR')&p.draft_year.isin([2023,2024])&p.forty.notna()].copy()
    all_dev = turn.merge(pd.read_parquet(path/'combine_results.parquet'),validate='one_to_one')
    all_dev = all_dev[(all_dev.combine_position=='WR')&all_dev.draft_year.isin([2023,2024])]
    p['TURN_z'] = (p.TURN-all_dev.TURN.mean())/all_dev.TURN.std(ddof=1)
    p = p.sort_values('nfl_id')
    candidates = []
    for i,a in enumerate(p.itertuples()):
        for b in list(p.itertuples())[i+1:]:
            if abs(a.forty-b.forty)<=.03+1e-12:
                candidates.append((abs(a.TURN_z-b.TURN_z),int(a.nfl_id),int(b.nfl_id)))
    if not candidates:
        raise ValueError('No pair satisfies the exposure-only trace rule')
    _,a,b = sorted(candidates,key=lambda r:(-r[0],r[1],r[2]))[0]
    selected = p[p.nfl_id.isin([a,b])].sort_values('TURN_z')
    frames = pd.read_parquet(path/'combine_frames.parquet',
        columns=['nfl_id','event_id','drill','attempt','time','x','y','a_lat'])
    frames = frames[frames.nfl_id.isin([a,b])&(frames.drill=='SPEED_OUT_ROUTE_LEFT')]
    attempt_traits = pd.read_parquet(path/'combine_attempts.parquet').set_index('event_id')
    fig,axes = plt.subplots(2,2,figsize=(9,7.2),layout='constrained')
    metadata = []
    for col,(row,color,label) in enumerate(zip(selected.itertuples(),['#0072B2','#D55E00'],['A','B'])):
        attempt = frames[frames.nfl_id==row.nfl_id].sort_values(['attempt','event_id','time'])
        event = attempt.iloc[0].event_id
        f = attempt[attempt.event_id==event].sort_values('time')
        x,y = f.x-f.x.iloc[0],f.y-f.y.iloc[0]
        elapsed = (f.time-f.time.iloc[0]).dt.total_seconds()
        axes[0,col].plot(x,y,color=color,lw=2)
        axes[0,col].scatter([0],[0],color=color,s=28)
        axes[0,col].set(xlabel='Start-relative x (yards)',ylabel='Start-relative y (yards)',aspect='equal')
        axes[0,col].set_title(f"WR {label} · 40: {row.forty:.2f} s\nCombine TURN: {row.TURN_z:+.2f} athlete SD",fontsize=11)
        axes[1,col].plot(elapsed,np.abs(f.a_lat),color=color,lw=1.6)
        q=float(attempt_traits.loc[event,'lat'])
        axes[1,col].axhline(q,color=color,ls='--',lw=.9,label=f'Attempt 90th percentile: {q:.2f}')
        axes[1,col].set(xlabel='Attempt time (seconds)',ylabel='Absolute lateral acceleration (yd/s²)')
        axes[1,col].legend(frameon=False,fontsize=8)
        metadata.append(dict(label=f'WR {label}',nfl_id=int(row.nfl_id),event_id=event,
                             forty=float(row.forty),TURN_z=float(row.TURN_z),
                             frames=len(f),attempt_turn=q))
    # Comparable geometry/acceleration axes, without rotating or deforming the trace.
    for row_axes in axes:
        xlim=[min(ax.get_xlim()[0] for ax in row_axes),max(ax.get_xlim()[1] for ax in row_axes)]
        ylim=[min(ax.get_ylim()[0] for ax in row_axes),max(ax.get_ylim()[1] for ax in row_axes)]
        for ax in row_axes:
            ax.set(xlim=xlim,ylim=ylim)
            ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Similar 40 times, different movement across Combine drills\nActual speed-out traces; TURN averages multiple non-40 drills',fontsize=13)
    fig.savefig(ROOT/'reports/figures/combine_route_trace.png',dpi=200)
    plt.close(fig)
    (ROOT/'reports/route_trace_selection.json').write_text(json.dumps(dict(
        rule='2023/24 WRs with observed forty, within 0.03 s; greatest training-reference TURN difference; '
             'ties by ascending athlete IDs; first recorded speed-out attempt',
        outcome_information_used=False,coordinate_transform='Translation to attempt start only',
        players=metadata),indent=2)+'\n')


def main():
    transfer_panel()
    route_trace()
    print('Saved transfer_audited.png and combine_route_trace.png; pair selection metadata recorded.')


if __name__=='__main__':
    main()
