import os
import numpy
from flask import Flask, redirect, request, render_template, make_response, escape, session, jsonify
import json

app = Flask(__name__)

company_name = "Apple"
age = 52
employees = 123000
market = "Technology"
has_competitive_advantage = True
profit = 0.4

markets = {'Industrial': 15, 'Financial Services': 5, 'Technology': 5, 'Food Producing': 15,
           'Aerospace and Defence': 10, 'Drug Retailers': 10, 'Mining': 5, 'Travel and Leisure': 10}

prices = [183, 184, 186, 185, 186, 186, 184, 185, 183, 184, 186, 185, 186, 186, 184, 186, 185, 186, 186]


@app.route("/api/flask/calculations", methods = ['GET','POST'])
def get_test_calculation():
    return jsonify(calculate_computation_variable())


def calculate_computation_variable():
    step_1_total = calculate_step_1_variable()
    step_2_total = calculate_step_2_variable()
    computation_variable = (0.5 * step_1_total) + (0.5 * step_2_total)

    return computation_variable


def calculate_step_1_variable():
    age_percentage = check_company_age() / 20
    market_percentage = check_market() / 20
    size_percentage = check_company_size() / 20
    profit_percentage = check_profit_margin() / 20
    advantage_percentage = check_competitive_advantage() / 20

    standard_weighting = 0.225
    competitive_weighting = 0.1

    total = (age_percentage * standard_weighting) + (market_percentage * standard_weighting) \
        + (size_percentage * standard_weighting) + (profit_percentage * standard_weighting) \
        + (advantage_percentage * competitive_weighting)

    return total * 100


def calculate_step_2_variable():
    highest = max(prices)
    lowest = min(prices)
    median = numpy.median(prices)
    deviation = numpy.std(prices)

    # Lowest
    if lowest < median * -1.5:
        lowest_points = 0
    elif lowest > median * -1:
        lowest_points = 10
    else:
        lowest_points = 20

    # Highest
    if highest > median * 1.5:
        highest_points = 20
    else:
        highest_points = 10

    # SD
    if deviation < 1:
        sd_points = 20
    elif 1 < deviation < 1.5:
        sd_points = 15
    elif 1.5 < deviation < 2.0:
        sd_points = 10
    else:
        sd_points = 0

    lowest_points = lowest_points / 20
    highest_points = highest_points / 20
    deviation = sd_points / 20

    standard_weighting = 0.2
    deviation_weighting = 0.6

    total = (lowest_points * standard_weighting) + (highest_points * standard_weighting) + (
            deviation * deviation_weighting)

    return total * 100


def check_company_age():
    if age < 3:
        points = 5
    elif 5 < age < 10:
        points = 8
    elif 10 < age < 15:
        points = 15
    else:
        points = 20
    return points


def check_market():
    points = markets[market]
    return points


def check_company_size():
    if employees < 20:
        points = 5
    elif 50 < employees < 100:
        points = 8
    elif 100 < employees < 1000:
        points = 15
    else:
        points = 20
    return points


def check_competitive_advantage():
    if has_competitive_advantage:
        points = 20
    else:
        points = 0
    return points


def check_profit_margin():
    if profit < 0:
        points = 0
    elif 0 < profit < 0.05:
        points = 10
    elif 0.05 < profit < 0.10:
        points = 15
    else:
        points = 20
    return points



if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=int("80")
     )
