
D := $(HOME)/Downloads
F := $(HOME)/Plain/Forms

FDFS=$(wildcard $F/*.fdf)
PDFS=$(patsubst $F/%.fdf, $D/%.pdf, $(FDFS))

all: $(PDFS)

$(PDFS): $D/%.pdf: $F/%.fdf \
		permit-request.pdf permit-request.pdf.1 \
		overlay.pdf
	pdftk permit-request.pdf`grep -q Initial $< && echo .1` fill_form $< output - flatten \
	| pdftk - stamp overlay.pdf output - \
	| pdftk A=- cat A2 output $@

overlay.pdf: overlay.py
	python3 $< $@

req: $D/request-2022.pdf

$D/request-2022.pdf: $D/grand-canyon-2022a.pdf $D/grand-canyon-2022b.pdf
	pdftk $^ cat output $@

# permit-request.pdf:
# 	wget https://www.nps.gov/grca/planyourvisit/upload/permit-request.pdf
