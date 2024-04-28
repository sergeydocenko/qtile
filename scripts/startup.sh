#!/bin/bash

xrandr --output eDP-1 --primary --mode 1280x720

pkill greenclip
pkill nm-applet 
pkill xfce4-power-manager 
pkill sxhkd 
pkill dunst

greenclip daemon &
nm-applet &
xfce4-power-manager --daemon &
sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &
dunst &