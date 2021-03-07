
triptych1.png triptych2.png triptych3.png: section3.png crop.py
	python crop.py

section3.png: section2.svg
	inkscape --export-dpi=300 --export-png=$@ $<

section2.svg: section.svg trail_elevation.csv transform.py
	python transform.py

trail_elevation.csv: process_gps_tracks.py
	python process_gps_tracks.py

section.svg: i-2688.pdf
	pdftocairo \
	    -x 2800 -y 1900 -W 500 -H 200 \
	    -svg i-2688.pdf $@
