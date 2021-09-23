#!/usr/bin/env python3

from PIL import Image
import io
import re
import sys
import urllib.request

f = open('text.md')
r = re.compile(r'=w(\d+)-h(\d+)')
size = 0

for line in f:
    if not line.startswith('https://lh3.googleusercontent.com/'):
        print(line, end='')
        continue
    url = line.strip()

    # 900 = 6 inches wide at 150 dpi, chosen as a trade-off between the
    # resolution of modern displays versus the bandwidth of mobile
    # devices that might view the page.  Maybe someday we could have
    # some JS choose the image dimensions instead.  But today is not
    # that day.
    u = r.sub('=w900', url)

    with urllib.request.urlopen(u) as response:
        data = response.read()
    print(f'{len(data) // 1024}k', file=sys.stderr)
    size += len(data)
    im = Image.open(io.BytesIO(data))
    w, h = im.size
    u = r.sub(f'=w{w}-h{h}', url)
    print(u)

print(f'Total weight: {size // 1024}k', file=sys.stderr)
