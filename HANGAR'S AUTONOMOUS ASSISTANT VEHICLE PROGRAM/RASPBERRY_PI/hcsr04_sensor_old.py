import RPi.GPIO as GPIO
import time


class hcsr04:
    def __init__(self,trig_pin,echo_pin):
        self.trig_pin=trig_pin
        self.echo_pin=echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
    
    def distance(self,print_distance=False, delay=0.01):
        while True:
            time.sleep(delay)
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)
            while GPIO.input(self.echo_pin)==0:
                 pulse_start = time.time()
                 
            while GPIO.input(self.echo_pin)==1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            if distance >2 and distance < 400:
                if print_distance:
                    print(distance)
                return distance
            else:
                if print_distance:
                    print('range exceeded')
                return -1