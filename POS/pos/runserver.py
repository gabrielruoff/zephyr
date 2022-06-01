import platform
import subprocess
import os

certargs = []
if platform.system() == "linux" or platform.system() == "linux2":
    # linux
    pass
elif platform.system() == "Darwin":
    # OS X
    exe = '{}/bin/python'.format(os.environ['VIRTUAL_ENV'])
elif platform.system() == "win32" or platform.system() == "Windows":
    exe = '{}\\Scripts\\python.exe'.format(os.environ['VIRTUAL_ENV'])

startcommand = [exe, 'manage.py', 'runserver', '127.0.0.1:8000']
# start ganache and detach process
sp = subprocess.Popen(startcommand)#, start_new_session=True)
out, err = sp.communicate()
print(out)
print(err)