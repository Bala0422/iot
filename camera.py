import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import mysql.connector
import base64
from PIL import Image
import io

s1 = 8
s2 = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setup(s1, GPIO.IN)
GPIO.setup(s2, GPIO.IN)

print("IR Sensor Ready.....")
print(" ")

mydb = mysql.connector.connect(
    host="34.132.50.61",
    user="root",
    password='bala',
    database="image"
)

print("Connected to database .....")
print(" ")

cursor = mydb.cursor()
query = 'INSERT INTO img_table VALUES(%s, %s)'

try:
    while True:
        if not GPIO.input(s1):
            start_time = time.time()
            print("Object Detected in s1")
            while GPIO.input(s1):
                time.sleep(0.2)

        if not GPIO.input(s2):
            end_time = time.time()
            print("Object Detected in s2")
            time_diff = end_time - start_time
            distance = 5
            speed = distance / time_diff
            print(speed)

            camera = PiCamera()
            camera.start_preview(alpha=192)
            time.sleep(1)
            camera.capture('/home/pi/Desktop/pic.png')
            camera.stop_preview()

            file = open('/home/pi/Desktop/pic.png', 'rb').read()
            file = base64.b64encode(file)

            args = (file, speed)
            cursor.execute(query, args)
            print("Image send to cloud ... ")
            while GPIO.input(s2):
                time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
