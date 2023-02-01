from app import app
from dash import Input, Output, html, dcc
from visualisations import create_visualisation
from index import page_references
from SQLConnection import SQLConnection

# SQL connection variable
# sql = SQLConnection('./ec2-dash/dash.db')

# Call backs for updating the components once a second
@app.callback(
	Output(
		"rpm_graph",'figure'
	),
	Output(
		"rpm_text",'children'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_rpm_figure(n):
	# df = sql.query("""
	# 		SELECT rpm FROM 
	# 	""")
	return create_visualisation(df, range(n+1), 'rpm')

# @app.callback(
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