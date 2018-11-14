#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys

routes = [[
    (0.0, 'CIG Indian Garden'),
    (2.5, 'BL4 Horn Creek'),
    (4.8, 'BL5 Salt Creek'),
    (3.4, 'BL7 Monument Creek'),
    (3.5, 'BM7 Hermit Creek'),
    (5.0, ''),
]]


# https://www.nps.gov/grca/planyourvisit/upload/tonto_distances.pdf

"""
A9 Little Colorado
9.1 BB9 Tanner Beach
7.8 BB9 Tanner Trailhead
10.8 BC9 Cardenas Creek
7.0 BC9 Nevills Rapids
2.0 BD9 Hance Rapids
> 6.5 New Hance Trailhead
13.0 BE9 Hance Creek
1.9 BF5 Horseshoe Mesa
> 3.0 Grandview Trailhead
4.5 BG9 Cottonwood Creek
5.5 BH9 Grapevine Creek
8.7 BJ9 Lonetree Canyon
3.5 BJ9 Cremation Creek
4.8 CIG Indian Garden water camp
2.5 BL4 Horn Creek camp
4.8 BL5 Salt Creek camp
2.1 BL6 Cedar Spring water? camp
1.3 BL7 Monument Creek water camp
3.4 Hermit Tonto Junction
1.2 BM7 Hermit Creek water camp toilet
6.6 BN9 Boucher Upper Creek Crossing
5.7 BO9 Slate Creek
9.3 BO9 Turquoise Creek
5.8 BP9 Ruby Creek
4.8 BP9 Serpentine Canyon
3.8 BQ9 Bass Upper Creek Crossing
5.0 South Bass Trailhead

BL7 Monument Creek
1.6 BL8 Granite Rapids water camp

BM7 Hermit Creek
1.5 BM8 Hermit Rapids water camp

Hermit Trailhead
2.2 Santa Maria Spring water
3.3 Breezy Point
1.5 Hermit Tonto Junction

Hermit Trailhead
2.7 Boucher Hermit Junction
2.5 Yuma Point
2.4 Boucher top of Redwall
1.3 Boucher Tonto junction
"""

water = {'b', 'e'}
camping = {'c', 'e'}
mileages = [
    ('a', 'b', 3.0),
    ('b', 'c', 1.5),
    ('c', 'd', 3.5),
    ('d', 'e', 2.0),
]

def main(argv):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('waypoints', nargs='+', help='waypoint codes')
    args = parser.parse_args(argv)

    distances = {}
    for start, finish, mileage in mileages:
        distances[(start, finish)] = mileage
        distances[(finish, start)] = mileage

    start = args.waypoints[0]
    waypoints = [start]
    last_waypoint = start
    for waypoint in args.waypoints[1:]:
        if waypoint == 'camp':
            waypoints.append('camp')
            continue
        waypoints.extend(find_path(last_waypoint, waypoint, distances))
        last_waypoint = waypoint

    # waypoints = ['a', 'b', 'c', 'camp', 'd', 'e']

    day = 1
    miles = 0.0
    miles_today = 0.0
    miles_since_water = 0.0
    print('Day 1')
    print('Starting at', waypoints[0])
    last_waypoint = 'a'
    for waypoint in waypoints[1:]:
        if waypoint == 'camp':
            print()
            day = day + 1
            print('Day {}'.format(day))
            miles_today = 0.0
            continue
        new_miles = distances[(last_waypoint, waypoint)]
        miles += new_miles
        miles_today += new_miles
        miles_since_water += new_miles
        words = [waypoint, new_miles, miles_today, miles]
        words.append('{} since water'.format(miles_since_water))
        if waypoint in camping:
            words.append('camping')
        if waypoint in water:
            words.append('water')
            miles_since_water = 0.0
        print(words)
        last_waypoint = waypoint

def find_path(start, end, distances):
    already_found = {start}
    destinations = [(0.0, [start])]
    while True:
        miles_so_far, waypoints = destinations.pop(0)
        here = waypoints[-1]
        for w1, w2, mileage in mileages:
            if w1 == here:
                w = w2
            elif w2 == here:
                w = w1
            else:
                continue
            if w in already_found:
                continue
            if w == end:
                return waypoints[1:] + [w]
            tup = (miles_so_far + mileage, waypoints + [w])
            destinations.append(tup)
            already_found.add(w)
        destinations.sort()
    return ['b', 'c', 'd', 'e']

if __name__ == '__main__':
    main(sys.argv[1:])
