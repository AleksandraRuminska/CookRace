import threading

from Cook import Cook
from Messages.MessageType import MessageType


class ReadThread(threading.Thread):
    def __init__(self, client, cooks, plate, semaphore):
        threading.Thread.__init__(self)
        self.client = client
        self.cooks = cooks
        self.plate = plate
        self.semaphore = semaphore

    def run(self):
        while True:
            in_data = self.client.recv(5)
            if in_data[0] == MessageType.CREATE:
                # absolute
                self.cooks.append(Cook(True if in_data[2] == 1 else False, in_data[1]))
                # self.cooks.append(Cook(in_data[2]*100, in_data[3], True if in_data[4] == 1 else False, in_data[1]))
                # if in_data[4] == 1:
                #     self.cook = self.cooks[-1]
                if len(self.cooks) == 2:
                    self.semaphore.release()

                if in_data[2] == 1:
                    self.cook = self.cooks[-1]
                if len(self.cooks) == 2:
                    self.semaphore.release()
            elif in_data[0] == MessageType.SPAWN:
                self.cooks[in_data[1]].rect.x = in_data[2]*100
                print("Setting x as: ", in_data[2]*100)
                self.cooks[in_data[1]].rect.y = in_data[3]
                print("Setting y as: ", in_data[3])

            elif in_data[0] == MessageType.MOVE:
                # relative
                movement_x = in_data[2]
                movement_y = in_data[3]
                if movement_x == 50:
                    movement_x = -5

                if movement_y == 50:
                    movement_y = -5

                print("Moving by:", movement_x , "position x: ", self.cooks[1].rect.x)
                print("Moving by:", movement_y, "position y: ", self.cooks[1].rect.y)

                self.cooks[in_data[1]].move(movement_x, movement_y, True)

                # self.cooks[in_data[1]].rect.x = movement_x
                # self.cooks[in_data[1]].rect.y = movement_y

            elif in_data[0] == MessageType.PICKUP:
                # pick up
                if self.cooks[in_data[1]].is_carrying():
                    self.cooks[in_data[1]].put_down()
                else:
                    self.cooks[in_data[1]].pick_up(self.plate)

            print("From Server :", in_data.decode())
            if 'bye' == in_data.decode():
                break
