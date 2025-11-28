#!/usr/bin/env python3

import datetime as dt
import fileinput
import sys
from collections import defaultdict

def main(argv):
    date = '(Unknown)'
    dates = []
    date_miles = defaultdict(float)
    date_segments = defaultdict(list)
    factor = 1.0
    for line in fileinput.input():
        line = line.strip()
        if not line:
            continue
        if line == 'km':
            factor = 0.62137119
            continue
        if not line[0].isdigit():
            print(line)
            continue
        fields = iter(line.split())
        description = []
        duration = dt.timedelta(0)
        miles = 0.0
        fields = list(fields)
        for field in fields:
            if field.startswith('(') and field.endswith(')'):
                date = field[1:-1]
                break
        fields = iter(fields)
        for field in fields:
            wordish = not field[0].isdigit() or not field[-1].isdigit()
            if wordish and field[0] != '-':
                description.append(field)
                continue
            if '.' in field:
                miles += float(field) * factor
            else:
                check_hhmm(field)
                hour = int(field[:2])
                minute = int(field[2:])
                start = dt.datetime(1900, 1, 1, hour, minute)

                field = next(fields)
                check_hhmm(field)
                hour = int(field[:2])
                minute = int(field[2:])
                end = dt.datetime(1900, 1, 1, hour, minute)

                date_segments[date].append((start, end))
                duration += end - start

        if not duration:
            continue

        date_miles[date] += miles
        hours = duration.total_seconds() / 3600.0
        mph = miles / hours
        print('{:.1f} miles in {:.2f} hours = {:.1f} mph {}'.format(
            miles, hours, mph, ' '.join(description)))

    print()

    date_segments = dict(date_segments)
    for date, segments in sorted(date_segments.items()):
        segments = sorted(segments)
        day_start = segments[0][0]
        day_end = segments[-1][1]
        duration = day_end - day_start
        m, s = divmod(int(duration.total_seconds()), 60)
        h, m = divmod(m, 60)
        miles = date_miles[date]
        mph = date_miles[date] / (h + m / 60.0)
        print(
            date, day_start.strftime('%H:%M'), '-', day_end.strftime('%H:%M'),
            f' {h:2}h {m:2}m  {m:.1f} miles  {mph:.2f} mph',
        )

def check_hhmm(field):
    if not (len(field) == 4 and field.isdigit()):
        exit(f'Error: expected field to be HHMM: {field!r}')

if __name__ == '__main__':
    main(sys.argv[1:])
