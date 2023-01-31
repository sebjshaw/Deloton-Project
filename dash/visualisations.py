import plotly
import plotly.express as px
import pandas as pd

def create_visualisation(df: pd.DataFrame, x: str, y:str) -> px.line:
	"""
	Generate a line graph from a dataframe

	Args:
			df (pd.DataFrame): _description_
			x (str): _description_
			y (str): _description_

	Returns:
			px.line: _description_
	"""