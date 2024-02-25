# NFC cardreader for (headless) Plexamp on a Raspberry Pi
A python based script to read the Plexamp library URL of a NFC tag or card.

## Workings
NFC cards can be writen from within the Plexamp mobile app. This will write the library or playlist URL to the NFC card. This script will read the data of the NFC card and converts it back to a URL. That URl is then openend on the system the system the script runs on.

## Prerequisites
This code is tested, and meant to be used with:

- Raspberry Pi 3 with Raspberry Pi OS 64bit
- A S50 Mifare Classic 1K NFC compatible tag:
 - [S50 Mifare Classic 1K card](https://aliexpress.com/item/1005006282512971.html)
 - [S50 Mifare Classic 1K FOB](https://aliexpress.com/item/1005006029241048.html)
 - [S50 Mifare Classic 1K sticker](https://aliexpress.com/item/1005005823042872.html)
- a [Elechouse PN532 V3 NFC/RFID card reader](https://aliexpress.com/item/1005005973913526.html)

------------

##Installation of PN532 hardware on Raspberry Pi
The PN532 has 3 connection modes, SPI, HSU and I2C. For this usecase the I2C connection is exclusively used by the IQaudio DigiAMP+ and therefore not avaible for use with the PN532. Luckily there are 2 other ways, SPI and HSU:

###...in SPI mode (recommended)

Install dependent packages:
```bash
sudo apt-get update
sudo apt-get  install  libpcsclite-dev  -y
```

Download and unzip the source code package of libnfc
```bash
cd ~
wget https://github.com/nfc-tools/libnfc/releases/download/libnfc-1.8.0/libnfc-1.8.0.tar.bz2
tar -xf libnfc-1.7.1.tar.bz2
```

Compile and install libnfc.
```bash
cd libnfc-1.7.1
./configure --prefix=/usr --sysconfdir=/etc
make
sudo make install
```

Open SPI interface
```bash
sudo raspi-config
```
Interface Options -> I4 SPI -> Yes -> Ok -> Finish

Write the configuration file for NFC communication
```bash
sudo mkdir /etc/nfc
cd /etc/nfc
sudo nano libnfc.conf
```

Add:
```bash
# Allow device auto-detection (default: true)
# Note: if this auto-detection is disabled, user has to set manually a device
# configuration using file or environment variable
allow_autoscan = true

# Allow intrusive auto-detection (default: false)
# Warning: intrusive auto-detection can seriously disturb other devices
# This option is not recommended, user should prefer to add manually his device.
allow_intrusive_scan = false

# Set log level (default: error)
# Valid log levels are (in order of verbosity): 0 (none), 1 (error), 2 (info), 3 (debug)
# Note: if you compiled with --enable-debug option, the default log level is "debug"
log_level = 1

# Manually set default device (no default)
# To set a default device, you must set both name and connstring for your device
# Note: if autoscan is enabled, default device will be the first device available in device list.
device.name = "_PN532_SPI"
device.connstring = "pn532_spi:/dev/spidev0.0:280000"
```

**WIRING**
Toggle the switch to the SPI mode

Connect the PN532:
| PN532 | Raspberry Pi |
| ------------ | ------------ |
| VCC | 3.3V |
| SCK | SCKL |
| MISO | MISO |
| MOSI | MOSI |
| SS | CE0 |

**Testing**
Check whether the SPI is opened or not:
```bash
ls   /dev/spidev0.*
```

Check if NFC module is found
```bash
nfc-list
```

Run nfc-poll to scan the RFID tag and you can read information on the card
```bash
nfc-poll
```
When you can do a succesfull nfc-poll you can continue with [installing the pn532pi library]()

source: https://osoyoo.com/2017/07/20/pn532-nfc-rfid-module-for-raspberry-pi/


###...in HSU mode

Install dependent packages:
```bash
sudo apt-get update
sudo apt-get  install git autoconf libtool libusb-dev  -y
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
sudo cp contrib/libnfc/pn532_uart_on_rpi_3.conf.sample /etc/nfc/devices.d/pn532_uart_on_rpi_3.conf
```

Compile and install libnfc.
```bash
autoreconf -vis
./configure --with-drivers=pn532_uart --sysconfdir=/etc --prefix=/usr
make
sudo make install all
```

**Wiring**
Toggle the switch to the HSU mode

Connect the PN532:
| PN532 | Raspberry Pi |
| ------------ | ------------ |
| VCC | 3.3V |
| GND | GND |
| TXD | GPIO14 (TXD0) |
| RXD | GPIO15 (RXD0) |


**Testing**
Check if NFC module is found
```bash
nfc-list
```

Run nfc-poll to scan the RFID tag and you can read information on the card
```bash
nfc-poll
```
pn53x_check_communication error: Try swapping the RX and TX wires

When you can do a succesfull nfc-poll you can continue with [installing the pn532pi library]()

source: https://cdn-learn.adafruit.com/downloads/pdf/adafruit-nfc-rfid-on-raspberry-pi.pdf

## Installing the Plexamp NFC reader script

Install python dependent packages:
```bash
pip install pn532pi curlify requests time
```
