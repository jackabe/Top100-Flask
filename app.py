import numpy
from flask import Flask, jsonify, request, json
import urllib.parse
import random

# This module will return a dictionary linking each company id to each updated company share price
# This share price will be updated by probability based upon computation variables which are calculated below
# SpringBoot will send a GET request to this server containing a list of companies (JSON objects) as a parameter
# This module will iterate over the list and perform the calculations for returning

"""
    Revenue is in our case - the company value - a share is a dividend of this value
        - i.e Apple is worth in our case - 5m - it is going to have 10,000 shares - so each is 5m/10,000 - £500.00 each
    The computation will determine probability - which will determine if the revenue increases/decrease or stays the same
    The share price will then be updated by dividing revenue by the quantity of shares allocated
    The market is based upon risk - high risk transactions can go bad but PAY OFF VERY WELL
"""

"""
    The computation variable will be calculated by: 
        - Going though every company in the market list:
            - Check the market
            - Check the age
            - Check the number of employees
            - Check if the company has some sort of advantage over its competitors
"""

""" 
    Now we need to create probability events off of this variable which will increase/reduce revenue
        # This would be a safe transaction
        If the computation is more than 60: 
            - Standard probability of failure is 1/10
            - Standard Probability of big success is 1/10
            - It is very likely that it will stay the same / have various small changes (8/10).
 
        # This would be a very high risk but potentially very rewarding transaction
        If the computation is less than 30: 
            - Standard probability of failure is 2/5
            - Standard Probability of big success is 2/5
            - It is unlikely to stay the same (1/5).
            
         # This would be a regular transaction
        If the computation is between 30 and 60
            - Standard probability of failure is 1/5
            - Standard Probability of big success is 1/5
            - Chances are, it will stay the same / have various small changes (3/5).
                   
"""

app = Flask(__name__)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("80")
     )


# Each company has a market and each market has a risk level
markets = {'Industry': 15, 'Finance': 5, 'Technology': 5, 'Consumption': 15,
           'Aerospace and Defence': 10, 'Pharmacy': 10, 'Mining': 5, 'Travel and Leisure': 10, 'Retail': 10,
           'Insurance': 10, 'Oil': 5, 'Automobiles': 10}


# Take the market data from Spring, format the data and execute/return the required data
@app.route("/api/flask/market/calculate", methods=['GET'])
def get_test_calculation():
    # Get the data from URI query parameter
    url_encoded = request.args.get('company-data')
    # Decode the URI string
    url_decoded = urllib.parse.unquote(url_encoded)
    # Convert the string into JSON
    company_data = json.loads(url_decoded)

    # This array will contain dictionaries linking a company ID to a calculated revenue
    return_market_calculations = []

    # Iterate over company data
    for company in company_data:
        # Calculate the computation variable
        computation_variable = calculate_computation_variable(company)
        company_revenue = company['revenue']

        # If the variable is more than 60:
        # Chance of failure = 1/10
        # Chance of big success = 1/10
        # Otherwise standard performance chance = 8/10
        if computation_variable > 60:
            # Random number between 1 and 10 to simulate probabilities
            number = random.randint(1, 10)
            # If number is a one, the trade will be a SUCCESS
            if number == 1:
                new_revenue = create_success_revenue(company_revenue)
            # If number is a 10, the trade will be a FAILURE
            elif number == 10:
                new_revenue = create_fail_revenue(company_revenue)
            # If number is anything else the trade will be STANDARD
            else:
                new_revenue = create_standard_revenue(company_revenue)

        # If the variable is less than 30:
        # Chance of failure = 2/5
        # Chance of big success = 2/5
        # Otherwise standard performance chance = 1/5
        elif computation_variable < 30:
            # Random number between 1 and 100 to simulate probabilities
            number = random.randint(1, 100)
            # If number is less than or equal to 40, the trade will be a SUCCESS
            if number <= 40:
                new_revenue = create_success_revenue(company_revenue)
            # If number is larger than 40 but less than or equal to 80, the trade will be a FAILURE
            elif 40 < number <= 80:
                new_revenue = create_fail_revenue(company_revenue)
            # If number is anything else the trade will be STANDARD
            else:
                new_revenue = create_standard_revenue(company_revenue)

        # If the variable is more than 30 but less than 60
        # Chance of failure = 1/5
        # Chance of big success = 1/5
        # Otherwise standard performance chance = 3/5
        else:
            # Random number between 1 and 100 to simulate probabilities
            number = random.randint(1, 100)
            # If number is less than or equal to 20, the trade will be a SUCCESS
            if number <= 20:
                new_revenue = create_success_revenue(company_revenue)
            # If number is larger than 20 but less than or equal to 40, the trade will be a FAILURE
            elif 20 < number <= 40:
                new_revenue = create_fail_revenue(company_revenue)
            # If number is anything else the trade will be STANDARD
            else:
                new_revenue = create_standard_revenue(company_revenue)

        # Create company dict and append to the return array
        calculation_data = {company['id']: str(new_revenue)}
        return_market_calculations.append(calculation_data)

    # Return the array as JSON
    return jsonify(return_market_calculations)


