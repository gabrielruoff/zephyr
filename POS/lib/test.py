# import os
# import subprocess
# import sys
#
# def reader(fd):
#     with os.fdopen(fd, bufsize=bufsize) as f:
#         while True:
#             data = f.read(bufsize)
#             if not data:
#                 break
#             print(data)
#
# def writer(fd, data):
#     with os.fdopen(fd, bufsize=bufsize) as f:
#         while True:
#             f.write(data)
#             if not data:
#                 break
#             print(data)
#
# startcommand = ['{}\\Scripts\\python.exe'.format(os.environ['VIRTUAL_ENV']), 'HardwareSerial.py']#, *certargs]
# # start ganache and detach process
# bufsize = 256
# print(startcommand)
# p = subprocess.Popen(startcommand, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
# print('open')
# # grep_stdout, stderr = p.communicate(input=b'read_card_data\n')
# p.stdin.write(b'send.r\n')
# for line in p.stdout:
#     print(line)