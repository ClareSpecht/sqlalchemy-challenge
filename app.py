# imports
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

#Create an app
app = Flask(__name__)

#Define what to do when a user hits the index route
@app.route("/")
def welcome():
    return (
        f"Welcome to my 'Home' page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

#Precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    session.close()
    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip.append(precip_dict)
    return jsonify(precip)

#Stations page
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_query = session.query(Station.station).all()
    session.close()
    allstations = list(np.ravel(station_query))
    return jsonify(allstations)

#Tobs page
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_query = session.query(Measurement.tobs).filter(Measurement.date >= year_ago).filter_by(station="USC00519281").all()
    session.close()
    bigstations = list(np.ravel(temp_query))
    return jsonify(bigstations)

#Start page
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    lowtemp = session.query(Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date >= start).filter_by(station="USC00519281").all()
    hightemp = session.query(Measurement.tobs, func.max(Measurement.tobs)).filter(Measurement.date >= start).filter_by(station="USC00519281").all()
    avgtemp = session.query(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter_by(station="USC00519281").all()
    lowtemps = list(np.ravel(lowtemp))
    hightemps = list(np.ravel(hightemp))
    avgtemps = list(np.ravel(avgtemp))
    session.close()
    return jsonify(lowtemps, hightemps, avgtemps)

#Start/End page
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    session = Session(engine)
    lowtemp = session.query(Measurement.tobs, func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).filter_by(station="USC00519281").all()
    hightemp = session.query(Measurement.tobs, func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).filter_by(station="USC00519281").all()
    avgtemp = session.query(Measurement.tobs, func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).filter_by(station="USC00519281").all()
    lowtemps = list(np.ravel(lowtemp))
    hightemps = list(np.ravel(hightemp))
    avgtemps = list(np.ravel(avgtemp))
    session.close()
    return jsonify(lowtemps, hightemps, avgtemps)

if __name__ == "__main__":
    app.run(debug=True)