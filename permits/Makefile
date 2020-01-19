
FDFS=$(wildcard $(HOME)/Plain/forms/*.fdf)
PDFS=$(patsubst $(HOME)/Plain/forms/%.fdf, $(HOME)/Downloads/%.pdf, $(FDFS))

all: $(PDFS)

$(PDFS): $(HOME)/Downloads/%.pdf: $(HOME)/Plain/forms/%.fdf
	pdftk permit-request.pdf fill_form $< output - | pdftk A=- cat A2 output $@

permit-2020a.pdf: permit-request.pdf ~/Plain/forms/grand-canyon-2020a.fdf
	pdftk permit-request.pdf fill_form ~/Plain/forms/grand-canyon-2020a.fdf output - | pdftk A=- cat A2 output ~/Downloads/permit-out.pdf

permit-out.pdf: permit-request.pdf ~/Plain/forms/grand-canyon-permit.fdf
	pdftk permit-request.pdf fill_form ~/Plain/forms/grand-canyon-permit.fdf output - | pdftk A=- cat A2 output ~/Downloads/permit-out.pdf

permit-request.pdf:
	wget https://www.nps.gov/grca/planyourvisit/upload/permit-request.pdf
