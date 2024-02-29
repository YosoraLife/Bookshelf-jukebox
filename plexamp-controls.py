#! /usr/bin/env python3

# Plexamp Jukebox controls

import RPi.GPIO as GPIO
import time
import os
import requests
import xml.etree.ElementTree as ET

# Pin numbers on Raspberry Pi
CLK_PIN = 13   # GPIO7 connected to the rotary encoder's CLK pin
DT_PIN = 6    # GPIO8 connected to the rotary encoder's DT pin
SW_PIN = 5    # GPIO5 connected to the rotary encoder's SW pin
NEXT_PIN = 12 # GPIO12 connected to the next song touch button pin
PREV_PIN = 16 # GPIO16 connected to the previous song touch button pin

# Times for button presses
SHORT_PRESS_TIME = 1.5    # Time for shortpress in seconds
LONG_PRESS_TIME = 2.0     # Time for longpress in seconds
DEBOUNCE_TIME = 0.1       # Debounce time, default = 0.1. Increase when experience unwanted "extra" button presses 

# Volume steps
VOLUME_ADJUSTEMENT = 2    # How much to add to the volume every step. Range: 0-100

# At boot there is no playlist yet. For autoplay library radio to work you need the machineIdentifier of your plexserver
PLEX_ID = ''                  # Find the machineIdentifier at http://[IP address]:32400/identity/
AUTOPLAY = 0                  # 0 = Autoplay on start, 1 = No autoplay on start
START_VOLUME = 10             # Set volume level at start Range: 1-100, 0 = disable

# General variables
PPO_PREV_STATE = GPIO.HIGH
NEXT_PREV_STATE = GPIO.LOW
PREV_PREV_STATE = GPIO.LOW
PRESS_TIME_START = 0
IS_PRESSING = False
IS_LONG_DETECTED = False

DIRECTION_CW = 0
DIRECTION_CCW = 1

CLK_STATE = 0
PREV_CLK_STATE = 0

# Configure GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN)
GPIO.setup(DT_PIN, GPIO.IN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEXT_PIN, GPIO.IN)
GPIO.setup(PREV_PIN, GPIO.IN)

# Read the initial state of the rotary encoder's CLK pin
PREV_CLK_STATE = GPIO.input(CLK_PIN)

# Function for getting the current state from Plexamp
def getState(TYPE):
    # Poll for the state of Plexamp
    getState = requests.get('http://localhost:32500/player/timeline/poll?wait=0&includeMetadata=0&commandID=1')
    if getState.ok:
        content = getState.content
        root = ET.fromstring(content)

        # Search the poll state data for the timeline
        for type_tag in root.findall('Timeline'):
            item_type = type_tag.get('itemType')
            # Seach the timeline data for the music data
            if item_type == 'music':
                if TYPE == 'volume':
                    # Get the current volume data
                    state = int(type_tag.get('volume'))
                elif TYPE == 'state':
                    # Get the current state data
                    state = type_tag.get('state')
                return state

# Function for controlling Plexamp
def setState(CONTROL):
    if CONTROL == 'playMedia' and PLEX_ID != '':
        # Play the (general) library radio
        action = f'playMedia?uri=server%3A%2F%2F{PLEX_ID}%2Fcom.plexapp.plugins.library%2Flibrary%2Fsections%2F15%2Fstations%2F1'
    elif CONTROL == 'playPause':
        action = 'playPause'
    elif CONTROL == 'stop':
        action = 'stop'
    elif CONTROL == 'next':
        action = 'skipNext'
    elif CONTROL == 'prev':
        action = 'skipPrevious'
    elif CONTROL == 'volUp':
        # Get current volume and increase by specified adjustment
        volume = getState('volume') + VOLUME_ADJUSTEMENT
        if volume > 100:
            # If volume > 100 set it to 100
            volume = 100
        action = f'setParameters?volume={volume}'
    elif CONTROL == 'volDown':
        # Get current volume and decrease by specified adjustment
        volume = getState('volume') - VOLUME_ADJUSTEMENT
        if volume < 0:
            # If volume < 0 set it to 0
            volume = 0
        action = f'setParameters?volume={volume}'
    elif CONTROL >= 1 and CONTROL <= 100:
        # Set volume to specified volume level
        action = f'setParameters?volume={CONTROL}'

    setState = requests.get(f'http://localhost:32500/player/playback/{action}')
    return

