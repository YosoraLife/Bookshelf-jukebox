https://forums.raspberrypi.com/viewtopic.php?t=197472

cd /usr/share/plymouth/themes
sudo cp -a pix mytheme
cd mytheme
sudo mv pix.plymouth mytheme.plymouth
sudo mv pix.script mytheme.script
sudo rm splash.png
sudo wget http://example.com/images/splash.png
sudo sed -i 's/pix/mytheme/g; s/Raspberry Pi/My/g' mytheme.plymouth
sudo sed -i 's/pix/mytheme/g' /etc/plymouth/plymouthd.conf

### Resources
https://github.com/emanuele-scarsella/vortex-ubuntu-plymouth-theme
https://github.com/wboevink/raspberry
https://askubuntu.com/questions/2007/how-do-i-change-the-plymouth-bootscreen
https://www.youtube.com/watch?v=YRuqn2sliqA
https://techoverflow.net/2021/10/19/how-to-hide-all-boot-text-blinking-cursor-on-raspberry-pi/
https://raspberrypi.stackexchange.com/questions/136783/how-can-i-customize-what-rpi-displays-on-boot

https://florianmuller.com/polish-your-raspberry-pi-clean-boot-splash-screen-video-noconsole-zram