from dash import Input, Output, callback, html, dcc
from visualisations import create_visualisation
from SQLConnection import SQLConnection
from datetime import datetime

# SQL connection variable
# sql = SQLConnection('./ec2-dash/dash.db')

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

# # Update user info at the start of a new ride
# @callback(
# 	Output(
# 		'name', 'children'
# 	),
# 	Output(
# 		'age', 'children',
# 	),
# 	Output(
# 		'gender', 'children',
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_user_info(n):
# 	pass

# # # Call backs for updating the components once a second
# # RPM figure
# @callback(
# 	Output(
# 		"rpm_graph",'figure'
# 	),
# 	Output(
# 		"rpm_text",'children'
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_rpm_figure(n):
# 	# df = sql.query("""
# 	# 		SELECT rpm FROM 
# 	# 	""")
# 	return create_visualisation(df, range(n+1), 'rpm')

# # Heart Rate figure
# @callback(
# 	Output(
# 		"heart_rate_graph",'figure'
# 	),
# 	Output(
# 		"heart_rate_text",'children'
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_heart_rate_figure(n):
# 	return visualisations.create_visualisation()

# @app.callback(
# 	Output(
# 		"power_graph",'figure'
# 	),
# 	Output(
# 		"power_text",'children'
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_power_figure(n):
# 	return visualisations.create_visualisation()

# @app.callback(
# 	Output(
# 		"rpm_graph",'figure'
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_resistance(n):
# 	return visualisations.create_visualisation()