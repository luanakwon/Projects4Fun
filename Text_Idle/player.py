import pickle

from inventory import Inventory

class User:
    def __init__(self):
        self.money = 0
        self.inven = Inventory()
        self.actions = {}

    def save_data(self):
        with open('userdata.pkl','wb') as f:
            pickle.dump(self,f,pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_data():
        with open('userdata.pkl','rb') as f:
            return pickle.load(f)

    def status(self):
        out = f"money : {self.money}\n"
        out += "inventory : \n"
        out += str(self.inven)
        print(out)

if __name__ == '__main__':
    dummy = User()
    dummy.save_data()