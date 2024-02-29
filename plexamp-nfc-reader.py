#! /usr/bin/env python3

"""
    This code is tested, and meant to be used with:
    - a Mifare Classic 1K card
    - a Elechouse PN532 V3 NFC/RFID card reader

    The NFC card can be writen with an (android) phone to contain a
    plexamp playlist URL. This code attempts to read the contents of 
    the NFC card and convert is back to a URL and open the URL.

    Note that you need the baud rate to be 115200 because we need to print
    out the data and read from the card at the same time!

    This code is a modified version of https://github.com/gassajor000/pn532pi/blob/master/examples/mifareclassic_memdump.py
"""

import curlify
import requests
import time

from pn532pi import pn532, Pn532
from pn532pi import Pn532Hsu
from pn532pi import Pn532Spi

SPI = True
HSU = False

# Config when the NFC reader is connected through SPI mode
if SPI:
    PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
    nfc = Pn532(PN532_SPI)
# Config when the NFC reader is connected through HSU Mode
elif HSU:
    PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
    nfc = Pn532(PN532_HSU)

def setup():
  nfc.begin()

  versiondata = nfc.getFirmwareVersion()
  if not versiondata:
    raise RuntimeError("Didn't find PN53x board")  # halt

  # Configure board to read RFID tags
  nfc.SAMConfig()      


if __name__ == '__main__':
    setup()
    while True:
      authenticated = False               # Flag to indicate if the sector is authenticated

      # Keyb on NDEF and Mifare Classic should be the same
      keyuniversal = bytearray([ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ])
      # Set an empty data string for all the data to collect in
      data_string = 'http://'

      # Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
      # if the uid is 4 bytes (Mifare Classic)
      success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

      if (success):
        if (len(uid) == 4):

          # Set blockcounter to skip every 4th block
          blockcount = 0
          # Stop processing when 4 consecutive empty blocks are found
          emptyblockcount = 0

          # Now we try to go through all 16 sectors (each having 4 blocks)
          for currentblock in range(64):
            if (blockcount == 3):
              # Reset counter and skip
              blockcount = 0
            else:
              # Add to blockcount and proceed
              blockcount += 1

              # Check if this is a new block so that we can reauthenticate
              if (nfc.mifareclassic_IsFirstBlock(currentblock)):
                authenticated = False

              # Keep trying to authenticated the block until authentication succeeded
              while (not authenticated and currentblock > 3):
                success = nfc.mifareclassic_AuthenticateBlock (uid, currentblock, 1, keyuniversal)
                if (success):
                  authenticated = True       
                
              if (authenticated):
                # Authenticated ... we should be able to read the block now
                # Skip reading empty blocks 
                emptyblock = bytearray([ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ])
                
                # Dump the data into the 'data' array
                success, data = nfc.mifareclassic_ReadDataBlock(currentblock)

                if (data == emptyblock):
                  # If block is empty add to counter
                  emptyblockcount += 1
                  if (emptyblockcount > 3):
                    # 4 empty blocks in a row, break from the loop
                    break
                else:
                  if (success):
                    # Block contains data, reset emptyblockcount
                    emptyblockcount = 0
                    # Read successful
                    if (currentblock == 4):
                      # On the 4th block (start of our data), remove the first 7 characters
                      data = data[7:]
                    # convert data to string
                    string_object = data.decode('utf8', 'ignore')
                    # Add string to the other strings
                    data_string = data_string + string_object

        # Replace listen.plex.tv for localhost so the link will open on the local device
        data_string = data_string.replace("listen.plex.tv", "localhost:32500")

        # Open the link
        response = requests.get(data_string)
        # print(curlify.to_curl(response.request))

        # Sleep for 3 seconds
        time.sleep(3)