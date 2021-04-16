#!/usr/bin/env python3

import re
import sys

def main(argv):
    text = sys.stdin.read()

    def f(match):
        url = match.group(1)
        return f'<img src="{url}">'
    text = re.sub(r'<p>(https://lh3.googleusercontent.com/[^<]*)</p>', f, text)

    def f(match):
        url = match.group(1)
        return f'<img src="{url}">'
    text = re.sub(r'<p>(triptych[^<]*\.png)</p>', f, text)

    def f(match):
        url = match.group(1)
        return f'<img class="legend" src="{url}">'
    text = re.sub(r'<p>(legend-[^<]*\.png)</p>', f, text)

    print(text)

if __name__ == '__main__':
    main(sys.argv[1:])
