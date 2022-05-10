# Importing dependencies and packages
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import flask and jsonify
from flask import Flask, jsonify

# Flask setup
app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
# print(Base.classes.keys()) --> commented out so it doesn't run everytime

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask routes
@app.route("/")
def home():
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>")
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session from python to database
    session = Session(engine)
    
    # Make the query for last year of precipitation data
    sel = [Measurement.date, func.sum(Measurement.prcp)]
    year_data = session.query(*sel).filter(func.strftime(Measurement.date)>=dt.date(2016, 8, 23)).\
        order_by(Measurement.date).group_by(Measurement.date).all()
    
    # Close the session
    session.close
    
    # Create a dictionary from the data retrieved
    precipitation_data = []
    for date, prcp in year_data:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        precipitation_data.append(dict)
    
    # Return dictionary jsonified for the API route
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create a session from python to database
    session = Session(engine)

    # Make query to get the stations from the dataset
    stations = session.query(Station.station).all()

    # Close the session
    session.close

    # Return list jsonified for API route
    stations = list(np.ravel(stations))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session from python to database
    session = Session(engine)

    # Make query to get the temp of most active station during last year
    temp_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281',\
        func.strftime(Measurement.date)>=dt.date(2016, 8, 23)).all()
    
    # Close the session
    session.close

    # Return list jsonified for API route
    temp_data = list(np.ravel(temp_data))
    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)
