# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request,redirect, url_for

import numpy as np
import pandas as pd
import datetime as dt

import pprint as pp

from datetime import timedelta, datetime


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():

    return (
        "This is the documentation page of Anna's APIs.<br/>"
        "<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a> | <i>Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.</i><br/>"
        "<a href='/api/v1.0/stations'>/api/v1.0/stations</a> | <i>Return a JSON list of stations from the dataset.</i><br/>"
        "<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a> | <i>Query the dates and temperature observations of the most-active station for the previous year of data.</i><br/>"
        "/api/v1.0/&lt;start&gt; & /api/v1.0/&lt;start&gt;/&lt;end&gt; <a href='/api/v1.0/start_end'> Click here to directly get your api result <a/> | <i>Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.</i><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Find the most recent date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    # Convert date to datetime for reference
    most_recent_date_dt = datetime.strptime(most_recent_date, '%Y-%m-%d')

    # Calculate the date one year ago
    query_date = most_recent_date_dt - timedelta(days=365)

    # Run query for last 12 months prcp data from query date.
    last_12_months_precipitation = session.query(
        Measurement.station, 
        Measurement.date, 
        Measurement.prcp, 
        Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date.desc()).all()

    # Perform a query to retrieve only the date and precipitation scores
    last_12_months_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()
    
    # Create dictionary to store prcp data for last 12 months with date as the key.
    last_12_months_dict = dict()

    for row in last_12_months_prcp:
        last_12_months_dict[row.date] = row.prcp
    
    pp.pprint(last_12_months_dict)

    return jsonify(last_12_months_dict)

@app.route("/api/v1.0/stations")
# Perform a query to find total stations in database
def stations():
    active_stations = session.query(
        Measurement.station,
    ).group_by(
        Measurement.station
    ).all()

# Create list of stations with their respective data from database
    station_list = list()

    for station in active_stations:
        station_list.append(station.station)

    return jsonify(station_list) 

@app.route("/api/v1.0/tobs")
# Perform query to count the number of data entry (rows) for each station to show the most active stations
# in descending order (most to least active)
def tobs():
    active_stations = session.query(
        Measurement.station,
        func.count()
    ).group_by(
        Measurement.station
    ).order_by(
        func.count().desc()
    ).all()

# Print station activity results
    for station, count in active_stations:
        print(f"Station: {station}, Row Count: {count}")

# Print the most active station from the database (station with most data output)
    most_active_id = None
    if active_stations:
        most_active_station = active_stations[0] 
        station, count = most_active_station
        most_active_id = station
        print()
        print(f"Most Active Station: {station}, Row Count: {count}")
    else:
        print("No data found")

# Find temperature statistics for the most active station    
    temp_stats = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.round(func.avg(Measurement.tobs),1)
    ).filter(
        Measurement.station == most_active_id
    ).all()

    # Initialize the variables to hold the final values
    lowest_temp = None
    highest_temp = None
    avg_temp = None
    
    for lowest, highest, avg in temp_stats:
        lowest_temp = lowest
        highest_temp = highest
        avg_temp = avg

    return jsonify([lowest_temp, highest_temp, avg_temp]) 

# URL for specified start date only (no end date)
@app.route("/api/v1.0/<start>")
def start(start):
    '''
    Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date.
    '''

    return jsonify(get_temp_data(start)) 

# URL for specified timeframe (start and end dates)
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    '''
    Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start and specified end date.
    '''
    return jsonify(get_temp_data(start,end)) 

# URL for test interface for user inputs 
@app.route("/api/v1.0/start_end",methods=['GET', 'POST'])
def input_date():
    if request.method == 'POST':
        # Retrieve the dates entered by the user from the form
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Redirect to the appropriate route based on input
        if end_date:
            return redirect(url_for('start_end', start=start_date, end=end_date))
        else:
            return redirect(url_for('start', start=start_date))

    # Render the HTML form for user input
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Date Input Form</title>
        </head>
        <body>
            <h1>Enter Start and (optional) End Dates</h1>
            <form method="post">
                <label for="start_date">Start Date:</label>
                <input type="text" id="start_date" name="start_date" placeholder="YYYY-MM-DD"><br><br>
                
                <label for="end_date">End Date (optional):</label>
                <input type="text" id="end_date" name="end_date" placeholder="YYYY-MM-DD"><br><br>
                
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
    '''

# Get corresponding temperature data for user input date(s) with start date and (optional) end date.
def get_temp_data(start, end=None):

    print("Start:",start," End:",end)
    if end == None:
        temp_stats = session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.round(func.avg(Measurement.tobs),1)
        ).filter(
            Measurement.date >= start
        ).all()
    else:
        temp_stats = session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.round(func.avg(Measurement.tobs),1)
        ).filter(
            Measurement.date >= start
        ).filter(
            Measurement.date <= end
        ).all()


    # Initialize the variables to hold the final values
    lowest_temp = None
    highest_temp = None
    avg_temp = None
    
    for lowest, highest, avg in temp_stats:
        lowest_temp = lowest
        highest_temp = highest
        avg_temp = avg

    return [lowest_temp,highest_temp,avg_temp]
if __name__ == "__main__":
    app.run(debug=True)