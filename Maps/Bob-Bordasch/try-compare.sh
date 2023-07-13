#!/bin/bash

a='www.bobbordasch.com/trips/GC-Oct13-Flip/Map-Day1.jpg'
b='www.bobbordasch.com/trips/GC-Oct13-Flip/Map-Day2.jpg'

compare \
    -metric RMSE \
    -subimage-search \
    $a $b locations.png
