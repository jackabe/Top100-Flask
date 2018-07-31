import numpy
from flask import Flask, jsonify, request, json
import urllib.parse

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
            - Check the size of revenue
            - Check standard deviation and average of previous prices
            - Check if the company has some sort of advantage over its competitors
"""

""" 
    Now we need to create probability events off of this variable which will increase/reduce revenue
        # This would be a safe transaction
        If the computation is more than 70: 
            - Standard probability of failure is 1/10
            - Standard Probability of big success is 1/10
            - It is very likely that it will stay the same / have various small changes (8/10).
 
        # This would be a regular transaction
        If the computation is less than 30: 
            - Standard probability of failure is 2/5
            - Standard Probability of big success is 2/5
            - It is unlikely to stay the same (1/5).
            
        # This would be a very high risk but rewarding transaction
        If the computation is between 30 and 70
            - Standard probability of failure is 1/5
            - Standard Probability of big success is 1/5
            - Chances are, it will stay the same / have various small changes (3/5).
                   
"""

app = Flask(__name__)

# Each company has a market and each market has a risk level
markets = {'Industrial': 15, 'Financial Services': 5, 'Technology': 5, 'Food Producing': 15,
           'Aerospace and Defence': 10, 'Drug Retailers': 10, 'Mining': 5, 'Travel and Leisure': 10}


@app.route("/api/flask/market/calculate", methods=['GET'])
def get_test_calculation():
    url_encoded = request.args.get('company-data')
    url_decoded = urllib.parse.unquote(url_encoded)
    company_data = json.loads(url_decoded)
    print(company_data[0]['id'])
    return jsonify(company_data[0])

# def calculate_computation_variable():
#     step_1_total = calculate_step_1_variable()
#     step_2_total = calculate_step_2_variable()
#     computation_variable = (0.5 * step_1_total) + (0.5 * step_2_total)
#
#     return computation_variable
#
#
# def calculate_step_1_variable():
#     age_percentage = check_company_age() / 20
#     market_percentage = check_market() / 20
#     size_percentage = check_company_size() / 20
#     profit_percentage = check_profit_margin() / 20
#     advantage_percentage = check_competitive_advantage() / 20
#
#     standard_weighting = 0.225
#     competitive_weighting = 0.1
#
#     total = (age_percentage * standard_weighting) + (market_percentage * standard_weighting) \
#         + (size_percentage * standard_weighting) + (profit_percentage * standard_weighting) \
#         + (advantage_percentage * competitive_weighting)
#
#     return total * 100
#
#
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
#
#
# def check_company_age():
#     if age < 3:
#         points = 5
#     elif 5 < age < 10:
#         points = 8
#     elif 10 < age < 15:
#         points = 15
#     else:
#         points = 20
#     return points
#
#
# def check_market():
#     points = markets[market]
#     return points
#
#
# def check_company_size():
#     if employees < 20:
#         points = 5
#     elif 50 < employees < 100:
#         points = 8
#     elif 100 < employees < 1000:
#         points = 15
#     else:
#         points = 20
#     return points
#
#
# def check_competitive_advantage():
#     if has_competitive_advantage:
#         points = 20
#     else:
#         points = 0
#     return points
#
#
# def check_profit_margin():
#     if profit < 0:
#         points = 0
#     elif 0 < profit < 0.05:
#         points = 10
#     elif 0.05 < profit < 0.10:
#         points = 15
#     else:
#         points = 20
#     return points



if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("80")
     )
