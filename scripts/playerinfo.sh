#!/bin/sh

artist=$(playerctl --player=audacious metadata --format "{{artist}}")
title=$(playerctl --player=audacious metadata --format "{{title}}")

notify-send "Now playing..." "Artist: $artist\nTile:$title"