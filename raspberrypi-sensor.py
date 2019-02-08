import requests

#testing url before heroku
#url = 'http://172.20.10.3:8000/post-chair-status'

url = 'http://chop-chope.herokuapp.com/post-chair-status'

# start the sensor 
status = 'free'

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18
LED = 8

print("Distance Measurement in Progress")
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
GPIO.output(LED, False)
print("Waiting for sensor to settle")
time.sleep(2)

try:
    while (1):
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        # formula to convert pulse duration to centimeters
        distance = pulse_duration * 17150
        # round to 2 decimal point
        distance = round(distance, 2)
        print("Distance:", distance, "cm")
        time.sleep(1)
        try:
            # turn on LED if "sit"
            if distance >= 20:
                GPIO.output(LED, False)
                print("Status = FREE")
                if status == "sit":
                    print("free - to send")
                    query = {u'chair_code': [u'1'], u'status_change': [u'free']}
                    res = requests.post(url, data=query)
                    status = "free"
                    print("-------sent------")
                    # print("sent " + res.text)
                    time.sleep(5)
                else:
                    print("not sent")
                    time.sleep(1)
            else:
                GPIO.output(LED, True)
                print("Status = SIT")
                if status == "free":
                    print("sit - to send")
                    query = {u'chair_code': [u'1'], u'status_change': [u'sit']}
                    res = requests.post(url, data=query)
                    status = "sit"
                    print("-------sent------")
                    # print("sent " + res.text)
                    time.sleep(5)
                else:
                    print("not sent")
                    time.sleep(1)
        except requests.exceptions.RequestException as e:
            print("Connnection Request Error", e)
        except requests.exceptions.HTTPError as e:
            print("Connnection HTTP Error", e)
        except requests.exceptions.Timeout as e:
            print("Connnection timeout", e)
        except requests.exceptions.ConnectionError as e:
            print("Connnection Error", e)



except KeyboardInterrupt:
    print("User terminate program...")
    time.sleep(2)

finally:
    GPIO.cleanup()
