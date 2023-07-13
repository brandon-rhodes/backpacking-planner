#!/bin/bash
#
# Before running this again, I should probably build a URL whitelist to
# limit image downloads to maps only, and also maybe switch over to
# archive.org so that I don't impose a bandwidth drain on the web site.
# The download was, alas, rather hefty:
#
# Total wall clock time: 3m 57s
# Downloaded: 4174 files, 708M in 1m 6s (10.7 MB/s)

cd "$(readlink -f $(dirname "${BASH_SOURCE[0]}"))"

if [ -d www.bobbordasch.com ]
then
    echo $0: Site has already been downloaded
    exit 0
fi

# https://www.linuxjournal.com/content/downloading-entire-web-site-wget

wget \
    --mirror \
    --page-requisites \
    --html-extension \
    --domains www.bobbordasch.com \
    http://www.bobbordasch.com/
