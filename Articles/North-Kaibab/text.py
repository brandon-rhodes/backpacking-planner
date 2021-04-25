#!/usr/bin/env python3

import re
import sys
from PIL import Image

subs = {
    'Pc': 'Coconino Sandstone',
    'Mr': 'Redwall Limestone',
    'Ct': 'Tapeats Sandstone',
    'Yh': 'Hakatai Shale',
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

    for a, b in subs.items():
        b = f'({a}) {b}'
        text = text.replace('$' + a, b)

    print(text)

def p(text):
    print(text, file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])
