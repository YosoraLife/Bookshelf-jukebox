# Installation of the hardware
Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash Raspberry Pi OS (legacy, 64bit) Lite to an SD card. 

<img src="https://gitlab.com/YosoraLife/plexamp-jukebox/-/raw/main/_Resources/RPI_settings.png" style="float: right" width="200"/>

During installation you will get prompted to apply your own settings on the OS.
- setup hostname
- username/password
- wireless LAN (if needed)
- Locale settings

Flash Raspberry Pi OS lite to the SD card and boot the Raspberry Pi.

- Install GUI:
```bash
sudo apt update && sudo apt upgrade
sudo apt install xserver-xorg raspberrypi-ui-mods
```

- Enable GUI at boot with autologin:
```bash
sudo raspi-config
```
System options > S5 Boot / Auto login > B4 Desktop Autologin

- Reboot the Raspberry Pi.

### Enable IQAudio DAC+ and Waveshare Qled display:
```bash
sudo nano /boot/config.txt
```
##### For IQAudio DAC +:
  <sub>nb: Consult the documentation if you use a different audiocard, or skip if you dont use a seperate audiocard.</sub>
  - Disable the default Raspberry Pi audiocard:
Find:
```bash
# Enable audio (loads snd_bcm2835)
dtparam=audio=on
```
And change it to:
```bash
# Enable audio (loads snd_bcm2835)
# dtparam=audio=on
dtoverlay=iqaudio-dacplus,unmute_amp
```

- Disable HDMI audio output:
 Find:
```bash
 # Enable DRM VC4 V3D driver
dtoverlay=vc4-kms-v3d
```
And change it into:
```bash
 # Enable DRM VC4 V3D driver
dtoverlay=vc4-kms-v3d,noaudio
```

- Enable SPI mode:
Find:
```bash
# dtparam=spi=on
```
And uncomment:
```bash
dtparam=spi=on
```

##### For Waveshare Qled display:
<sub>nb: Consult the documentation if you use a different screen</sub>

 - Add to the bottom:
```bash
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
hdmi_drive=1
```

Save changes:
```bash
ctrl+x > yes
```
Reboot the Raspberry Pi:
```bash
sudo reboot now
```