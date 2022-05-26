import socket
import threading
from copy import deepcopy
from queue import Queue
from time import sleep

from pygame import Rect
from pygame.sprite import Sprite

from Messages import PickUp
from Messages.Create import Create
from Messages.DoActivity import DoActivity
from Messages.MessageType import MessageType
from Messages.Move import Move
from Messages.PutInPlace import PutInPlace
from Messages.PickUp import PickUp
from Server.CookServerData import CookServerData

SPRITE_SIZE = 50


class ClientThread(threading.Thread):

    def __init__(self, clientAddress, clientsocket, counter, queue):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = deepcopy(clientAddress)
        print("New connection added: ", self.caddress)
        self.queue = queue
        msg = Create(0, 1 if counter == 0 else 0)
        self.csocket.send(((msg.encode())))
        sleep(1)
        msg2 = Create(1, 1 if counter == 1 else 0)
        self.csocket.send(((msg2.encode())))

        # if len(sockets) == 2:
        #     msg3 = PutInPlace(0, 2, 0, 2, 0)
        #     for x in self.sockets:
        #         x.send(((msg3.encode())))
        #     # self.csocket.send(((msg3.encode())))
        #     sleep(1)
        #     msg4 = PutInPlace(1, 16, 0, 2, 0)
        #     for x in self.sockets:
        #         x.send(((msg4.encode())))

        # self.csocket.send(((msg4.encode())))

    def run(self):
        while True:
            msg = self.csocket.recv(6)
            #print("WHAT??")
            if msg[0] == MessageType.MOVE:
                dx = int.from_bytes(msg[2:3], byteorder='big', signed=True)
                dy = int.from_bytes(msg[3:4], byteorder='big', signed=True)
                #if (msg[1] == 1):
                print("____________________________________________________")
                print(dx)
                print(dy)
                print("____________________________________________________")
                self.queue.put(Move(msg[1], dx, dy))
            #     i = 0
            #     #for cook in self.cooks:
            #         #print("i: ", i, " x: ", cook.rect.x, " y: ", cook.rect.y)
            #         #i+=1
            #     self.cooks[msg[1]].move(dx, dy)
            #     #print("Cook: ", self.cooks[msg[1]].rect.x, " , ", self.cooks[msg[1]].rect.y)
            #     msg = PutInPlace(msg[1], int(self.cooks[msg[1]].rect.x / SPRITE_SIZE), self.cooks[msg[1]].rect.x % SPRITE_SIZE,
            #                      int(self.cooks[msg[1]].rect.y / SPRITE_SIZE), self.cooks[msg[1]].rect.y % SPRITE_SIZE)
            #     for x in self.sockets:
            #         x.send((msg.encode()))
            #     # self.csocket.send(msg)
            elif msg[0] == MessageType.PICKUP:
                self.queue.put(PickUp(msg[1], msg[2]))
            #     for x in self.sockets:
            #         x.send(msg)
            #     # self.csocket.send(msg)
            #     print("SUCCESS!!")
            #     # pick up
            elif msg[0] == MessageType.PUTINPLACE:
                self.queue.put(PutInPlace(msg[1], msg[2], msg[3], msg[4], msg[5]))
            #     for x in self.sockets:
            #         x.send(msg)
            elif msg[0] == MessageType.DOACTIVITY:
                self.queue.put(DoActivity(msg[1], msg[2], msg[3]))
            #     for x in self.sockets:
            #         x.send(msg)


# userMap = {}
#TODO ADD HAMACHI CONF, CUSTOM CONF
choice = int(input("Choose conf: \n 1: Private Kacper \n 2: Localhost \n 3: Hamachi Kacper"))
if choice == 1:
    ADDRESS = "192.168.0.108"
elif choice == 2:
    ADDRESS = "127.0.0.1"
elif choice == 3:
    ADDRESS = "25.47.123.189"


PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ADDRESS, PORT))
print("Server started")
print("Waiting for client request..")
counter = 0
sockets = []
updateQueue = Queue()
cooks = []

matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
rect_list = []
for i in range(len(matrix[0])):
    for j in range(len(matrix)):
        if matrix[j][i] == 0:
            rect = Rect(i*SPRITE_SIZE, j*SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE)
            rect_list.append(rect)
for i in range(8):
    cooks.append(CookServerData(rect_list))

cooks[0].move(100, 100)
cooks[1].move(800, 100)
cooks[2].move(100, 350)
cooks[3].move(300, 350)
cooks[4].move(550, 350)
cooks[5].move(50, 550)
cooks[6].move(300, 550)
cooks[7].move(750, 600)


while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    sockets.append(clientsock)
    newthread = ClientThread(clientAddress, clientsock, counter, updateQueue)
    newthread.start()
    counter += 1
    if counter == 2:
        msg = PutInPlace(0, int(cooks[0].rect.x / SPRITE_SIZE), cooks[0].rect.x % SPRITE_SIZE,
                         int(cooks[0].rect.y / SPRITE_SIZE), cooks[0].rect.y % SPRITE_SIZE)
        for x in sockets:
            x.send(((msg.encode())))
        sleep(1)
        msg = PutInPlace(1, int(cooks[1].rect.x / SPRITE_SIZE), cooks[1].rect.x % SPRITE_SIZE,
                         int(cooks[1].rect.y / SPRITE_SIZE), cooks[1].rect.y % SPRITE_SIZE)
        for x in sockets:
            x.send(((msg.encode())))
        moveCounter = 0
        move_tick = 1
        while True:
            msg = updateQueue.get(block=True)
            if msg._messageType == MessageType.MOVE:
                moveCounter += 1
                cooks[msg._id].move(msg._dx, msg._dy)
                if moveCounter == move_tick:
                    moveCounter = 0
                    msg = PutInPlace(msg._id, int(cooks[msg._id].rect.x / SPRITE_SIZE), cooks[msg._id].rect.x % SPRITE_SIZE,
                                     int(cooks[msg._id].rect.y / SPRITE_SIZE), cooks[msg._id].rect.y % SPRITE_SIZE)
                    #if(msg._id==1):
                    print("____________________________________________________")
                    print(msg._id)
                        #print(int(cooks[msg._id].rect.x))
                    print(cooks[msg._id].rect.x)
                        #print(int(cooks[msg._id].rect.rect.rect.y))
                    print(cooks[msg._id].rect.y)
                    print("____________________________________________________")
                    for x in sockets:
                        x.send((msg.encode()))
                    #if(msg._id==1):
                    #    sockets[0].send((msg.encode()))
                    #else:
                    #    sockets[1].send((msg.encode()))
            elif msg._messageType == MessageType.DOACTIVITY:
                for x in sockets:
                    x.send((msg.encode()))
            elif msg._messageType == MessageType.PUTINPLACE:
                cooks[msg._id].move(msg._x_s * SPRITE_SIZE + msg._x_r,msg._y_s * SPRITE_SIZE + msg._y_r)
                for x in sockets:
                    x.send((msg.encode()))
            elif msg._messageType == MessageType.PICKUP:
                for x in sockets:
                    x.send((msg.encode()))
