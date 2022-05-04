import socket, threading
from copy import deepcopy
from time import sleep

from Messages.Create import Create
from Messages.MessageType import MessageType
from Messages.Spawn import Spawn


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
            msg3 = Spawn(0, 1, 100)
            for x in self.sockets:
                x.send((b''.join(msg3.encode())))
            # self.csocket.send((b''.join(msg3.encode())))
            sleep(1)
            msg4 = Spawn(1, 8, 100)
            for x in self.sockets:
                x.send((b''.join(msg4.encode())))

            # self.csocket.send((b''.join(msg4.encode())))

    def run(self):
        while True:
            msg = self.csocket.recv(6)
            print("WHAT??")
            if msg[0] == MessageType.SPAWN:
                # abs
                pass
            elif msg[0] == MessageType.MOVE:
                # rel
                for x in self.sockets:
                    x.send(msg)
                #self.csocket.send(msg)
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
LOCALHOST = "127.0.0.1"
# LOCALHOST = "25.41.143.165"

PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
counter = 0
sockets = []
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    sockets.append(clientsock)
    newthread = ClientThread(clientAddress, clientsock, counter, sockets)
    newthread.start()
    counter += 1
