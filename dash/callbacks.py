from dash import Input, Output, callback
from visualisations import create_visualisation
from SQLConnection import SQLConnection
from datetime import datetime, timedelta

# SQL connection variable
sql = SQLConnection('./ec2-dash/dash_db.db')

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


# # Call backs for updating the components once a second
# RPM figure
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
	return create_visualisation(df, 'duration', 'rpm')

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
	return create_visualisation(df, 'duration', 'heart_rate')

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
	df = sql.get_df("""SELECT duration, ROUND(power, 3) as power FROM current_ride""")
	return create_visualisation(df, 'duration', 'power')

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