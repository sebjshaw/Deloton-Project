import plotly
import plotly.express as px
import pandas as pd

def create_visualisation(df: pd.DataFrame, x: str, y:str) -> px.line:
	"""
	Generate a line graph from a dataframe

	Args:
			df (pd.DataFrame): dataframe containing columns to be plotted
			x (str): string of column name
			y (str): string of column name

	Returns:
			px.line: line graph plotting x and y
	"""
	fig = px.line(df, x, y).update_layout(paper_bgcolor="#0d1f22", plot_bgcolor='#0d1f22')
	fig.update_xaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_xaxes(gridcolor='#8d5b4c', zerolinecolor='#8d5b4c', zerolinewidth=3)
	fig.update_yaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_yaxes(gridcolor='#8d5b4c', zerolinecolor='#8d5b4c', zerolinewidth=3)
	return fig