# Take the market data from Spring and calculate the prices changes for all companies
@app.route("/api/flask/market/prices/update", methods=['GET'])
def calculate_market_price_changes():
    # Get the data from URI query parameter
    url_encoded = request.args.get('company-data')
    # Decode the URI string
    url_decoded = urllib.parse.unquote(url_encoded)
    # Convert the string into JSON
    company_data = json.loads(url_decoded)

    # This array will contain dictionaries linking a company ID to a price change
    return_price_calculations = []

    # Iterate over company data
    for company in company_data:
        # Get the company id, share price and transactions
        company_id = company['companyId']
        company_current_share_price = company['sharePrice']
        transactions = company['transactions']
        print(transactions)
        # Calculate the price change for each company
        # Create dictionary of company id to price change and add to array for returning
        if not transactions:
            return_price_calculations.append({company_id: '+/-0.0%'})
        else:
            price_change = calculate_price_changes(company_current_share_price, transactions)
            return_price_calculations.append({company_id: price_change})

    # Return the array as JSON
    return jsonify(return_price_calculations)


# Calculate the computation variable by checking the company stats
def calculate_computation_variable(company):
    company_age = company['age']
    company_employees = company['employees']
    company_market = company['marketType']
    company_advantage = company['competitiveAdvantage']

    # Each variable should represent 25% of the total value
    age_percentage = check_company_age(company_age) / 25
    market_percentage = check_market(company_market) / 25
    size_percentage = check_company_size(company_employees) / 25
    advantage_percentage = check_competitive_advantage(company_advantage) / 25

    # The company stats will have a weighting of 30% whereas advantage will only account for 10% of final variable
    standard_weighting = 0.3
    competitive_weighting = 0.1

    total = (age_percentage * standard_weighting) + (market_percentage * standard_weighting) \
        + (size_percentage * standard_weighting) + (advantage_percentage * competitive_weighting)

    # Multiply by 100 to get a number between 0-100.
    computation_variable = total * 100
    # Cast to int to remove trailing spaces
    return int(computation_variable)


# Assign points dependant on the companies age
def check_company_age(company_age):
    if company_age < 5:
        points = 0
    elif 5 < company_age < 10:
        points = 5
    elif 10 < company_age < 30:
        points = 10
    elif 30 < company_age < 60:
        points = 15
    else:
        points = 20
    return points


# Assign points dependant on the companies market
def check_market(company_market):
    # Get value from the markets dict with the key
    points = markets[company_market]
    return points


# Assign points dependent on the number of employees
def check_company_size(employees):
    if employees < 20:
        points = 0
    elif 20 < employees < 60:
        points = 5
    elif 60 < employees < 100:
        points = 10
    elif 100 < employees < 1000:
        points = 15
    else:
        points = 20
    return points


# If the company has some sort of advantage, give them 20 points, else 0
def check_competitive_advantage(company_advantage):
    if company_advantage:
        points = 20
    else:
        points = 0
    return points


