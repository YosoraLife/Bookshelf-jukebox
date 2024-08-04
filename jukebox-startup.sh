#!/bin/bash

/usr/bin/python3 /home/$USER/bookshelf-jukebox/controls.py &
/usr/bin/python3 /home/$USER/bookshelf-jukebox/screen.py &
/usr/bin/python3 /home/$USER/bookshelf-jukebox/nfc_reader.py &