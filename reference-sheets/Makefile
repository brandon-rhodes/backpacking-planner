
2020-gc.pdf: 2020-gc.txt.pdf
	pdftk $^ cat output /tmp/pdf
	pdfnup -n 2 -o /tmp/pdf2 /tmp/pdf
	pdftk /tmp/pdf2 cat 1-end output $@

2020-gc.txt.pdf: 2020-gc.txt
	,enscript 2020-gc.txt

2019-gc.pdf: Escalante_Route.pdf 2019-gc.txt.pdf /home/brandon/Dropbox/Backpacking/Grand_Canyon/1815140.pdf MessierChart-Spring.pdf
	pdftk $^ cat output - | pdfnup --nup 2x2 --no-landscape -o /dev/stdout | pdftk - cat 1-endsouth output $@

2019-gc.txt.pdf: 2019-gc.txt
	,enscript 2019-gc.txt

permit-upside-down.pdf: /home/brandon/Dropbox/Backpacking/Grand_Canyon/1815140.pdf
	pdftk $^ cat 1south 3south output $@

Escalante_Route.pdf:
	wget https://www.nps.gov/grca/planyourvisit/upload/Escalante_Route.pdf
