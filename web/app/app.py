from flask import Flask, abort, jsonify, render_template, redirect
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS

import pandas as pd
import json

import plotly
import plotly.graph_objs as go

from datetime import datetime, timedelta

from covid19.expogo.core import ExponentialGrowth, PlotCummulative
from covid19.expogo.dataset import WorldPopulation, Covid19DataSet

app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# world population datasets
world_population = WorldPopulation('datasets/world_population.csv')

# load the pandas dataframes
confirmed_df = Covid19DataSet('confirmed')
deaths_df = Covid19DataSet('deaths')
recovered_df = Covid19DataSet('recovered')

DF_TYPES = {
    'confirmed': confirmed_df,
    'deaths': deaths_df,
    'recovered': recovered_df
}


def information_table_by_type_and_country_backend(dftype, country):

    with open('./datasets/last_run.txt', 'r') as file:
        last_run_at = file.read().replace('\n', '')

    total_world_population = world_population.population_by_country(country)

    total_deaths_by_country = DF_TYPES['deaths'].find_by(
        country).transpose().iloc[-1, 0]
    total_confirmed_by_country = DF_TYPES['confirmed'].find_by(
        country).transpose().iloc[-1, 0]
    total_per_type_and_country = DF_TYPES[dftype].find_by(
        country).transpose().iloc[-1, 0]

    cfr = round(total_deaths_by_country / total_confirmed_by_country, 5)

    percentage_of_population = round(
        (total_per_type_and_country * 100) / total_world_population, 5)

    return {'percentage_of_population': percentage_of_population,
            'total_per_country': total_per_type_and_country,
            'last_run_at': last_run_at,
            'cfr': cfr
            }


@app.route('/information/country/<string:dftype>/<string:country>', methods=['GET'])
@as_json
def information_table_by_type_and_country(dftype, country):
    return jsonify(information_table_by_type_and_country_backend(dftype, country))

# make it case insensitive
@app.route('/exponential/country/<string:dftype>/<string:country>', methods=['GET'])
@as_json
def exponential_growth_table_by_type_and_country(dftype, country):
    if dftype not in ['deaths', 'recovered', 'confirmed']:
        abort(404, description="dataset type not valid")
    if country not in ['Brazil', 'Germany', 'Spain', 'Italy', 'Portugal']:
        abort(404, description="country not available")
    # add all the conditions
    return json.loads(ExponentialGrowth(DF_TYPES[dftype].find_by(country)).table_json())

#
@app.route('/plot/exponential/country/<string:dftype>/<string:country>', methods=['GET'])
@as_json
def plot_exponential_by_type_and_country(dftype, country):
    if dftype not in ['deaths', 'recovered', 'confirmed']:
        abort(404, description="dataset type not valid")
    if country not in ['Brazil', 'Germany', 'Spain', 'Italy', 'Portugal']:
        abort(404, description="country not available")

    return json.dumps(ExponentialGrowth(DF_TYPES[dftype].find_by(country)).plot_by_country_json(),
                      cls=plotly.utils.PlotlyJSONEncoder)
# make it case insensitive
@app.route('/plot/country/<string:dftype>/<string:country>', methods=['GET'])
@as_json
def plot_by_type_and_country(dftype, country):
    if dftype not in ['deaths', 'recovered', 'confirmed']:
        abort(404, description="dataset type not valid")
    if country not in ['Brazil', 'Germany', 'Spain', 'Italy', 'Portugal']:
        abort(404, description="country not available")
    # add all the conditions
    return json.dumps(PlotCummulative(DF_TYPES[dftype].find_by(country)).plot_by_country_json(),
                      cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/datasets', methods=['GET'])
@as_json
def datasets():
    return jsonify({'datasets': ['confirmed', 'deaths', 'recovered']})


@app.route('/datasets/<string:name>', methods=['GET'])
@as_json
def get_dataset(name):
    if name not in ['deaths', 'recovered', 'confirmed']:
        abort(404, description="Dataset not found")
    return json.loads(DF_TYPES[name].to_json())


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/country/<string:dftype>/<string:country>', methods=['GET'])
def country_page(dftype, country):
    return render_template('index.jinja2', report_type=dftype, country=country)


@app.route('/')
def index():
    return render_template('index.jinja2', report_type='confirmed', country='brazil')


if __name__ == '__main__':
    app.run(debug=True)
