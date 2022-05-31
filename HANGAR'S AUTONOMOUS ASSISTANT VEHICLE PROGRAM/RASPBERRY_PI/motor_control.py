from hcsr04_sensor import hcsr04
import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# 1. motor driver signal pins (L298N)
IN1_1 = 16 # 1.right wheel, forward 
IN2_1 = 19 # 1.right wheel, back    
IN3_1 = 26 # 1.left wheel, forward  
IN4_1 = 20 # 1.left whell, back
ENA_1 = 13
ENB_1 = 21


# 2. motor driver signal pins (L298N)
IN1_2 = 17 # 2.right wheel, forward
IN2_2 = 18 # 2.right wheel, back
IN3_2 = 27 # 2.left wheel, forward
IN4_2 = 22 # 2.left whell, back
ENA_2 = 14
ENB_2 = 15

trig_pin=23
echo_pin=24


GPIO.setup(IN1_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENA_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB_1, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(IN1_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENA_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB_2, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(trig_pin,GPIO.OUT)
GPIO.setup(echo_pin,GPIO.IN)


state_current = 5   # stop
state_previous = 5
turn = False


#PWM SETUP
PWM11 = GPIO.PWM(ENA_1, 50)
PWM12 = GPIO.PWM(ENB_1, 50)
PWM21 = GPIO.PWM(ENA_2, 50)
PWM22 = GPIO.PWM(ENB_2, 50)

PWM11.start(100)
PWM12.start(100)
PWM21.start(100)
PWM22.start(100)

def gogo_A(duty=0):
    GPIO.output(IN1_1, True)
    GPIO.output(IN2_1, False)
    GPIO.output(IN3_2, True)
    GPIO.output(IN4_2, False)
    PWM11.ChangeDutyCycle(duty)
    PWM22.ChangeDutyCycle(duty)

def gogo_B(duty=0):
    GPIO.output(IN1_2, True)
    GPIO.output(IN2_2, False)
    GPIO.output(IN3_1, True)
    GPIO.output(IN4_1, False)
    PWM12.ChangeDutyCycle(duty)
    PWM21.ChangeDutyCycle(duty)

def back_A(duty=0):
    GPIO.output(IN1_1, False)
    GPIO.output(IN2_1, True)
    GPIO.output(IN3_2, False)
    GPIO.output(IN4_2, True)
    PWM11.ChangeDutyCycle(duty)
    PWM22.ChangeDutyCycle(duty)

def back_B(duty=0):
    GPIO.output(IN1_2, False)
    GPIO.output(IN2_2, True)
    GPIO.output(IN3_1, False)
    GPIO.output(IN4_1, True)
    PWM12.ChangeDutyCycle(duty)
    PWM21.ChangeDutyCycle(duty)


def stop_A():
    GPIO.output(IN1_1, False)
    GPIO.output(IN2_1, False)
    GPIO.output(IN3_2, False)
    GPIO.output(IN4_2, False)
    PWM11.ChangeDutyCycle(0)
    PWM22.ChangeDutyCycle(0)


def stop_B():
    GPIO.output(IN1_2, False)
    GPIO.output(IN2_2, False)
    GPIO.output(IN3_1, False)
    GPIO.output(IN4_1, False)
    PWM12.ChangeDutyCycle(0)
    PWM21.ChangeDutyCycle(0)
	
def speed_gogo(duty_ratio=0.7):
    # higher duty_ratio, higher speed
    global state_current, turn , distance,object_D
    turn = False

    if duty_ratio == 0.4 and object_D==False:
        state_current = 0
    elif duty_ratio == 0.7 and object_D==False:
        state_current = 1
    elif duty_ratio == 1 and object_D==False:
        state_current = 2
    else:
        state_current = None
		
    gogo_A(100*duty_ratio)
    gogo_B(100*duty_ratio)


def speed_back(duty_ratio=0.7):
    global state_current, turn , distance,object_D
    turn = False
    # higher duty_ratio, higher speed
    if object_D==False:
        duty_counter = 0
        time_counter = 0
        while time_counter < 10000:
            time_counter += 1
            if duty_counter < 1000 * duty_ratio:
                back_A()
                back_B()
            else:
                stop_A()
                stop_B()
            duty_counter += 1
            if duty_counter == 1000:
                duty_counter = 0


def gogo():
	time_counter = 0
	while time_counter < 10000:
		gogo_A()
		gogo_B()
		time_counter += 1
	stop()
	print("go")


def back():
	time_counter = 0
	while time_counter < 10000:
		back_A()
		back_B()
		time_counter += 1
	stop()
	print("back")


def stop():
	global state_current, turn
	turn = False
	state_current = 5
	stop_A()
	stop_B()
	# print("stop")


def stop_return():
	global state_current, state_previous
	state_current = state_previous
	stop_A()
	stop_B()
	# print("stop")


def turn_left(angle=0.5):
	global state_current, state_previous, turn,object_D
	state_previous = state_current
	state_current = 3
	
	if turn==False and object_D==False:
		turn = True
		angle_counter = 0
		gogo_B(70)
		stop_A()
		
		#while angle_counter < 100000 * angle:
		#	gogo_A()
		#	stop_B()
		#	angle_counter += 1
		#stop_return()
		
		print("turn left")


def turn_right(angle=0.5):
	global state_current, state_previous, turn,object_D
	state_previous = state_current
	state_current = 4
	
	if turn==False and object_D==False:
		turn = True
		angle_counter = 0
		gogo_A(70)
		stop_B()
		
		#while angle_counter < 100000 * angle:
		#	stop_A()
		#	gogo_B()
		#	angle_counter += 1
		#stop_return()
		
		print("turn right")


def do_nothing():
	if state_current == 0:
		speed_gogo(0.4)
	elif state_current == 1:
		speed_gogo(0.7)
	elif state_current == 2:
		speed_gogo(1)
	# elif state_current == 3:
	# 	turn_left()
	# elif state_current == 4:
	# 	turn_right()
	elif state_current == 5:
		stop()


def buzzer():
	os.system('omxplayer -o local blow.mp3')
	print("buzzing")


def test():
	turn_right(angle=0.65)
	speed_gogo()
	stop()
	time.sleep(1)
	turn_left(angle=0.65)
	speed_back(duty_ratio=0.5)	

def operate_order(order):
    global distance, object_D

    if order == "0" and object_D==False:
        speed_gogo(duty_ratio=0.2)
    elif order == "1" and object_D==False:
        speed_gogo(duty_ratio=0.5)
    elif order == "2"and object_D==False:
        speed_gogo(duty_ratio=1)
    elif order == "3"and object_D==False:
        turn_left()
    elif order == "4" and object_D==False:
        turn_right()
    elif order == "5":
        stop()
    else:
        do_nothing()      


def operate_buzz(buzz):
    pass
    #print('buzzer')
    #if buzz == "1":
        #buzzer()

def object_detect2():
    global distance, object_D
    
    GPIO.output(trig_pin, True)
    time.sleep(0.0001)
    GPIO.output(trig_pin, False)
        
    while GPIO.input(echo_pin) == False:
        start = time.time()
    while GPIO.input(echo_pin) == True:
        end = time.time()

    sig_time = end-start

    distance = sig_time / 0.000058
    distance = round (distance, 2)
    
    if distance > 350:
        distance = 350

    if distance < 5 and distance > 2:
        stop()
        print('Stopping..Object')
        object_D = True
    else:
        object_D = False
    #print('Distace: {} cm'.format(distance))
    return distance

        
    
    #if distance >2 and distance < 400:
        #if distance<=5:
            #stop()
            #buzzer()
        #print ("Distance ="+str(distance))

    #else:
        #print('range exceeded')
        #return -1
