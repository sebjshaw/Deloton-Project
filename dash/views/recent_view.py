from dash import html, dcc

recent_layout = html.Div(
	children=[
		html.Div(
			children = [
				html.Div(
					children = [
						html.Div(
							children = [
								html.Div(
									html.H2('TIME',id='time_text'),
								),
								html.H2('00:00:00',id='time_value')
							],
							id="time",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('HEART RATE',id='heart_rate_text'),
								),
								html.H2('BPM',id='heart_rate_value')
							],
							id="heart_rate",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('REVOLUTION',id='rpm_text'),
								),
								html.H2('RPM',id='rpm_value')
							],
							id="rpm",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('RESISTANCE',id='resistance_text'),
								),
								html.H2('RES',id='resistance_value')
							],
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
