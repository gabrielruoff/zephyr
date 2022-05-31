import subprocess
from dotenv import load_dotenv
import os

load_dotenv('../../.env')

cert = os.environ.get('CERTFILE')
key = os.environ.get('CERT_KEYFILE')
# certargs = ['--cert-file', cert, '--key-file', key]
startcommand = ['{}\\Scripts\\python.exe'.format(os.environ['VIRTUAL_ENV']), 'manage.py', 'runserver', '0.0.0.0:8000']#, *certargs]
# start ganache and detach process
print(startcommand)
sp = subprocess.Popen(startcommand)#, start_new_session=True)
out, err = sp.communicate()
print(out)
print(err)