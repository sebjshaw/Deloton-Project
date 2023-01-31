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
						href='/current'
					),
					id="icon"
				),
				html.Div(id='rider_info')
			],
			id='header'
		),
	],
	id='page'
)