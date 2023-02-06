from SQLConnection import SQLConnection
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import dotenv
from datetime import datetime

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:8090"],  supports_credentials=True)

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
	
def delete_ride_by_id(path: list) -> dict:
	"""
		DELETE /ride/:id\n
		Delete a ride with a specific ID
	"""
	ride_id = path[-2]
	try:
			sql.get_list(
				f"""
					DELETE FROM rides
					WHERE ride_id = {ride_id}
				"""
			)
			return {'success': f"Ride ID {ride_id} deleted"}
	except Exception as e:
		return {'error':str(e)}

def lambda_handler(event,context):
	path = event['rawPath'].split('/')
	return jsonify(delete_ride_by_id(path))