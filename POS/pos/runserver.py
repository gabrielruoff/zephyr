import subprocess
import os

startcommand = ['{}\\Scripts\\python.exe'.format(os.environ['VIRTUAL_ENV']), 'manage.py', 'runserver', '127.0.0.1:8000']
# start ganache and detach process
sp = subprocess.Popen(startcommand)#, start_new_session=True)
out, err = sp.communicate()
print(out)
print(err)