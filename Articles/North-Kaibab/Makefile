
LEGENDS := legend-Mr.png

all: index.html triptych1.png triptych2.png triptych3.png map.png $(LEGENDS)

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

# convert -size 768x1024 xc:none \
# 	-draw "roundrectangle 0,0,768,1024,120,120" /tmp/mask.png
# convert $(HOME)/Downloads/hikers1.jpeg -scale x1024 -crop 768x1024 \
# 	-matte /tmp/mask.png -compose DstIn -composite \
# 	-background none \
# 	/tmp/hikers1.png
# convert $(HOME)/Downloads/hikers2.jpeg \
# 	-background none \
# 	-scale x1024 -crop 768x1024 \
# 	-matte /tmp/mask.png -compose DstIn -composite \
# 	 /tmp/hikers2.png
# convert +append \
# 	-background white \
# 	/tmp/hikers1.png /tmp/hikers2.png \
# 	-background white \
# 	hikers.jpg

$(LEGENDS): crop_legends.py layers-screenshot-1.png layers-screenshot-2.png
	python crop_legends.py

publish: index.html
	cp index.html \
		HighAlpine.otf \
		Charis*.woff \
		legend*.png \
		map.png \
		triptych*.png \
		$(HOME)/tmp/