# If the company is a success, how much of a success is it?
# Chance of big success is 1/3, chance of small success is 1/3, chance of normal success is 1/3.
def create_success_revenue(revenue):
    # Introduce proportion so that companies with a small starting revenue will face large increase
    # if revenue < 100000:
    #     revenue = revenue * 10
    # Get a number between 1 and 300 to simulate some probabilities
    number = random.randint(1, 300)
    # If number is less than or equal to 100, the success will be big
    if number <= 100:
        return revenue * 1.5
    # If number is larger than 100 but less than or equal to 200, the success will be standard
    elif 100 < number <= 200:
        return revenue * 1.10
    # If number is anything else the success will be small
    else:
        return revenue * 1.05


# If the company growth is standard
# Chance of small gain is 1/3, chance of small fail is 1/3, chance of staying exact same is 1/3.
def create_standard_revenue(revenue):
    # Get a number between 1 and 300 to simulate some probabilities
    number = random.randint(1, 300)
    # If number is less than or equal to 100, the revenue will grow by 5%
    if number <= 100:
        return revenue * 1.05
    # If number is larger than 100 but less than or equal to 200, the revenue will stay the same
    elif 100 < number <= 200:
        return revenue
    # If number is anything else the revenue will go down 5%
    else:
        return revenue * 0.95


# If the company is a fail, how much of a fail is it?
# Chance of big fail is 1/3, chance of small fail is 1/3, chance of normal fail is 1/3.
def create_fail_revenue(revenue):
    # Get a number between 1 and 300 to simulate some probabilities
    number = random.randint(1, 300)
    # If number is less than or equal to 100, the fail will be big
    if number <= 100:
        return revenue * 0.5
    # If number is larger than 100 but less than or equal to 200, the fail will be standard
    elif 100 < number <= 200:
        return revenue * 0.9
    # If number is anything else the fail will be small
    else:
        return revenue * 0.95


# Calculate the price change according to supply and demand of trades
def calculate_price_changes(company_share_price, transactions):
    # Array to add all the prices this company has been traded at
    price_array = []
    # Go through the transactions and add the array the trade price of each transaction
    for transaction in transactions:
        price_array.append(transaction['price'])
    # Get the mean of the prices
    price_average = numpy.mean(price_array)
    # Now calculate the percentage increase/decrease
    new_share_price = price_average/company_share_price
    # Now determine whether the change is positive. negative or 0.
    if new_share_price < 1:
        new_share_price = '-'+str(round(new_share_price, 2))+'%'
    elif new_share_price == 0:
        new_share_price = '+/-0.0%'
    else:
        new_share_price = '+'+str(round(new_share_price, 2))+'%'

    return new_share_price








"""

    This code is for future calculations using standard deviation etc
    
    # def calculate_step_2_variable():
    #     highest = max(prices)
    #     lowest = min(prices)
    #     median = numpy.median(prices)
    #     deviation = numpy.std(prices)
    #
    #     # Lowest
    #     if lowest < median * -1.5:
    #         lowest_points = 0
    #     elif lowest > median * -1:
    #         lowest_points = 10
    #     else:
    #         lowest_points = 20
    #
    #     # Highest
    #     if highest > median * 1.5:
    #         highest_points = 20
    #     else:
    #         highest_points = 10
    #
    #     # SD
    #     if deviation < 1:
    #         sd_points = 20
    #     elif 1 < deviation < 1.5:
    #         sd_points = 15
    #     elif 1.5 < deviation < 2.0:
    #         sd_points = 10
    #     else:
    #         sd_points = 0
    #
    #     lowest_points = lowest_points / 20
    #     highest_points = highest_points / 20
    #     deviation = sd_points / 20
    #
    #     standard_weighting = 0.2
    #     deviation_weighting = 0.6
    #
    #     total = (lowest_points * standard_weighting) + (highest_points * standard_weighting) + (
    #             deviation * deviation_weighting)
    #
    #     return total * 100

"""