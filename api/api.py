from SQLConnection import SQLConnection
from flask import Flask, current_app, request, jsonify, abort,json, Response
from flask_cors import CORS
import os
import dotenv
from datetime import datetime, timedelta

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8090"],  supports_credentials=True)

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

def users_tuple_to_dict(user_info:tuple) -> dict:
	return { 
		'user_id':user_info[0],
		'first_name':user_info[1],
		'last_name':user_info[2],
		'gender':user_info[3],
		'address':user_info[4],
		'date_of_birth':user_info[5],
		'email_address':user_info[6],
		'height_cm':user_info[7],
		'weight_kg':user_info[8],
		'account_create_date':user_info[9],
		'bike_serial':user_info[10],
		'original_source':user_info[11]
	}



# # GET /ride/:id
# Get a ride with a specific ID
@app.route("/ride/<int:ride_id>", methods=["GET"])
def get_ride_info(ride_id:int):
	try:
		ride_info_tuple = sql.get_list(
			f"""
				SELECT *
				FROM rides
				WHERE rides_id = {ride_id}
			"""
		)[0]
	except Exception as e:
		return jsonify({'error':e})
	ride_info = rides_tuple_to_dict(ride_info_tuple)
	return jsonify(ride_info)

# # GET /rider/:user_id
# Get rider information (e.g. name, gender, age, avg. heart rate, number of rides)
@app.route("/rider/<int:user_id>", methods=["GET"])
def get_user_info(user_id:int):
	try:
		user_info_tuple = sql.get_list(
			f"""
				SELECT *
				FROM users
				WHERE user_id = {user_id}
			"""
		)[0]
	except Exception as e:
		return jsonify({'error':e})
	user_info = users_tuple_to_dict(user_info_tuple)
	return jsonify(user_info)

# # GET /rider/:user_id/rides
# Get all rides for a rider with a specific ID
@app.route("/rider/<int:user_id>/rides", methods=["GET"])
def get_user_ride_info(user_id: int):
	try:
		user_ride_info_tuple = sql.get_list(
			f"""
				SELECT *
				FROM rides
				WHERE user_id = {user_id}
			"""
		)
	except Exception as e:
		return jsonify({'error':e})
	user_ride_info = [rides_tuple_to_dict(entry) for entry in user_ride_info_tuple]
	return jsonify(user_ride_info)

# # DELETE /ride/:id
# Delete a with a specific ID
@app.route("/ride/<int:ride_id>", methods=["DELETE"])
def delete_ride_info(ride_id:int):
	try:
		sql.get_list(
			f"""
				DELETE FROM rides
				WHERE ride_id = {ride_id}
			"""
		)
	except Exception as e:
		return jsonify({'error':e})
	return jsonify({'success': f"Ride ID {ride_id} deleted"})

# # GET /daily
# Get all of the rides in the current day
@app.route("/daily", methods=["GET"])
def get_current_day_ride_info():
	try:
		day_before = datetime.now() - timedelta(day=1)
		last_24_hours_rides = (
			f"""
				SELECT *
				FROM rides
				WHERE (date + time) > {day_before} 
			"""
		)
	except Exception as e:
		return jsonify({'error': e})
	rides = [rides_tuple_to_dict(entry) for entry in last_24_hours_rides]
	return jsonify(rides)

# # GET /daily?date=01-01-2020
# Get all rides for a specific date
@app.route("/daily", methods=["GET"])
def get_ride_info_for_specific_day():
	try:
		date = request.args.get('date')
		day = int(date[:2])
		month = int(date[3:5])
		year = int(date[6:])
		date = datetime(year=year, month=month, day=day).strftime("%Y-%m-%d")
		days_rides = (
			f"""
				SELECT *
				FROM rides
				WHERE TO_DATE(date, YYYY-MM-DD) = TO_DATE({date}, YYYY-MM-DD)
			"""
		)
	except Exception as e:
		return jsonify({'error': e})
	days_rides_info = [rides_tuple_to_dict(entry) for entry in days_rides]
	return jsonify(days_rides_info)
