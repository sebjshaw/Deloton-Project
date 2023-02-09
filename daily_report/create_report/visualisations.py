import plotly.express as px
import pandas as pd

def create_line_graph(df: pd.DataFrame, x: str, y:str) -> px.line:
	"""
	Generate a line graph from a dataframe

	Args:
			df (pd.DataFrame): dataframe containing columns to be plotted
			x (str): string of column name
			y (str): string of column name
			units (str): the units to go on the axis

	Returns:
			px.line: line graph plotting x and y
	"""
	y_title = y.replace("_"," ").capitalize()
	x_title = x.replace("_"," ").capitalize()
	title = "Total Rides across the last 7 days"

	fig = px.line(df, x, y, title=title).update_layout(paper_bgcolor="#333333", plot_bgcolor='#333333')

	fig.update_xaxes(title = x_title, title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_xaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3)
	fig.update_yaxes(title=y_title, title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_yaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3)
	fig.update_layout(
    legend=dict(
        font=dict(
            color="red"
        )
    ), 
		title={
        'x':0.5,
        'xanchor': 'center',
		},
		title_font_size=22,
		font_color='#fefee2'
	)

	return fig

def create_grouped_bar_graph(df:pd.DataFrame, x:str, y:str, group:str, title: str, units:str) -> px.bar:
	"""
	Create a bar graph visualisation for the dataframe passed in the function

	Args:
			df (pd.DataFrame): df containing the data
			x (str): variable to be plotted on x
			y (str): variable to be plotted in y
			group (str): group by column
			title (str): graph title
			units (str): the units to be displayed on the y axis

	Returns:
			px.bar: bar graph
	"""
	y_title = y.replace("_"," ").capitalize()
	x_title = x.replace("_"," ").capitalize()

	fig = px.bar(df, x, y, color=group, barmode='group', text_auto='.0f', title=title).update_layout(paper_bgcolor="#333333", plot_bgcolor='#333333')

	fig.update_xaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_xaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3, title=x_title)
	fig.update_yaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_yaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3, title=f"{y_title} / {units}")
	fig.update_layout(
    legend=dict(
        font=dict(
            color="#fefee2"
        )
    ),
		title={
        'x':0.5,
        'xanchor': 'center',
		},
		title_font_size=22,
		font_color='#fefee2'
	)
	return fig
