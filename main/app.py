# Importing dependencies and packages
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
    # Create a dictionary from the data retrieved
    precipitation_data = []
    for date, prcp in year_data:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        precipitation_data.append(dict)
    return jsonify(precipitation_data)

if __name__ == "__main__":
    app.run(debug=True)
