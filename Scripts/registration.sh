#!/bin/bash
#
# For using Chrome to check campsite availability at:
# https://www.recreation.gov/permits/4675337/registration/detailed-availability?date=2025-10-10

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
