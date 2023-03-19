import time
import RPi.GPIO as GPIO

def handleObstacle (detection):
    print(f"obstacle detected - score: {detection.categories[0].score}")


    
    # # set the raspberry pi GPIO pin to high
    # GPIO.output(18, GPIO.HIGH)
    # # wait 5 seconds
    # time.sleep(5)