# Helpers to read GPS tracks.

import os
import re
import time
import xml.etree.ElementTree as ET

def main():
    track_ids = read_tracks()
    content_list = []

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    for track_id in track_ids:
        content = load_track(track_id)
        content_list.append(content)
        add_to_plot(content, ax)

    ax.grid()
    #ax.set(xlabel='time (s)', ylabel='voltage (mV)', title='Title')
    #ax.set_aspect(aspect=1.0)
    #ax.axhline(1.0)
    #ax.axvline(1.0)
    #plt.legend()
    fig.savefig('tmp.png')

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

def add_to_plot(content, ax):
    gpx = '{http://www.topografix.com/GPX/1/1}'
    root = ET.fromstring(content) #.getroot()
    elevation = []
    latitude = []
    for trkpt in root.findall(f'.//{gpx}trkpt'):
        ele = trkpt.get('ele')
        if ele is None:
            continue
        elevation.append(float(ele))
        latitude.append(float(trkpt.get('lat')))
    for rtept in root.findall(f'.//{gpx}rtept'):
        latitude.append(float(rtept.get('lat')))
        ele = rtept[0]
        elevation.append(float(ele.text))
    if not elevation:
        return
    print(len(elevation))
    ax.plot(latitude, elevation, ',', label='label', alpha=0.5)
    #, linestyle='--')

if __name__ == '__main__':
    main()
