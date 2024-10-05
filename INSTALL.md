# Installation instructions bookshelf jukebox

  

[TOC]

  

## Prerequisites
### Plex
This installation asummes that you have an active Plex server. [Plex](https://www.plex.tv) is software to manage your personal media collection (Movies, TV series and Music). Plex consist of 2 parts, a central server (Plex Media Server) to manage and stream the media. And the client to play the media. This installation uses Plex dedicated music player called Plexamp for the playback of music. To be able to use the headless version of Plexamp you do need an paid PlexPass subscription.

### NFC reader
The NFC reader was a bit tricky to setup, this code is tested, and meant to be used with:

- A S50 Mifare Classic 1K NFC compatible [card](https://aliexpress.com/item/1005006282512971.html), [sticker](https://aliexpress.com/item/1005005823042872.html) or [FOB](https://aliexpress.com/item/1005006029241048.html) :
- a [Elechouse PN532 V3 NFC/RFID card reader](https://aliexpress.com/item/1005005973913526.html)

### Jukebox
Take a look at the [Bill of Materials](/BOM.md) for a complete list of materials. Building plans for the jukebox itself can be found [here](/Building%20plans/Plexamp%20jukebox%20buildplan.pdf), and building plans for the speakers crossovers can be found [here](/Building%20plans/Speaker%20cross-over%20buildplan.pdf).

## Wiring
The IQaudio DigiAMP+ is connected directly to the Raspberry Pi GPIO header. The power is provided to the IQaudio DigiAMP+ (12-24V DC) that in its turn also provides power to the Raspberry Pi itself. The IQaudio DigiAMP+ also provide GPIO passthrough.

The NFC reader, rotary encoder and 2 touch buttons need to be wired according to following GPIO pins:

<img  src="https://gitlab.com/YosoraLife/plexamp-jukebox/-/raw/main/_Resources/plexamp-jukebox-wiring.png"  width="600"/>

For reference pin 1 is on the SD card side and pin 40 is on the USB side.

Note: The rotery button (sw) is connected BOTH to pin 5 and pin 29. When the Raspberry Pi is powered off it can be turned on by connecting pin 5 to ground. But when the Raspberry Pi is powered on pin 5 is exclusively used by the DAC and can therefore pin 29 is used instead.

## Installation of the hardware
Download the [DietPi Bookworm](https://dietpi.com/#downloadinfo) image for Raspberry Pi 2/3/4/Zero 2 (ARMv8). unzip it with a tool like [7Zip](https://www.7-zip.org). I always prefer to use [rufus](https://rufus.ie/) to flash the dietpi.img to a SD card. Wait for the flashing process to be finished.

Dietpi has some great way to automate the setup process. Follow the follow steps in order to make use of that:

### Setup wifi
The following steps are only needed if you want to make use of WiFi, open the SD card folder, and update next two files using a text editor:

In the file dietpi-wifi.txt:

- set `aWIFI_SSID[0]` to the name of your WiFi network (keep the qoutes)
- set `aWIFI_KEY[0]` to the password of your WiFi network (keep the qoutes)

Save and close the file

**Enable wifi:**
In the file named dietpi.txt:

- find `AUTO_SETUP_NET_WIFI_ENABLED` and set to value `1`
- find `AUTO_SETUP_NET_WIFI_COUNTRY_CODE` and set it too the correct countrycode

### Setup locale
(Still) In the file dietpi.txt:

- find `AUTO_SETUP_LOCALE=c.UTF-8`, change the c.UTF-8 for your own localization. In my case this would be `nl_NL.UTF-8` or for English: `en_GB.UTF-8`. Im not sure if this is 100% necessary but the first time running without this caused the keyboard setup to fail.
- find `AUTO_SETUP_KEYBOARD_LAYOUT`, set the keyboard layout. You only need the keyboard to login to the Plexamp userinterface
- find `AUTO_SETUP_TIMEZONE` and set your correct timezone

### Setup dietpi:
(Still) In the file dietpi.txt:

- find `AUTO_SETUP_NET_HOSTNAME` and set it to: `Jukebox`
- find `AUTO_SETUP_CUSTOM_SCRIPT_EXEC` and set it to: `https://gitlab.com/YosoraLife/bookshelf-jukebox/-/raw/main/jukebox-install.sh` (no qoutes needed)
- find `AUTO_SETUP_BROWSER_INDEX` and set it to `-2`
- find `AUTO_SETUP_AUTOSTART_TARGET_INDEX` and set it to `11`
- find `AUTO_SETUP_AUTOSTART_LOGIN_USER` and set it to `root`
- find `AUTO_SETUP_AUTOMATED` and set it to `1`
- find `AUTO_SETUP_INSTALL_SOFTWARE_ID` and add to the line underneath:

```bash
AUTO_SETUP_INSTALL_SOFTWARE_ID=5 # Install ALSA
AUTO_SETUP_INSTALL_SOFTWARE_ID=17 # Install Git
AUTO_SETUP_INSTALL_SOFTWARE_ID=69 # Install RPi.GPIO
AUTO_SETUP_INSTALL_SOFTWARE_ID=72 # Install I2C
AUTO_SETUP_INSTALL_SOFTWARE_ID=113 # Install Chromium
AUTO_SETUP_INSTALL_SOFTWARE_ID=130 # Install Python 3 pip
```

- find `SURVEY_OPTED_IN` and set it to what your comfortable with
- find `SOFTWARE_CHROMIUM_RES_X` and set it to your screens width, in my case `1024`
- find `SOFTWARE_CHROMIUM_RES_Y` and set it to your screens height, in my case `600`
- find `SOFTWARE_CHROMIUM_AUTOSTART_URL` and set it to: `http://127.0.0.1:32500/`

### Recommandations:

- find `AUTO_SETUP_GLOBAL_PASSWORD` and change the root password

Save and close the file

### Setup screen
In the file named config.txt add to the bottom:

```bash
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
hdmi_drive=1
# Disable HDMI audio
dtoverlay=vc4-kms-v3d,noaudio
# Enable DAC
dtoverlay=iqaudio-dacplus,unmute_amp
```

Save and close the file. And now its time to put the sd card in the Raspberry Pi and boot up for the first time. The installation of all the required software starts automaticly. The Raspberry Pi does need an active internet connection. So make sure you either have set up a wired or a wireless connection.

Dietpi automatically run through all installation steps. Near the end you will be prompted to enter your Plex claim code followed by the prompt to name your Plexamp player. Make sure you have a keyboard connected to the Raspberry Pi for this. When finished the Raspberry Pi will reboot into the Plexamp interface. Even though you claimed the Plexamp player already you will still need to do a (onetime) login into the (web)interface with your Plex credentials. For this you also need to have a keyboard connected to your Raspberry Pi. After this you don't need an keyboard anymore since you can use SSH to access the jukebox.

## SSH into the jukebox
You can use SSH to access the jukebox from another computer. Use a tool like [Advanced IP scanner](https://www.advanced-ip-scanner.com/) to find the IP address of the Jukebox. Next use [PuTTY](https://www.putty.org) to connect to the jukebox. The username is root, and the default password is "dietpi", although you should have changed that in the previous step.

### Enable autoplay on boot
By default Plexamp doesnt start playing until music is choosen. You can enable the script to autoplay the (general) Library radio.

In a webbrowser go to the following page on you **Plex Media Server** and find the *machineIdentifier*

```bash
http://[IP  address]:32400/identity/
```

Edit the Plexamp controls:

```bash
cd  ~/bookshelf-jukebox
sudo nano settings.py
```
Find `PLEX_ID` and set the machineIdentifier.

Here you can also change the short and long press duration, the volume adjustment steps, starting volume at boot and screen timeout at idle (no playing).

### Changing sound levels

Now these speakers can go LOUD! If you ask me, way too loud. I like to use this bookshelf speakers more as background music, and only occasionally turning op the volume. But even when I do turn up the volume I could never push them above 50% volume on Plexamp, while only being more around 5% volume at background music levels.

This would make the volume knob pretty useless of course. Luckily there is a way to manage this. You can adjust the maximum volume levels for the soundcard. By changing the maximum levels for the soundcard you can use the entire volume range on Plexamp.

Open AlsaMixer:
```bash
alsamixer
```

Choose the sound card by hitting `F6` and selecting IQaudIODAC. You will now see different sound levels meters. Use the left and right arrow keys to select the "Digital" sound level meter, and use the up and down arrow keys to change the sound levels. This can be done while playing music. I set mine to 67%.

When the desired level is set hit the ESC key to exit alsamixer.

## Controlling the Jukebox

### Turning off/on
If you build your jukebox just like mine you will have a power toggle at the back, and at the front a volume control knob and a previous/next touch button. DO NOT use the power toggle to shutdown the Raspberry Pi, this can cause a corrupt SD card! 

The correct way of shutting down is to long press the volume knob until the system is in idle state. Only then it's safe to turn off the power toggle. When the power toggle is turned on it will automatically boot the system. Alternatively if the system is still in idle state it can be turned back on by pressing the volume knob.

### Physical controls
You can use the touchscreen, volume knob and previous/next touch buttons. The volume knob also doubles as play/pause (short press) or off/on (long press).

### Control by phone
You can control the jukebox with the Plexamp app for both iPhone and Android. Use the cast function in the app and select the jukebox. Your phone will now work as a remote for the jukebox.

### Control by web browser
Similarly you can control the jukebox by going to `http://[IP  address]:32500/`




## Updating plexamp
Check the [plexamp download](https://www.plex.tv/media-server-downloads/?cat=headless&plat=raspberry-pi#plex-plexamp) page to see the required NodeJS (Node) version

Check if the right version is installed:

```bash
node  -v
```

If needed update NodeJS

```bash
NODE_MAJOR=20
echo  deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main | sudo  tee  /etc/apt/sources.list.d/nodesource.list
sudo  apt-get  update && sudo  apt-get  install  -y  nodejs
```

replace `20` with the required NodeJS version

Check for update (one time):

```bash
sh  /root/bookshelf-jukebox/plexamp-upgrade.sh
```

You can setup an automatic weekly update run: 

```bash
sudo (crontab -l; echo  "@weekly /usr/bin/sh /root/bookshelf-jukebox/plexamp-upgrade.sh &")|awk  '!x[$0]++'|crontab  -
```

 Be aware: this will only run the plexamp update script and it will not update NodeJS. 
At times a newer version of Plexamp also requires a newer version of NodeJS (Node). The required version of NodeJS (node) can be found on the download page: https://www.plex.tv/media-server-downloads/?cat=headless&plat=raspberry-pi#plex-plexamp

To check the installed version of NodeJS connect to the Raspberry Pi through SSH an run the command: node -v

If needed update NodeJS

```bash
NODE_MAJOR=20
echo  deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main | sudo  tee  /etc/apt/sources.list.d/nodesource.list
sudo  apt-get  update && sudo  apt-get  install  -y  nodejs
```

replace `20` with the required NodeJS version

And finally reboot:
```bash
sudo reboot now
```