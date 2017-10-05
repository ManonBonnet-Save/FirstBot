import time
from comm_serie import serial_init, serial_close, commande

serial_init()
commande(1,200,1)
time.sleep(5)
commande(16,1,200)
time.sleep(5)
commande(17,200,200)
time.sleep(5)
commande(20,200,200)
time.sleep(5)
serial_close()