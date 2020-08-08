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
    ('Corridor: Other', {'CIG', 'CBG', 'CCG'}),
    ('Corridor + Winter North Rim Campground', {'CIG', 'CBG', 'CCG', 'NCG'}),
    ('Corridor + North Rim Area', {'CIG', 'CBG', 'CCG', 'NRA'}),
    ('Corridor + Clear Creek', {'CIG', 'CBG', 'AK9'}),
    ('N: Nankoweap Trail', {'AE9'}),
    ('S: Boucher', {'BN9', 'BM7'}),
    ('S: Tonto West', {'BM8', 'BM7', 'BL8', 'BL7', 'BL6', 'BL5', 'BL4', 'CIG'}),
    ('S: Tanner and Confluence', {'BA9', 'BB9'}),
    ('S: Horseshoe Hance Cottonwood New Hance', {'BD9', 'BE9', 'BF5', 'BG9'}),
    ('S: Tanner to New Hance and Grandview', {'BB9','BC9','BD9','BE9','BF5'}),
    ('S: Tonto East', {'BG9', 'BH9', 'BJ9'}),
    ('North Rim: Point Sublime', {'NH1'}),
    ('North Rim: Point Final', {'NA1'}),
    ('Marble Canyon: Soap Creek', {'AB0'}),
    ('S: South Bass', {'BQ9'}),
    ('Marble Canyon: South Canyon', {'AC9'}),
    ('N: Tapeats and Deer Creek', {'AM9', 'AW7', 'AW8', 'AX7', 'AY9'}),
    ('North Rim: Tuweep', {'TCG'}),
    ('North Rim: Widforss Trail', {'NF9'}),
]

def main(argv):
    parser = argparse.ArgumentParser(description='Load Grand Canyon stats')
    parser.parse_args(argv)

    stats = list(read_stats())
    stats.sort(reverse=True)

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

    print('Total: {} instances of {} unique itineraries:'.format(
        len(stats),
        sum(count for count, itinerary in stats),
    ))

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
        #print(itinerary, moves)
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
    return '~Other~'

def move_of(a, b):
    return 'n' if b > a else 's' if a > b else ''

if __name__ == '__main__':
    main(sys.argv[1:])
