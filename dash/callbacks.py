from dash import Input, Output, callback
from visualisations import create_line_graph, create_bar_graph
from SQLConnection import SQLConnection
from PGConnection import SQLConnection as postgres
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv("api/.env")

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB_NAME')

# SQL connection variable
sql = SQLConnection('./ec2-dash/dash_db.db')
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
	age = calculate_age(dob)
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
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_heart_rate_value(n):
	value = sql.get_list("""SELECT heart_rate FROM current_ride""")[-1][0]
	return value

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
	return create_line_graph(df, 'duration', 'rpm')

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
	return create_line_graph(df, 'duration', 'heart_rate')

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
			SELECT 
				duration,
				AVG(power) OVER (ORDER BY duration asc ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as 'moving avg. power'
			FROM current_ride
		"""
	)
	# INTERESTING
	# Raw power graph is correlated with the rpm
	# Moving average power graph looks correlated with the hr 
	return create_line_graph(df, 'duration', 'moving avg. power')

# # RECENT RIDES FIGURES
# GENDER
@callback(
	Output(
		"gender_avg_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_avg_ride_length_by_gender(n):
	df = pg.get_df(
		"""
			SELECT 
				DISTINCT(u.gender) as gender,
				AVG(total_duration) OVER (PARTITION BY u.gender) as 'average duration'
			FROM users U 
			JOIN rides r 
				USING(user_id)
		"""
	)
	return create_bar_graph(df, 'gender', 'average duration')

@callback(
	Output(
		"gender_total_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_total_rides_by_gender(n):
	df = pg.get_df(
		"""
			SELECT
				DISTINCT(u.gender) as gender,
				COUNT(u.user_id) OVER (PARTITION BY u.gender) as count
			FROM
				users u
			JOIN rides r
				USING(user_id)
		"""
	)
	return create_bar_graph(df, 'gender', 'count')


# AGE
@callback(
	Output(
		"age_avg_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_avg_ride_length_by_age(n):
	pass

@callback(
	Output(
		"age_total_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_total_rides_by_age(n):
	pass

# POWER
@callback(
	Output(
		"avg_power_age_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_avg_power_by_age(n):
	pass

@callback(
	Output(
		"avg_power_gender_graph",'figure'
	),
	[
		Input(
			'fifteen_minute_refresh', 'n_intervals'
		)
	]
)
def get_avg_power_by_gender(n):
	pass
