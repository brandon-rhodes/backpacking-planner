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

some_input = """
A9 Little Colorado
9.1 BB9 Tanner Beach
3.0 BC9 Cardenas Creek
7.0 BC9 Nevills Rapids
2.0 BD9 Hance Rapids
6.5 BE9 Hance Creek
1.9 BF5 Horseshoe Mesa
1.5 BG9 Cottonwood Creek
5.5 BH9 Grapevine Creek
8.7 BJ9 Lonetree Canyon
3.5 BJ9 Cremation Creek
4.8 CIG Indian Garden water camp
2.5 BL4 Horn Creek camp
4.8 BL5 Salt Creek camp
2.1 BL6 Cedar Spring water? camp
1.3 BL7 Monument Creek water camp
3.4 Hermit Tonto junction
1.2 BM7 Hermit Creek water camp toilet
6.2 Boucher Tonto junction
0.4 BN9 Boucher Upper Creek Crossing water
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
1.6 Mile-and-a-Half Resthouse water
1.5 Three-Mile Resthouse water
1.7 CIG Indian Garden water

BL7 Monument Creek
1.6 BL8 Granite Rapids water camp

BM7 Hermit Creek
1.5 BM8 Hermit Rapids water camp

Hermit Trailhead
2.2 Santa Maria Spring water
3.3 Breezy Point
1.5 Hermit Tonto junction

Hermit Trailhead
2.7 Boucher Hermit Junction
2.5 Yuma Point
2.4 Boucher top of Redwall
1.3 Boucher Tonto junction
"""

water = {'b', 'e'}
camping = {'c', 'e'}
# mileages = [
#     ('a', 'b', 3.0),
#     ('b', 'c', 1.5),
#     ('c', 'd', 3.5),
#     ('d', 'e', 2.0),
# ]
attribute_words = {'camp', 'toilet', 'water', 'water?'}
HEADING = '''
miles miles miles since
      today total water
'''.strip()

def main(argv):
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('waypoints', nargs='+', help='waypoint codes')
    # args = parser.parse_args(argv)

    attributes = {}  # {(waypoint, attr)}
    mileages = {}    # {w1: {w2: mileage}}

    for line in some_input.splitlines():
        line = line.strip()
        if not line:
            continue
        if not line[0].isdigit():
            here = line
            attributes[here] = set()
            continue
        words = line.split()
        miles = float(words[0])
        these_attributes = set()
        while words[-1] in attribute_words:
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
        attributes[here] = these_attributes

    pprint(mileages)

    # distances = {}
    # for start, finish, mileage in mileages:
    #     distances[(start, finish)] = mileage
    #     distances[(finish, start)] = mileage

    waypoints = [
        'Hermit Trailhead',
        'BN9 Boucher Upper Creek Crossing',
        'camp',
        'BM7 Hermit Creek',
        'BM8 Hermit Rapids',
        'camp',
        'BL8 Granite Rapids',
        'camp',
        'BL4 Horn Creek',
        'camp',
        'Bright Angel Trailhead',
    ]

    waypoints = [
        'BB9 Tanner Trailhead',
        'BB9 Tanner Beach',
        'camp',
        'A9 Little Colorado',
        'camp',
        'BB9 Tanner Beach',
        'camp',
        'BC9 Cardenas Creek',
        'camp',
        'BD9 Hance Rapids',
        'camp',
        'BE9 Hance Creek',
        'camp',
        'Grandview Trailhead',
    ]

    waypoints = list(expand_waypoints(waypoints, mileages))
    pprint(waypoints)

    day = 1
    miles = 0.0
    miles_today = 0.0
    miles_since_water = 0.0
    print('Day 1')
    print('Starting at', waypoints[0])
    print(HEADING)
    last_waypoint = waypoints[0]
    for waypoint in waypoints[1:]:
        #print('*', waypoint)
        if waypoint == 'camp':
            print()
            day = day + 1
            print('Day {}'.format(day))
            print(HEADING)
            miles_today = 0.0
            continue
        new_miles = mileages[last_waypoint][waypoint]
        miles += new_miles
        miles_today += new_miles
        miles_since_water += new_miles
        words = [waypoint]
        if waypoint in camping:
            words.append('camping')
        #if waypoint in water:
        if 'water' in attributes[waypoint]:
            words.append('water')
            miles_since_water = 0.0
        words = ' '.join(words)
        print('{:5.1f} {:5.1f} {:5.1f} {:5.1f} {}'.format(
            new_miles, miles_today, miles, miles_since_water, words))
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
