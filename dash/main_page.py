from dash import html, dcc, Input, Output
import visualisations
from app import app

layout = html.Div(
	children=[
		html.Div(
			children = [
				html.Div(id="icon"),
				html.Div(id='rider_info')
			],
			id='header'
		),
		html.Div(
			children = [
				html.Div(
					children = [	
						html.Div(
							dcc.Graph(id='rpm_graph'),
							dcc.Interval(
								id='interval_component',
								interval=1*1000, # in milliseconds
								n_intervals=0
							),
							id='rpm'
						),
						html.Div(
							children = [	
								html.Div(
									html.H2(id='time_text'),
									id='time'
								),
								html.Div(
									html.H2(id='resistance_text'),
									id='resistance'
								)
							],
							id="time_resistance"
						)
					],
					id='upper_body'
				),
				html.Div(
					children = [
						html.Div(
							children = [
								dcc.Graph(id="power_graph"),
								html.Div(
									html.H2(id="power_text")
								)
							],
							id="power"
						),
						html.Div(
							children = [
								dcc.Graph(id="heart_rate_graph"),
								html.Div(
									html.H2(id="heart_rate_text")
								)
							],
							id="heart_rate"
						)
					],
					id='lower_body'
				)
			],
			id='body'
		),
	],
	id='page'
)

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