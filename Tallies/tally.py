#!/usr/bin/env python3

import datetime as dt
import fileinput
import sys

def main(argv):
    for line in fileinput.input():
        line = line.strip()
        if not line:
            continue
        if not line[0].isdigit():
            print(line)
            continue
        fields = iter(line.split())
        description = []
        duration = dt.timedelta(0)
        miles = 0.0
        for field in fields:
            wordish = not field[0].isdigit() or not field[-1].isdigit()
            if wordish and field[0] != '-':
                description.append(field)
                continue
            if '.' in field:
                miles += float(field)
            else:
                hour = int(field[:2])
                minute = int(field[2:])
                start = dt.datetime(1900, 1, 1, hour, minute)

                field = next(fields)
                hour = int(field[:2])
                minute = int(field[2:])
                end = dt.datetime(1900, 1, 1, hour, minute)

                duration += end - start

        if not duration:
            continue

        hours = duration.total_seconds() / 3600.0
        mph = miles / hours
        print('{:.1f} miles in {:.2f} hours = {:.1f} mph {}'.format(
            miles, hours, mph, ' '.join(description)))

if __name__ == '__main__':
    main(sys.argv[1:])
