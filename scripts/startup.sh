#!/bin/bash

xrandr --output eDP-1 --primary --mode 1280x720

pkill greenclip
pkill nm-applet 
pkill xfce4-power-manager 
pkill sxhkd 
pkill dunst
pkill volumeicon

greenclip daemon &
nm-applet &
xfce4-power-manager &
#sxhkd -c "$HOME/.config/qtile/sxhkd/sxhkdrc" &
sxhkd -c "/home/bams/.config/qtile/sxhkd/sxhkdrc" &
dunst &
volumeicon &

setxkbmap -layout "us,ru" -option "grp:caps_toggle,grp_led:caps"