import plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from SQLConnection import SQLConnection

sql = SQLConnection('./ec2-dash/dash_db.db')

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

	if "heart_rate" in df.columns.to_list():
		max_hr = sql.get_list("SELECT max_hr FROM user_info")
		x_values = sql.get_df("SELECT duration FROM current_ride")

		fig.add_trace(go.Scatter(x=df.duration, y=max_hr, mode='lines', line_color="red")) # Add line for max heart rate
	return fig

