#!/usr/bin/env python3

import re
import sys
from PIL import Image

abbrevs = {
    'BA': 'Bright Angel',
    'BAC': 'Bright Angel Creek',
    'BAH': 'Bright Angel Hiker',
    'BAT': 'Bright Angel Trail',
    'NKT': 'North Kaibab Trail',
    'NK': 'North Kaibab',
    'SKT': 'South Kaibab Trail',
    'SK': 'South Kaibab',
    'PP': 'Plateau Point',
    'A': 'A',
    'B': 'Billingsley',
    'CG': 'CG',
    'H': 'H',
    'I': 'I',
    'IMG': 'IMG',
    'PDF': 'PDF',
    'USGS': 'USGS',
    'CC': '<i class="nobr">C–C′</i>',
    'DD': '<i class="nobr">D–D′</i>',
    # s/(\d)[ap]m\b/\1 <span class="sc">pm</span>/
}

layers = {
    'Pc': 'Coconino Sandstone',
    'Mr': 'Redwall Limestone',
    'Ct': 'Tapeats Sandstone',
    'Yb': 'Bass Formation',
    'Yd': 'Dox Formation',
    'Yh': 'Hakatai Shale',
    'Yi': 'Intrusive sills and dikes',
    'Ys': 'Shinumo Quartzite',
    'Xbr': 'Brahma Schist',
    'Xgr': 'Granite',
    'Xr': 'Rama Schist',
}

def main(argv):
    text = sys.stdin.read()

    def f(match):
        url = match.group(0)
        if '-h' not in url:
            return url
        #print(url, file=sys.stderr)
        w, h = re.search(r'w(\d+)-h(\d+)', url).groups()
        return f'<img src="{url}" width={w} height={h}>'
    text = re.sub(r'https://lh3.googleusercontent.com/[^<]*', f, text)

    def f(match):
        url = match.group(1)
        im = Image.open(url)
        w, h = im.size
        return f'<img src="{url}" height={h} width={w}>'
    text = re.sub(r'<p>(triptych[^<]*\.png)</p>', f, text)

    def f(match):
        url = match.group(1)
        im = Image.open(url)
        w, h = im.size
        return f'<img class="legend" src="{url}" height={h} width={w}>'
    text = re.sub(r'<p>(legend-[^<]*\.png)</p>', f, text)

    def get_layer(match):
        abbrev = match[0][1:]
        return f'{layers[abbrev]} ({abbrev})'

    text = re.sub(r'\$\w+', get_layer, text)

    def expand_abbrev(match):
        abbrev = match[1]
        return abbrevs[abbrev]

    text = re.sub(r'\b([A-Z]+)(?![\w-])', expand_abbrev, text)

    text = re.sub(r'(\d+)ft', r'\1 feet', text)

    text = re.sub(
        r'(\d+)([ap]m)\b',
        r'\1<span class="am-pm">\2</span>',
        text,
    )

    print(text)

def p(text):
    print(text, file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])
