#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import re
import sys
from collections import defaultdict

corridor_numbers = {'CIG': 1, 'CBG' :2, 'CCG': 3}
corridor = set(corridor_numbers)

simple_categories = [
    ('Corridor (other)', {'CIG', 'CBG', 'CCG'}),
    ('Corridor (winter)', {'CIG', 'CBG', 'CCG', 'NCG'}),
    ('Clear Creek', {'CIG', 'CBG', 'AK9'}),
    ('Boucher', {'BN9', 'BM7'}),
    ('Tonto West', {'BM8', 'BM7', 'BL8', 'BL7', 'BL6', 'BL5', 'BL4', 'CIG'}),
    ('Tanner to Confluence', {'BA9', 'BB9'}),
    ('Horseshoe Hance Cottonwood', {'BE9', 'BF5', 'BG9'}),
    ('New Hance Trail', {'BD9'}),
    ('Tanner to Horseshoe', {'BB9', 'BC9', 'BD9', 'BE9', 'BF5'}),
    ('Tonto East', {'BG9', 'BH9', 'BJ9'}),
    ('Nankoweap Trail', {'AE9'}),
    ('Point Sublime (North Rim)', {'NH1'}),
    ('Point Final (North Rim)', {'NA1'}),
    ('Soap Creek (Marble Canyon)', {'AB0'}),
    ('South Bass', {'BQ9'}),
    ('South Canyon (Marble Canyon)', {'AC9'}),
    ('Tapeats and Deer Creek', {'AM9', 'AW7', 'AW8', 'AX7', 'AY9'}),
    ('Tuweep', {'TCG'}),
    ('Widforss Trail (North Rim)', {'NF9'}),
]

def main(argv):
    parser = argparse.ArgumentParser(description='Load Grand Canyon stats')
    parser.parse_args(argv)

    stats = list(read_stats())
    stats.sort()

    by_category = defaultdict(list)
    for count, itinerary in stats:
        # print('{:5}  {}'.format(count, itinerary))
        category = assign_category(itinerary)
        by_category[category].append((count, itinerary))

    print()

    # exit()
    for category, itineraries in sorted(by_category.items()):
        print('{:5}  {}'.format(
            sum(count for count, itinerary in itineraries),
            category,
        ))
        for count, itinerary in itineraries:
            print('{:5}  {:5}  {}'.format('', count, ','.join(itinerary)))
        print()

def read_stats():
    for line in open(os.path.dirname(os.path.abspath(__file__)) + '/text'):
        line = line.strip()
        if not line or line[0] == '#':
            continue
        pieces = line.split()
        for i in range(0, len(pieces), 2):
            yield int(pieces[i]), pieces[i+1].replace(',OUT', '').split(',')

MOVES = {0: '', -1: 's', 1: 'n'}

def assign_category(itinerary):
    codes = set(itinerary)
    if codes <= corridor:
        nums = [corridor_numbers[code] for code in itinerary]
        moves = ''.join(
            move_of(nums[i], nums[i+1]) for i in range(len(nums) - 1)
        )
        print(itinerary, moves)
        if not moves:
            return('Corridor: {} only'.format(itinerary[0]))
        if re.match(r'n+$', moves):
            return('Corridor: northbound')
        if re.match(r's+$', moves):
            return('Corridor: southbound')
        if re.match(r'n+s+$', moves):
            return('Corridor: north then south')
        if re.match(r's+n+$', moves):
            return('Corridor: south then north')
        # delta = [nums[i+1] - nums[i] for i in range(len(nums) - 1)]
        # if all(d == 0 for d in delta):
        #     return('corridor_only_' + itinerary[0])
        # delta2 = delta #[delta[i+1] - delta[i] for i in range(len(delta) - 1)]
        # if all(d <= 0 for d in delta2):
        #     return('corridor_from_south')
        # if all(d >= 0 for d in delta2):
        #     return('corridor_from_north')
        # print(itinerary, delta)
    for name, code_set in simple_categories:
        if codes <= code_set:
            return name
    return '~other'

def move_of(a, b):
    return 'n' if b > a else 's' if a > b else ''

if __name__ == '__main__':
    main(sys.argv[1:])
