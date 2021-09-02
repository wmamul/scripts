#!/usr/bin/zsh

PAPES=($(ls $WALLS_PATH | awk '{print $9}'))
PAPES_COUNT=${#PAPES[*]}
RANDOM_NUMBER=$(shuf -i 0-$(expr $PAPES_COUNT - 1) -n 1)

DISPLAY=:0 feh --bg-fill $WALLS_PATH/${PAPES[$RANDOM_NUMBER]}
