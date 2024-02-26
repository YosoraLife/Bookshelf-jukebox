# Prerequisites
This installation asummes that you have an active Plex server. [Plex](https://www.plex.tv) is software to manage your personal media collection (Movies, TV series and Music). Plex consist of 2 parts, a central server (Plex Media Server) to manage and stream the media. And the client to play the media. This installation uses Plex dedicated music player called Plexamp for the playback of music. To be able to use the headless version of Plexamp you do need an paid PlexPass subscription.

# Installation of the hardware
Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash Raspberry Pi OS (legacy, 64bit) Lite to an SD card. 

<img src="https://gitlab.com/YosoraLife/plexamp-jukebox/-/raw/main/_Resources/RPI_settings.png" style="float: right" width="200"/>

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

ctrl+x > yes

Reboot the Raspberry Pi:
```bash
sudo reboot now
```

# Installation of (headless) Plexamp
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

### Open Plexamp in kioskmode at boot
Note: I like to use Thorium as webbrowser. Thorium is a chromium based webbrowser thats is optimized to be as quick and light as possible.

Install chromium as webbrowser and tools
```bash
sudo apt install chromium-browser unclutter xdotool
```


Make it excecutable:
```bash
chmod u+x ~/kiosk.sh
```
