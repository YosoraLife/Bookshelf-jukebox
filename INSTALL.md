# Installation instructions Plexamp jukebox

[TOC]

## Prerequisites
### Plex
This installation asummes that you have an active Plex server. [Plex](https://www.plex.tv) is software to manage your personal media collection (Movies, TV series and Music). Plex consist of 2 parts, a central server (Plex Media Server) to manage and stream the media. And the client to play the media. This installation uses Plex dedicated music player called Plexamp for the playback of music. To be able to use the headless version of Plexamp you do need an paid PlexPass subscription.

### NFC reader
The NFC reader was a bit tricky to setup, this code is tested, and meant to be used with:

- A S50 Mifare Classic 1K NFC compatible [card](https://aliexpress.com/item/1005006282512971.html), [sticker](https://aliexpress.com/item/1005005823042872.html) or [FOB](https://aliexpress.com/item/1005006029241048.html) :
- a [Elechouse PN532 V3 NFC/RFID card reader](https://aliexpress.com/item/1005005973913526.html)

## Wiring
The IQaudio DigiAMP+ is connected directly to the Raspberry Pi GPIO header. The power is provided to the IQaudio DigiAMP+ (12-24V DC) that in its turn also provides power to your Raspberry Pi itself. The IQaudio DigiAMP+ also provide GPIO passthrough.

The NFC reader, rotary encoder and 2 touch buttons need to be wired according to following GPIO pins:

<img src="https://gitlab.com/YosoraLife/plexamp-jukebox/-/raw/main/_Resources/plexamp-jukebox-wiring.png" width="600"/>
For reference pin 1 is on the SD card side and pin 40 is on the USB side.


## Installation of the hardware
Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash Raspberry Pi OS (legacy, 64bit) Lite to an SD card. 

<img src="https://gitlab.com/YosoraLife/plexamp-jukebox/-/raw/main/_Resources/RPI_settings.png" width="300"/>

During installation you will get prompted to apply your own settings on the OS.
- setup hostname
- username/password
- wireless LAN (if needed)
- Locale settings

Flash Raspberry Pi OS lite to the SD card, put the SD card in the Raspberry Pi and turn on the Raspberry Pi.

[Find the IP number](https://www.makeuseof.com/ways-to-find-raspberry-pi-ip-address/)  of the Raspberry Pi and SSH into the Raspberry Pi with (for example) [PuTTY](https://www.putty.org).

- Install GUI:
```bash
sudo apt update && sudo apt upgrade
sudo apt install xserver-xorg raspberrypi-ui-mods
```

- Enable GUI at boot with autologin:
```bash
sudo raspi-config
```
Go to:
System options > S5 Boot / Auto login > B4 Desktop Autologin

- Reboot the Raspberry Pi.

### Enable IQaudio DigiAMP+ and Waveshare Qled display:
```bash
sudo nano /boot/config.txt
```
#### IQaudio DigiAMP+:
<sub>nb: IQaudio DigiAMP+ and Raspberry Pi DigiAMP+ are the same  audiocard.</sub>
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

#### Waveshare Qled display:
<sub>nb: Consult the documentation if you use a different screen</sub>

 - Add to the bottom:
```bash
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
hdmi_drive=1
```

Save changes:

ctrl+x > yes

Reboot the Raspberry Pi:
```bash
sudo reboot now
```

### Install NFC reader

Install dependent packages:
```bash
sudo apt-get  install git autoconf libtool libusb-dev
```

Download the source code package of libnfc
```bash
cd ~
git clone https://github.com/nfc-tools/libnfc
```

Write the configuration file for NFC communication
```bash
sudo mkdir -p /etc/nfc/devices.d
cd libnfc
sudo cp contrib/libnfc/pn532_spi_on_rpi_3.conf.sample /etc/nfc/devices.d/pn532_spi_on_rpi_3.conf
```

Compile and install libnfc.
```bash
autoreconf -vis
./configure --with-drivers=pn532_spi --sysconfdir=/etc --prefix=/usr
make
sudo make install all
```

#### Testing
Check if NFC module is found
```bash
nfc-list
```

Run nfc-poll to scan the RFID tag and you can read information on the card
```bash
nfc-poll
```
<img src="https://gitlab.com/YosoraLife/plexamp-jukebox/-/raw/main/_Resources/nfc-test.png" width="500"/>

## Installation of (headless) Plexamp
### Install NodeJS:
```bash
sudo apt-get install -y ca-certificates curl gnupg && sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=16
echo deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update && sudo apt-get install -y nodejs
```

Check if the right version is installed:
```bash
node -v
```
You should get a response like **v16.x.x** 

### Install (headless) Plexamp:
```bash
curl https://plexamp.plex.tv/headless/Plexamp-Linux-headless-v4.9.5.tar.bz2 > plexamp.tar.bz2
tar -xvf plexamp.tar.bz2
```

Start Plexamp for the first time:
```bash
node plexamp/js/index.js
```
Follow the instructions, go to [plex.tv/claim](plex.tv/claim), login with you plex account and copy the claim code into the terminal window. Give a name to your headless plexamp instance (for example Plexamp jukebox).

### Make (headless) Plexamp startup at boot:
Find your username:
```bash
whoami
```
Edit the startup script:
```bash
nano plexamp/plexamp.service
```
Find the lines refering to the default pi user and change it to your own username:
From:

```bash
User=pi
WorkingDirectory=/home/pi/plexamp
ExecStart=/usr/bin/node /home/pi/plexamp/js/index.js
```

To:

```bash
User=YosoraLife
WorkingDirectory=/home/YosoraLife/plexamp
ExecStart=/usr/bin/node /home/YosoraLife/plexamp/js/index.js
```
Leave the other lines as they where, close: ctrl+x > yes

Enable the startup script and start Plexamp:
```bash
cd plexamp
sudo cp plexamp.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable plexamp
sudo systemctl start plexamp
```

## Install Plexamp jukebox controls
Install tools
```bash
sudo apt install chromium-browser unclutter xdotool pip
```

Install python dependent packages:
```bash
pip install pn532pi curlify requests
```

Download the jukebox scripts:
```bash
cd ~
git clone https://gitlab.com/YosoraLife/plexamp-jukebox
cd plexamp-jukebox
```

Enable the startup script and start:
```bash
chmod u+x ~/plexamp-startup.sh
sudo cp jukebox.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable jukebox
sudo systemctl start jukebox
```
