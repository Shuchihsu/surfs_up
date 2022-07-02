from secrets import token_bytes
from flask import Flask
app= Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello world'


import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///hawaii.sqlite",connect_args={'check_same_thread': False})
Base= automap_base()
Base.prepare(engine, reflect = True)
Measurement= Base.classes.measurement
Station= Base.classes.station
session = Session(engine)

app = Flask(__name__)
@app.route("/")
def welcome():
    return(
    '''
    Welcome to Climate AnalysisAPI!
    Avaialble Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/token
    /api/v1.0/start/end
    ''')
@app.route("/api/v1.0/precipitation")
def precipitation():
  pre_year = dt.date(2017,8,23) - dt.timedelta(days=365)
  precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >=pre_year).all()
  precip = {date: prcp for date  , prcp in precipitation}
  return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
  results = session.query(Station.station).all()
  stations =list(np.ravel(results))
  return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
  pre_year = dt.datetime(2017,8,23) - dt.timedelta(days=365)
  results= session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= pre_year).all()
  temps = list(np.ravel(results))
  return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sql=[func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    if not end:
      results = session.query(*sql).\
        filter(Measurement.date >= start).all()
      temps = list(np.ravel(results))
      return jsonify(temps)
      
    results = session.query(*sql).\
      filter(Measurement.date >= start).\
      filter(Measurement.date <= end).all()
    temps= list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':

  app.run()