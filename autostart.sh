#!/bin/bash

# https://github.com/BlueDev5/Arco-DotFiles/blob/main/.config/qtile/scripts/autostart.sh

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}

run xrandr --output eDP-1 --primary --mode 1280x720
run nitrogen --restore &
run nm-applet &
run pamac-tray &
run xfce4-power-manager &