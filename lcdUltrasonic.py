# Ultrasonic sensing for CharLCD

import time
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

# Use pin array of BCM type
GPIO.setmode(GPIO.BCM)
# Configure LCD
lcd = CharLCD(pin_rs = 11, pin_rw = None, pin_e = 10, pins_date = [13, 6, 5, 11], numbering_mode = GPIO.BOARD, cols = 16, rows = 2, dotsize = 8)
# Set trigger pin to 17, echo pin to 27 of HC-SR04
GP_TRI = 17
GP_ECH = 27
GPIO.setup(GP_TRI, GPIO.OUT)
GPIO.setup(GP_ECH, GPIO.IN) 

try:
    while True:
        stop = 0
        start = 0

        # Set trigger to OFF
        GPIO.output(GP_TRI, False)

        # Send 10us pulse. By the way, HC-SR04 agree 10us?
        # TODO: Checkout HC-SR04 datasheet
        time.sleep(0.1)
        GPIO.output(GP_TRI, True)
        time.sleep(0.00001)
        GPIO.output(GP_TRI, False)

        # Set start time when echo pin going to ON
        while GPIO.input(GP_ECH) == 0:
            start = time.time()

        # Set reflected wave rx time, when echo pin going to OFF
        while GPIO.input(GP_ECH) == 1:
            stop = time.time()

        # Calculate pulse length
        el = stop - start

        # Ultrasonic is reflected wave, so real distance is 2-times.
        # For convenience, caculate speed of sound to 340m/s. 
        if (start and stop):
            dis = (el * 34000.0) / 2
            print("Distance: %3.2fcm" % dis)
            lcd.clear()
            lcd.write_string("Distance: " + str(dis))


except KeyboardInterrupt:
    print("Ultrasonic Distance Tester End")
    lcd.close()
    Lcd.cleanup()
    GPIO.cleanup()

GPIO.cleanup()
lcd.close()
Lcd.cleanup()
