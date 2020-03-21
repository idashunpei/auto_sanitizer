# ref: https://umiushizn.blogspot.com/2017/10/hc-sr04raspberry-pi.html
# ref: https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/

import RPi.GPIO as GPIO
import time

def pulse_in(pin, value=GPIO.HIGH, timeout=1.0):
    start_time = time.time()
    not_value = (not value)

    while GPIO.input(pin) == value:
        if time.time() - start_time > timeout:
            return 0

    while GPIO.input(pin) == not_value:
        if time.time() - start_time > timeout:
            return 0

    start = time.time()

    while GPIO.input(pin) == value:
        if time.time() - start_time > timeout:
            return 0

    end = time.time()

    return end - start


def init_sensors(trig, echo, mode=GPIO.BCM):
    GPIO.cleanup()
    GPIO.setmode(mode)
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)


def get_distance(trig, echo, temp=15):
    GPIO.output(trig, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.000011)
    GPIO.output(trig, GPIO.LOW)

    dur = pulse_in(echo, GPIO.HIGH, 1.0)

    return dur * (331.50 + 0.61 * temp) * 50


if __name__ == "__main__":

    # Sensor init
    GPIO_TRIG = 26
    GPIO_ECHO = 19
    init_sensors(GPIO_TRIG, GPIO_ECHO)

    # Servo motor init
    GPIO_SERVO = 17
    GPIO.setup(GPIO_SERVO, GPIO.OUT)
    p = GPIO.PWM(GPIO_SERVO, 50)    # PWM 50Hz
    p.start(4)                      # init

    while True:
        # get distance
        dist = get_distance(GPIO_TRIG, GPIO_ECHO)
        print("distance: {0} cm".format(dist))
        # Servo motor control
        if dist < 10:
            p.ChangeDutyCycle(15)
        else:
            p.ChangeDutyCycle(4)
        # Sleep
        time.sleep(1)

