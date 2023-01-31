from dash import html, dcc, Input,Output

recent_layout = html.Div(
	children=[
		html.Div(
			children = [
				html.Div(
					dcc.Link(
						children = html.Button(
							id="view_switch",
							children='RECENT'
						),
						href='/'
					),
					id="icon"
				),
				html.Div(id='rider_info')
			],
			id='header'
		),
		html.Div(
			children=[
				html.Div(
					children = [	
						dcc.Interval(
							id='interval_component',
							interval=1*1000, # in milliseconds
							n_intervals=0
						),
						html.Div(
							children = [
								html.Div(
									html.H2('00:00:00',id='time_text'),
									id='time'
								),
								html.Div(
									html.H2('BPM',id='heart_rate_text'),
									id='heart_rate'
								),
								html.Div(
									html.H2("RPM", id="rpm_text"),
									id="time"
								),
								html.Div(
									html.H2('30',id='resistance_text'),
									id='resistance'
								),
							]
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
	],
	id='page'
)