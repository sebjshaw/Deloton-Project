from dash import html, dcc, Input, Output

current_layout = html.Div(
	children=[
		html.Div(
			children = [
				html.Div(
					dcc.Link(
						children = html.Button(
							id="view_switch",
							children='CURRENT'
						),
						href='/recent'
					),
					id="icon"
				),
				html.Div(id='rider_info')
			],
			id='header'
		),
		html.Div(
			children = [
				html.Div(
					children = [	
						html.Div(
							children = [
								dcc.Graph(id='rpm_graph'),
								dcc.Interval(
									id='interval_component',
									interval=1*1000, # in milliseconds
									n_intervals=0
								),
								html.Div(
									html.H2('32RPM',id='rpm_text')
								)
							],
							id='rpm'
						),
						html.Div(
							children = [	
								html.Div(
									html.H2('00:00:00',id='time_text'),
									id='time'
								),
								html.Div(
									html.H2('30',id='resistance_text'),
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