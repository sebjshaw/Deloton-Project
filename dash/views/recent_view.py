from dash import html, dcc, Input,Output
from app import app
from visualisations import create_visualisation

recent_layout = html.Div(
	children=[
		html.Div(
			children = [
				html.Div(
					children = [
						html.Div(
							html.H2('00:00:00',id='time_text'),
							id='time',
							className='bit'
						),
						html.Div(
							html.H2('BPM',id='heart_rate_text'),
							id='heart_rate',
							className='bit'
						),
						html.Div(
							html.H2("RPM", id="rpm_text"),
							id="time",
							className='bit'
						),
						html.Div(
							html.H2('30',id='resistance_text'),
							id='resistance',
							className='bit'
						),
					],
					id='bit_container'
				),
			],
			id='upper_recent_body'
		),
		html.Div(
			children = [
				html.Div(
					children = [
						html.Div(
							html.H2('gender',id="gender_text")
						),
						dcc.Graph(id="gender_graph"),
					],
					id="gender_share",
					className='shares'
				),
				html.Div(
					children = [
						html.Div(
							html.H2('age',id="age_text")
						),
						dcc.Graph(id="age_graph"),
					],
					id="age_share",
					className='shares'
				),
				html.Div(
					children = [
						html.Div(
							html.H2('power',id="power_text")
						),
						dcc.Graph(id="power_graph"),
					],
					id="power_share",
					className='shares'
				),
			],
			id='lower_recent_body'
		)
	],
	id="body"
)
