#!/usr/bin/env python3

import argparse
import sys

NORTH = 36.188
SOUTH = 1

def main(argv):
    parser = argparse.ArgumentParser(description='Transform SVG using Python')
    parser.parse_args(argv)

    with open('section.svg') as f:
        lines = list(f)

    #lines[1] = lines[1].replace('0 0 4176 3024', '2800 1900 3300 2100')
    x = 1800
    y = 1400
    w = 550
    h = 300
    lines[1] = lines[1].replace('4176pt', f'{w}pt')
    lines[1] = lines[1].replace('3024pt', f'{h}pt')
    lines[1] = lines[1].replace(
        '0 0 4176 3024',
        f'{x} {y} {w} {h}')

    lines = list(transform(lines))

    with open('section2.svg', 'w') as f:
        f.write(''.join(lines))

def transform(lines):
    for line in lines:
        if '<use' in line:
            fields = line.split()
            assert fields[2].startswith('x=')
            x = float(fields[2][3:-1])
            if x > 2300:  # remove text from right-hand scale
                continue
        # if 'xlink:href="#glyph0-1' in line:
        #     continue
        yield line

if __name__ == '__main__':
    main(sys.argv[1:])
