from SQLConnection import SQLConnection
from flask import Flask, current_app, request, jsonify, abort,json, Response
from flask_cors import CORS
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8080"],  supports_credentials=True)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB_NAME')

sql = SQLConnection(USERNAME, PASSWORD, HOST, PORT, DB_NAME)

def rides_tuple_to_dict(ride_info:tuple) -> dict:
	return { 
		'user_id': ride_info[0],
		'ride_id': ride_info[1],
		'date': ride_info[2],
		'time_started': ride_info[3],
		'time_ended': ride_info[4],
		'total_duration': ride_info[5],
		'max_resistance':ride_info[6],
		'max_heart_rate': ride_info[7],
		'max_rpm': ride_info[8],
		'max_power': ride_info[9],
		'average_resistance': ride_info[10],
		'average_heart_rate': ride_info[11],
		'average_rpm': ride_info[12],
		'average_power': ride_info[13]
	}

# # GET /ride/:id
# Get a ride with a specific ID
@app.route("/ride/<int:ride_id>", methods=["GET"])
def get_ride_info(ride_id:int):
	ride_info_tuple = sql.get_list(
		f"""
			SELECT *
			FROM rides
			WHERE rides_id = {ride_id}
		""")[0]
	ride_info = rides_tuple_to_dict(ride_info_tuple)
	return jsonify(ride_info)

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
