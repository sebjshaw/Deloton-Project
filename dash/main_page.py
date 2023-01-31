from dash import html, dcc, Input, Output
import visualisations
from app import app

from SQLConnection import SQLConnection

#SQL connection
sql = SQLConnection('DB_NAME')

#Layout of the dashboard
current_layout = html.Div(
	children=[
		html.Div(
			children = [
				html.Div(id="icon"),
				html.Div(id='rider_info')
			],
			id='header'
		),
	],
	id='page'
)

#Call backs for updating the components once a second
@app.callback(
	[
		Output(
			"rpm_graph",'figure'
		),
		Output(
			"rpm_text",'children'
		),
	]
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_rpm_figure(n):

	return visualisations.create_visualisation()

@app.callback(
	[
		Output(
			"heart_rate_graph",'figure'
		),
		Output(
			"heart_rate_text",'children'
		),
	]
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_heart_rate_figure(n):
	return visualisations.create_visualisation()

@app.callback(
	[
		Output(
			"power_graph",'figure'
		),
		Output(
			"power_text",'children'
		),
	]
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_power_figure(n):
	return visualisations.create_visualisation()

@app.callback(
	Output(
		"rpm_graph",'figure'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_resistance(n):
	return visualisations.create_visualisation()