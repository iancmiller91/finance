import mortgage
import buy
import rent
import matplotlib.pyplot as plt
import argparse
    #default assumptions:
    #purchase_price = 600000
    #down_percent = .20
    #years=30
    #interest = 3.0
    #closing = .03 #.02824 (including some tax and home insurance)
    #selling_cost = .07
    #tax = .015 #.01311
    #appreciation = 0.02 #apprecation rate - repair rate
    #insurance = .005 #quote of .004
    #market_gains = .06
    #current_rent = 1600.0
    #rental_increase = .0075
    #deposit = current_rent*2
    #house_rental = 0.00

def rentVsBuy(purchase_price, down_decimal, years, interest, closing, selling_cost,\
        tax, appreciation, insurance, market_gains, current_rent, rental_increase, deposit,\
        rental_income):

    months = years*12
    market_gains_p = 1+market_gains/12
    down = purchase_price*down_decimal
    principle = purchase_price-down

    m = mortgage.Mortgage(interest, years, principle)
    payment = m.monthlyPayment()
    print ("down: $", down)
    print("monthly mortgage payment: $", payment, "total monthly: $ ", \
            round(payment+(insurance+tax)*purchase_price/12.0,2), "cost to us: ",\
            round(payment+(insurance+tax)*purchase_price/12.0 - rental_income,2 ))
    print("total paid on mortgage: $", round(m.totalPaid(),2), "total paid: $", \
            round(down+m.totalPaid(),2))

    #print("amotorization schedule")
    #for month in range(0,months):
    #    principle, i_pmt, p_pmt = m.update(payment, principle)
        #print("month: ", month, "\t principle: ", principle)
    house_rental = rent.Rent(rental_income,0)
    b = buy.Buy(purchase_price, down_decimal, interest, years, closing, tax, appreciation,\
            insurance,selling_cost,house_rental)
    r = rent.Rent(current_rent, deposit)
    costs = []

    #One time costs:
    rental = r.deposit()
    purchase = closing*purchase_price + down
    b_opp_cost = purchase
    r_opp_cost = rental
    opp_cost_after_sale = purchase_price*(selling_cost+closing)
    costs.append([rental,r_opp_cost,purchase,b_opp_cost, opp_cost_after_sale])

    flag = [1,1,1,1]
    for month in range(1,months):
        if month % 12==0:
            #print("year end results:", costs[-1])
            r.increase(rental_increase)
            b.taxAppraisal()
        r_cost = r.update()
        b_cost, b_sell = b.update(b.monthlyPayment()) #includes rental if applicable
        rental += r_cost
        purchase += b_cost
        b_opp_cost = b_opp_cost*market_gains_p + b_cost
        r_opp_cost = r_opp_cost*market_gains_p + r_cost
        opp_cost_after_sale = b_opp_cost - b_sell
        costs.append([rental, r_opp_cost, purchase, b_opp_cost, opp_cost_after_sale])

        if rental > purchase and flag[0]:
            print("straight costs crossing at month: ", month, month/12.)
            flag[0] = 0
        if r_opp_cost > b_opp_cost and flag [1]:
            print("buying_opp cost is better after month: ", month, month/12.)
            flag[1] = 0
        if r_opp_cost > opp_cost_after_sale and flag[2]:
            print("buying cost is better with sale of property after month: ", month, month/12.) 
            flag[2] = 0
        if 0 > opp_cost_after_sale and flag[3]:
            print("reselling makes a profit after: ", month, month/12.)

    print("monthly cost for last payment year 30: ", b_cost)

    #plots
    purchase_costs = [c[2] for c in costs]
    purchase_opp_costs = [c[3] for c in costs]
    resale_opp_costs = [c[4] for c in costs]
    rent_costs =  [c[0] for c in costs]
    rent_opp_costs =  [c[1] for c in costs]

    if 0:
        fig, ax = plt.subplots(2,1)
        ax[0].plot(range(0,months), purchase_costs, label='purchase costs')
        ax[0].plot(range(0,months), rent_costs, label='rent costs')
        ax[1].plot(range(0,months), purchase_opp_costs, label = 'purchase opp costs')
        ax[1].plot(range(0,months), resale_opp_costs, label = 'resale opp costs')
        ax[1].plot(range(0,months), rent_opp_costs, label = 'rent costs')

        ax[0].legend()
        ax[1].legend()
        plt.show()
    if 1:
        fig, ax = plt.subplots()
        ax.plot(range(0,months), purchase_opp_costs, label = 'purchase opp costs')
        ax.plot(range(0,months), resale_opp_costs, label = 'resale opp costs')
        ax.plot(range(0,months), rent_opp_costs, label = 'rent costs')
        title = "purchase_price:"+str(purchase_price)+"; rent: "+str(current_rent)+\
                "; renter: "+str(house_rental.rent())
        ax.set_title(title)
        ax.set_xlabel('months')
        ax.set_ylabel('$')
        ax.legend()
        plt.show()

def main(): 
    parser = argparse.ArgumentParser(description='Rent vs buying a house calculator')

    parser.add_argument('-i', '--interest', default=3.0, type=float, dest='interest')
    parser.add_argument('-y', '--loan_years', default=30, type=float,  dest='years')
    parser.add_argument('-p', '--purchase_price', default=600000.0, type=float, dest='purchase_price')
    parser.add_argument('-d', '--down', default=.2, type=float, dest='down')
    parser.add_argument('-c', '--closing', default=.03, type=float, dest='closing')
    parser.add_argument('-s', '--selling', default=.07, type=float, dest='selling_cost')
    parser.add_argument('-t', '--tax', default=.015, type=float, dest='tax')
    parser.add_argument('-a', '--appreciation', default=.01, type=float, dest='appreciation')
    parser.add_argument('-n', '--insurance', default=.005, type=float, dest='insurance')
    parser.add_argument('-g', '--market_gains', default=.06, type=float, dest='market_gains')
    parser.add_argument('-r', '--current_rent', default=1600.0, type=float, dest='current_rent')
    parser.add_argument('-R', '--rental_income', default=0.0, type=float, dest='rental_income')
    parser.add_argument('-I', '--rental_increase', default=0.0075, type=float, dest='rental_increase')
    parser.add_argument('-D', '--deposit', default=3200.0, type=float, dest='deposit')

    args = parser.parse_args()
    print(args)
    rentVsBuy(args.purchase_price, args.down, args.years, args.interest,\
            args.closing, args.selling_cost, args.tax, args.appreciation, args.insurance,\
            args.market_gains, args.current_rent, args.rental_increase, args.deposit,\
            args.rental_income)

if __name__ == '__main__':
    main()
