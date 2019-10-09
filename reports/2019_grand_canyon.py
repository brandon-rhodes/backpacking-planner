#!/usr/bin/env python3

import datetime as dt
import os
import re
import sys

here = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(here))

import planner

log = """
2019-04-23
8:51a Tanner Trailhead
B 29.9 L 24.6 D 31.0
# todo
4:04p Tanner Beach
B ate ½ Mountain House Chicken Fried Rice

2019-04-24
5:30a
55°
7:07a Tanner Beach
D 25.6 L 21.7 B 26.7
# 17.1? "autorades"?
75°
# 10:50a-11:50a Palisades Creek
6:45p Beach below confluence
# todo: drink

2019-04-25
5:00p Start
5:30p Little Colorado
6:32p Beach below confluence

2019-04-26
5:04a Awake
B 26.4 D 25.8 L 23.7
6:08a Start
7:36a (Red helicopter flew east above us.)
# 10:14a Palisades Beach
# 10:58a Start
1:40p Tanner Beach
5:04p Start
7:30p Cardenas Creek

2019-04-27
5:30a Awake
70°
7:30a Start
# 8:10a Unkar
# 8:30a Start
# GPS
# made up:
6:00p Seventyfivemile Creek

2019-04-28
5:22a Awake
74°
6:06a Start
7:02a Papago Creek
9:38a Hance Rapids
B 27.9 D 23.7
11:22a Start
1:48p Mineral Canyon
# 2:15p 3,600 ft
4:47p Hance Creek

2019-04-29
5:01a Awake
6:05a Start
8:15a Horseshoe Mesa saddle
8:35a Horseshoe Mesa campsites
8:55a Horseshoe Mesa saddle
12:00n Grandview Trailhead
B 21.2 L 14.6 D 15.3
"""

def main(argv):
    with open(os.path.join(here, '../mileages')) as f:
        mileages, attributes = planner.parse_mileage_file(f)

    names = list(attributes)

    waypoints = []
    waypoint = None

    itinerary = list(read_itinerary(names))

    print('Start - End   Miles  MPH  Start -> End')

    for i in range(len(itinerary) - 1):
        time1, waypoint1 = itinerary[i]
        time2, waypoint2 = itinerary[i + 1]
        if waypoint1 == waypoint2:
            continue
        hours = (time2 - time1).total_seconds() / 3600.0
        path = planner.find_path(waypoint1, waypoint2, mileages)
        miles = sum(planner.path_mileages(path, mileages))
        mph = miles / hours
        print('{:%H:%M} - {:%H:%M}  {:.1f}  {:.2f}  {} -> {}'.format(
            time1, time2, miles, mph, waypoint1, waypoint2))
        #miles = sum(

def read_itinerary(names):
    time_re = re.compile(r'\d+:\d+(a|p|am|pm|n|m)?\b')
    previous_place = None

    for line in log.splitlines():
        if line.startswith('2019'):
            datestr = line
        elif time_re.match(line):
            fields = line.split()
            timestr = fields[0]
            if not timestr[-2].isalpha():
                timestr = timestr.replace('m', ' am').replace('n', ' pm')
            dtstr = datestr + ' ' + timestr
            if dtstr.endswith(('a', 'p')):
                dtstr = dtstr[:-1] + ' ' + dtstr[-1] + 'm'
            time = dt.datetime.strptime(dtstr, '%Y-%m-%d %I:%M %p')
            if len(fields) > 1:
                place = ' '.join(fields[1:])
                if place.startswith('('):
                    place = previous_place
                elif place == 'Start':
                    place = previous_place
                elif place == 'Awake':
                    place = previous_place
                else:
                    matches = [name for name in names if place in name]
                    if len(matches) != 1:
                        print()
                        print('Error: unable to find a match for %r' % place)
                        print()
                        #print([name for name in names if name in place])
                        exit(1)
                    place = matches[0]
            yield time, place
            previous_place = place

if __name__ == '__main__':
    main(sys.argv[1:])
