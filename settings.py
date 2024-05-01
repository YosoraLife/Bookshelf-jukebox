#! /usr/bin/env python3
# Bookshelf jukebox setings

# Times for button presses
SHORT_PRESS_TIME = 1.5                      # Time for shortpress in seconds
LONG_PRESS_TIME = 2.0                       # Time for longpress in seconds
DEBOUNCE_TIME = 0.1                         # Debounce time, default = 0.1. Increase when experience unwanted "extra" button presses 

# Volume steps
VOLUME_ADJUSTEMENT = 3                      # How much to add to the volume every step. Range: 0-100

# At boot there is no playlist yet. For autoplay library radio to work you need the machineIdentifier of your plexserver
PLEX_ID = ''                                # Find the machineIdentifier at http://[IP address]:32400/identity/
AUTOPLAY = 0                                # 0 = Autoplay on start, 1 = No autoplay on start
START_VOLUME = 10                           # Set volume level at start Range: 1-100, 0 = disable

# Screen backlight control
SCREEN_TIMEOUT = 5                          # Turn screen backlight off after * minutes

# Pin numbers on Raspberry Pi
CLK_PIN = 13                                # GPIO7 connected to the rotary encoder's CLK pin
DT_PIN = 6                                  # GPIO8 connected to the rotary encoder's DT pin
SW_PIN = 5                                  # GPIO5 connected to the rotary encoder's SW pin
NEXT_PIN = 12                               # GPIO12 connected to the next song touch button pin
PREV_PIN = 16                               # GPIO16 connected to the previous song touch button pin
SCREEN_PIN = 23                             # GPIO23 connected to the screen backlight pin