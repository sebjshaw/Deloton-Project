from dash import html, dcc, Input, Output, callback
from app import app
from views import current_view, recent_view

app.layout = html.Div(
	children = [
		html.Header(
			children=[
				dcc.Location(
					id='url',
					refresh=False,
				),
				dcc.Interval(
					id='interval_component',
					interval=1*1000, # in milliseconds
					n_intervals=0
				),
			],
		),
		html.Div(
			children=[
				html.Div(
					children = [
						html.Div(
							dcc.Link(
								children = html.Button(
									'CURRENT',
									id="view_switch",
									n_clicks=0
								),
								href='/recent',
								id='page_link'
							),
							id="icon"
						),
						html.Div(
							children = [
								html.Div(
									html.H1("SOMEONES NAME",
										className='info_div',
										id='name'
									)
								),
								html.Div(
									html.H2("AGE",
										className='info_div',
										id='age'
									)
								),
								html.Div(
									html.H2("GENDER",
										className='info_div',
										id='gender'
									)
								),
								html.Div(
									children = [
										html.Div(
											html.H2("",
												className='info_div',
												id='current_date'
											)
										),
										html.Div(
											html.H2("",
												className='info_div',
												id='current_time'
											)
										),
									],
									id='datetime'
								),
							],
							id='rider_info'
						)
					],
					id='header'
				),
				html.Div(
					id='page_content'
				)
			]
		)
	],
	id='page'
)

page_references = {
	"/": current_view.current_layout,
	"/recent": recent_view.recent_layout
}

@callback(
	Output(
			component_id='page_content',
			component_property='children',
			),
	[Input(
			component_id='url',
			component_property='pathname',
			)]
)
def display_page(pathname: str) -> html.Div:
	if pathname in list(page_references.keys()):
		print(pathname)
		return page_references[pathname]
	else:
			return '404'