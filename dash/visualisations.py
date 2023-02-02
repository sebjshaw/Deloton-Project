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
	cols = df.columns.tolist()
	fig = px.line(df, x, y).update_layout(paper_bgcolor="#0d1f22", plot_bgcolor='#0d1f22')

	fig.update_xaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_xaxes(gridcolor='#8d5b4c', zerolinecolor='#8d5b4c', zerolinewidth=3)
	fig.update_yaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'))
	fig.update_yaxes(gridcolor='#8d5b4c', zerolinecolor='#8d5b4c', zerolinewidth=3)

	if "heart_rate" in df.columns.tolist():
		max_hr = sql.get_list("SELECT max_hr FROM user_info")[0][0]
		x_values = df.duration.tolist()
		y_values = [max_hr]*len(x_values)
		fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', line_color="red", name='Max')) # Add line for max heart rate
	return fig

