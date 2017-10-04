from serial import *
import time

motor_g_d_direction = 97
motor_g_speed = 97
motor_d_speed = 97

with Serial(port="/dev/ttyUSB2", baudrate=9600, timeout=1, writeTimeout=1) as port_serie:
	while port_serie.read() != 'z':
		pass
	print('a')
	direction = chr(motor_g_d_direction)
	pwm1 = chr(motor_g_speed)
	pwm2 = chr(motor_d_speed)
	nombre = ''.join([direction,pwm1,pwm2])
	port_serie.write(nombre.encode('ascii'))
	port_serie.close()
