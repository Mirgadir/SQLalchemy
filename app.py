from flask import Flask, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app=Flask(__name__)

@app.route("/")
def home():
    
    return( "Welcome to my Climate Analysis API!<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start-date><br/>"
            f"/api/v1.0/<start-date>/<end-date><br/>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    precips = session.query(Measurement.date, Measurement.prcp)\
            .filter((Measurement.date > '2016-08-22') & (Measurement.prcp != 'None')).all()
    session.close()
    
    precipitation = []
    for date, prcp in precips:
        precip_dict={}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        precipitation.append(precip_dict)
        
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    st=session.query(Station).all()
    stations=[]  
    for station in st:
        stations.append(station.station)
    session.close()
    return jsonify(stations)    
        
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_year = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
            .filter(Measurement.station == 'USC00519281').filter(Measurement.date > '2016-08-22').all()
    session.close()
    year_temp = []
    for tobs in last_year:
        year_temp.append(tobs)
    return jsonify(year_temp)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                  func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                  filter(Measurement.date <= end).all()
    session.close()
    return jsonify(calc)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                  func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    return jsonify(calc)

if __name__ == "__main__":
    app.run(debug=False)