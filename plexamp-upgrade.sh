cd ~

# Change root user location
sudo sed -i 's/\/home\//\//' plexamp/upgrade.sh

# Run update script
/usr/bin/sh /root/plexamp/upgrade.sh