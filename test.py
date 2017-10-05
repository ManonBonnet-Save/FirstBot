import time
from comm_serie import serial_init, serial_close, commande, gauche, droite, stop

serial_init()
droite()
stop()
gauche()
serial_close()