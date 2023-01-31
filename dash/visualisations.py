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
	return px.line(df, x, y)
