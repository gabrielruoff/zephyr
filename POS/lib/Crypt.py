import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
from base64 import b64encode
from base64 import b64decode
import logging
from dotenv import load_dotenv

# logging.basicConfig(filename='/home/common/dev/logs/zephyr.log', level=logging.DEBUG)

class RSACrypt:
    def __init__(self):
        self.key = None
        self.pkcs = None
        self.sha384 = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def setkey(self, keyfile, code=""):
        # if this is a raw key
        if isinstance(keyfile, bytes):
            self.key = RSA.import_key(keyfile, passphrase=code)
        else:
            with open(keyfile, 'rb') as f:
                self.key = RSA.import_key(f.read(), passphrase=code)
                f.close()

    def encrypt(self, data):
        plaintext = b64encode(str(data).encode())
        rsa_encryption_cipher = PKCS1_OAEP.new(self.key)
        ciphertext = rsa_encryption_cipher.encrypt(plaintext)
        return b64encode(ciphertext).decode()

    def decrypt(self, data):
        ciphertext = b64decode(data.encode())
        rsa_decryption_cipher = PKCS1_OAEP.new(self.key)
        plaintext = rsa_decryption_cipher.decrypt(ciphertext)
        return b64decode(plaintext).decode()

    def sign(self, data, key):
        self.pkcs = pkcs1_15.new(key)
        self.sha384 = SHA384.new()
        self.sha384.update(str.encode(data, 'utf-8'))
        sig = self.pkcs.sign(self.sha384)

        return binascii.hexlify(sig).decode('ascii')

    def verify(self, data, key, signature):
        self.pkcs = pkcs1_15.new(key)
        self.sha384 = SHA384.new()
        # if this is already a byte array
        if not isinstance(data, bytes):
            data = str.encode(data)
        self.sha384.update(data)

        return self.pkcs.verify(self.sha384, binascii.unhexlify(signature)) is None

# private_key = RSA.generate(2048)
# public_key = private_key.publickey()
# print(private_key.exportKey(format='PEM').decode('utf-8'))
# print(public_key.exportKey(format='PEM').decode('utf-8'))
#
# with open ("zephyr", "w") as prv_file:
#     prv_file.write(private_key.exportKey(format='PEM').decode('utf-8'))
#
# with open ("zephyr.pub", "w") as pub_file:
#     pub_file.write(public_key.exportKey(format='PEM').decode('utf-8'))