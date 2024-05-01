#! /usr/bin/env python3
# Bookshelf jukebox controls

import RPi.GPIO as GPIO
import time
import os
import settings
from functions import *


# Pin numbers on Raspberry Pi
CLK_PIN = settings.CLK_PIN                          # GPIO7 connected to the rotary encoder's CLK pin
DT_PIN = settings.DT_PIN                            # GPIO8 connected to the rotary encoder's DT pin
SW_PIN = settings.SW_PIN                            # GPIO5 connected to the rotary encoder's SW pin
NEXT_PIN = settings.NEXT_PIN                        # GPIO12 connected to the next song touch button pin
PREV_PIN = settings.PREV_PIN                        # GPIO16 connected to the previous song touch button pin

# Times for button presses
SHORT_PRESS_TIME = settings.SHORT_PRESS_TIME        # Time for shortpress in seconds
LONG_PRESS_TIME = settings.LONG_PRESS_TIME          # Time for longpress in seconds
DEBOUNCE_TIME = settings.DEBOUNCE_TIME              # Debounce time, default = 0.1. Increase when experience unwanted "extra" button presses 

# Volume steps
VOLUME_ADJUSTEMENT = settings.VOLUME_ADJUSTEMENT    # How much to add to the volume every step. Range: 0-100

# At boot there is no playlist yet. For autoplay library radio to work you need the machineIdentifier of your plexserver
PLEX_ID = settings.PLEX_ID                          # Find the machineIdentifier at http://[IP address]:32400/identity/
AUTOPLAY = settings.AUTOPLAY                        # 0 = Autoplay on start, 1 = No autoplay on start
START_VOLUME = settings.START_VOLUME                # Set volume level at start Range: 1-100, 0 = disable

# General variables
PPO_PREV_STATE = GPIO.HIGH                          # Play/Pause/Off (PPO) button, previous state
NEXT_PREV_STATE = GPIO.LOW                          # Next song button, previous state
PREV_PREV_STATE = GPIO.LOW                          # Previous song button, previous state
PB_PREV_STATE = None                                # Playback (PB), pervious state
IS_PRESSING = False
IS_LONG_DETECTED = False
PRESS_TIME_START = 0
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



#########################################################
### START OF: Autoplay functionality ####################
#########################################################

# Only at startup, autoplay music
if AUTOPLAY == 0 and PLEX_ID != '':
    AUTOPLAY = 1 # Make sure Autoplay is only run the first time
    if START_VOLUME >= 1 and START_VOLUME <= 100:
        setState(START_VOLUME) # Set volume at start if enabled
    setState('playMedia') # Autoplay at startup if enabled
    time.sleep(1)



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

    
    time.sleep(0.1)