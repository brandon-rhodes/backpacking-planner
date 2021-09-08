#!/usr/bin/env python3

import argparse
import re
import sys
from dataclasses import dataclass

@dataclass
class Point:
    latitude: float
    longitude: float
    elevation: float
    mileage: float

def dms(degrees, minutes, seconds):
    return round(degrees + minutes / 60 + seconds / 3600, 4)

X_LEFT = 1892
X_RIGHT = 2295
Y_SEA_LEVEL = 1578
Y_6000_FEET = 1476 # was 1473.4, until we doubted scale
#Y_6000_FEET = 1474 # was 1473.4, until we doubted scale
NORTH_LATITUDE = 36.1825  # Line on map would make you think 36,11,18
PHANTOM_CREEK_LATITUDE = dms(36,6,58)  # from Google Earth mouse cursor
RIVER_LATITUDE = 36.1001  # Just north of Bright Angel Campground bathroom
FEET_IN_A_METER = 3.2808399
PATH_STYLE = (
    'fill:none;stroke-width:0.5;stroke-linecap:butt;stroke-linejoin:miter;'
    'stroke:black;stroke-opacity:1;stroke-miterlimit:4;'
)
FILL_STYLE = 'fill:black;stroke:none'
BLANK_STYLE = 'fill:red;stroke:none'
TEXT_STYLE = 'font-size:4;text-anchor:middle'
LEFT_STYLE = 'font-size:4;text-anchor:end'
RIGHT_STYLE = 'font-size:4;text-anchor:start'
FEET_STYLE = 'font-size:3;text-anchor:start'
YELLOW = 'rgb(96.078491%,84.313965%,14.509583%)'

