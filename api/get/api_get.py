from SQLConnection import SQLConnection
import json
import os
import dotenv
from datetime import datetime

dotenv.load_dotenv()

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
		row_dict[title] = str(tup[idx])
	return row_dict

def get_ride_by_id(path:list) -> dict:
	"""
	GET /ride/:id\n
	Get a ride with a specific ID
	"""
	ride_id = path[-1]
	try:
		ride_info_tuple = sql.get_list(
			f"""
				SELECT *
				FROM rides
				WHERE ride_id = {ride_id}
			"""
		)[0]
		print(ride_info)
		if ride_info_tuple:
			ride_info = tuple_to_dict(ride_info_tuple, 'rides')
			return ride_info
		else:
			return {"output": 'No matching records'}
	except Exception as e:
		return {'error':str(e)}

def get_user_info(path: list) -> dict:
	user_id = path[-1]
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
			return user_info
		else:
			return {"output": 'No matching records'}
	except Exception as e:
		return {'error':str(e)}

def get_user_ride_info(path: list) -> dict:
	"""
		GET /rider/:user_id/rides\n
		Get all rides for a rider with a specific ID
	"""
	user_id = path[-2]
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
			return user_ride_info
		else:
			return {"output": 'No matching records'}
	except Exception as e:
		return {'error':str(e)}

def get_ride_info_for_specific_day(path:list) -> dict:
	"""
		GET /daily?date=01-01-2020\n
		Get all rides for a specific date\n
		If no date has been specified, return all rides from the last 24 hours
	"""
	date = path['rawQueryString']
	try:
		if 'date' in date:
			date = date.split('=')[-1]
			day = int(date[:2])
			month = int(date[3:5])
			year = int(date[6:8])
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
				return days_rides_info
			else:
				return {"output": 'No matching records'}
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
				return rides
			else:
				return {"output": 'No matching records'}
	except Exception as e:
		return {'error': str(e)}

def lambda_handler(event, context):
	path = event['rawPath'].split('/')
	if path[1] == 'ride':
		print(path)
		return json.dumps(get_ride_by_id(path))
	elif path[1] == 'rider' and path[-1] != 'rides':
		print(path)
		return json.dumps(get_user_info(path))
	elif path[1] == 'rider':
		print(path)
		return json.dumps(get_user_ride_info(path))
	elif path[1] == 'daily':
		print(path)
		return json.dumps(get_user_ride_info(path))