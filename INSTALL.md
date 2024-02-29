# Installation instructions Plexamp jukebox

[TOC]

## Prerequisites
### Plex
This installation asummes that you have an active Plex server. [Plex](https://www.plex.tv) is software to manage your personal media collection (Movies, TV series and Music). Plex consist of 2 parts, a central server (Plex Media Server) to manage and stream the media. And the client to play the media. This installation uses Plex dedicated music player called Plexamp for the playback of music. To be able to use the headless version of Plexamp you do need an paid PlexPass subscription.

### NFC reader
The NFC reader was a bit tricky to setup, this code is tested, and meant to be used with:

- A S50 Mifare Classic 1K NFC compatible [card](https://aliexpress.com/item/1005006282512971.html), [sticker](https://aliexpress.com/item/1005005823042872.html) or [FOB](https://aliexpress.com/item/1005006029241048.html) :
- a [Elechouse PN532 V3 NFC/RFID card reader](https://aliexpress.com/item/1005005973913526.html)

### Jukebox
Take a look at the [Bill of Materials](/BOM.md) for a complete list of materials. Building plans for the jukebox itself can be found [here](/Building%20plans/Plexamp%20jukebox%20buildplan.pdf), and building plans for the speakers crossovers can be found [here](/Building%20plans/Speaker%20cross-over%20buildplan.jpg).

## Wiring
The IQaudio DigiAMP+ is connected directly to the Raspberry Pi GPIO header. The power is provided to the IQaudio DigiAMP+ (12-24V DC) that in its turn also provides power to the Raspberry Pi itself. The IQaudio DigiAMP+ also provide GPIO passthrough.

The NFC reader, rotary encoder and 2 touch buttons need to be wired according to following GPIO pins:

<img src="https://gitlab.com/YosoraLife/plexamp-jukebox/-/raw/main/_Resources/plexamp-jukebox-wiring.png" width="600"/>
For reference pin 1 is on the SD card side and pin 40 is on the USB side.

Note: The rotery button (sw) is connected BOTH to pin 5 and pin 29. When the Raspberry Pi is powered off it can be turned on by connecting pin 5 to ground. But when the Raspberry Pi is powered on pin 5 is exclusively used by the DAC and can therefore pin 29 is used instead.


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

### Install of the NFC reader

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
Download the jukebox scripts:
```bash
cd ~
git clone https://gitlab.com/YosoraLife/plexamp-jukebox
cd plexamp-jukebox
```

Install tools
```bash
sudo apt install xdotool python3 pip
pip install pn532pi curlify requests
```

Setup desktop:
```bash
sudo nano ~/.config/pcmanfm/LXDE-pi/desktop-items-0.conf
```
And change the following lines from:
```bash
wallpaper=/usr/share/rpd-wallpaper/clouds.jpg
show_documents=1
show_trash=1
show_mounts=1
```
to:
```bash
wallpaper=/home/pi/plexamp-jukebox/plexamp-splash.png
show_documents=0
show_trash=0
show_mounts=0
```
note: For the wallpaper change `pi` to your own username.
Save flie by ctrl+x > Yes

Disable menubar, screensaver, screenlock and mousepointer
```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
sudo sed -i -- "s/#xserver-command=X/xserver-command=X -nocursor/" /etc/lightdm/lightdm.conf
```
Make the content of the file look like this
```bash
# @lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
# @xscreensaver -no-splash
@xset s 0 0
@xset s noblank
@xset s noexpose
@xset dpms 0 0 0
```
Save file by ctrl+x > Yes

Change splash screen:
```bash
sudo nano /boot/config.txt
```
add to the bottom:
```bash
disable_splash=1
```
Save file by ctrl+x > Yes

```bash
sudo nano /boot/cmdline.txt
```
replace: 
`console=tty1` with `console=tty3`

Add to the end of the line:
(make sure there is a space between the end of the line and the added values)
```bash
splash quiet plymouth.ignore-serial-consoles logo.nologo vt.global_cursor_default=0
```
Save file by ctrl+x > Yes

```bash
sudo cp ~/plexamp-jukebox/plexamp-splash.png /usr/share/plymouth/themes/pix/splash.png
```

**Enable autoplay on boot**
By default Plexamp doesnt start playing until music is choosen. You can enable the script to autoplay the (general) Library radio.

In a webbrowser go to the following page on you **Plex Media Server** and find the *machineIdentifier*
```bash
http://[IP address]:32400/identity/
```
Edit the Plexamp controls:
```bash
cd ~/plexamp-jukebox
sudo nano plexamp-controls.py
```

Find the line `PLEX_ID = ''` and put your machineIdentifier between the quotes.
On the next 2 lines you can enable/disable autoplay and set te initial starting volume when autoplay. 


**Thorium**
The installation of Plexamp is headless, meaning without an graphical user interface (GUI). Yet through a webbrowser you can still access the GUI and control Plexamp. As webbrowser i decided to use [Thorium](https://thorium.rocks). Thorium is a optimized version of Chromium.

Thorium is not without controversy though. More about this controversy [here](https://www.youtube.com/watch?v=Q-02fW-n4qg). Still I decided to use Thorium, why? First of all I believe the developer of Thorium made a mistake which he since then rectified. Secondly, and for me most importantly is (in my opinioun) the speed of Thorium unmatched compaired to Chromium.

Would you rather want to use chromium instead? You can use the command: `sudo apt install chromium-browser` . 

Install Thorium
```bash
wget -c https://github.com/Alex313031/Thorium-Raspi/releases/download/M121.0.6167.204/thorium-browser_121.0.6167.204_arm64.deb -O thorium-browser.deb
sudo apt install ./thorium-browser.deb
```

Setting up the startup script:

Did you decide to use the Chromium browser instead of Thorium? Then you should edit the startup script with: `sudo nano plexamp-startup.sh`. Change the references to `thorium` into `chromium` (2x) and `thorium-browser` into `chromium-browser` (1x).

Enable the startup script and make it start at boot:
```bash
cd ~/plexamp-jukebox
chmod u+x plexamp-startup.sh
crontab -e 
```

Add to the bottom:
```bash
@reboot sleep 45 &&  /usr/bin/sh /home/pi/plexamp-jukebox/plexamp-startup.sh &
```
note: Change `pi` to your own username. And save file by ctrl+x > Yes.

Reboot system:
```bash
sudo reboot now
```

## First login
After the Raspberry Pi is booted up you should now see the "Welcome to Plexamp" screen. If you use the same screen as i do, the button to continue will be just out of sight. Since we need to do a (one time) login anyway the easiest way is to attach a keyboard to the Raspberry Pi.

Use ctrl and the minus key (-) to zoom out until you see the buttons. Now continue and login to Plexamp.

After login in you can use the ctrl and the plus key (+) to zoom uit till 100% again. You can now detach the keyboard and enjoy your Plexamp jukebox.

## Setup auto-update
Install tools:
```bash
sudo apt install jq
```

Check for update (one time):
```bash
sh plexamp/upgrade.sh
```

Setup a weekly update run with crontab:
```bash
crontab -e
```

Add to the bottom:
```bash
@weekly /usr/bin/sh /home/pi/plexamp/upgrade.sh &
```
note: Change `pi` to your own username. And save file by ctrl+x > Yes.
