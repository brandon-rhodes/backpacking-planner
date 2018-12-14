#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys
from pprint import pprint

routes = [[
    (0.0, 'CIG Indian Garden'),
    (2.5, 'BL4 Horn Creek'),
    (4.8, 'BL5 Salt Creek'),
    (3.4, 'BL7 Monument Creek'),
    (3.5, 'BM7 Hermit Creek'),
    (5.0, ''),
]]


# https://www.nps.gov/grca/planyourvisit/upload/tonto_distances.pdf

# TODO: Page Spring #water
# TODO: Lower Boucher trail?

some_input = """
A9 Little Colorado
6.5 BA9 Lava Canyon Rapids
3.0 BB9 Tanner Beach #camp #toilet
3.0 BC9 Cardenas Creek #camp
4.3 BC9 Escalante Creek #water #camp
2.3 BC9 Seventyfivemile Creek #water #camp
# Neville Rapids #rafters
# BC9 Papago Creek #camp
2.4 BD9 Hance Rapids #water #rafters
2.6 BE9 Mineral Canyon
3.9 BE9 Hance Creek #water
1.9 BF5 Horseshoe Mesa #toilet #camp
1.5 BG9 Cottonwood Creek #water?
5.5 BH9 Grapevine Creek
8.7 BJ9 Lonetree Canyon
3.5 BJ9 Cremation Creek
2.1 Tip Off
2.7 CIG Indian Garden #water #toilet #camp
2.5 BL4 Horn Creek #toilet #camp
4.8 BL5 Salt Creek #toilet #camp
2.1 BL6 Cedar Spring #water? #camp
1.3 BL7 Monument Creek #toilet #water #camp
3.4 Hermit Tonto junction
1.2 BM7 Hermit Creek #water #toilet #camp
6.2 Boucher Tonto junction
0.4 BN9 Boucher Upper Creek Crossing #water #camp
5.7 BO9 Slate Creek
9.3 BO9 Turquoise Creek
5.8 BP9 Ruby Creek
4.8 BP9 Serpentine Canyon
3.8 BQ9 Bass Upper Creek Crossing
5.0 South Bass Trailhead

BB9 Tanner Beach
7.8 BB9 Tanner Trailhead

BD9 Hance Rapids
6.5 New Hance Trailhead

BF5 Horseshoe Mesa
1.9 Grandview Coconino Saddle
1.1 Grandview Trailhead

Bright Angel Trailhead
1.6 Mile-and-a-Half Resthouse #water
1.5 Three-Mile Resthouse #water
1.7 CIG Indian Garden #water

BL7 Monument Creek
1.6 BL8 Granite Rapids #water #camp

BM7 Hermit Creek
1.5 BM8 Hermit Rapids #water #camp

Hermit Trailhead
2.2 Santa Maria Spring #water
0.5 Boucher Hermit Junction
2.8 Breezy Point
1.5 Hermit Tonto junction

Boucher Hermit Junction
2.5 Yuma Point #camp
2.4 Boucher top of Redwall #camp
1.3 Boucher Tonto junction

CIG Indian Garden
3.2 River Resthouse #water #toilet
1.5 CBG Bright Angel Campground #water #toilet #camp
0.4 Phantom Ranch #water #toilet

South Kaibab Trailhead
1.5 Cedar Ridge #toilet
1.5 Skeleton Point #toilet
1.4 Tip Off #toilet
2.6 CBG Bright Angel Campground

North Kaibab Trailhead
1.7 Supai Tunnel #water?
3.0 Roaring Springs #water
0.7 Manzanita Rest Area #water
1.4 Cottonwood Campground #water #camp
1.6 Ribbon Falls
4.9 North Kaibab Clear Creek junction
0.3 Phantom Ranch

North Kaibab Trailhead
1.5 North Rim Campground #water? #camp

North Kaibab Clear Creek junction
1.7 AK9 Sumner Wash #camp
6.7 AK9 Clear Creek #toilet #water #camp
6.0 AK9 Clear Creek at Colorado River

AK9 Clear Creek
5.0 AJ9 Cheyava Falls
"""

some_input += """
CBG Bright Angel Campground
2.0 Utah Flats
2.0 Phantom Creek
"""

#water = {'b', 'e'}
# mileages = [
#     ('a', 'b', 3.0),
#     ('b', 'c', 1.5),
#     ('c', 'd', 3.5),
#     ('d', 'e', 2.0),
# ]
attribute_words = {'#camp', '#toilet', '#water', '#water?'}
HEADING = '''
miles miles miles since  Day {}
      today total water
'''.strip()