try:
    while True:
        #########################################################
        ### START OF: Rotery encoder functionality ##############
        #########################################################

        # Read the current state of the rotary encoder's CLK pin
        CLK_STATE = GPIO.input(CLK_PIN)

        # If the state of CLK is changed, then pulse occurred
        # React to only the rising edge (from LOW to HIGH) to avoid double count
        if CLK_STATE != PREV_CLK_STATE and CLK_STATE == GPIO.HIGH:
            if GPIO.input(DT_PIN) == GPIO.HIGH:
                setState('volDown') # The encoder is rotating in anti-clockwise direction => Volume down
            else:
                setState('volUp') # The encoder is rotating in clockwise direction => Volume up

        # Save last CLK state
        PREV_CLK_STATE = CLK_STATE

        #########################################################
        ### END OF: Rotery encoder functionality ################
        #########################################################
        ### START OF: Rotery button functionality ###############
        #########################################################

        # Read current state for the rotery button
        PPO_STATE = GPIO.input(SW_PIN)
        
        # Check button state
        if PPO_PREV_STATE == GPIO.HIGH and PPO_STATE == GPIO.LOW: # Button is pressed
            time.sleep(DEBOUNCE_TIME) # Perform debounce by waiting for DEBOUNCE_TIME
            PRESS_TIME_START = time.time() # Start tracking the time
            IS_PRESSING = True
            IS_LONG_DETECTED = False
        elif PPO_PREV_STATE == GPIO.LOW and PPO_STATE == GPIO.HIGH:  # Button is released
            PRESS_TIME_END = time.time() # Stop tracking the time
            IS_PRESSING = False

            press_duration = PRESS_TIME_END - PRESS_TIME_START # Calculate the time pressed

            # Button is press short, but longer then the debounce time
            if press_duration < SHORT_PRESS_TIME and press_duration > DEBOUNCE_TIME:
                if getState('state') == 'stopped':
                    setState('playMedia')
                else:
                    setState('playPause')

        # Check if the button still being pressed
        if IS_PRESSING and not IS_LONG_DETECTED:
            press_duration = time.time() - PRESS_TIME_START # Calculate the time pressed

            # Button is pressed for longer then the long press time
            if press_duration > LONG_PRESS_TIME:
                IS_LONG_DETECTED = True
                setState('stop') # Stop playing
                os.system('sudo shutdown -h now') # shutdown system
   
        # Save the last state
        PPO_PREV_STATE = PPO_STATE

        #########################################################
        ### END OF: Rotery button functionality #################
        #########################################################
        ### START OF: Touch next button functionality ###########
        #########################################################

        # Read the current state of the next song touch button
        NEXT_STATE = GPIO.input(NEXT_PIN)

        # Check if button is pressed
        if NEXT_STATE == GPIO.HIGH and NEXT_PREV_STATE == GPIO.LOW:
            # Button is pressed, setState
            setState('next')

        # Save the last state
        NEXT_PREV_STATE = NEXT_STATE

        #########################################################
        ### END OF: Touch next button functionality #############
        #########################################################
        ### START OF: Touch previous button functionality #######
        #########################################################

        # Read the current state of the previous song touch button
        PREV_STATE = GPIO.input(PREV_PIN)

        # Check if button is pressed
        if PREV_STATE == GPIO.HIGH and PREV_PREV_STATE == GPIO.LOW:
            # Button is pressed, setState
            setState('prev')

        # Save the last state
        PREV_PREV_STATE = PREV_STATE

        #########################################################
        ### END OF: Touch previous button functionality #########
        #########################################################
        ### START OF: Autoplay functionality ####################
        #########################################################

        # Autoplay music on startup
        if AUTOPLAY == 0 and PLEX_ID != '':
            AUTOPLAY = 1 # Make sure Autoplay is only run the first time
            if START_VOLUME >= 1 and START_VOLUME <= 100:
                setState(START_VOLUME) # Set volume at start if enabled
            setState('playMedia') # Autoplay at startup if enabled
            time.sleep(1)

        #########################################################
        ### END OF: Autoplay functionality ######################
        #########################################################