# Helpers to read GPS tracks.

import csv
import numpy as np
import os
import re
import time
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

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

    average = latitude, elevation = average_tracks(tracks)
    ax.plot(latitude, elevation, '-k')
    ax.grid()
    #ax.set(xlabel='time (s)', ylabel='voltage (mV)', title='Title')
    #ax.set_aspect(aspect=1.0)
    #ax.axhline(1.0)
    #ax.axvline(1.0)
    #plt.legend()
    fig.savefig('elevations.png')

    with open('trail_elevation.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['latitude', 'elevation'])
        writer.writerows(average.T)

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
    elevation = []
    latitude = []
    for trkpt in root.findall(f'.//{gpx}trkpt'):
        ele = trkpt.find(f'{gpx}ele')
        elevation.append(float(ele.text))
        latitude.append(float(trkpt.get('lat')))
    for rtept in root.findall(f'.//{gpx}rtept'):
        latitude.append(float(rtept.get('lat')))
        ele = rtept[0]
        elevation.append(float(ele.text))
    if not elevation:
        print('-')
        return
    print(len(elevation), 'elevations')
    return latitude, elevation

def average_tracks(tracks):
    # Actually, use the median.  The average winds up way off because of
    # one back track that recorded a consistent -1000 feet.  But the
    # median is wonderful because it chooses the middle sample of the
    # many tracks, giving a realistic but representative elevation.
    x_min = 36. + 6./60
    x_max = 36. + 11./60 + 35./3600
    x = np.arange(x_min, x_max, 0.0002)
    x = np.around(x, 4)
    ystack = []
    # ysum = 0.0 * x
    # n = 0
    for track in tracks:
        latitude, elevation = track
        latitude = np.array(latitude)
        elevation = np.array(elevation)
        order = latitude.argsort()
        latitude = latitude[order]
        elevation = elevation[order]
        y = np.interp(x, latitude, elevation)
        ystack.append(y)
    ystack = np.array(ystack)
    print('Computing median over', ystack.shape)
    y = np.median(ystack, axis=0)
    y = np.around(y, 1)
    return np.array([x, y])

def add_to_plot(track, ax):
    latitude, elevation = track
    ax.plot(latitude, elevation, ',', label='label', alpha=0.5)
    #, linestyle='--')

if __name__ == '__main__':
    main()
