from dash import Input, Output, callback
from visualisations import create_line_graph, create_grouped_bar_graph
from SQLConnection import SQLConnection
from PGConnection import SQLConnection as postgres
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB_NAME')

# SQL connection variable
sql = SQLConnection('./ec2/ingestion/dash_db.db')
pg = postgres(USERNAME, PASSWORD, HOST, PORT, DB_NAME)

# Update current time
@callback(
	Output(
		"current_date",'children'
	),
	Output(
		"current_time",'children'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_current_time(n):
	return datetime.now().strftime("%d/%m/%Y"),datetime.now().strftime("%H:%M")

# Update page label button
@callback(
	Output(
		'view_switch', 'children'
	),
	Output(
		'page_link', 'href'
	),
	[
		Input(
			'view_switch', 'n_clicks'
		)
	]
)
def change_link(n):
	print(n)
	if n % 2 == 0:
		return 'CURRENT', '/recent'
	else:
		return 'RECENT', '/'

# Update user info at the start of a new ride
@callback(
	Output(
		'name', 'children'
	),
	Output(
		'age', 'children',
	),
	Output(
		'gender', 'children',
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_user_info(n):
	info = sql.get_list(
		"""
			SELECT name, date_of_birth, gender
			FROM user_info
		"""
	)
	name = info[0][0]
	dob = info[0][1]
	age = 'AGE: ' + str(int(calculate_age(dob)))
	gender = info[0][2]
	return name, age, gender

def calculate_age(dob:str) -> int:
	"""
	Convert DOB to age

	Args:
			dob (str): date of birth as a string (YYYY/MM/DD)

	Returns:
			int: current age
	"""
	year=int(dob[:4])
	month=int(dob[5:7])
	day=int(dob[8:10])
	return (datetime.now() - datetime(year=year, month=month, day=day)).total_seconds()//31536000


# # # Call backs for updating the components once a second
# # VALUES
# RPM
@callback(
	Output(
		"rpm_value",'children'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_rpm_value(n):
	value = sql.get_list("""SELECT rpm FROM current_ride""")[-1][0]
	return value
# HEART RATE
@callback(
	Output(
		"heart_rate_value",'children'
	),
	Output(
		"heart_rate_value",'style'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_heart_rate_value(n):
	value = sql.get_list("""SELECT heart_rate FROM current_ride""")[-1][0]
	max = sql.get_list("""SELECT max_hr from user_info""")[-1][0]
	if 0.9 * int(max) < int(value) < 0.95 * int(max):
		return value, {'color': '#ffe700'}
	elif 0.95 * int(max) < int(value) <  int(max):
		return value, {'color': '#ff6700'}
	elif int(value) >= int(max):
		return value, {'color': '#ff0018'}
	else:
		return value, {}

# POWER
@callback(
	Output(
		"power_value",'children'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_power_value(n):
	value = sql.get_list("""SELECT power FROM current_ride""")[-1][0]
	return value
# RESISTANCE
@callback(
	Output(
		"resistance_value",'children'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_resistance_value(n):
	value = sql.get_list("""SELECT resistance FROM current_ride""")[-1][0]
	return value
# TIME
@callback(
	Output(
		"time_value",'children'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_resistance(n):
	duration = int(sql.get_list("""SELECT duration from current_ride""")[-1][0])
	return str(timedelta(seconds=duration))[2:]


# # CURRENT RIDES FIGURES
# RPM
@callback(
	Output(
		"rpm_graph",'figure'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_rpm_figure(n):
	df = sql.get_df("""SELECT duration, rpm FROM current_ride""")
	return create_line_graph(df, 'duration', 'rpm', 'RPM')
# HEART RATE
@callback(
	Output(
		"heart_rate_graph",'figure'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_heart_rate_figure(n):
	df = sql.get_df("""SELECT duration, heart_rate FROM current_ride""")
	return create_line_graph(df, 'duration', 'heart_rate', 'Heart Rate')
# POWER
@callback(
	Output(
		"power_graph",'figure'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_power_figure(n):
	df = sql.get_df(
		"""
			SELECT duration, ROUND(power, 0) AS power FROM current_ride
		"""
	)
	# INTERESTING
	# Raw power graph is correlated with the rpm
	# Moving average power graph looks correlated with the hr 
	return create_line_graph(df, 'duration', 'power', 'Power')


# # RECENT RIDES FIGURES
# AVERAGE RIDE LENGTH
@callback(
	Output(
		"gender_age_avg_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_avg_ride_length_by_gender_and_age(n):
	df = pg.get_df(
		"""
			SELECT 
				u.gender,
				CASE
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) < '18 years' THEN '<18'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '18 years' AND '24 years' THEN '18-24'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '25 years' AND '34 years' THEN '25-34'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '35 years' AND '44 years' THEN '35-44'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '45 years' AND '54 years' THEN '45-54'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '55 years' AND '64 years' THEN '55-64'
					ELSE '65+'
				END AS age_group,
				AVG(r.total_duration) AS average_duration
			FROM users u
				JOIN rides r
					USING(user_id)
			WHERE (date || ' ' || time_started)::timestamp >= (current_timestamp - interval '12 hours')::timestamp
			GROUP BY age_group, gender
			ORDER BY age_group;
		"""
	)
	return create_grouped_bar_graph(df, 'age_group', 'average_duration', 'gender', 'Average Ride Duration')
# TOTAL NUMBER OF RIDES
@callback(
	Output(
		"gender_age_total_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_total_rides_by_gender_and_age(n):
	df = pg.get_df(
		"""
			SELECT u.gender,
       CASE
         WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) < '18 years' THEN '<18'
         WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '18 years' AND '24 years' THEN '18-24'
         WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '25 years' AND '34 years' THEN '25-34'
         WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '35 years' AND '44 years' THEN '35-44'
         WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '45 years' AND '54 years' THEN '45-54'
         WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '55 years' AND '64 years' THEN '55-64'
         ELSE '65+'
       END AS age_group,
       COUNT(r.user_id) AS count
			FROM users u
				JOIN rides r
					USING(user_id)
			WHERE (date || ' ' || time_started)::timestamp >= (current_timestamp - interval '12 hours')::timestamp
			GROUP BY gender, age_group
			ORDER BY age_group;
		"""
	)
	return create_grouped_bar_graph(df, 'age_group', 'count', 'gender','Total No. of Rides')
# POWER
@callback(
	Output(
		"avg_power_age_gender_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_avg_power_by_age(n):
	df = pg.get_df(
		f"""
				SELECT 
					u.gender,
					CASE
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) < '18 years' THEN '<18'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '18 years' AND '24 years' THEN '18-24'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '25 years' AND '34 years' THEN '25-34'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '35 years' AND '44 years' THEN '35-44'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '45 years' AND '54 years' THEN '45-54'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '55 years' AND '64 years' THEN '55-64'
						ELSE '65+'
					END AS age_group,
					AVG(r.average_power*r.total_duration) AS average_power
				FROM users u
					JOIN rides r
						USING(user_id)
				WHERE (date || ' ' || time_started)::timestamp >= (current_timestamp - interval '12 hours')::timestamp
				GROUP BY gender, age_group
				ORDER BY age_group;
		"""
	)
	return create_grouped_bar_graph(df, 'age_group', 'average_power', 'gender', 'Average Power')

@callback(
	Output(
		"total_power_value",'children'
	),
	Output(
		"average_power_value",'children'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def total_average_power(n):
	power = pg.get_list(
	"""
		SELECT 
			ROUND(SUM(average_power*total_duration), 1),
			ROUND(AVG(average_power*total_duration), 1)
		FROM rides
		WHERE (date || ' ' || time_started)::timestamp >= (current_timestamp - interval '12 hours')::timestamp
	"""
	)[0]
	print(power)
	return power[0], power[1]