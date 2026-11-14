"""Render a 560 x 280 card from the already selected Combine trajectories."""
import json
from pathlib import Path

import polars as pl
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def main():
    scale = 3
    img = Image.new('RGB', (560 * scale, 280 * scale), '#102b38')
    draw = ImageDraw.Draw(img)

    def line(points, fill, width=1):
        draw.line([(round(x * scale), round(y * scale)) for x, y in points],
                  fill=fill, width=width * scale, joint='curve')

    def label(x, y, text, size, color, bold=False):
        font = ImageFont.truetype('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',
                                  size * scale)
        draw.text((x * scale, y * scale), text, fill=color, font=font)

    for y in range(39, 235, 28):
        line([(349, y), (537, y)], '#274450')
        for x in (395, 483):
            line([(x, y - 3), (x, y + 3)], '#48606a')
    line([(333, 35), (333, 232)], '#48606a')
    line([(29, 39), (67, 39)], '#79cbd3', 3)
    label(29, 54, 'BEYOND THE', 25, '#ffffff', True)
    label(29, 86, 'STOPWATCH', 32, '#ffffff', True)
    label(29, 140, 'When should tracking change', 15, '#d7e8ec')
    label(29, 163, 'a scouting decision?', 15, '#d7e8ec')
    label(29, 226, 'NFL BIG DATA BOWL 2027', 12, '#9bc1ca', True)

    selection = json.loads((ROOT / 'reports/route_trace_selection.json').read_text())
    players = selection['players']
    frames = (pl.scan_parquet(ROOT / 'data/interim/combine_frames.parquet')
              .filter(pl.col('event_id').is_in([p['event_id'] for p in players]))
              .select('event_id', 'time', 'x', 'y').collect())
    # Same origin translation and one common yard-to-pixel scale for both attempts.
    for player, color in zip(players, ('#79cbd3', '#efb15a')):
        rows = frames.filter(pl.col('event_id') == player['event_id']).sort('time')
        coords = list(zip(rows['x'].to_list(), rows['y'].to_list()))
        x0, y0 = coords[0]
        points = [(354 + (x - x0) * 10.5, 218 - (y - y0) * 10.5)
                  for x, y in coords]
        line(points, color, 3)
        for x, y in points[::7]:
            draw.ellipse(((x - 2.5) * scale, (y - 2.5) * scale,
                          (x + 2.5) * scale, (y + 2.5) * scale), fill=color)
    label(351, 248, 'COMBINE SPEED-OUT TRACKS', 9, '#9bc1ca')
    out = ROOT / 'writeup/assets/thumbnail.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    img.resize((560, 280), Image.Resampling.LANCZOS).save(out)
    print(out)


if __name__ == '__main__':
    main()
