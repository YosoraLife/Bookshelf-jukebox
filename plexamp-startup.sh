#!/bin/bash

# Disable display power management
xset s noblank
xset s off
xset -dpms

# Disable mouse
unclutter -root &

# Subpress the warning baar
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/chromium/Default/Preferences

# Open a single tab
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:32500/ &



# Allow switching between tabs on buttonpress
# /usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:32500/ http://localhost/settings &
# while true; do
#          xdotool keydown ctrl+Next; xdotool keyup ctrl+Next;
#       sleep 15
# done