def main(argv):
    parser = argparse.ArgumentParser(description='Transform SVG using Python')
    parser.parse_args(argv)

    with open('section.svg') as f:
        lines = list(f)

    x = 1850
    y = 1440
    w = 494
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
        # Remove all text.
        if '<use' in line:
            continue
            # fields = line.split()
            # assert fields[2].startswith('x=')
            # x = float(fields[2][3:-1])
            # y = float(fields[3][3:-3])
            # if X_LEFT < x < X_RIGHT and y < 1590:
            #     continue

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

        line = line.replace(YELLOW, 'rgb(93.333435%,58.432007%,10.980225%)')

        if line.startswith('<path ') and line.endswith('/>\n'):
            x_list = []
            pairs = re.findall(r' \d+\.\d+ \d+\.\d+ ', line)
            for pair in pairs:
                pieces = pair.split()
                x = float(pieces[0])
                x_list.append(x)
            #print(x_list)
            if all(1900 < x < 2200 for x in x_list):
                #print('yeah')
                #continue
                pass

        # if 'xlink:href="#glyph0-1' in line:
        #     continue
        yield line

    points = list(read_trail_elevation())
    strings = [f'{to_x(p.latitude)} {to_y(p.elevation)}' for p in points]

    path_pieces = ['M ', 'L '.join(strings)]
    d = ''.join(path_pieces)

    elevation = points[-1].elevation
    path_pieces.append(f' L {X_RIGHT-0.2} {to_y(elevation)}')
    path_pieces.append(f' L {X_RIGHT-0.2} {to_y(0)}')

    p = points[0]
    path_pieces.append(f' L {to_x(p.latitude)} {to_y(0)}')

    style = 'fill:#fff;fill-opacity:0.9;'
    yield f'<path style="{style}" d="{"".join(path_pieces)}" />\n'

    yield f'<path style="{PATH_STYLE}" d="{d}" />\n'

    m = FEET_IN_A_METER
    for (lat, ele) in [
            (RIVER_LATITUDE + (NORTH_LATITUDE - RIVER_LATITUDE) * 2/3,0),# 1/3 break
            (RIVER_LATITUDE + (NORTH_LATITUDE - RIVER_LATITUDE) * 1/3,0),# 2/3 break

            (RIVER_LATITUDE, 2420), # Black Bridge
            (36.1018, 2507), # Bright Angel CG
            (36.10498, 774*m), # Phantom Ranch
            (dms(36,6,58), 2800), # Phantom Creek enters Bright Angel Creek
            (dms(36,8,19.3), 3252), # Where canyon hits supergroup and opens out!
            (dms(36,9,32), 3773), # Ribbon Falls
            (36.1704, 1234*m), # Cottonwood CG
            (dms(36,11,10.2), 4566), # Manzanita Rest Area
    ]:
        break
        yield (f'<path style="{PATH_STYLE.replace("black","red")}" d="'
               f'M {to_x(lat)} {to_y(ele + 500)} '
               f'L {to_x(lat)} {to_y(ele)} '
               f'" />\n')

    # Erase stuff near the river.

    x0 = to_x(RIVER_LATITUDE) - 10
    x1 = to_x(RIVER_LATITUDE) - 4.2
    y0 = to_y(0)
    y1 = to_y(3430)
    yield (f'<path style="{PATH_STYLE}" d="'
           f'M {x0} {y0} '
           f'L {x1} {y1} '
           f'Z" />\n')
    # yield (f'<path style="{BLANK_STYLE}" d="'
    #        f'M {x0} {y0} '
    #        f'L {x0} {y1} '
    #        f'L {x1} {y1} '
    #        f'L {x1} {y0} '
    #        f'Z" />\n')

    # Draw mile markers.

    offset = +0 #.25  # Distance from bridge to intersection at 36°6'0"
    start = points[0].mileage - offset
    mile = 0
    for p in points:
        mileage = p.mileage - start
        if mileage < mile:
            continue
        yield triangle(to_x(p.latitude), to_y(0))
        y = to_y(0)+7
        yield from put_label(to_x(p.latitude), y, f'Mile|{mile}.0')

        feet = round(p.elevation)
        x = to_x(p.latitude)
        y = to_y(p.elevation)
        yield f'<circle cx="{x}" cy="{y}" r="1" style="{FILL_STYLE}" />'
        label = f'{feet} ft'
        if mile == 8:
            label = label.replace(' ', '|')
        yield from put_label(x+0.5, y+3.25, label, style=FEET_STYLE)

        mile += 1

    # Draw text labels.

    for latitude, elevation, label in [
            (36.0908, 3650, 'Colorado|River'),
            (36.1049, 0, '^Phantom|Ranch'),
            (dms(36,6,57), 4200, 'Phantom|Creek'),
            (36.1323, 5300, 'Hillers|Butte'),
            (36.1432, 5900, 'Clement|Powell Butte'),
            (36.1580, 4900, 'Ribbon|Falls'),
            (36.1704, 1175*m, '^Cottonwood|CG'),
            (36.1737, 5100, 'Transept'),
    ]:
        y = to_y(elevation)
        if label.startswith('^'):
            yield triangle(to_x(latitude), y)
            label = label[1:]
            y += 7
        yield from put_label(to_x(latitude), y, label)

    # Draw our own vertical scale.

    scale_range = range(1000, 6001, 1000)

    lat = 36.08
    x = int(to_x(lat))
    yield f'<path style="{PATH_STYLE}" d="'
    yield f'M {x} {to_y(6000)} L {x} {to_y(-25)} '
    for elevation in scale_range:
        y = to_y(elevation)
        yield f'M {x-2} {y} L {x+2} {y} '
    yield '" />\n'

    for elevation in scale_range:
        y = to_y(elevation) + 1.5
        yield (f'<text style="{LEFT_STYLE}"'
               f' x="{x-3}" y="{y}">{elevation}</text>')
        yield (f'<text style="{RIGHT_STYLE}"'
               f' x="{x+3}" y="{y}">{elevation}</text>')

    # The small print.

    y = to_y(5700)
    yield (f'<text style="{RIGHT_STYLE}; font: 2.5"'
           f' x="{x+3}" y="{y}">Elevation</text>')
    y += 3
    yield (f'<text style="{RIGHT_STYLE}; font: 2.5"'
           f' x="{x+3}" y="{y}">(feet)</text>')

    x += 0.5
    y = to_y(-280)
    pre = f'<text style="font-size:2.5;text-anchor:start" x="{x}"'
    yield pre + f' y="{y}">Vertical</text>'
    y += 3
    yield pre + f' y="{y}">Exaggeration</text>'
    y += 3
    yield pre + f' y="{y}">2x</text>'

    x += 0.5
    y = to_y(-500)
    pre = f'<text style="font-size:2.5;text-anchor:end" x="{x-3}"'
    yield pre + f' y="{y}">North →</text>'


    # Close the svg tag.

    yield lines[-1]  # "</svg>"

def read_trail_elevation():
    with open('trail_elevation.csv') as f:
        lines = iter(f)
        next(f)  # Skip column names
        for line in lines:
            fields = line.split(',')
            latitude = float(fields[0])
            longitude = float(fields[1])
            elevation = float(fields[2])
            mileage = float(fields[3])
            x = to_x(latitude)
            if latitude < RIVER_LATITUDE or x > X_RIGHT:
                continue
            yield Point(latitude, longitude, elevation, mileage)

def put_label(x, y, label, style=TEXT_STYLE):
    pieces = label.split('|')
    for piece in pieces:
        yield (f'<text style="{style}"'
               f' x="{x}" y="{y}">{piece}</text>')
        y += 4

def triangle(x, y):
    return (f'<path style="{FILL_STYLE}" d="'
            f'M {x} {y} L {x-2} {y+3} L {x+2} {y+3} Z" />\n')

def to_x(latitude):
    X_PHANTOM_CREEK = 2018
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
