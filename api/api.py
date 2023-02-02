from SQLConnection import SQLConnection
from flask import Flask, current_app, request, jsonify, abort,json, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8080"],  supports_credentials=True)

# # GET /ride/:id
# Get a ride with a specific ID
@app.route("/ride/<int:ride_id>", methods=["GET"])
def get_ride_info(ride_id:int):
  return 

# # GET /rider/:user_id
# Get rider information (e.g. name, gender, age, avg. heart rate, number of rides)
@app.route("/rider/<int:user_id>", methods=["GET"])
def get_user_info(user_id:int):
  return 

# # GET /rider/:user_id/rides
# Get all rides for a rider with a specific ID
@app.route("/rider/<int:user_id>/rides", methods=["GET"])
def get_user_ride_info(user_id: int):
  return 

# # DELETE /ride/:id
# Delete a with a specific ID
@app.route("/ride/<int:ride_id>", methods=["DELETE"])
def delete_ride_info(user_id):
  return 

# # GET /daily
# Get all of the rides in the current day
@app.route("/daily", methods=["GET"])
def get_current_day_ride_info():
  return 

# # GET /daily?date=01-01-2020
# Get all rides for a specific date
@app.route("/daily", methods=["GET"])
def get_ride_info_for_specific_day():
	date = request.args.get('date')
	return 
