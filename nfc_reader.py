#! /usr/bin/env python3

"""
    NFC Reader for Mifare Classic 1K cards using Elechouse PN532 V3 NFC/RFID card reader.
    Reads and converts the contents of the NFC card back to a URL and opens it.
"""

import curlify
import requests
import time

from pn532pi import pn532, Pn532
from pn532pi import Pn532Hsu
from pn532pi import Pn532Spi

SPI = True
HSU = False

# Configure NFC reader connection mode (SPI or HSU)
if SPI:
    PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
    nfc = Pn532(PN532_SPI)
elif HSU:
    PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
    nfc = Pn532(PN532_HSU)


def setup():
    """Setup NFC module and wait until it is found."""
    module_found = False
    retries = 10  # Max retries to avoid indefinite looping
    while not module_found and retries > 0:
        nfc.begin()
        version_data = nfc.getFirmwareVersion()
        if version_data:
            module_found = True
        else:
            retries -= 1
            time.sleep(1)
    if module_found:
        nfc.SAMConfig()
    else:
        print("Error: NFC module not found. Exiting.")
        exit(1)


if __name__ == '__main__':
    setup()

    key_universal = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

    while True:
        authenticated = False
        data_strings = ['http://']  # Collect strings in a list for better efficiency

        success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
        if success and len(uid) == 4:
            block_count = 0
            empty_block_count = 0

            # Try to read all 16 sectors (each sector has 4 blocks)
            for current_block in range(64):
                if block_count == 3:
                    block_count = 0  # Skip every 4th block (authentication block)
                    continue
                block_count += 1

                if nfc.mifareclassic_IsFirstBlock(current_block):
                    authenticated = False

                # Authenticate if needed
                retry_limit = 3
                while not authenticated and current_block > 3 and retry_limit > 0:
                    success = nfc.mifareclassic_AuthenticateBlock(uid, current_block, 1, key_universal)
                    if success:
                        authenticated = True
                    else:
                        retry_limit -= 1

                if authenticated:
                    empty_block = bytearray([0x00] * 16)
                    success, data = nfc.mifareclassic_ReadDataBlock(current_block)

                    if data == empty_block:
                        empty_block_count += 1
                        if empty_block_count > 3:
                            break  # Stop if more than 3 consecutive empty blocks are found
                    elif success:
                        empty_block_count = 0
                        if current_block == 4:
                            data = data[7:]  # Skip first 7 bytes (start of data)
                        data_strings.append(data.decode('utf8', 'ignore'))

        if data_strings:
            url = ''.join(data_strings).replace("listen.plex.tv", "localhost:32500")
            try:
                response = requests.get(url)
                print(curlify.to_curl(response.request))
            except requests.RequestException as e:
                print(f"Error opening URL: {e}")

        time.sleep(3)  # Sleep before the next read attempt
