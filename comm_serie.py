from __future__ import print_function
import time
from serial import *

global direction
global pwm1
global pwm2

direction = 0
pwm1 = 0
pwm2 = 0

global port_serie

port_serie = Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1, writeTimeout=1)

def stop():
	commande(0,0,0)
        
def right(ratio):
	commande(16,130,130,ratio)#16
        
def left(ratio):
	commande(1,130,130,ratio)#1

def forward():
	print('>>>>>>>>>>>>>>>>>>>>>><forward')
	commande(17,80,80)

def backward():
	commande(20,70,70,0.5)

def serial_init():
	while port_serie.read() != 'z':
		pass

def serial_close():
	commande(0,0,0)
	time.sleep(1)
	port_serie.close()

def commande(motor_g_d_direction,motor_g_speed,motor_d_speed,ratio=1):
	direction = motor_g_d_direction
	pwm1 = motor_g_speed
	pwm2 = motor_d_speed
	#nombre = ''.join([chr(direction),chr(pwm1),chr(pwm2)])
	#print(nombre)
	port_serie.write(chr(direction))
	port_serie.write(chr(pwm1))
	port_serie.write(chr(pwm2))
        time.sleep(0.3*ratio)
        port_serie.write(chr(0))
	port_serie.write(chr(0))
	port_serie.write(chr(0))
