import os
from dotenv import load_dotenv
from Crypt import RSAcrypt
from HardwareSerial import arduino
import time

# load .env
load_dotenv()
# set env variables
DATADIR = os.environ.get("DATADIR")
MASTER_KEY_PREF = os.environ.get("MASTER_KEY_PREF")
MASTER_KEY_DIR = os.environ.get("MASTER_KEY_DIR")
KEY_PRIV_SUFFIX = os.environ.get("KEY_PRIV_SUFFIX")
MASTER_KEY_PASS = os.environ.get("MASTER_KEY_PASS")

rsacrypt = RSAcrypt()
# rsacrypt.set_key(DATADIR+MASTER_KEY_DIR+MASTER_KEY_PREF+KEY_PRIV_SUFFIX, MASTER_KEY_PASS)
arduino = arduino()

arduino.connect("COM3")
print('connecting to arduino')
time.sleep(3)

arduino.send('r')
recv = arduino.receive()
recv = rsacrypt.decrypt(recv)

print("decrypted account identifier: "+recv)

# while(1):
#
#     if(arduino.serialport.in_waiting):
#         print(arduino.serialport.readline())
