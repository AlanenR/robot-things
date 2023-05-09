import time
import RPi.GPIO as GPIO
from flask import Flask

def shutDown():
    GPIO.cleanup()

EYE_L_R = 22
EYE_L_G = 27
EYE_L_B = 17
EYE_R_R = 23
EYE_R_G = 24
EYE_R_B = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(EYE_L_R, GPIO.OUT)
GPIO.setup(EYE_L_G, GPIO.OUT)
GPIO.setup(EYE_L_B, GPIO.OUT)
GPIO.setup(EYE_R_R, GPIO.OUT)
GPIO.setup(EYE_R_G, GPIO.OUT)
GPIO.setup(EYE_R_B, GPIO.OUT)

app = Flask(__name__)


@app.route("/")
def hello_world():

    # LED päälle
    GPIO.output(EYE_L_R, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(EYE_L_R, GPIO.LOW)

    GPIO.output(EYE_L_G, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(EYE_L_G, GPIO.LOW)

    GPIO.output(EYE_L_B, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(EYE_L_B, GPIO.LOW)

    GPIO.output(EYE_R_R, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(EYE_R_R, GPIO.LOW)

    GPIO.output(EYE_R_G, GPIO.HIGH) 
    time.sleep(1)
    GPIO.output(EYE_R_G, GPIO.LOW)

    GPIO.output(EYE_R_B, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(EYE_R_B, GPIO.LOW)
    return "<p>Hello, World!</p>"