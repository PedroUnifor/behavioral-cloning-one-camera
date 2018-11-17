import argparse
import base64
from datetime import datetime
import os
import shutil

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO

import requests

import rospy
from geometry_msgs.msg import Twist

from keras.models import load_model

import utils

sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None

#MAX_SPEED = 25
#MIN_SPEED = 6
MAX_SPEED = 0.5
MIN_SPEED = 0.1

speed_limit = MAX_SPEED

url = "http://192.168.0.65/jpg/image.jpg"

def telemetry():
        # The current steering angle of the car
        #steering_angle = float(data["steering_angle"].replace(',','.'))
        #steering_angle = float(data["steering_angle"])
        steering_angle = 0.0
        # The current throttle of the car
        #throttle = float(data["throttle"].replace(',','.'))
        #throttle = float(data["throttle"])
        throttle = 0.0
        # The current speed of the car
        #speed = float(data["speed"].replace(',','.'))
        #speed = float(data["speed"])
        speed = 0.0
        # The current image from the center camera of the car
        response = requests.get(url)
        image = Image.open(BytesIO(base64.b64decode(response.content)))
        try:
            image = np.asarray(image)       # from PIL image to numpy array
            image = utils.preprocess(image) # apply the preprocessing
            image = np.array([image])       # the model expects 4D array
            steering_angle = float(model.predict(image, batch_size=1)) # colocar valores do throttle junto do steering_angle
         
            throttle = 1.0 - abs(steering_angle)
            if throttle>MAX_SPEED:
                throttle=MAX_SPEED
            if throttle<MIN_SPEED:
                throttle=MIN_SPEED
            print('{} {}'.format(steering_angle, throttle))
            velocidade.linear.x = throttle
            velocidade.angular.z = steering_angle
            pub.publish(velocidade)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    velocidade = Twist()
    pub = rospy.Publisher('drrobot_cmd_vel', Twist, queue_size=10)
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument(
        'model',
        type=str,
        help='Path to model h5 file. Model should be on the same path.'
    )
    parser.add_argument(
        'image_folder',
        type=str,
        nargs='?',
        default='',
        help='Path to image folder. This is where the images from the run will be saved.'
    )
    args = parser.parse_args()

    model = load_model(args.model)
    while not rospy.is_shutdown():
       telemetry()

