class Inventory():
    def __init__(self):
        self._inven = {}

    def __str__(self):
        return str(self._inven)

    def get_save_data(self):
        return self._inven
    def load_save_data(self, datadict):
        self._inven = datadict

    def addItem(self, name, quantity):
        if quantity > 0:
            stored = self._inven.get(name,0)
            self._inven[name] = stored + quantity
    def popItem(self, name, quantity):
        if quantity > 0:
            stored = self._inven.get(name,0)
            pop_quant = min(quantity,stored)
            self._inven[name] = stored-pop_quant
            return pop_quant
        else:
            return 0
    