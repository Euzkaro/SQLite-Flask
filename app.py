#################################################################
            #Getting Started
#################################################################

# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from flask import Flask, jsonify

#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database 
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#################################################################
            #Behold the APP!
#################################################################

app = Flask(__name__)

# List of Routes
@app.route('/')
def home_route():
    return (
        f"/api/v1.0/precipitation/ <br><br/>"  
        f" /api/v1.0/stations/ <br><br/>" 
        f" /api/v1.0/tobs/ <br><br/>"
        f"/api/v1.0/start/ <br><br/>"
        f"/api/v1.0/start/end/")

       
# Feeding the Routes 
# Precipitation
@app.route('/api/v1.0/precipitation/')
def precipitation():
    prcp_results = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date >= '2017-01-01').all()
    p_dict = dict(prcp_results)
    return jsonify(p_dict)

# Station
@app.route('/api/v1.0/stations/')
def stations():
    station_list = session.query(Station.station)\
    .order_by(Station.station).all()   
    for row in station_list:
        print (row[0])
    return jsonify(station_list)

#Tobs
@app.route('/api/v1.0/tobs/')
def tobs():
    temp_obs = session.query(Measurement.tobs)\
    .order_by(Measurement.date).all()
    return jsonify(temp_obs)

#Start
@app.route('/api/v1.0/<start>/')
def combined_start_stats(start):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date >= start).all()                  

    for row in q:
        print()
        print(row)
    return jsonify(q)

# Start/End
@app.route('/api/v1.0/<start>/<end>/')
def combined_start_end_stats(start,end):
    q = session.query(Station.id,
                  Station.station,
                  func.min(Measurement.tobs),
                  func.max(Measurement.tobs),
                  func.avg(Measurement.tobs))\
                  .filter(Measurement.station == Station.station)\
                  .filter(Measurement.date <= end)\
                  .filter(Measurement.date >= start).all()
    
    for row in q:
        print()
        print(row)
    return jsonify(q)
    
# Running the App
if __name__ == "__main__":
    app.run(debug=True)

#################################################################
            #The End...
#################################################################