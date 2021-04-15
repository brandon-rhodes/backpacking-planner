
LEGENDS := legend-Mr.png

all: triptych1.png triptych2.png triptych3.png column.png $(LEGENDS)

triptych1.png triptych2.png triptych3.png: section3.png crop_triptych.py
	python crop_triptych.py

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

$(LEGENDS): crop_legends.py layers-screenshot-1.png layers-screenshot-2.png
	python crop_legends.py

# Rotate and fix Project Gutenberg image.

column.png: pg010.jpg
#	convert $< -rotate -1 -white-threshold 92% -adaptive-sharpen 1x9 $@
#	convert $< -rotate -1 -white-threshold 92% $@
	convert $< -rotate -0.8 -white-threshold 92% -unsharp 2 $@
#	convert $< -rotate -0.8 -white-threshold 92% -morphology Open Square $@

# From this Project Gutenberg book:
# https://www.gutenberg.org/files/48126/48126-h/48126-h.htm

pg010.jpg:
	rm -f pg010.jpg
	wget https://www.gutenberg.org/files/48126/48126-h/images/pg010.jpg
