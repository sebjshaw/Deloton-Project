from SQLConnection import SQLConnection
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import dotenv
from datetime import datetime

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8080"],  supports_credentials=True)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB_NAME')

# Creating connection to hosted postgres db
sql = SQLConnection(USERNAME, PASSWORD, HOST, PORT, DB_NAME)

# Converting the tuple to dicts to be sent as JSON in responses
def tuple_to_dict(tup:tuple, table:str) -> dict:
	"""
	Convert the tuple for a row of table data into a dictionary
	Args:
			tup (tuple): tuple containing all data points from a specific row
			table (str): name of table from which the row data has been taken,
						must be exactly identical
	Returns:
			dict: dictionary containing the row data
	"""
	# All columns from each of the tables
	table_columns = {
		'rides' : [
			'user_id','ride_id','date','time_started','time_ended','total_duration','max_resistance',
			'max_heart_rate','max_rpm','max_power','average_resistance','average_heart_rate','average_rpm',
			'average_power'
		],
		'users': [
			'user_id','first_name','last_name','gender','address','date_of_birth','email_address','height_cm',
			'weight_kg','account_create_date','bike_serial','original_source'
		]
	}
	row_dict = {}
	keys = table_columns[table]
	for idx, title in enumerate(keys):
		row_dict[title] = tup[idx]
	return row_dict

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
		if ride_info_tuple:
			ride_info = tuple_to_dict(ride_info_tuple, 'rides')
			return jsonify(ride_info)
		else:
			return jsonify({"output": 'No matching records'})
	except Exception as e:
		return jsonify({'error':e})

# # GET /rider/:user_id
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
		if user_info_tuple:
			user_info = tuple_to_dict(user_info_tuple, 'users')
			return jsonify(user_info)
		else:
			return jsonify({"output": 'No matching records'})
	except Exception as e:
		return jsonify({'error':e})

# # GET /rider/:user_id/rides
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
		if user_ride_info_tuple:
			user_ride_info = [tuple_to_dict(entry, 'rides') for entry in user_ride_info_tuple]
			return jsonify(user_ride_info)
		else:
			return jsonify({"output": 'No matching records'})
	except Exception as e:
		return jsonify({'error':e})

# # DELETE /ride/:id
# Delete a ride with a specific ID
@app.route("/ride/<int:ride_id>", methods=["DELETE"])
def delete_ride_info(ride_id:int):
	try:
		sql.get_list(
			f"""
				DELETE FROM rides
				WHERE ride_id = {ride_id}
			"""
		)
		return jsonify({'success': f"Ride ID {ride_id} deleted"})
	except Exception as e:
		return jsonify({'error':e})

# # GET /daily?date=01-01-2020
# Get all rides for a specific date
# If no date has been specified, return all rides from the last 24 hours
@app.route("/daily", methods=["GET"])
def get_ride_info_for_specific_day():
	try:
		date = request.args.get('date')
		if date:
			day = int(date[:2])
			month = int(date[3:5])
			year = int(date[6:])
			date = datetime(year=year, month=month, day=day).strftime("%Y-%m-%d")
			days_rides = sql.get_list(
				f"""
					SELECT *
					FROM rides
					WHERE TO_DATE(date, 'YYYY-MM-DD') = TO_DATE('{date}', 'YYYY-MM-DD')
				"""
			)
			if days_rides:
				days_rides_info = [tuple_to_dict(entry, 'rides') for entry in days_rides]
				return jsonify(days_rides_info)
			else:
				return jsonify({"output": 'No matching records'})
		else:
			last_24_hours_rides = sql.get_list(
				f"""
					SELECT *
					FROM rides
					WHERE CAST(CONCAT(date,' ',time_started) AS TIMESTAMP) > now() - INTERVAL '1 day' 
				"""
			)
			if last_24_hours_rides:
				rides = [tuple_to_dict(entry, 'rides') for entry in last_24_hours_rides]
				return jsonify(rides)
			else:
				return jsonify({"output": 'No matching records'})
	except Exception as e:
		return jsonify({'error': str(e)})
