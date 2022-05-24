from dotenv import load_dotenv
from lib.Crypt import RSAcrypt
from lib.Monero import multiwallet
from lib.HardwareSerial import arduino
import time, os

# load .env
load_dotenv()
# set env variables
DATADIR = os.environ.get("DATADIR")
MASTER_KEY_PREF = os.environ.get("MASTER_KEY_PREF")
MASTER_KEY_DIR = os.environ.get("MASTER_KEY_DIR")
KEY_PRIV_SUFFIX = os.environ.get("KEY_PRIV_SUFFIX")
MASTER_KEY_PASS = os.environ.get("MASTER_KEY_PASS")

rsacrypt = RSAcrypt()
arduino = arduino()
# make a wallet handler

rsacrypt.set_key(DATADIR+MASTER_KEY_DIR+MASTER_KEY_PREF+KEY_PRIV_SUFFIX, MASTER_KEY_PASS)

identifier = "customer"

enc_message = rsacrypt.encrypt(identifier)
print("\n\n encrypted message: "+enc_message)
# print(rsacrypt.decrypt(enc_message))
# print(len(enc_message))

arduino.connect("COM3")
print('connecting to arduino')
time.sleep(3)

input('place card on reader and press return')

arduino.send('w')
arduino.send(enc_message)
while(1):

    if arduino.serialport.in_waiting:
        print(arduino.serialport.readline())
        # arduino.send('a')
    # time.sleep(1)