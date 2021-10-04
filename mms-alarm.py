#!/usr/bin/python

# this Python application turns a Raspberry Pi into a security camera system
# it requires that you have a Pi camera installed and an Apache web server running on your Pi

# Written by Mike Haldas
# Detailed documentation about this project here: http://www.cctvcamerapros.com/Pi-Alarm-MMS
# Email me at mike@cctvcamerapros.net if you have questions
# You can also reach me @haldas on twitter or +Mike Haldas on Google+
# If you make any improvements to this code or use it in a cool way, please let me know

import re
import pyimgur
import time
import picamera
import RPi.GPIO as GPIO
from twilio.rest import Client
from time import sleep

SERVO = 13

def spin(pwm) -> None:
    pwm.ChangeDutyCycle(7.5)
    sleep(1.5)
    pwm.ChangeDutyCycle(100)
    sleep(1)
    #pwm.ChangeDutyCycle(5)
    #sleep(1)
    #pwm.ChangeDutyCycle(11.5)

def main() -> None:
    # define the GPIO port you will use for the door sensor
    SENSOR = 19
    button = 16
    # number of seconds to delay between alarm and snapshot
    # in case you want to wait a second or two for the person to enter the room after triggering the sensor
    DELAY = 1

    # setup GPIO using Broadcom SOC channel numbering
    GPIO.setmode(GPIO.BCM)

    # set to pull-up (normally closed position for a door sensor)
    GPIO.setup(SERVO, GPIO.OUT)
    GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button, GPIO.OUT)
    GPIO.output(button, False)

    pwm = GPIO.PWM(SERVO, 50)
    pwm.start(0)

    # Twilio Credentials
    ACCOUNT_SID = "AC8eb2d2b3101619334cdc931825affcc8"
    AUTH_TOKEN = "0f4cdc607620f8430ae25a1095f39c63"

    # make sure to use format with +1 for USA #s. E.G +12463338910
    TO_PHONE = "+13032534350"
    FROM_PHONE = "+12059536969"

    # text message to send with photo
    TXT_MSG = "Selfie from Finley!"

    IMAGE_DIR = "/home/pi/Desktop/"

    CLIENT_ID = "c7d1033709f4f58"

    IMG = "snap.jpg"
    IMG_WIDTH = 800
    IMG_HEIGHT = 600

    # initalize the Twilio client
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    # client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    im = pyimgur.Imgur(CLIENT_ID)

    try:
        while True:
            print("Waiting for button press...")
            GPIO.wait_for_edge(SENSOR, GPIO.RISING)
            print("Button Pressed!\n")
#            time.sleep(DELAY)
#            with picamera.PiCamera() as camera:
#                camera.resolution = (IMG_WIDTH, IMG_HEIGHT)
#                camera.capture(IMAGE_DIR + IMG)
#            uploaded_image = im.upload_image(IMAGE_DIR + IMG, title=TXT_MSG)
#            print("Taking selfie now")
#            client.messages.create(
#                to=TO_PHONE,
#                from_=FROM_PHONE,
#                body=TXT_MSG,
#                media_url=uploaded_image.link,
#            )
            spin(pwm)
            print("Triggering feeder. Finished one iteration of loop")
    finally:
        GPIO.cleanup()  # ensures a clean exit


if __name__ == "__main__": 
    main()
