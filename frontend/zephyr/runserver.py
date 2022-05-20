import subprocess
import manage

startcommand = ['/home/common/dev/venv/bin/python3.8', 'manage.py', 'runserver']
# start ganache and detach process
sp = subprocess.Popen(startcommand)#, start_new_session=True)
out, err = sp.communicate()
print(out)
print(err)