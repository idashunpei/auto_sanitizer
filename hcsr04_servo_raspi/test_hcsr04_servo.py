# 
# test_hcsr04_servo
# 
# measure distance by using hc-sr04
# and control servo motor
# 

# ref: https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
# ref: https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/


# Libraries
import RPi.GPIO as GPIO
import time

# Pins
GPIO_TRIG = 22
GPIO_ECHO = 27
GPIO_SERVO = 17

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)


# measure distance by using hc-sr04
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIG, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


if __name__ == "__main__":

    # Sensor initialization
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    # Servo motor initialization
    GPIO.setup(GPIO_SERVO, GPIO.OUT)
    p = GPIO.PWM(GPIO_SERVO, 50)    # PWM 50Hz
    p.start(4)                      # init

    try:
        while True:
            # get distance
            dist = distance()
            print("distance: {0} cm".format(dist))
            # Servo motor control
            if dist < 10:
                p.ChangeDutyCycle(15)
            else:
                p.ChangeDutyCycle(4)
            # Sleep
            time.sleep(1)
        
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
