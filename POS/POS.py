from lib import Crypt, HardwareSerial
from dotenv import load_dotenv
import os
import time

load_dotenv('../.env')
_winroot = 'C:/Users/GEruo/Documents/GitHub/zephyr/'

class POS:
    def __init__(self):
        self.pkey = os.environ.get('RSA_KEYFILE').replace('/home/common/dev/', _winroot)
        self.keypass = os.environ.get('RSA_KEYPAS')
        self.key = os.environ.get('RSA_KEYFILE').replace('/home/common/dev/', _winroot) + os.environ.get('RSA_PUB_SUFFIX')
        self.arduinoport = 'COM3'

    def writeuidtocard(self, prompt=True):
        with Crypt.RSACrypt() as crypt:
            uid = int(input('Enter userid to write: '))
            print('encrypting userid')
            crypt.setkey(self.key)
            euid = crypt.encrypt(uid)
        with HardwareSerial.arduino() as arduino:
            arduino.connect(self.arduinoport)
            time.sleep(2)
            input('-- Place the zephycard on the payment terminal and press the enter key --')
            arduino.send('w')
            print('writing uid to card...')
            arduino.send(euid)
            done = False
            while not done:
                if arduino.serialport.in_waiting:
                    line = arduino.serialport.readline().decode('utf-8').rstrip('\n')
                    if 'NAK' in line:
                        done = True
                        print('\n')
                    else:
                        print(line)
        if self._verifyuidwrite(uid):
            return '-- Write successful. uid verified: {} --'.format(uid)

    def readuidfromcard(self, prompt=True):
        with HardwareSerial.arduino() as arduino:
            arduino.connect(self.arduinoport)
            time.sleep(2)
            arduino.send('r')
            if prompt:
                print('Place the zephycard on the payment terminal')
            uid = arduino.receive()
            # print('read enc uid {}'.format(uid))
        with Crypt.RSACrypt() as crypt:
            crypt.setkey(self.pkey, self.keypass)
            uid = crypt.decrypt(uid)
        return uid

    def _verifyuidwrite(self, uid):
        return int(self.readuidfromcard(prompt=False)) == int(uid)


print('-- Zephyr POS --')
options = {
    '1': {
        'method': 'writeuidtocard',
        'description': 'Write a userid to a Zephyrcard'
    },
    '2': {
        'method': 'readuidfromcard',
        'description': 'Read a userid from a Zephyrcard'
    },
    '3': {
        'method': 'sentransaction',
        'description': 'Process a transaction'
    },
}

selected = input(
    'options\n' + str('\n'.join(['{} - {}'.format(option, options[option]['description']) for option in options]) + '\n'))

pos = POS()
func = getattr(pos, options[selected]['method'])
print(func())
