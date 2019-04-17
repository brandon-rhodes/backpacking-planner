
2019-gc.pdf: Escalante_Route.pdf 2019-gc.txt.pdf
	pdftk $^ cat output - | pdfnup --nup 2x2 --no-landscape -o $@

2019-gc.txt.pdf: 2019-gc.txt
	,enscript 2019-gc.txt

Escalante_Route.pdf:
	wget https://www.nps.gov/grca/planyourvisit/upload/Escalante_Route.pdf
