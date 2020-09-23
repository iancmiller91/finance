class Rent:
    def __init__(self, rent, deposit):
        self._deposit = float(deposit)
        self._rent = float(rent)
        #self._increase = increase

    def rent(self):
        return self._rent

    def deposit(self):
        return self._deposit

    def update(self):
        return self.rent()

    def increase(self, rate):
        self._rent = self._rent*(1+rate)
