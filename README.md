# Financial Analysis

# Rent vs Buy
## Env
pip3 install -r requirements.txt

## Use
The script can be run with all defalt values via: `python3 rent_vs_by.py`

A list of all the values can be found via: `python3 rent_vs_by.py -h`

## The default assumptions:
    * purchase_price = 600000
    * down_percent = .20
    * years=30
    * interest = 3.0
    * closing = .03 
        * a better estimate for my zip is .02824 (including some tax and home insurance)
    * selling_cost = .07
    * tax = .015 
        * a better estimate for my zip is .01311
    * appreciation = 0.01 
        * apprecation rate - repair rate, note default tax+insurance is higher
    * insurance = .005 #quote of .004 for my area
    * market_gains = .06
    * current_rent = 1600.0
    * rental_increase = .0075
    * deposit = current_rent*2
    * rental_income = 0.00
