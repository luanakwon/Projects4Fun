from abc import *
from player import User
import time

class Action(metaclass=ABCMeta):
    @abstractmethod
    def act(self, user:User):
        pass

class IdleAction(Action):
    def __init__(self):
        # idle action speed in /s
        self.onIdle = False
        self.idle_speed = 1
        self.idle_start_t = 0
    @abstractmethod
    def setIdleAct(self):
        if not self.onIdle:
            self.onIdle = True
            self.idle_start_t = time.time()
    def updateIdleAct(self):
        dt = (time.time()-self.idle_start_t)
        self.idle_start_t = time.time()
        return self.idle_speed * dt

class Dig(IdleAction):
    def __init__(self):
        super(Dig, self).__init__()
        self.idle_speed = 0.1
    def act(self, user:User):
        print("digging... found dirt")
        user.inven.addItem('dirt',1)
    def setIdleAct(self):
        super().setIdleAct()
    def updateIdleAct(self, user:User):
        quant = super().updateIdleAct()
        user.inven.addItem('dirt',quant)

if __name__ == '__main__':
    user = User()
    Dig.act(user)
    print(user.inven.get_save_data())