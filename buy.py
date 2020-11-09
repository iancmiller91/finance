import mortgage
import rent
class Buy:
    def __init__(self, price, down_percent, interest, years, closing, taxes, appreciation, insurance, selling_cost, rent):
        self._price = float(price)
        self._down = float(price*down_percent)
        self._closing = float(closing)
        self._taxes = float(taxes/12)
        self._appreciation = float(appreciation)/12.0
        self._rent = rent
        self._mortgage = mortgage.Mortgage(interest, years, price-self._down)
        self._current_value = self._price
        self._tax_appraisal = self._price
        self._insurance = float(insurance/12)
        self._selling_cost = selling_cost
        self._sell_profit = 0
        self._equity = self._down

    def update(self):
        self.update(self.monthlyPayment())

    def update(self, payment):
        principle,interest,eq = self._mortgage.update(payment)
        self._equity += eq
        payment -= self._rent.update() - (self._insurance+self._taxes)*self._tax_appraisal    #total cost of payment to purchaser
        self._current_value *= (1+self._appreciation)
        #update roi for selling house
        self._sell_profit = (self._current_value)*(1-self._selling_cost)-self._mortgage.principle()
        return payment, self._sell_profit

    def taxAppraisal(self):
        if self._current_value/self._tax_appraisal > 1.02: #CA tax can't go up by more than 2%
            self._tax_appraisal = self._tax_appraisal*1.02
        else:
            self._tax_appraisal = self._current_value

    def monthlyPayment(self):
        return self._mortgage.monthlyPayment()
