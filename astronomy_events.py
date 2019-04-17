#!/usr/bin/env python
#
# python astronomy_events.py 36.0544 -112.1401 2019-04-23 2019-04-29 US/Arizona

from __future__ import print_function

import argparse
import datetime as dt
import sys

from pytz import timezone
from numpy import arange
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
    end = dt.datetime.strptime(args.end, fmt)
    tz = timezone(args.timezone)

    start = start.replace(tzinfo=tz)
    end = end.replace(tzinfo=tz)

    load = api.Loader('~/.cache/skyfield')
    ts = load.timescale()
    start = ts.utc(start)
    end = ts.utc(end)

    topos = api.Topos('{} N'.format(args.latitude), '{} E'.format(args.longitude))

    e = load('de421.bsp')
    sun = e['sun']
    earth = e['earth']
    moon = e['moon']
    times, events = almanac.find_discrete(
        start, end, almanac.sunrise_sunset(e, topos)
    )
    assert events[0] == 1  # make sure sequence starts with sunrise

    def f(t):
        return t.astimezone(tz).strftime('%H:%M')

    width = 34
    sun_ra_array = earth.at(times).observe(sun).radec()[0].hours
    planets = [
        ('s', earth.at(times).observe(e['saturn barycenter']).radec()[0].hours),
        ('j', earth.at(times).observe(e['jupiter barycenter']).radec()[0].hours),
        ('m', earth.at(times).observe(e['mars']).radec()[0].hours),
        ('e', earth.at(times).observe(e['mercury']).radec()[0].hours),
        ('v', earth.at(times).observe(e['venus']).radec()[0].hours),
        ('M', earth.at(times).observe(e['moon']).radec()[0].hours),
    ]

    for i in range(0, len(times), 2):
        sunrise, sunset = times[i], times[i+1]
        hours = (sunset.tt - sunrise.tt) * 24.0
        t = sunset
        sky = [' '] * width
        sun_ra = sun_ra_array[i+1]
        for letter, ra_array in planets:
            ra = ra_array[i+1]
            j = int(((sun_ra - ra) / 24.0) * width)
            sky[j] = letter
        yield '{} sunrise {:.1f}h daylight {} sunset |{}|'.format(
            f(sunrise), hours, f(sunset), ''.join(sky),
        )

if __name__ == '__main__':
    main(sys.argv[1:])
