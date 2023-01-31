from dash import Dash, html, dcc

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
								id='interval-component',
								interval=1*1000, # in milliseconds
								n_intervals=0
							),
							id='rpm'
						),
						html.Div(
							html.Div(id='time'),
							html.Div(id='resistance')
						)
					],
					id='upper_body'
				),
				html.Div(
					children=[

					],
					id='lower_body'
				)
			],
			id='body'
		),
	],
	id='page'
)