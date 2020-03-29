import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from flask import session
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our Session (link) from Python to the DB
Session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/api/v1.0/<start><br/>"
        f"/api/v1.0//api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
# Create our Session (link) from Python to the DB    
    session = Session(engine)
    
    #Convert the query results to a Dictionary using `date` as the key and `prcp` as the value
    
    max_date = Session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = max_date[0]
    year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)
    results_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    precipitation_dict = dict(results_precipitation)
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations(): 
    # Create our Session (link) from Python to the DB
    session = Session(engine)
    #Return a JSON list of stations from the dataset.
    results_stations =  session.query(Measurement.station).group_by(Measurement.station).all()
    stations_list = list(np.ravel(results_stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    max_date = Session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = max_date[0]
    year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)
    results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()
    tobs_list = list(results_tobs)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    from_start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    from_start_list=list(from_start)
    return jsonify(from_start_list)

@app.route("/api/v1.0/<start>/<end>")
# def range_temp(start,end):
def calc_temps_start_end(start, end):
    print("In start & end date section.")
    
    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    result_temp = session.query(*select).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    print()
    print(f"Calculated temp for start date {start} & end date {end}")
    print(result_temp)
    print("Out of start & end date section.")
    return jsonify(result_temp)

    # """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given range"""
    # year, month, date = map(int, start.split('-'))
    # date_start = dt.datetime(year,month,day)
    # year2, month2, date2 = map(int, end.split('-'))
    # date_end = dt.date(year2,month2,day2)
   
# Query for tobs for definied date range
    # results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs).\
    #                         func.avg(Measurement.tobs)).filter(Measurement.date >= date_start).filter(Measurement.date <= date_end).all()
    # data = list(np.ravel(results))
    # return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)






