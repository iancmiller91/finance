#amortizing loan calc
class Mortgage:
    def __init__(self,interest, years, total):
        self._interest = float(interest/(12)) #convert interest to interest/mo
        self._months = int(years*12)
        self._amount = float(round(total,2))
        self._principle = float(round(total,2))
        self._months_remaining = int(years*12)
        self._monthly_payment = self.calcMonthlyPayment()

    def interest(self):
        return self._interest*12*100

    def rate(self):
        return self._interest

    def amount(self):
        return self._amount

    def principle(self):
        return self._principle

    def yrs(self):
        return float(self._months)/12

    def months(self):
        return self._months

    def monthlyPayment(self):
        return self._monthly_payment

    def calcMonthlyPayment(self):
        payment = self.amount() * self.rate() \
                / (1.-(1.+self.rate())**float(-self.months()))
        return (round(payment,2))

    def totalPaid(self):
        return self.monthlyPayment()*self.months()

    def update(self, payment):
        i = self.rate()*self._principle
        #print(i)
        self._principle -= (payment - i)
        return self._principle, i, payment-i

