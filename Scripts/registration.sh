#!/bin/bash

set -ex

dt () {
       xdotool "$@"
       sleep 1
}

sleep 5
dt key ctrl+r
sleep 5
dt key ctrl+f
dt type group
dt key ctrl+Return
dt key Tab
dt type 1
dt key ctrl+f
dt type classic
dt key ctrl+Return
dt key ctrl+f
