#!/bin/bash

#################################
### START OF INSTALL CONTROLS ###
#################################

cd ~

# Install tools
sudo apt install -y python3 pip gcc-arm-linux-gnueabihf plymouth plymouth-themes jq
pip install pn532pi curlify requests

# Download the jukebox scripts:
git clone https://gitlab.com/YosoraLife/bookshelf-jukebox
cd bookshelf-jukebox

# Enable the startup script and make it start at boot:
chmod u+x jukebox-startup.sh

# Add startup script to crontab
(crontab -l; echo "@reboot /usr/bin/sh /home/dietpi/bookshelf-jukebox/jukebox-startup.sh &")|awk '!x[$0]++'|crontab -

# Set quiet startup screen:
sudo sed -i 's/console=tty1/console=tty3 loglevel=3 quiet logo.nologo vt.global_cursor_default=0/' /boot/cmdline.txt

# Set plymouth startup theme
sudo plymouth-set-default-theme -R spinner

# Set plymouth watermark
sudo cp ~/bookshelf-jukebox/plexamp-splash.png /usr/share/plymouth/themes/spinner/watermark.png

# Hide mouse
sudo G_CONFIG_INJECT 'xinit[[:blank:]]' 'xinit $FP_CHROMIUM $CHROMIUM_OPTS -- -nocursor' /var/lib/dietpi/dietpi-software/installed/chromium-autostart.sh

###############################
### END OF INSTALL CONTROLS ###
###############################

################################
### START OF INSTALL PLEXAMP ###
################################

cd ~

# Install NodeJS
sudo apt-get install -y ca-certificates curl gnupg && sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=20
echo deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update && sudo apt-get install -y nodejs

# Install Plexamp
curl https://plexamp.plex.tv/headless/Plexamp-Linux-headless-v4.11.1.tar.bz2 > plexamp.tar.bz2
tar -xvf plexamp.tar.bz2

# Start Plexamp for the first time
node plexamp/js/index.js

# User interaction required, fill in claim code and name player

# Change username
sed -i 's/pi/dietpi/' plexamp/plexamp.service

# Enable the startup script and start Plexamp:
sudo cp plexamp/plexamp.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable plexamp
sudo systemctl start plexamp

##############################
### END OF INSTALL PLEXAMP ###
##############################