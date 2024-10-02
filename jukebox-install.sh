#!/bin/bash

###################################
### START OF INSTALL NFC READER ###
###################################

cd ~

# Install nfc tools
sudo apt-get install -y autoconf libtool libusb-dev automake make libglib2.0-dev

# Download the source code package of libnfc
git clone https://github.com/YosoraLife/libnfc

# Write the configuration file for NFC communication
sudo mkdir -p /etc/nfc/devices.d
cd libnfc
sudo cp contrib/libnfc/pn532_spi_on_rpi.conf.sample /etc/nfc/devices.d/pn532_spi_on_rpi_3.conf

# Compile and install libnfc.
autoreconf -vis
#./configure --with-drivers=pn532_spi --sysconfdir=/etc --prefix=/usr
./configure --with-drivers=pn532_spi --sysconfdir=/etc --prefix=/usr --disable-dependency-tracking
#make
make="gmake"
sudo make install all

#################################
### END OF INSTALL NFC READER ###
#################################

#################################
### START OF INSTALL CONTROLS ###
#################################

cd ~

# Install control tools
sudo apt install -y python3 python3-spidev pip plymouth plymouth-themes jq
sudo pip install pn532pi curlify requests

# Download the jukebox scripts:
git clone https://gitlab.com/YosoraLife/bookshelf-jukebox.git
cd bookshelf-jukebox

# Enable the startup script and make it start at boot:
chmod u+x jukebox-startup.sh

# Add startup script to crontab
(crontab -l; echo "@reboot /usr/bin/sh /home/dietpi/bookshelf-jukebox/jukebox-startup.sh &")|awk '!x[$0]++'|crontab -

# Set quiet startup screen:
sudo sed -i 's/console=tty1/console=tty3 splash quiet plymouth.ignore-serial-consoles logo.nologo vt.global_cursor_default=0/' /boot/cmdline.txt

# Set plymouth startup theme
sudo plymouth-set-default-theme -R spinner

# Set plymouth watermark
sudo cp ~/bookshelf-jukebox/plexamp-splash.png /usr/share/plymouth/themes/spinner/watermark.png

# Hide mouse
# G_CONFIG_INJECT 'xinit[[:blank:]]' 'xinit $FP_CHROMIUM $CHROMIUM_OPTS -- -nocursor' /var/lib/dietpi/dietpi-software/installed/chromium-autostart.sh
G_AGI unclutter && echo '/usr/bin/unclutter -idle 0.1 &' > /etc/chromium.d/dietpi-unclutter

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
sudo sed -i 's/pi/root/' plexamp/plexamp.service

# Change root user location
sudo sed -i 's/\/home\//\//' plexamp/plexamp.service

# Enable the startup script and start Plexamp:
sudo cp plexamp/plexamp.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable plexamp
sudo systemctl start plexamp

##############################
### END OF INSTALL PLEXAMP ###
##############################