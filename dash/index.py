from dash import html, dcc, Input, Output
import visualisations
from app import app
from views import current_view, recent_view

from SQLConnection import SQLConnection

#SQL connection
sql = SQLConnection('ec2-dash/dash.db')

app.layout = html.Div(
	children = [
		dcc.Location(
			id='url',
			refresh=False,
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
								href='/recent'
							),
							id="icon"
						),
						html.Div(id='rider_info')
					],
					id='header'
				),
			],
			id='page_content'
		)
	]
)

page_references = {
	"/": current_view.current_layout,
	"/recent": recent_view.recent_layout
}

#Call backs for updating the components once a second
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



# @app.callback(
# 	Output(
# 		"rpm_graph",'figure'
# 	),
# 	Output(
# 		"rpm_text",'children'
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_rpm_figure(n):

# 	return visualisations.create_visualisation()

# @app.callback(
# 	Output(
# 		"heart_rate_graph",'figure'
# 	),
# 	Output(
# 		"heart_rate_text",'children'
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_heart_rate_figure(n):
# 	return visualisations.create_visualisation()

# @app.callback(
# 	Output(
# 		"power_graph",'figure'
# 	),
# 	Output(
# 		"power_text",'children'
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_power_figure(n):
# 	return visualisations.create_visualisation()

# @app.callback(
# 	Output(
# 		"rpm_graph",'figure'
# 	),
# 	[
# 		Input(
# 			'interval_component', 'n_intervals'
# 		)
# 	]
# )
# def update_resistance(n):
# 	return visualisations.create_visualisation()