import datetime as dt
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite") 

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def Welcome():
    return(
        f"All Routes that are available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():    
    session = Session(engine)
    
    """Return the Precipitation dictionary"""
    results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date.desc()).all()

    session.close()

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    """Return a list of stations."""
    results = session.query(Station.name).all()

    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return the temperature observations (tobs) for previous year."""
    cur_year = dt.date(2017, 8, 23)
    prev_year = cur_year - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    session.close()
    
    temps_list = list(np.ravel(results))
    return jsonify(temps_list)


@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    start_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),
    func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    temp_list = []
    for tmin, tavg, tmax in start_temp:
        start_dict = {}
        start_temp["Min Temperature"] = tmin
        start_temp["Max Temperature"] = tmax
        start_temp["Avg Temperature"] = tavg

    
        temp_list.append(start_dict)

    return jsonify(temp_list)   

    

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    end_temp = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),
    func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()   

    end_list = []
    for tmin, tavg, tmax in end_temp:
        end_dict = {}
        end_dict["Min Temperature"] = tmin
        end_dict["Max Temperature"] = tmax
        end_dict["Avg Temperature"] = tavg

        end_list.append(end_dict)

    return jsonify(end_list)


if __name__ == "__main__":
    app.run(debug=True)
