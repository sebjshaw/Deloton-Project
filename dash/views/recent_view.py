from dash import html, dcc, Input,Output

recent_layout = html.Div(
	children=[
		html.Div(
			children = [
				html.Div(
					html.Button(
						
					),
					id="icon"),
				html.Div(id='rider_info')
			],
			id='header'
		),
	],
	id='page'
)