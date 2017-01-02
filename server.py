#!/usr/bin/python
from socket import socket, AF_INET, SOCK_STREAM ,SOL_SOCKET,SO_REUSEADDR,gethostbyaddr,error
from thread import start_new_thread
from os import system,path
from time import sleep
from sys import exit

# settings
host = ''
port = 1234
buffer_size = 4096
connections = []
max_connections = 5
sock = socket(AF_INET,SOCK_STREAM)
sock.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)

try:
    sock.bind((host, port))
except error as msg:
    print "Socket Error: %s" % msg
    exit()

sock.listen(max_connections)

def GetConnections():
    num = 1
    try:
        for client in connections:
            ip = client[1][0]
            hostname = gethostbyaddr(ip)[0]
            print "%s) ip %s - %s" % (num, ip, hostname)
            num += 1
    except Exception as e:
        print e
        pass
def ShowClients():
    if connections.__len__() == 0:
        print "no active connections!"
        EnterToMenu()
    else:
        print "Clients:"
        GetConnections()
    EnterToMenu()
def SendCommand(TypeAction):
    inp = ChoseClient(typeoption="normal")
    if TypeAction == "sendcommand":
        com = raw_input("Enter Command: ")
    if TypeAction == "install" or TypeAction == "remove":
        program = raw_input("Enter Program Name ")
        com = "package -y %s %s " % (TypeAction,program)
    if inp == 0:
        for i in connections:
            try:
                i[0].send(com)
                print "success on : %s" % (i[1][0])
                sleep(0.5)
                print(i[0].recv(buffer_size))
            except:
                print "failed on :", i[1][0]
                connections.remove(i)
                break
    else:
        try:
            connections[inp - 1][0].send(com)
            print "success on : %s " % (connections[inp - 1][1][0])
            sleep(0.5)
            print(connections[inp - 1][0].recv(buffer_size))
        except:
            print "failed on : %s " % (connections[inp - 1][1][0])
            connections.remove(connections[inp - 1])
    EnterToMenu()
def ChoseClient(typeoption):
    if connections.__len__() == 0:
        print "no active connections!"
        EnterToMenu()
    else:
        print "Clients:"
        GetConnections()
    while True:
        try:
            if typeoption == "shell":
                inp = int(raw_input("Enter Client Number "))
            else:
                inp = int(raw_input("Enter Client Number or 0 for all "))
        except ValueError:
            print "Numbers only!"
            continue
        else:
            break
    return inp
def SendFile():
    inp = ChoseClient(typeoption="normal")
    while True:
        sourcefile = raw_input("Enter Source ")
        if path.isfile(sourcefile) == False:
            print "File not found!"
            continue
        else:
            break
    destination = raw_input("Enter Destination ")
    if inp == 0:
        for i in connections:
            try:
                i[0].send("F")
                print "success on : %s" % (i[1][0])
            except:
                print "failed on :", i[1][0]
                connections.remove(i)
                break
            sleep(1)
            i[0].send(destination)
            f = open(sourcefile, 'rb')
            l = f.read(1024)
            while (l):
                i[0].send(l)
                l = f.read(1024)
            f.close()
            i[0].send("E")
    else:
        try:
            connections[inp - 1][0].send("F")
            print "success on : %s " % (connections[inp - 1][1][0])
        except:
            print "failed on : %s " % (connections[inp - 1][1][0])
            connections.remove(connections[inp - 1])
        sleep(1)
        connections[inp - 1][0].send(destination)
        f = open(sourcefile, 'rb')
        l = f.read(1024)
        while (l):
            connections[inp - 1][0].send(l)
            l = f.read(1024)
        f.close()
        sleep(1)
        connections[inp - 1][0].send("E")
    EnterToMenu()
def ShellAcsess():
    inp = ChoseClient(typeoption="shell")
    print "Remmber write Enter to exit!"
    while True:
        commandtosend = raw_input("-> ")
        if len(commandtosend) == 0:
            print "you didn't type command!"
            continue
        if (commandtosend == "exit"):
            print "Exiting...."
            connections.remove(connections[inp - 1])
            EnterToMenu()
        try:
            connections[inp - 1][0].send(commandtosend)
            sleep(0.5)
            print(connections[inp - 1][0].recv(buffer_size))
        except:
            print "failed on : %s " % (connections[inp - 1][1][0])
            connections.remove(connections[inp - 1])
    EnterToMenu()
def NotFound():
    print "Option not found!"
    menu(a=1)
def EnterToMenu():
    try:
        input("Hit Enter to Back Menu..")
    except:
        menu(a=1)
def menu(a):
    system("clear")
    print """
    ################################################################
    #       Python 102          name: Ben Hakim                    #
    ################################################################
    1) Show clients
    2) Send command to clients
    3) Transfer file to clients
    4) Install on clients
    5) Remove on clients
    6) Shell on a client """
    userChose = raw_input("Chose Options -> ")
    choice = {
        "1": ShowClients,
        "2": lambda : SendCommand(TypeAction="sendcommand"),
        "3": SendFile,
        "4": lambda : SendCommand(TypeAction="install"),
        "5": lambda : SendCommand(TypeAction="remove"),
        "6": ShellAcsess
    }
    choice.get(userChose, NotFound)()

start_new_thread(menu, (1,))
while True:
    conn, addr = sock.accept()
    connections.append([conn, addr])
sock.close()
