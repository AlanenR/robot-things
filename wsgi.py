import time
# import RPi.GPIO as GPIO
from flask import Flask, request, jsonify, make_response
import os
import openai
from dotenv import load_dotenv
import json
import requests
import simpleaudio as sa
load_dotenv()

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def shutDown():
    GPIO.cleanup()

def chat_completion(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }

    data = {
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": text}],
     "temperature": 0.7
   }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    result = response.json()

    return result['choices'][0]['message']['content']

def get_sound(text):
    headers = {
        "Content-Type": "application/json",
    }
    data = {"robo": text}
    response = requests.post("http://192.168.110.128:5000/speak", headers=headers, json=data)
    with open("movie.wav", "wb") as f:
        f.write(response.content)
    filename = "movie.wav"
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

# EYES
EYE_L_R = 22
EYE_L_G = 27
EYE_L_B = 17
EYE_R_R = 23
EYE_R_G = 24
EYE_R_B = 25

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(EYE_L_R, GPIO.OUT)
# GPIO.setup(EYE_L_G, GPIO.OUT)
# GPIO.setup(EYE_L_B, GPIO.OUT)
# GPIO.setup(EYE_R_R, GPIO.OUT)
# GPIO.setup(EYE_R_G, GPIO.OUT)
# GPIO.setup(EYE_R_B, GPIO.OUT)

# left_red_pwm = GPIO.PWM(EYE_L_R, 1000)
# left_green_pwm = GPIO.PWM(EYE_L_G, 1000)
# left_blue_pwm = GPIO.PWM(EYE_L_B, 1000)
# right_red_pwm = GPIO.PWM(EYE_R_R, 1000)
# right_green_pwm = GPIO.PWM(EYE_R_G, 1000)
# right_blue_pwm = GPIO.PWM(EYE_R_B, 1000)

# left_red_pwm.start(0)
# left_green_pwm.start(0)
# left_blue_pwm.start(0)
# right_red_pwm.start(0)
# right_green_pwm.start(0)
# right_blue_pwm.start(0)

# MOTOR

MOTOR = 26

# GPIO.setup(MOTOR, GPIO.OUT)

app = Flask(__name__)

@app.route("/talk", methods=['GET', 'POST', 'OPTIONS'])
def talk():
    html = """
    <html>
    <head>
        <style>
            p {
                color: #f5b81d;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <p>Make me speak</p>
    </body>
    </html>
    """
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    if request.method == 'POST':
        content = request.get_json()
        text = content["text"]
        answer = chat_completion(text)
        get_sound(answer)
        return _corsify_actual_response(jsonify({}))
    else:
        return html

@app.route("/motor", methods=['GET', 'POST'])
def motor():
    html = """
    <html>
    <head>
        <style>
            p {
                color: #f5b81d;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <p>Put motor on or off.</p>
    </body>
    </html>
    """
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    if request.method == 'POST':
        content = request.get_json()
        if(content["motor"] == 'on'):
            GPIO.output(MOTOR, GPIO.HIGH)
        elif(content["motor"] == 'off'):
            GPIO.output(MOTOR, GPIO.LOW)
        return _corsify_actual_response(jsonify({}))
    else:
        return html


@app.route("/eyes", methods=['GET', 'POST', 'OPTIONS'])
def choosing_eyes_colors():
    html = """
    <html>
    <head>
        <style>
            p {
                color: #f5b81d;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <p>Knock knock.</p>
        <p>Who's there? </p>
        <p>Art</p>
        <p>Art who?</p>
        <p>R2D2</p>
    </body>
    </html>
    """
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    if request.method == 'POST':
        content = request.get_json()
        left_color = content["left"]
        right_color = content["right"]
        # Parse hex color strings to integers
        left_red = int(left_color[0:2], 16)
        left_green = int(left_color[2:4], 16)
        left_blue = int(left_color[4:6], 16)
        right_red = int(right_color[0:2], 16)
        right_green = int(right_color[2:4], 16)
        right_blue = int(right_color[4:6], 16)

        # Normalize RGB values to 0-100 range
        left_red_normalized = (left_red / 255.0) * 100
        left_green_normalized = (left_green / 255.0) * 100
        left_blue_normalized = (left_blue / 255.0) * 100
        right_red_normalized = (right_red / 255.0) * 100
        right_green_normalized = (right_green / 255.0) * 100
        right_blue_normalized = (right_blue / 255.0) * 100

        # Set PWM duty cycle for left eye
        left_red_pwm.ChangeDutyCycle(left_red_normalized)
        left_green_pwm.ChangeDutyCycle(left_green_normalized)
        left_blue_pwm.ChangeDutyCycle(left_blue_normalized)

        # Set PWM duty cycle for right eye
        right_red_pwm.ChangeDutyCycle(right_red_normalized)
        right_green_pwm.ChangeDutyCycle(right_green_normalized)
        right_blue_pwm.ChangeDutyCycle(right_blue_normalized)

        return _corsify_actual_response(jsonify({}))

    else:
        return html


@app.route("/")
def hello_world():

    html = """
    <html>
    <head>
        <style>
            p {
                color: #f5b81d;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <p>Knock knock.</p>
        <p>Who's there? </p>
        <p>Art</p>
        <p>Art who?</p>
        <p>R2D2</p>
    </body>
    </html>
    """

    # EYES
    left_color = request.args.get("left", default="000000")
    right_color = request.args.get("right", default="000000")

    # MOTOR
    motor = request.args.get("motor", default="0")

    # Parse hex color strings to integers
    left_red = int(left_color[0:2], 16)
    left_green = int(left_color[2:4], 16)
    left_blue = int(left_color[4:6], 16)
    right_red = int(right_color[0:2], 16)
    right_green = int(right_color[2:4], 16)
    right_blue = int(right_color[4:6], 16)

    # Normalize RGB values to 0-100 range
    left_red_normalized = (left_red / 255.0) * 100
    left_green_normalized = (left_green / 255.0) * 100
    left_blue_normalized = (left_blue / 255.0) * 100
    right_red_normalized = (right_red / 255.0) * 100
    right_green_normalized = (right_green / 255.0) * 100
    right_blue_normalized = (right_blue / 255.0) * 100

    # Set motor
    GPIO.output(MOTOR, int(motor))

    # Set PWM duty cycle for left eye
    left_red_pwm.ChangeDutyCycle(left_red_normalized)
    left_green_pwm.ChangeDutyCycle(left_green_normalized)
    left_blue_pwm.ChangeDutyCycle(left_blue_normalized)

    # Set PWM duty cycle for right eye
    right_red_pwm.ChangeDutyCycle(right_red_normalized)
    right_green_pwm.ChangeDutyCycle(right_green_normalized)
    right_blue_pwm.ChangeDutyCycle(right_blue_normalized)

    # Sleep for 1 second
    time.sleep(1)

    # Turn off all LEDs
    left_red_pwm.ChangeDutyCycle(0)
    left_green_pwm.ChangeDutyCycle(0)
    left_blue_pwm.ChangeDutyCycle(0)
    right_red_pwm.ChangeDutyCycle(0)
    right_green_pwm.ChangeDutyCycle(0)
    right_blue_pwm.ChangeDutyCycle(0)

    # Turn off motor
    GPIO.output(MOTOR, GPIO.LOW)
    return html