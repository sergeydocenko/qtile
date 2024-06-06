#!/bin/bash

notify-send "Date/Time" "$(date +'%Y-%m-%d %H:%M:%S')\nRestart Network Manager..."

echo qwe | sudo -S pkill NetworkManager 
sleep 1s 
echo qwe | sudo -S NetworkManager

notify-send "Date/Time" "$(date +'%Y-%m-%d %H:%M:%S')\nRestarted"
