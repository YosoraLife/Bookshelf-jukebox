#!/bin/bash

# Set display
export DISPLAY=:0.0

# Disable display power management
xset s noblank
xset s off
xset -dpms

# Subpress the warning baar
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/thorium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/thorium/Default/Preferences

# Open a single tab
/usr/bin/thorium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:32500/ &

python3 /home/$USER/plexamp-jukebox/plexamp-controls.py &
python3 /home/$USER/plexamp-jukebox/plexamp-nfc-reader.py &

# Allow switching between tabs on buttonpress
# /usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:32500/ http://localhost/settings &
# while true; do
#          xdotool keydown ctrl+Next; xdotool keyup ctrl+Next;
#       sleep 15
# done
