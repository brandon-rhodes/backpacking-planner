#!/usr/bin/env python
#
# python astronomy_events.py 36.0544 -112.1401 2019-04-23 2019-04-29 US/Arizona
# python astronomy_events.py 36.0544 -112.1401 2020-09-27 2020-10-03 US/Arizona
# ../astronomy_events.py 36.0544 -112.1401 2021-10-10 2021-10-17 US/Pacific

from __future__ import print_function

import argparse
import datetime as dt
import sys

from pytz import timezone
from skyfield import api, almanac

def main(argv):
    parser = argparse.ArgumentParser(
        description='Print the astronomical events that will occur during a hike.'
    )
    parser.add_argument('latitude', type=float, help='degrees north')
    parser.add_argument('longitude', type=float, help='degrees east')
    parser.add_argument('start', type=str, help='In yyyy-mm-dd format')
    parser.add_argument('end', type=str, help='In yyyy-mm-dd format')
    parser.add_argument('timezone', type=str, help='hours from UTC')
    args = parser.parse_args(argv)
    for item in events(args):
        print(item)

def events(args):
    fmt = '%Y-%m-%d'
    start = dt.datetime.strptime(args.start, fmt)
    end = dt.datetime.strptime(args.end, fmt) + dt.timedelta(days=1)
    tz = timezone(args.timezone)

    start = start.replace(tzinfo=tz)
    end = end.replace(tzinfo=tz)

    load = api.Loader('~/.cache/skyfield')
    ts = load.timescale()
    start = ts.utc(start)
    end = ts.utc(end)

    topos = api.Topos(float(args.latitude), float(args.longitude))

    e = load('de421.bsp')
    sun = e['sun']
    earth = e['earth']
    moon = e['moon']
    times, events = almanac.find_discrete(
        start, end, almanac.sunrise_sunset(e, topos)
    )

    # Make sure sequence starts with sunrise.
    if events[0] != 1:
        times = times[1:]
        events = events[1:]

    def f(t):
        return t.astimezone(tz).strftime('%H:%M')

    width = 45
    sun_ra_array = earth.at(times).observe(sun).radec()[0].hours
    planets = [
        ('s', earth.at(times).observe(e['saturn barycenter']).radec()[0].hours),
        ('j', earth.at(times).observe(e['jupiter barycenter']).radec()[0].hours),
        ('m', earth.at(times).observe(e['mars']).radec()[0].hours),
        ('e', earth.at(times).observe(e['mercury']).radec()[0].hours),
        ('v', earth.at(times).observe(e['venus']).radec()[0].hours),
        ('M', earth.at(times).observe(e['moon']).radec()[0].hours),
    ]

    for i in range(0, len(times) - 1, 2):
        sunrise, sunset = times[i], times[i+1]
        hours = (sunset.tt - sunrise.tt) * 24.0
        sky = [' '] * width
        sun_ra = sun_ra_array[i+1]
        for letter, ra_array in planets:
            ra = ra_array[i+1]
            j = int(((sun_ra - ra) / 24.0) * width)
            sky[j] = letter
        yield '{:2} Daylight {}-{} = {:.1f}h |{}|'.format(
            sunrise.astimezone(tz).strftime('%d'),
            f(sunrise), f(sunset), hours, ''.join(sky),
        )

if __name__ == '__main__':
    main(sys.argv[1:])
