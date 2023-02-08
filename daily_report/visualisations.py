import plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

def create_line_graph(df: pd.DataFrame, x: str, y:str) -> px.line:
	"""
	Generate a line graph from a dataframe

	Args:
			df (pd.DataFrame): dataframe containing columns to be plotted
			x (str): string of column name
			y (str): string of column name

	Returns:
			px.line: line graph plotting x and y
	"""
	fig = px.line(df, x, y).update_layout(paper_bgcolor="#333333", plot_bgcolor='#333333')

	fig.update_xaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_xaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3)
	fig.update_yaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_yaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3)
	fig.update_layout(
    legend=dict(
        font=dict(
            color="red"
        )
    )
	)
	
	return fig

def create_grouped_bar_graph(df:pd.DataFrame, x:str, y:str, group:str, title: str) -> px.bar:
	"""
	Create a bar graph visualisation for the dataframe passed in the function

	Args:
			df (pd.DataFrame): df containing the data
			x (str): variable to be plotted on x
			y (str): variable to be plotted in y
			group (str): group by column
			title (str): graph title

	Returns:
			px.bar: bar graph
	"""
	fig = px.bar(df, x, y, color=group, barmode='group', text_auto='.0f', title=title).update_layout(paper_bgcolor="#333333", plot_bgcolor='#333333')

	fig.update_xaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_xaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3)
	fig.update_yaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_yaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3)
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
