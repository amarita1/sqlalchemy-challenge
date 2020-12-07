#Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

#SQLAlchemy 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create Routes with Flask
app = Flask(__name__)

#Define Main Route
@app.route("/")
def home():
    return(
    
    f"Welcome! Let's Explore Honolulu's Climate.<br/>"

    f"Available routes:<br/>"

    f"Precipitation Analysis<br/>"
    f"/api/v1.0/precipitation<br/>"
    
    f"Station Lists<br/>"
    f"/api/v1.0/stations<br/>"

    f"Temperature Observations from USC00519281<br/>"
    f"/api/v1.0/tobs<br/>"  

    f"Temperature Observations from USC00519281 by date<br/>"
    f"Date format used: YYYY-MM-DD<br/>"
    f"/api/v1.0/start<br/>"

    f"Temperature Observations from USC00519281 by date range<br/>"
    f"Date format used: YYYY-MM-DD<br/>"
    f"/api/v1.0/startdate/enddate<br/>"

)
   

#Define Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation(): 
    session = Session(engine)
    query_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_year).all()
    session.close

    precipitation = []
    for record in prcp:
        prcp_dict = {}
        prcp_dict["Date"] = value[0]
        prcp_dict["Precipitation"] = value[1]
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

#Define stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_names= session.query(Station.station, Station.name).all()
    session.close()

    stations = []
    for record in station_names:
        stations_dict = {}
        stations_dict["Station ID"] = value[0]
        stations_dict["Station Name"] = value[1]
        stations.append(stations_dict)
    
    return jsonify(stations)

#Define tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    query_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    temp_obvs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_year).filter(Measurement.station == 'USC00519281').all()
    session.close

    tobs_list = []
    for record in temp_obvs:
        tob_dict = {}
        tob_dict["Date"] = value[0]
        tob_dict["Temperature"] = value[1]
        tobs_list.append(tob_dict)
    return jsonify(tobs_list)

#Define start
@app.route("/api/v1.0/<start>/")
def start_date(start):
    session = Session(engine)
    start_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                   filter(Measurement.date >= start).all()
    session.close()

    temp = []
    for record in start_temp:
        temp_dict = {}
        temp_dict["Temp Min"] = value [0]
        temp_dict["Temp Avg"] = value [1]
        temp_dict["Temp Max"] = value [2]
        temp.append(temp_dict)
    return jsonify(temp)

#Define start-end range
@app.route('/api/v1.0/<startdate>/<enddate>')
def start_end_range(startdate, enddate):
    session = Session(engine)
    startend_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                            filter(Measurement.date >= startdate, Measurement.date <= enddate).all()
    session.close()

    range_temp = []
    for record in startend_temp:
        temp_range_dict = {}
        temp_range_dict["Temp Min"] = value [0]
        temp_range_dict["Temp Avg"] = value [1]
        temp_range_dict["Temp Max"] = value [2]
        range_temp.append(temp_range_dict)
    return jsonify(range_temp)

#Define main behavior
if __name__ == "__main__":
    app.run(debug=True)