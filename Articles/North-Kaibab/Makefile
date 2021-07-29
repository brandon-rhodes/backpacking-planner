
LEGENDS := legend-Mr.png

all: index.html triptych1.png triptych2.png triptych3.png $(LEGENDS)

index.html: text.md text.py
	pandoc -f markdown_strict $< | python text.py > /tmp/out
	mv /tmp/out $@

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
