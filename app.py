import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

        f"NOTE: when querying dates, use format YYYY-MM-DD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #create a session (link) from Python to the DB
    session = Session(engine)

    #query all precipitation data
    results = session.query(measurement.date, measurement.prcp).all()

    #close out the session
    session.close()

    #all precipitation data
    all_prcp = []

    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp

        all_prcp.append(precipitation_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/station")
def station():
    #create a session (link) from Python to the DB
    session = Session(engine)

    #query all precipitation data
    results = session.query(measurement.station).distinct().all()

    #close out the session
    session.close()

    #all precipitation data
    all_station = []

    for station in results:
        station_dict = {}
        station_dict["station"] = station
        all_station.append(station_dict)

    return jsonify(all_station)



@app.route("/api/v1.0/tobs")
def tobs():

    #create session
    session = Session(engine)

    #where temperature data for station with highest number of observations
    results = session.query(measurement.date,measurement.tobs).filter(measurement.station == 'USC00519281').filter(func.date(measurement.date)> '2016-08-23').all()
    #.filter(func.date(measure.date)>'2018-08-23')
    all_tobs = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):

    #create session
    session = Session(engine)

    #query data from after the start date
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(func.date(measurement.date)>=start_date).all()
    
    summary_list = []

    for x, y, z in results:
        summary_dict = {}
        summary_dict["Minimum Temperature"] = x
        summary_dict["Maximum Temperature"] = y
        summary_dict["Average Temperature"] = z
        summary_list.append(summary_dict)
    
    return jsonify(summary_list)



@app.route("/api/v1.0/<start_date>/<end_date>")
def sandwich_date(start_date,end_date):

    #create session
    session = Session(engine)

    #query data from after the start date
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(func.date(measurement.date)>=start_date, func.date(measurement.date)<=end_date).all()
    
    summary_list = []

    for x, y, z in results:
        summary_dict = {}
        summary_dict["Minimum Temperature"] = x
        summary_dict["Maximum Temperature"] = y
        summary_dict["Average Temperature"] = z
        summary_list.append(summary_dict)
    
    return jsonify(summary_list)


if __name__ == '__main__':
    app.run(debug=True)
