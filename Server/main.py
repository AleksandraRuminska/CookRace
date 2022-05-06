import socket
import threading
from copy import deepcopy
from queue import Queue
from time import sleep

from Messages.Create import Create
from Messages.MessageType import MessageType
from Messages.PutInPlace import PutInPlace
from Server.CookServerData import CookServerData

SPRITE_SIZE = 50


class ClientThread(threading.Thread):

    def __init__(self, clientAddress, clientsocket, counter, sockets):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = deepcopy(clientAddress)
        print("New connection added: ", self.caddress)
        self.sockets = sockets
        msg = Create(0, 1 if counter == 0 else 0)
        self.csocket.send((b''.join(msg.encode())))
        sleep(1)
        msg2 = Create(1, 1 if counter == 1 else 0)
        self.csocket.send((b''.join(msg2.encode())))

        if len(sockets) == 2:
            msg3 = PutInPlace(0, 2, 0, 2, 0)
            for x in self.sockets:
                x.send((b''.join(msg3.encode())))
            # self.csocket.send((b''.join(msg3.encode())))
            sleep(1)
            msg4 = PutInPlace(1, 16, 0, 2, 0)
            for x in self.sockets:
                x.send((b''.join(msg4.encode())))

            # self.csocket.send((b''.join(msg4.encode())))

    def run(self):
        while True:
            msg = self.csocket.recv(6)
            print("WHAT??")
            if msg[0] == MessageType.MOVE:
                dx = int.from_bytes(msg[2:3], byteorder='big', signed=True)
                dy = int.from_bytes(msg[3:], byteorder='big', signed=True)
                i = 0
                #for cook in self.cooks:
                    #print("i: ", i, " x: ", cook.x, " y: ", cook.y)
                    #i+=1
                self.cooks[msg[1]].move(dx, dy)
                #print("Cook: ", self.cooks[msg[1]].x, " , ", self.cooks[msg[1]].y)
                msg = PutInPlace(msg[1], int(self.cooks[msg[1]].x / SPRITE_SIZE), self.cooks[msg[1]].x % SPRITE_SIZE,
                                 int(self.cooks[msg[1]].y / SPRITE_SIZE), self.cooks[msg[1]].y % SPRITE_SIZE)
                for x in self.sockets:
                    x.send(b''.join(msg.encode()))
                # self.csocket.send(msg)
            elif msg[0] == MessageType.PICKUP:
                for x in self.sockets:
                    x.send(msg)
                # self.csocket.send(msg)
                print("SUCCESS!!")
                # pick up
            elif msg[0] == MessageType.PUTINPLACE:
                for x in self.sockets:
                    x.send(msg)
            elif msg[0] == MessageType.DOACTIVITY:
                for x in self.sockets:
                    x.send(msg)


# userMap = {}
LOCALHOST = "192.168.0.108"
# LOCALHOST = "25.41.143.165"

PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
counter = 0
sockets = []
updateQueue = Queue()
cooks = []
cooks.append(CookServerData())
cooks[0].move(100, 100)
cooks.append(CookServerData())
cooks[1].move(800, 100)

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    sockets.append(clientsock)
    newthread = ClientThread(clientAddress, clientsock, counter, sockets)
    newthread.start()
    counter += 1
