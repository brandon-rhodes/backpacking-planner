# Helpers to read GPS tracks.
#
# https://www.gaiagps.com/hike/1359/bright-angel-trailhead-via-north-kaibab-trail-and-bright-angel-trail/
#
# ^ Next step: scan that URL for track IDs then use them in URLs like:
#
# https://www.gaiagps.com/api/objects/track/2a24d194-fb51-4770-b5df-3e11256d4fe2.gpx/

import xml.etree.ElementTree as ET

def main():
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    for path in [
            'Bright Angel Trailhead via North Kaibab Trail'
            ' and Bright Angel Trail.gpx',
            'route-111618-093831-am.gpx',
    ]:
        print(path)
        add_to_plot(path, ax)
    ax.grid()
    #ax.set(xlabel='time (s)', ylabel='voltage (mV)', title='Title')
    #ax.set_aspect(aspect=1.0)
    #ax.axhline(1.0)
    #ax.axvline(1.0)
    #plt.legend()
    fig.savefig('tmp.png')

def add_to_plot(path, ax):
    gpx = '{http://www.topografix.com/GPX/1/1}'
    root = ET.parse(path).getroot()
    elevation = []
    latitude = []
    for trkpt in root.findall(f'.//{gpx}trkpt'):
        elevation.append(float(trkpt.get('ele')))
        latitude.append(float(trkpt.get('lat')))
    for rtept in root.findall(f'.//{gpx}rtept'):
        latitude.append(float(rtept.get('lat')))
        ele = rtept[0]
        elevation.append(float(ele.text))
    print(elevation)
    ax.plot(latitude, elevation, label='label') #, linestyle='--')

if __name__ == '__main__':
    main()

