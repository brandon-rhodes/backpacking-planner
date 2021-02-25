#!/usr/bin/env python3

import argparse
import re
import sys

X_LEFT = 1892
X_RIGHT = 2295
Y_SEA_LEVEL = 1578
Y_6000_FEET = 1473.4
NORTH_LATITUDE = 36 + 10/60 + 56/3600
SOUTH_LATITUDE = 36 + 5/60 + 21/3600
FEET_IN_A_METER = 3.2808399
PATH_STYLE = (
    'fill:none;stroke-width:0.5;stroke-linecap:butt;stroke-linejoin:miter;'
    'stroke:black;stroke-opacity:1;stroke-miterlimit:4;'
)

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
    for line in lines[:-1]:
        # Remove most text.
        if '<use' in line:
            #continue
            fields = line.split()
            assert fields[2].startswith('x=')
            x = float(fields[2][3:-1])
            y = float(fields[3][3:-3])
            if X_LEFT < x < X_RIGHT and y < 1590:
                continue

        # Get rid of the little tick lines that connected names
        # with strata.
        m = re.search(r' d="([^"]+)"', line)
        if m is not None:
            words = m[1].split()
            if len(words) == 6 and 'stroke-miterlimit:4' in line:
                continue

        # Get rid of vertical dashed line.
        if 'stroke-dasharray' in line:
            continue

        # if line.startswith('<path') and len(line) < 290:
        #     continue
        # if 'xlink:href="#glyph0-1' in line:
        #     continue
        yield line

    points = list(read_trail_elevation())
    strings = [f'{to_x(latitude)} {to_y(elevation)}'
               for latitude, elevation in points]

    path_pieces = ['M ', 'L '.join(strings)]
    d = ''.join(path_pieces)

    elevation = points[-1][-1]
    latitude = NORTH_LATITUDE - 0.00010  # Avoid graying out right elevation scale.
    path_pieces.append(f' L {to_x(latitude)} {to_y(elevation)}')
    path_pieces.append(f' L {to_x(latitude)} {to_y(0)}')

    latitude, elevation = points[0]
    path_pieces.append(f' L {to_x(latitude) + 7.5} {to_y(0)}')

    style = 'fill:#fffc;'
    yield f'<path style="{style}" d="{"".join(path_pieces)}" />\n'

    yield f'<path style="{PATH_STYLE}" d="{d}" />\n'

    lat = 36.1704
    m = FEET_IN_A_METER
    yield (f'<path style="{PATH_STYLE}" d="'
           f'M {to_x(lat)} {to_y(1234 * m)} '
           f'L {to_x(lat)} {to_y(1334 * m)} '
           f'" />\n')

    yield lines[-1]  # "</svg>"

def read_trail_elevation():
    with open('trail_elevation.csv') as f:
        lines = iter(f)
        next(f)
        for line in lines:
            fields = line.split(',')
            latitude = float(fields[0])
            elevation = float(fields[1]) * FEET_IN_A_METER
            if latitude > NORTH_LATITUDE:
                break
            yield [latitude, elevation]

def to_x(latitude):
    x_fraction = (latitude - SOUTH_LATITUDE) / (NORTH_LATITUDE - SOUTH_LATITUDE)
    return X_LEFT + x_fraction * (X_RIGHT - X_LEFT)

def to_y(elevation):
    y_fraction = elevation / 6000
    return Y_SEA_LEVEL + y_fraction * (Y_6000_FEET - Y_SEA_LEVEL)

if __name__ == '__main__':
    main(sys.argv[1:])
