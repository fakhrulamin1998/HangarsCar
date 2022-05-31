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


# 2. motor driver signal pins (L298N)
IN1_2 = 17 # 2.right wheel, forward
IN2_2 = 18 # 2.right wheel, back
IN3_2 = 27 # 2.left wheel, forward
IN4_2 = 22 # 2.left whell, back



GPIO.setup(IN1_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4_1, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(IN1_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4_2, GPIO.OUT, initial=GPIO.LOW)

state_current = 5   # stop
state_previous = 5
turn = False

def gogo_A():
	GPIO.output(IN1_1, True)
	GPIO.output(IN2_1, False)
	GPIO.output(IN1_2, True)
	GPIO.output(IN2_2, False)

def gogo_B():
	GPIO.output(IN3_1, True)
	GPIO.output(IN4_1, False)
	GPIO.output(IN3_2, True)
	GPIO.output(IN4_2, False)


def back_A():
	GPIO.output(IN1_1, False)
	GPIO.output(IN2_1, True)
	GPIO.output(IN1_2, False)
	GPIO.output(IN2_2, True)


def back_B():
	GPIO.output(IN3_1, False)
	GPIO.output(IN4_1, True)
	GPIO.output(IN3_2, False)
	GPIO.output(IN4_2, True)


def stop_A():
	GPIO.output(IN1_1, False)
	GPIO.output(IN2_1, False)
	GPIO.output(IN1_2, False)
	GPIO.output(IN2_2, False)


def stop_B():
	GPIO.output(IN3_1, False)
	GPIO.output(IN4_1, False)
	GPIO.output(IN3_2, False)
	GPIO.output(IN4_2, False)
	
def speed_gogo(duty_ratio=0.7):
	# higher duty_ratio, higher speed
	global state_current, turn
	turn = False
	if duty_ratio == 0.4:
		state_current = 0
	elif duty_ratio == 0.7:
		state_current = 1
	elif duty_ratio == 1:
		state_current = 2
	else:
		state_current = None
	duty_counter = 0
	time_counter = 0
	while time_counter < 10000:
		time_counter += 1
		if duty_counter < 1000 * duty_ratio:
			gogo_A()
			gogo_B()
		else:
			stop_A()
			stop_B()
		duty_counter += 1
		if duty_counter == 1000:
			duty_counter = 0


def speed_back(duty_ratio=0.7):
	# higher duty_ratio, higher speed
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
	global state_current, state_previous, turn
	state_previous = state_current
	state_current = 3
	if not turn:
		turn = True
		angle_counter = 0
		while angle_counter < 100000 * angle:
			gogo_A()
			stop_B()
			angle_counter += 1
		stop_return()
		print("turn left")


def turn_right(angle=0.5):
	global state_current, state_previous, turn
	state_previous = state_current
	state_current = 4
	if not turn:
		turn = True
		angle_counter = 0
		while angle_counter < 100000 * angle:
			stop_A()
			gogo_B()
			angle_counter += 1
		stop_return()
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

    if order == "0":
        speed_gogo(duty_ratio=0.4)
    elif order == "1":
        speed_gogo(duty_ratio=0.7)
    elif order == "2":
        speed_gogo(duty_ratio=1)
    elif order == "3":
        turn_left()
    elif order == "4":
        turn_right()
    elif order == "5":
        stop()
    else:
        do_nothing()


def operate_buzz(buzz):
       if buzz == "1":
        buzzer()


def object_detect(d=5):
	distance_sensor=hcsr04(23,24)
	distance_object=distance_sensor.distance()
	if distance_object<=d:
		stop()
		buzzer()