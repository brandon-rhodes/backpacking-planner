
FDFS=$(wildcard $(HOME)/Plain/forms/*.fdf)
PDFS=$(patsubst $(HOME)/Plain/forms/%.fdf, $(HOME)/Downloads/%.pdf, $(FDFS))

all: $(PDFS)

$(PDFS): $(HOME)/Downloads/%.pdf: $(HOME)/Plain/forms/%.fdf permit-request.pdf
	pdftk permit-request.pdf fill_form $< output - | pdftk A=- cat A2 output $@

permit-request.pdf:
	wget https://www.nps.gov/grca/planyourvisit/upload/permit-request.pdf
