from dash import html, dcc, Input, Output
import visualisations
from app import app
from views import current_view, recent_view
from datetime import datetime

app.layout = html.Div(
	children = [
		dcc.Location(
			id='url',
			refresh=False,
		),
		dcc.Interval(
			id='interval_component',
			interval=1*1000, # in milliseconds
			n_intervals=0
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

@app.callback(
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

# Update page label button
@app.callback(
	Output(
		'view_switch', 'children'
	),
	Output(
		'page_link', 'href'
	),
	[
		Input(
			'view_switch', 'n_clicks'
		)
	]
)
def change_link(n):
	print(n)
	if n % 2 == 0:
		return 'CURRENT', '/recent'
	else:
		return 'RECENT', '/'

# Update user info at the start of a new ride
# @app.callback(
# 	Output(
# 		'name', 'children'
# 	),
# 	Output(
# 		'age', 'children',
# 	),
# 	Output(
# 		'gender', 'children',
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_user_info(n):

# 	pass

#Update current time
@app.callback(
	Output(
		"current_date",'children'
	),
	Output(
		"current_time",'children'
	),
	[
		Input(
			'interval_component', 'n_intervals'
		)
	]
)
def update_current_time(n):
	return datetime.now().strftime("%d/%m/%Y"),datetime.now().strftime("%H:%M")
