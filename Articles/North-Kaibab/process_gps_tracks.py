# Helpers to read GPS tracks.

import csv
import numpy as np
import os
import re
import time
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from geopy.distance import distance as geopy_distance

FEET_IN_A_METER = 3.2808399

def main():
    track_ids = read_tracks()
    tracks = []

    for track_id in track_ids:
        print(track_id, end=' ')
        content = load_track(track_id)
        track = parse_gpx(content)
        tracks.append(track)

    fig, ax = plt.subplots()
    for track in tracks:
        add_to_plot(track, ax)

    latitude, longitude, elevation = average_tracks(tracks)
    miles = np.array(compute_miles(latitude, longitude))

    ax.plot(latitude, elevation, '-k')
    ax.grid()
    #ax.set(xlabel='time (s)', ylabel='voltage (mV)', title='Title')
    #ax.set_aspect(aspect=1.0)
    #ax.axhline(1.0)
    #ax.axvline(1.0)
    #plt.legend()
    fig.savefig('elevations.png')

    fig, ax = plt.subplots()
    ax.plot(latitude, longitude, '-k')
    ax.grid()
    fig.savefig('longitudes.png')

    elevation *= FEET_IN_A_METER

    table = np.array([latitude, longitude, elevation.round(2), miles.round(5)])

    with open('trail_elevation.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['latitude', 'longitude', 'elevation', 'miles'])
        writer.writerows(table.T)

def read_tracks():
    with open('../../../Downloads/tmp.html') as f:
        html = f.read()
    track_ids = set(re.findall(r'/datasummary/track/([^/]+)/', html))
    return sorted(track_ids)

def load_track(track_id):
    if not os.path.isdir('cache'):
        os.mkdir('cache')
    path = 'cache/' + track_id
    if not os.path.exists(path):
        url = f'https://www.gaiagps.com/api/objects/track/{track_id}.gpx/'
        import urllib.request
        time.sleep(0.8)
        with urllib.request.urlopen(url) as f:
            data = f.read()
        content = data.decode('utf-8')
        with open(path, 'w') as f:
            f.write(content)
    else:
        with open(path) as f:
            content = f.read()
    return content

def parse_gpx(content):
    gpx = '{http://www.topografix.com/GPX/1/1}'
    root = ET.fromstring(content) #.getroot()
    latitude = []
    longitude = []
    elevation = []
    for trkpt in root.findall(f'.//{gpx}trkpt') + root.findall(f'.//{gpx}rtept'):
        latitude.append(float(trkpt.get('lat')))
        longitude.append(float(trkpt.get('lon')))
        ele = trkpt.find(f'{gpx}ele')
        elevation.append(float(ele.text))
    if not elevation:
        print('-')
        return
    print(len(elevation), 'points')
    track = latitude, longitude, elevation
    return track

def average_tracks(tracks):
    # Actually, use the median.  The average winds up way off because of
    # one back track that recorded a consistent -1000 feet.  But the
    # median is wonderful because it chooses the middle sample of the
    # many tracks, giving a realistic but representative elevation.

    # Original, from mousing over trail on Google Earth:
    # x_min = 36. + 6./60
    # x_max = 36. + 11./60 + 35./3600

    # Revised, from transform.py, which got them by matching D-D' line
    # on contour map against Google Earth, then adjusting x_min to start
    # at the Colorado River:
    x_min = 36 + 5/60 + 47.5/3600 #+ 21/3600
    x_max = 36 + 11/60 + 19/3600

    x = np.arange(x_min, x_max, 0.0002)
    x = np.around(x, 4)
    longitude_stack = []
    elevation_stack = []
    # ysum = 0.0 * x
    # n = 0
    for track in tracks:
        latitude, longitude, elevation = track
        latitude = np.array(latitude)
        longitude = np.array(longitude)
        elevation = np.array(elevation)

        order = latitude.argsort()
        latitude = latitude[order]
        longitude = longitude[order]
        elevation = elevation[order]

        longitude_stack.append(np.interp(x, latitude, longitude))
        elevation_stack.append(np.interp(x, latitude, elevation))

    longitude_stack = np.array(longitude_stack)
    elevation_stack = np.array(elevation_stack)

    print('Computing medians over', longitude_stack.shape)

    longitude = np.median(longitude_stack, axis=0)
    longitude = np.around(longitude, 4)

    elevation = np.median(elevation_stack, axis=0)
    elevation = np.around(elevation, 1)

    return np.array([x, longitude, elevation])

def compute_miles(latitude, longitude):
    pairs = list(zip(latitude, longitude))
    prev_lat, prev_lon = pairs[0]
    m = 0.0
    miles = []
    for lat, lon in pairs:
        m += geopy_distance((prev_lat, prev_lon), (lat, lon)).miles
        miles.append(m)
        prev_lat, prev_lon = lat, lon
    return miles

def add_to_plot(track, ax):
    latitude, longitude, elevation = track
    ax.plot(latitude, elevation, ',', label='label', alpha=0.5)
    #, linestyle='--')

if __name__ == '__main__':
    main()
