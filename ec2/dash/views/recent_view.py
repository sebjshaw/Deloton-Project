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
									html.H2('DURATION ⏱️',id='time_text', className='bit_title'),
								),
								html.H2('00:00:00',id='time_value')
							],
							id="time",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('HEART RATE ❤️',id='heart_rate_text', className='bit_title'),
								),
								html.H2('BPM',id='heart_rate_value')
							],
							id="heart_rate",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('RPM 🔄',id='rpm_text', className='bit_title'),
								),
								html.H2('RPM',id='rpm_value')
							],
							id="rpm_recent",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('RESISTANCE 😤',id='resistance_text', className='bit_title'),
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
						html.Div(
							children = [
								dcc.Graph(id="gender_total_graph", className='recent_graph'),
								dcc.Graph(id="gender_avg_graph", className='recent_graph'),
							],
							className='demo_graphs'
						)
					],
					id="gender_share",
					className='shares'
				),
				html.Div(
					children = [
						html.Div(
							html.H2('age',id="age_text")
						),
						html.Div(
							children = [
								dcc.Graph(id="age_total_graph", className='recent_graph'),
								dcc.Graph(id="age_avg_graph", className='recent_graph'),
							],
							className='demo_graphs'
						),
					],
					id="age_share",
					className='shares'
				),
				html.Div(
					children = [
						html.Div(
							html.H2('power',id="power_text")
						),
						html.Div(
							children = [
								dcc.Graph(id="avg_power_age_graph", className='recent_graph'),
								dcc.Graph(id="avg_power_gender_graph", className='recent_graph'),
							],
							className='demo_graphs'
						),
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
