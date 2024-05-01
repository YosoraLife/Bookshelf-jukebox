#! /usr/bin/env python3
# Bookshelf jukebox screencontrol


import time
import settings
from functions import getState,setScreen


# Screen backlight control
SCREEN_TIMEOUT = settings.SCREEN_TIMEOUT    # Turn screen backlight off after * minutes

# Initial state setup
SCREEN_TIMEOUT_START = time.time()          # Start tracking the time
PB_PREV_STATE = 'paused'                    # Assume the player is in a paused state
setScreen('on')                             # Start with the screen on



#########################################################
### START OF: Screen backlight control ##################
#########################################################
while True:

    # Still being paused
    if getState('state') == 'paused' and PB_PREV_STATE == 'paused':

        # Check if timeout time is already exceded
        screen_timeout_duration = time.time() - SCREEN_TIMEOUT_START
        if screen_timeout_duration > (SCREEN_TIMEOUT * 60):
            setScreen('off')


    # Being paused again
    elif getState('state') == 'paused' and PB_PREV_STATE == 'playing':

        # Set state variables
        PB_PREV_STATE = 'paused'
        SCREEN_TIMEOUT_START = time.time() # Start tracking the time


    # Started playing again
    elif getState('state') == 'playing' and PB_PREV_STATE == 'paused':

        # Turn on screen
        setScreen('on')
        # Reset state variables
        PB_PREV_STATE = 'playing'

    # Run loop once a second
    time.sleep(1)
