#!/usr/bin/env python3
#
# Print a week's worth of temperatures from a NCEI CDO data file
# that has two data colums, maximum and minimum temperature.
# https://www.ncdc.noaa.gov/cdo-web/datasets#GHCND

import csv

def main():
    dates = []
    for day in range(27, 30+1):
        dates.append(f'-09-{day:02}')
    for day in range(1, 3+1):
        dates.append(f'-10-{day:02}')

    high = {}
    low = {}
    f = open('2262382.csv')
    rows = csv.reader(f)
    next(rows)
    for station, name, date, tmax, tmin in rows:
        high[date] = tmax
        low[date] = tmin

    print('Date', end='   ')
    for date in dates:
        print(date[-2:], end=' ')
    print(end='  ')
    for date in dates:
        print(date[-2:], end=' ')
    print()

    year_start = int(min(high)[:4])
    year_end = int(max(high)[:4])
    for year in range(year_start, year_end + 1):
        print(year, end='   ')
        for date in dates:
            key = f'{year}{date}'
            print(low.get(key, '--'), end=' ')
        print(end='  ')
        for date in dates:
            key = f'{year}{date}'
            print(high.get(key, '--'), end=' ')
        print()

if __name__ == '__main__':
    main()
