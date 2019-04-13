#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys
from pprint import pprint

# https://www.nps.gov/grca/planyourvisit/upload/tonto_distances.pdf

# TODO: Page Spring #water
# TODO: Lower Boucher trail?

HEADING = '''
miles miles miles since  Day {}
      today total water
'''.strip()

def main(argv):
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('waypoints', nargs='+', help='waypoint codes')
    # args = parser.parse_args(argv)

    with open('mileages') as f:
        mileages, attributes = parse_mileage_file(f)
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

    from fileinput import input

    waypoints = []
    for line in input():
        line = line.split('#')[0].strip()
        if not line:
            continue
        waypoints.append(line)

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

def parse_mileage_file(lines):
    mileages = {}    # {w1: {w2: mileage}}
    attributes = {}  # {waypoint: {attr)}

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if not line[0].isdigit():
            here, here_attributes = parse_location(line.split())
            if here not in attributes:
                attributes[here] = here_attributes
            else:
                attributes[here] = attributes[here] | here_attributes
            continue
        words = line.split()
        miles = float(words[0])
        there, these_attributes = parse_location(words[1:])
        # while words[-1].startswith('#'):
        #     attribute = words.pop()
        #     these_attributes.add(attribute)
        # there = ' '.join(words[1:])
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

    return mileages, attributes

def parse_location(words):
    """Parse the name and attributes of a location from a line of text.

    >>> name, attrs = parse_location('A9 Little Colorado #camp #water'.split())
    >>> name == 'A9 Little Colorado'
    True
    >>> attrs == {'#camp', '#water'}
    True

    """
    i = -1
    attributes = set()
    while words[i].startswith('#'):
        attribute = words[i]
        attributes.add(attribute)
        i -= 1
    name = ' '.join(words[:i+1 or None])
    return name, attributes

def expand_waypoints(waypoints, mileages):
    start = waypoints[0]
    yield start
    previous_waypoint = start
    for waypoint in waypoints[1:]:
        if waypoint == 'camp':
            yield 'camp'
            continue
        miles = mileages[previous_waypoint].get(waypoint)
        if miles is not None:
            yield waypoint
            previous_waypoint = waypoint
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
