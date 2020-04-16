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
def welcome():
    return(
        f"All Routes that are available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    cur_year = dt.date(2017, 8, 23)
    prev_year = cur_year - dt.timedelta(days=365)

    prcp=session.query(Measurement.date, func.sum(Measurement.prcp)).\
        filter(Measurement.prcp != None).filter(Measurement.date>=prev_year).\
            group_by(Measurement.date).all()
    session.close()

    prcp_data = []
    for d,p in prcp:
        prcp_dict = {}
        prcp_dict["date"] = d
        prcp_dict["prcp"] = p
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of stations."""
    results = session.query(Station.station).all()

    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():



if __name__ == "__main__":
    app.run(debug=True)
