#! /usr/bin/env python3
# Bookshelf jukebox controls

import RPi.GPIO as GPIO
import time
import os
import settings
from functions import *

##########################################################################################################
####### DONT CHANGE THE SETTINGS INBETWEEN THESE LINES. INSTEAD CHANGE THE SETTINGS IN SETTINGS.PY #######

# Pin numbers on Raspberry Pi
CLK_PIN = settings.CLK_PIN                          # GPIO7 connected to the rotary encoder's CLK pin
DT_PIN = settings.DT_PIN                            # GPIO8 connected to the rotary encoder's DT pin
SW_PIN = settings.SW_PIN                            # GPIO5 connected to the rotary encoder's SW pin
NEXT_PIN = settings.NEXT_PIN                        # GPIO12 connected to the next song touch button pin
PREV_PIN = settings.PREV_PIN                        # GPIO16 connected to the previous song touch button pin

# Times for button presses
SHORT_PRESS_TIME = settings.SHORT_PRESS_TIME        # Time for shortpress in seconds
LONG_PRESS_TIME = settings.LONG_PRESS_TIME          # Time for longpress in seconds
DEBOUNCE_TIME = settings.DEBOUNCE_TIME              # Debounce time in milli seconds, default = 100. Increase when experience unwanted "extra" button presses 

# Volume steps
VOLUME_ADJUSTEMENT = settings.VOLUME_ADJUSTEMENT    # How much to add to the volume every step. Range: 0-100

# At boot there is no playlist yet. For autoplay library radio to work you need the machineIdentifier of your plexserver
PLEX_ID = settings.PLEX_ID                          # Find the machineIdentifier at http://[IP address]:32400/identity/
AUTOPLAY = settings.AUTOPLAY                        # 0 = Autoplay on start, 1 = No autoplay on start
START_VOLUME = settings.START_VOLUME                # Set volume level at start Range: 1-100, 0 = disable

####### DONT CHANGE THE SETTINGS INBETWEEN THESE LINES. INSTEAD CHANGE THE SETTINGS IN SETTINGS.PY #######
##########################################################################################################

# General variables
PRESS_TIME_START = 0
IS_PRESSED = False

# Configure GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN)
GPIO.setup(DT_PIN, GPIO.IN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEXT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PREV_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prev_clk_state = GPIO.input(CLK_PIN)                        # Read the initial state of the rotary encoder's CLK pin

###################################################
### Autoplay functionality ########################
###################################################
def autoplay():
    if AUTOPLAY == 0 and PLEX_ID != '':                     # Check if autoplay is enabled and a PLEX ID is present
        if START_VOLUME >= 1 and START_VOLUME <= 100:       # Check if there is a start volume set
            setState(START_VOLUME)                          # Set start volume
        setState('playMedia')                               # Start playback

###################################################
### Rotery encoder functionality ##################
###################################################
def rotary_encoder_callback(channel):
    #global prev_clk_state
    #if GPIO.input(CLK_PIN) != prev_clk_state:               # Detect state change of CLK pin
    # Check state of the DT pin
    if GPIO.input(DT_PIN) == GPIO.HIGH:                 # State DT pin is high? Then its turning counter-clockwise
        setState('volDown')                             # Turn volume down
    elif GPIO.input(DT_PIN) == GPIO.LOW:                # Else the state of DT pin is low. Then its turning clockwise
        setState('volUp')                               # Turn volume up
    prev_clk_state = GPIO.input(CLK_PIN)                # Set state for the next turn

###################################################
### Rotery button functionality ###################
###################################################
def rotary_button_callback(channel):
    global PRESS_TIME_START, IS_PRESSED
    if GPIO.input(SW_PIN) == GPIO.LOW:                      # Detect button being pressed
        PRESS_TIME_START = time.time()                      # Start tracking the time
        IS_PRESSED = True                                   # Set variable for long press detection
    elif GPIO.input(SW_PIN) == GPIO.HIGH:                   # Detect button being released
        IS_PRESSED = False                                  # Reset variable for long press detection
    
        # Handle short button press, Long button press (Poweroff) is handled by check_long_press()
        press_duration = time.time() - PRESS_TIME_START      # Calculate press duration
        if press_duration < SHORT_PRESS_TIME:                # Check for short press
            if getState('state') == 'stopped':               # Check if current state is stopped
                setState('playMedia')                        # Start playback
            else:
                setState('playPause')                        # Pause playback

###################################################
### Rotery button long press check ################
###################################################
def check_long_press():
    global PRESS_TIME_START
    if GPIO.input(SW_PIN) == GPIO.LOW:                      # Check if button is still being pressed
        press_duration = time.time() - PRESS_TIME_START     # Calculate the time duration of it being pressed
        if press_duration > LONG_PRESS_TIME:                # If button is being pressed long time shutdown system
            setState('stop')                                # Stop playing
            os.system('sudo shutdown -h now')               # Shutdown system
    else:
        PRESS_TIME_START = 0                                # Reset time tracking
        IS_PRESSED = False                                  # Button is not pressed anymore, reset state

###############################################
### Touch next button functionality ###########
###############################################
def next_button_callback(channel):
    setState('next')                                        # Play next song

###################################################
### Touch previous button functionality ###########
###################################################
def prev_button_callback(channel):
    setState('prev')                                        # Play previous song

###################################################
### Set up interrupts for GPIO inputs #############
###################################################
GPIO.add_event_detect(CLK_PIN, GPIO.BOTH, callback=rotary_encoder_callback, bouncetime=int(10))
GPIO.add_event_detect(SW_PIN, GPIO.BOTH, callback=rotary_button_callback, bouncetime=int(DEBOUNCE_TIME))
GPIO.add_event_detect(NEXT_PIN, GPIO.FALLING, callback=next_button_callback, bouncetime=int(DEBOUNCE_TIME))
GPIO.add_event_detect(PREV_PIN, GPIO.FALLING, callback=prev_button_callback, bouncetime=int(DEBOUNCE_TIME))

###################################################
### Autoplay at startup if enabled ################
###################################################
autoplay()

try:
    while True:
        if IS_PRESSED == True:                              # Check for button press
            check_long_press()                              # Check if (poweroff) button is being long pressed
        time.sleep(0.1)                                     # Reduce CPU usage by adding a small delay

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()