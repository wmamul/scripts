#!/bin/zsh

WALLS_PATH="$HOME/Pictures/Wallpapers" 
PAPES=($(ls $WALLS_PATH | tr -s ' ' | cut -f 9 -d ' '))
PAPES_COUNT=${#PAPES[*]}
PAPES_LAST_INDEX=$(expr $PAPES_COUNT - 1)
RANDOM_NUMBER=$(shuf -i 0-$PAPES_LAST_INDEX -n 1)

DISPLAY=:0 feh --bg-fill $WALLS_PATH/${PAPES[$RANDOM_NUMBER]}
