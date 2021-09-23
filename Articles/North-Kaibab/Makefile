
LEGENDS := legend-Mr.png

ALL := index.html hikers.jpg map.png \
	triptych1.png triptych2.png triptych3.png \
	$(LEGENDS)

all: $(ALL)

index.html: text.md text.py
	pandoc -f markdown_strict $< | python text.py > /tmp/out
	mv /tmp/out $@

text.md: $(HOME)/Plain/Drafts/north-kaibab-geology
	cp $< $@

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

map.png: map-0.png
	convert +append map-0.png map-1.png map.png

map-0.png: corridor_map.pdf
	convert -density 25 $< map.png

hikers.jpg: hikers.py
	python hikers.py

D := $(HOME)/Downloads
FONTS := CharisSIL-Italic.woff GentiumPlus-Regular.woff HighAlpine.otf

fonts: $(FONTS)

HighAlpine.otf: $D/HighAlpine.otf
	cp $< $@

CharisSIL-Italic.woff: $D/CharisSIL-6.001/web/CharisSIL-Italic.woff
	./strip_woff.py $< $@ text.md

GentiumPlus-Regular.woff: $D/GentiumPlus-6.001/web/GentiumPlus-Regular.woff
	./strip_woff.py $< $@ text.md

$(LEGENDS): crop_legends.py layers-screenshot-1.png layers-screenshot-2.png
	python crop_legends.py

DEST := $(HOME)/tmp
DEST := $(HOME)/rhodesmill.org/brandon/north-kaibab-trail

publish: all $(FONTS)
	mkdir -p $(DEST)
	cp $(ALL) $(FONTS) legend-*.png $(DEST)
