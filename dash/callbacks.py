from app import app
from dash import Input, Output, html, dcc
from visualisations import create_visualisation
from index import page_references


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
# 	return create_visualisation()

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