import time
import RPi.GPIO as GPIO

runFunction = True

def handleObstacle (detection):
    print(f"obstacle detected - score: {detection.categories[0].score}")

    if (runFunction):
        runFunction = False

        # GPIO.output(17, GPIO.HIGH)
        print("LED on")
        GPIO.output(17,GPIO.HIGH)
        time.sleep(1)
        print("LED off")
        GPIO.output(17,GPIO.LOW)

        runFunction = True

    # GPIO.output(17,GPIO.HIGH)





    # physical pin 11 - signal - GPIO 17
    # ground 6
    # 5V power 2

def pushFrame ():
    # push the frame to a live webserver
    print("pushing frame but not really because this is just a test function :D")
