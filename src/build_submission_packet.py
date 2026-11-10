"""Build a standalone writeup preview, assets and conservative count checks."""
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import zipfile

import mistune
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def notebook_preview(source, target):
    """Export the saved notebook as a standalone reading preview with code hidden."""
    import nbformat
    from nbconvert import HTMLExporter
    notebook = nbformat.read(source, as_version=4)
    exporter = HTMLExporter(template_name='basic')
    exporter.exclude_input = True
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    content, _ = exporter.from_notebook_node(notebook)
    style = '''body{max-width:1040px;margin:48px auto;padding:0 26px;color:#253747;background:white;
        font:17px/1.7 system-ui,sans-serif}h1{font-size:42px;line-height:1.15;margin-bottom:12px}
        h2{font-size:27px;line-height:1.3;margin-top:42px}h3{font-size:20px;color:#527184}
        p{margin:14px 0}a{color:#0072b2}img{max-width:100%;height:auto}
        .prompt{display:none}.output_subarea{padding:0;margin:18px 0}.anchor-link{display:none}
        pre{padding:16px;background:#f4f7fa;overflow-x:auto;font-size:12px;line-height:1.5}
        table{border-collapse:collapse;font-size:13px}td,th{padding:8px;border-bottom:1px solid #dce4eb}
        details{margin:10px 0}summary{cursor:pointer}hr{border:0;border-top:1px solid #dce4eb;margin-top:40px}
        @media(max-width:640px){body{margin:24px auto;padding:0 16px;font-size:15px}h1{font-size:32px}}'''
    target = Path(target)
    target.write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
                      '<meta name="viewport" content="width=device-width,initial-scale=1">'
                      '<title>Beyond the stopwatch — notebook preview</title><style>'+style+
                      '</style><body>'+content+'</body></html>')


def word_count(text):
    # Count captions, headings and table cells. Include image alt text conservatively.
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',text)
    text = re.sub(r'<!--.*?-->','',text,flags=re.S)
    return len(re.findall(r"\b[\w]+(?:[’'−–.-][\w]+)*\b",text))


def main():
    table = pd.read_csv(ROOT/'reports/evaluation_table.csv')
    lines = ['| Comparison | Unit | Athletes | Baseline RMSE | + Tracking RMSE | RMSE gain [95% interval] |',
             '|---|---|---:|---:|---:|---:|']
    for r in table.itertuples(index=False):
        label = r.comparison.replace(' → ',' / ')
        unit = {'yards':'yd','seconds':'s','proportion':'proportion'}[r.units]
        lines.append(f'| {label} | {unit} | {r.evaluation_players} | {r.baseline_RMSE:.5f} | '
                     f'{r.tracking_RMSE:.5f} | {r.RMSE_improvement:+.5f} '
                     f'[{r.improvement_95_lo:.5f}, {r.improvement_95_hi:.5f}] |')
    table_md = '\n'.join(lines)+'\n\n*Table 1. Equal-athlete RMSE; positive gain is better. '
    table_md += 'Marginal 95% intervals condition on training fits; all original-family simultaneous intervals include zero.*'
    target = ROOT/'writeup/writeup.md'
    text = target.read_text()
    begin,end = '<!-- EVALUATION_TABLE -->','<!-- END_EVALUATION_TABLE -->'
    if end in text:
        text = re.sub(re.escape(begin)+'.*?'+re.escape(end),begin+'\n\n'+table_md+'\n\n'+end,text,flags=re.S)
    else:
        text = text.replace(begin,begin+'\n\n'+table_md+'\n\n'+end)
    target.write_text(text)
    figures = re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text)
    if len(figures)!=6 or text.count('|---|')!=1:
        raise AssertionError('Expected six figures and one table')
    count = word_count(text)
    if count>2000:
        raise AssertionError(f'Writeup exceeds limit: {count} words')
    html = mistune.create_markdown(plugins=['table'])(text)
    for relative in figures:
        image_path = (target.parent/relative).resolve()
        encoded = base64.b64encode(image_path.read_bytes()).decode()
        html = html.replace('src="'+relative+'"','src="data:image/png;base64,'+encoded+'"')
    style = '''body{max-width:1000px;margin:40px auto;padding:0 24px;color:#253747;background:white;
        font:18px/1.65 system-ui,sans-serif}h1{font-size:36px;line-height:1.2}h2{font-size:25px;margin-top:36px}
        img{width:100%;height:auto}table{border-collapse:collapse;font-size:12px;width:100%}
        th,td{padding:8px;border-bottom:1px solid #dce4e9;text-align:left}th{background:#f3f6f8}
        em{font-size:15px;color:#4e6475}a{color:#0072b2}strong{font-weight:650}'''
    preview = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
    preview += '<title>Combine movement evidence map</title><style>'+style+'</style><body>'+html+'</body></html>'
    (target.parent/'preview.html').write_text(preview)
    notebook_preview(ROOT/'notebooks/submission.ipynb', target.parent/'notebook_preview.html')
    paths = [target,ROOT/'notebooks/submission.ipynb',ROOT/'notebooks/kernel-metadata.json']
    paths += [target.parent/'notebook_preview.html']
    paths += [(target.parent/p).resolve() for p in figures]
    platform_path = ROOT/'reports/kaggle_execution.json'
    platform = json.loads(platform_path.read_text()) if platform_path.exists() else {}
    report = {'generated_utc':datetime.now(timezone.utc).isoformat(),
              'word_count_conservative_including_alt_text':count,'word_limit':2000,
              'figures':len(figures),'tables':1,'combined_visuals':7,
              'assets':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              'local_preview':'writeup/preview.html',
              'notebook_reading_preview':'writeup/notebook_preview.html',
              'public_notebook_verified':platform.get('public_access_verified',False),
              'notebook_url':platform.get('notebook_url'),
              'final_submission_complete':False}
    (ROOT/'reports/submission_packet.json').write_text(json.dumps(report,indent=2)+'\n')
    extra = [ROOT/'LICENSE',ROOT/'README.md',target.parent/'preview.html',
             ROOT/'reports/submission_packet.json',ROOT/'reports/submission_verification.json',
             ROOT/'reports/full_notebook_execution.json',ROOT/'reports/official_sources.md',
             ROOT/'reports/submission_handoff.md',ROOT/'reports/kaggle_execution.json',
             ROOT/'reports/kaggle_publication.json',ROOT/'reports/kaggle_full_notebook_execution.json',
             ROOT/'reports/kaggle_submission_verification.json']
    with zipfile.ZipFile(target.parent/'submission_packet.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in paths + extra:
            if path.exists():
                archive.write(path,str(path.relative_to(ROOT)))
    print(f'Built standalone HTML preview; {count} conservative words, six figures and one table.')


if __name__=='__main__':
    main()
