#! /usr/bin/env python3
# Bookshelf jukebox screen control

import time
import settings
from functions import getState, setScreen

##########################################################################################################
####### DONT CHANGE THE SETTINGS INBETWEEN THESE LINES. INSTEAD CHANGE THE SETTINGS IN SETTINGS.PY #######

# Screen backlight control
SCREEN_TIMEOUT = settings.SCREEN_TIMEOUT                            # Turn screen backlight off after * minutes

####### DONT CHANGE THE SETTINGS INBETWEEN THESE LINES. INSTEAD CHANGE THE SETTINGS IN SETTINGS.PY #######
##########################################################################################################

###################################################
### Initial state setup ###########################
###################################################
SCREEN_TIMEOUT_START = time.time()                                  # Start tracking of the time
PB_PREV_STATE = 'paused'                                            # Assume the initial state of the player is paused
setScreen('on')                                                     # Start with the screen on

###################################################
### Paused state handeling ########################
###################################################
def handle_paused_state():
    global SCREEN_TIMEOUT_START
    screen_timeout_duration = time.time() - SCREEN_TIMEOUT_START    # Calculate the time duration since last pause
    if screen_timeout_duration > (SCREEN_TIMEOUT * 60):             # Check if timeout time is already exceeded
        setScreen('off')                                            # Turn off screen

###################################################
### Playing state handeling #######################
###################################################
def handle_playing_state():
    setScreen('on')                                                 # Turn on screen, playback has started

while True:
    current_state = getState('state')                               # Get the current state

    if current_state == 'playing':                                  # State is playing
        if PB_PREV_STATE != 'playing':                              # Previous state was not playing
            PB_PREV_STATE = 'playing'                               # Set new previous state variable
            handle_playing_state()                                  # Turn on screen, playback has started

    else:                                                           # If state is paused or stopped
        if PB_PREV_STATE == 'playing':                              # Previous state was playing
            PB_PREV_STATE = 'paused'                                # Set new previous state variable
            SCREEN_TIMEOUT_START = time.time()                      # Reset tracking of the time
        handle_paused_state()                                       # Check if the screen should turn off after timeout

    time.sleep(5)                                                   # Run loop once every 5 seconds to reduce CPU usage
