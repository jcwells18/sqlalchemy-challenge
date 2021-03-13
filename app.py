#import necessary libraries
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create app and pass name
app = Flask(__name__)

#define info shown
@app.route("/")
def home():
    return(
        f"Hello and Welcome to the API<br/>"
        f"Available Routes:<br/>"
        f"api/v1.0/precipitation<br/>"
        f"api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"api/v1.0/start_date<br/>"
        f"api/v1.0/start_date/end_date<br/>"
        f"Please enter date as yyyy-mm-dd")

# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >="2016-08-23").\
    filter(Measurement.date <="2017-08-23").all()
    session.close()
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    station_names = session.query(Station.name).all()
    session.close()
    all_stations = list(np.ravel(station_names))
    return jsonify(all_stations)


#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    station_number = 'USC00519281'
    temperature_observations = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date>="2016-08-23").\
        filter(Measurement.date<="2017-08-23").\
            filter(Measurement.station == station_number).all()
    session.close()
    return jsonify(temperature_observations)

    
if __name__ == "__main__":
    app.run(debug=True)





    



