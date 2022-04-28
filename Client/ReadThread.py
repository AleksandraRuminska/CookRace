import threading

from Cook import Cook
from Messages.MessageType import MessageType


class ReadThread(threading.Thread):
    loaded = False

    def __init__(self, client, cooks, plate):
        threading.Thread.__init__(self)
        self.client = client
        self.cooks = cooks
        self.plate = plate

    def run(self):
        while True:
            in_data = self.client.recv(5)
            if in_data[0] == MessageType.SPAWN:
                # absolute
                self.cooks.append(Cook(in_data[2]*100, in_data[3], True if in_data[4] == 1 else False, in_data[1]))
                if in_data[4] == 1:
                    self.cook = self.cooks[-1]
                    pass
                if len(self.cooks) == 2:
                    ReadThread.loaded = True

            elif in_data[0] == MessageType.MOVE:
                # relative
                movement_x = in_data[2]
                movement_y = in_data[3]
                if movement_x == 50:
                    movement_x = -5

                if movement_y == 50:
                    movement_y = -5

                self.cooks[in_data[1]].move(movement_x, movement_y, True)

            elif in_data[0] == MessageType.PICKUP:
                # pick up
                if self.cooks[in_data[1]].is_carrying():
                    self.cooks[in_data[1]].put_down()
                else:
                    self.cooks[in_data[1]].pick_up(self.plate)

            print("From Server :", in_data.decode())
            if 'bye' == in_data.decode():
                break
