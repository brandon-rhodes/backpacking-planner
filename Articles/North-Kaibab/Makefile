
section2.svg: section.svg trail_elevation.csv transform.py
	python transform.py

trail_elevation.csv: track_reading.py
	python track_reading.py

section.svg: i-2688.pdf
	pdftocairo \
	    -x 2800 -y 1900 -W 500 -H 200 \
	    -svg i-2688.pdf $@
