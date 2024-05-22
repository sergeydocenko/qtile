#!/bin/bash

CONFIGS="/home/bams/.config/qtile/configs"

xrandr --output eDP-1 --primary --mode 1280x720

pkill greenclip
pkill nm-applet 
pkill xfce4-power-manager 
pkill sxhkd 
pkill dunst
pkill volumeicon
pkill picom

greenclip daemon &
nm-applet &
xfce4-power-manager &
sxhkd -c "$CONFIGS/sxhkd/sxhkdrc" &
DUNST_CONFIG="$CONFIGS/dunst/dunstrc" dunst &
volumeicon &
picom --config "$CONFIGS/picom/picom.conf" &

setxkbmap -layout "us,ru" -option "grp:caps_toggle,grp_led:caps"