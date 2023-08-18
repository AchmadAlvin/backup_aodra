import RPi.GPIO as GPIO
import time
import requests
import math
import random

TOKEN = "BBFF-zHRS2UoBMWILnH0NZf56Wc64DZ6D6d"  # Put your TOKEN here
DEVICE_LABEL = "alvinaodra"  # Put your device label here 
VARIABLE_LABEL_1 = "ultrasoniksatu"  # Put your first variable label here

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

PIN_TRIGGER_1 = 17
PIN_ECHO_1 = 27

GPIO.setup(PIN_TRIGGER_1, GPIO.OUT)
GPIO.setup(PIN_ECHO_1, GPIO.IN)

def distance_1():
    GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
    print ("Waiting for sensor to settle")
    time.sleep(2)
    print ("Calculating distance")
    GPIO.output(PIN_TRIGGER_1, GPIO.HIGH)
    time.sleep(0.00001)

    while GPIO.input(PIN_ECHO_1)==0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO_1)==1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    jarak = round(pulse_duration * 34300, 2)
    print(jarak)
    return jarak


def build_payload(variable_1):
    # Creates two random values for sending data
    value_1 = distance_1()
    payload = {variable_1: value_1}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(VARIABLE_LABEL_1)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
