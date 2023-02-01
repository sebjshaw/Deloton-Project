from dash import html, dcc, Input, Output
from app import app
from visualisations import create_visualisation
from datetime import datetime

current_layout = html.Div(
	children = [
		html.Div(
			children = [	
				html.Div(
					children = [
						dcc.Graph(id='rpm_graph'),
						html.Div(
							html.H2('32RPM',id='rpm_text'),
							className='bit'
						)
					],
					id='rpm'
				),
				html.Div(
					children = [	
						html.Div(
							html.H2('00:00:00',id='time_text'),
							id='time',
							className='bit'
						),
						html.Div(
							html.H2('30',id='resistance_text'),
							id='resistance',
							className='bit'
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
)