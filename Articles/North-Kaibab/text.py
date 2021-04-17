#!/usr/bin/env python3

import re
import sys
from PIL import Image

def main(argv):
    text = sys.stdin.read()

    def f(match):
        url = match.group(1)
        # TODO: parse w515-h344 in URL
        return f'<img src="{url}" width=515 height=344>'
    text = re.sub(r'<p>(https://lh3.googleusercontent.com/[^<]*)</p>', f, text)

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

    print(text)

def p(text):
    print(text, file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])
