#!/usr/bin/env python3

import argparse
import re
import sys

def dms(degrees, minutes, seconds):
    return degrees + minutes / 60 + seconds / 3600

X_LEFT = 1892
X_RIGHT = 2295
Y_SEA_LEVEL = 1578
Y_6000_FEET = 1473.4
# NORTH_OFFSET = +0.0021  # degrees latitude
# SOUTH_OFFSET = -0.0041  # degrees latitude
NORTH_LATITUDE = 36 + 10/60 + 56/3600 #+ NORTH_OFFSET
SOUTH_LATITUDE = 36 + 5/60 + 21/3600 #+ SOUTH_OFFSET
PHANTOM_CREEK_LATITUDE = dms(36,6,58)
RIVER_LATITUDE = 36.1009
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
    path_pieces.append(f' L {X_RIGHT-0.2} {to_y(elevation)}')
    path_pieces.append(f' L {X_RIGHT-0.2} {to_y(0)}')

    latitude, elevation = points[0]
    path_pieces.append(f' L {to_x(latitude) + 7.5} {to_y(0)}')

    style = 'fill:#fffc;'
    yield f'<path style="{style}" d="{"".join(path_pieces)}" />\n'

    yield f'<path style="{PATH_STYLE}" d="{d}" />\n'

    m = FEET_IN_A_METER
    for (lat, ele) in [
            (RIVER_LATITUDE, 2420), # Black Bridge
            (36.1018, 2507), # Bright Angel CG
            (36.10498, 774*m), # Phantom Ranch
            (dms(36,6,58), 2800), # Phantom Creek enters Bright Angel Creek
            (dms(36,9,32), 3773), # Ribbon Falls
            (36.1704, 1234*m), # Cottonwood CG
    ]:
        yield (f'<path style="{PATH_STYLE.replace("black","red")}" d="'
               f'M {to_x(lat)} {to_y(ele + 500)} '
               f'L {to_x(lat)} {to_y(ele)} '
               f'" />\n')

    yield lines[-1]  # "</svg>"

def read_trail_elevation():
    with open('trail_elevation.csv') as f:
        lines = iter(f)
        next(f)  # Skip column names
        for line in lines:
            fields = line.split(',')
            latitude = float(fields[0])
            elevation = float(fields[1]) * FEET_IN_A_METER
            x = to_x(latitude)
            if latitude < RIVER_LATITUDE or x > X_RIGHT:
                continue
            yield [latitude, elevation]

def to_x(latitude):
    X_PHANTOM_CREEK = 2018
    if latitude < PHANTOM_CREEK_LATITUDE:
        n = PHANTOM_CREEK_LATITUDE
        s = SOUTH_LATITUDE + 0.007
        x1 = X_LEFT
        x2 = X_PHANTOM_CREEK
    else:
        n = NORTH_LATITUDE
        s = PHANTOM_CREEK_LATITUDE
        x1 = X_PHANTOM_CREEK
        x2 = X_RIGHT - 9
    x_fraction = (latitude - s) / (n - s)
    return x1 + x_fraction * (x2 - x1)

def to_y(elevation):
    y_fraction = elevation / 6000
    return Y_SEA_LEVEL + y_fraction * (Y_6000_FEET - Y_SEA_LEVEL)

if __name__ == '__main__':
    main(sys.argv[1:])