def main(argv):
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('waypoints', nargs='+', help='waypoint codes')
    # args = parser.parse_args(argv)

    attributes = {}  # {waypoint: {attr)}
    mileages = {}    # {w1: {w2: mileage}}

    for line in some_input.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if not line[0].isdigit():
            here = line
            if here not in attributes:
                attributes[here] = set()
            continue
        words = line.split()
        miles = float(words[0])
        these_attributes = set()
        while words[-1].startswith('#'):
            attribute = words.pop()
            these_attributes.add(attribute)
        there = ' '.join(words[1:])
        if here not in mileages:
            mileages[here] = {}
        if there not in mileages:
            mileages[there] = {}
        mileages[here][there] = miles
        mileages[there][here] = miles
        here = there
        if here in attributes:
            attributes[here] = attributes[here] | these_attributes
        else:
            attributes[here] = these_attributes

    #pprint(mileages)

    # distances = {}
    # for start, finish, mileage in mileages:
    #     distances[(start, finish)] = mileage
    #     distances[(finish, start)] = mileage

    waypoints9 = [
        'Hermit Trailhead',
        'Yuma Point',
        'camp',
        'Boucher top of Redwall',
        'Boucher Hermit Junction',
        'Hermit Tonto junction',
        'BN9 Boucher Upper Creek Crossing',  # fix
        'camp',
        'BM7 Hermit Creek',
        'BM8 Hermit Rapids',  # camp at Tonto? or river?
        'camp',
        'BL8 Granite Rapids',
        'camp',
        'BL5 Salt Creek',  # bad idea? BL6 instead?
        'camp',
        'BL4 Horn Creek',
        'camp',
        'Bright Angel Trailhead',
    ]

    waypoints = [
        'Hermit Trailhead',
        'Yuma Point',
        'camp',
        'BN9 Boucher Upper Creek Crossing',  # fix
        'camp',
        'BM7 Hermit Creek',
        'BM8 Hermit Rapids',  # camp at Tonto? or river?
        'camp',
        'BL8 Granite Rapids',
        'camp',
        'BL5 Salt Creek',  # bad idea? BL6 instead?
        'camp',
        'BL4 Horn Creek',
        'camp',
        'Bright Angel Trailhead',
    ]

    waypoints = [
        'BB9 Tanner Trailhead',
        'BB9 Tanner Beach',
        'camp',
        'BA9 Lava Canyon Rapids',
        'camp',
        'A9 Little Colorado',
        'BA9 Lava Canyon Rapids',
        'camp',
        'BB9 Tanner Beach',
        'BC9 Cardenas Creek',
        'camp',
        'BC9 Seventyfivemile Creek',
        'camp',
        'BE9 Mineral Canyon',
        #'BD9 Hance Rapids',  # water?
        'camp',
        'Grandview Trailhead',  # how get back?
    ]

    waypoints = [
        'BB9 Tanner Trailhead',
        'BB9 Tanner Beach',
        'camp',
        'A9 Little Colorado',
        'camp',
        'BA9 Lava Canyon Rapids',
        'camp',
        'BC9 Cardenas Creek',
        'camp',
        'BC9 Seventyfivemile Creek',
        'camp',
        #'BD9 Hance Rapids',  # water?
        #'BE9 Mineral Canyon',
        'BE9 Hance Creek',
        'camp',
        'Grandview Trailhead',  # how get back?
    ]

    waypoints2 = [
        'Grandview Trailhead',
        'BH9 Grapevine Creek',  # TODO: didn't make it all the way
        'camp',
        'BJ9 Lonetree Canyon',
        'camp',
        'CBG Bright Angel Campground',
        'camp',
        'CIG Indian Garden',
        'camp',
        'Bright Angel Trailhead',
    ]

    waypoints2 = [
        'South Kaibab Trailhead',
        'Cottonwood Campground',
        'camp',
        'Cottonwood Campground',
        'camp',
        'Utah Flats',
        'camp',
        'Phantom Creek',
        'camp',
        'Utah Flats',
        'camp',
        'CBG Bright Angel Campground',
        'camp',
        'Bright Angel Trailhead'
    ]

    waypoints2 = [
        'South Kaibab Trailhead',
        'Cottonwood Campground',
        'camp',
        #'Bright Angel Campground',
        'Phantom Ranch',
        'AK9 Sumner Wash',
        'camp',
        'AK9 Clear Creek',
        'camp',
        'AJ9 Cheyava Falls',
        'camp',
        'AK9 Clear Creek',
        'camp',
        'CBG Bright Angel Campground',
        'camp',
        'Bright Angel Trailhead'
    ]

    waypoints = list(expand_waypoints(waypoints, mileages))
    #pprint(waypoints)

    day = 1
    miles = 0.0
    miles_today = 0.0
    miles_since_water = 0.0
    line_format = '{:5.1f} {:5.1f} {:5.1f} {:5.1f}  {}'
    print(HEADING.format(1))
    print(line_format.format(0.0, 0.0, 0.0, 0.0, waypoints[0]))
    last_waypoint = waypoints[0]
    for waypoint in waypoints[1:]:
        #print('*', waypoint)
        if waypoint == 'camp':
            if '#camp' not in attributes[last_waypoint]:
                print('WARNING: no campground')
            print()
            day = day + 1
            print(HEADING.format(day))
            miles_today = 0.0
            continue
        new_miles = mileages[last_waypoint][waypoint]
        miles += new_miles
        miles_today += new_miles
        miles_since_water += new_miles
        words = [waypoint]
        words.extend(sorted(attributes[waypoint], reverse=True))
        #if waypoint in water:
        print(line_format.format(
            new_miles, miles_today, miles, miles_since_water, ' '.join(words)
        ))
        if '#water' in attributes[waypoint]:
            miles_since_water = 0.0
        last_waypoint = waypoint

def expand_waypoints(waypoints, mileages):
    start = waypoints[0]
    yield start
    previous_waypoint = start
    for waypoint in waypoints[1:]:
        if waypoint == 'camp':
            yield 'camp'
            continue
        path = list(find_path(previous_waypoint, waypoint, mileages))
        for w in path[1:]:
            yield w
        previous_waypoint = waypoint

def find_path(start, end, mileages):
    already_found = set()
    destinations = [(0.0, [start])]
    while True:
        try:
            miles_so_far, waypoints = destinations.pop(0)
        except IndexError:
            raise ValueError('cannot go from %r to %r' % (start, end))
        here = waypoints[-1]
        if here == end:
            return waypoints
        if here in already_found:
            continue
        already_found.add(here)
        for waypoint, miles in mileages[here].items():
            tup = (miles_so_far + miles, waypoints + [waypoint])
            destinations.append(tup)
        destinations.sort()

if __name__ == '__main__':
    main(sys.argv[1:])
