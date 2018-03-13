from flask import Flask, render_template, send_file, jsonify, request
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
from classifier import KNNClassifier, Query
from collections import Counter

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/predict_dispatch', methods=['GET', 'POST'])
def predict_dispatch():
  """
  Utilizes the classifier.py file to predict incident type based on
  latitude, longitude, and time of the day.
  """
  try:
    classifier = KNNClassifier()
    latitude, longitude = request.args['latitude'], request.args['longitude']
    [hour, minute, seconds] = map(int, [request.args['hour'], request.args['minute'], request.args['second']])
    time = hour*3600 + minute*60 + seconds
    x = Query(latitude, longitude, time)
    p = classifier.predict(x)
    print p
    return jsonify(result=p)
  except Exception as e:
    print e
    return jsonify(error=e)

@app.route('/zip_statistics/<zipcode>', methods=['GET', 'POST'])
def zip_statistics(zipcode="All"):
  """
  Returns statistics based on zipcode, default (no zipcode) calculates
  statistics for all zipcodes.
  Calculates:
  (1) Total incidents.
  (2) Average incidents per day.
  (3) Average response time per incident.
  (4) Percentage of incidents that are emergencies.
  """
  try:
    df = pd.read_csv('./data/cleaned_data.csv')
    if zipcode != "All":
      # Filter by zipcode
      df = df[df['zipcode_of_incident'] == int(zipcode)]
    # Based on data exploration, we know there are 12 days in the dataset.
    total_incidents = len(df)
    incidents_per_day = round(total_incidents / 12., 1)
    average_response_time = round(np.mean(df['response_time'])/60., 2)
    num_emergencies = len(df[df['final_priority'] == 3])
    percent_emergencies = round(num_emergencies / float(total_incidents) * 100, 1)
    return jsonify(
      total_incidents=total_incidents,
      incidents_per_day=incidents_per_day,
      average_response_time=average_response_time,
      percent_emergencies=percent_emergencies)
  except Exception as e:
    print e
    return jsonify(error=e)


@app.errorhandler(500)
def internal_error(error):
  return jsonify(error='There was an error processing your request.')