import numpy as np
import csv
import os
from collections import Counter, defaultdict

lows = defaultdict(list)
highs = defaultdict(list)

f = open('4325949.csv')
#yyy=[]

def deres(n):
    return (n + 2.5) // 5 * 5

rows = list(csv.DictReader(f))

for row in rows:
    # print(row)
    # exit()

    if not row['TMIN'] or not row['TMAX']:
        continue

    row_date = row['DATE']
    row_doy = row_date[5:]
    date = np.datetime64('2020-' + row_doy)
    #dates.append(date)

    # if row['DATE'][5:] == '01-01':
    #     yyy.append(row['TMAX'])

    tmin = int(row['TMIN'])
    tmax = int(row['TMAX'])

    if row_doy == '10-25' and tmax < 60:
        print(row_date, tmin)

    tmin = deres(tmin)
    lows[date].append(tmin)

    tmax = deres(tmax)
    highs[date].append(tmax)

for mmdd in '10-25', '10-31':
    date = np.datetime64('2020-' + mmdd)

    number_of_years = min(len(lows[date]), len(highs[date]))
    over = f'over {number_of_years} years'

    high_counts = Counter(highs[date])
    print(high_counts)

    low_counts = Counter(lows[date])
    print(low_counts)

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    lowx = np.array(list(low_counts.keys()))
    lowy = low_counts.values()

    highx = np.array(list(high_counts.keys()))
    highy = high_counts.values()

    w = 1.2

    ax.bar(lowx + w/2, lowy, color='blue', width=w, label='Lows')
    ax.bar(highx - w/2, highy, color='red', width=w, label='Highs')

    ax.bar(lowx - w/2, lowy, color='blue', width=w)
    ax.bar(highx + w/2, highy, color='red', width=w)

    highest = max(max(lowy), max(highy))
    ax.hlines(range(highest), 0, 100, color='white')

    ax.set(
        xlabel='Temperature rounded to nearest 5°F',
        ylabel='Days with a high or low at that temperature',
        title='Highs and Lows at Phantom Ranch'
        f'\non {date.item().strftime("%B %d")} {over}',
    )
    ax.set_xlim(30, 100)
    ax.set_xlim(30, 100)

    plt.legend()

    fig.savefig(f'tmp-{mmdd}.png')

