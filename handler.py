import time
import RPi.GPIO as GPIO

def handleObstacle (detection):
    print(f"obstacle detected - score: {detection.categories[0].score}")





    GPIO.output(17, GPIO.HIGH)

    # physical pin 11 - signal - GPIO 18
    # ground 6
    # 5V power 2

def pushFrame ():
    # push the frame to a live webserver
    print("pushing frame but not really because this is just a test function :D")
