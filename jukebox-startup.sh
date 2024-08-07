#!/bin/bash

/usr/bin/python3 /root/bookshelf-jukebox/controls.py &
/usr/bin/python3 /root/bookshelf-jukebox/screen.py &
/usr/bin/python3 /root/bookshelf-jukebox/nfc_reader.py &