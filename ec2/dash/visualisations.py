import plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from SQLConnection import SQLConnection

sql = SQLConnection('./ec2/ingestion/dash_db.db')

def create_line_graph(df: pd.DataFrame, x: str, y:str, title:str) -> px.line:
	"""
	Generate a line graph from a dataframe

	Args:
			df (pd.DataFrame): dataframe containing columns to be plotted
			x (str): string of column name
			y (str): string of column name
			title (str): graph title

	Returns:
			px.line: line graph plotting x and y
	"""
	fig = px.line(df, x, y).update_layout(paper_bgcolor="#333333", plot_bgcolor='#333333', title=title)



	fig.update_xaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'), title=add_units(format_axes_labels(x)))
	fig.update_xaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3)
	fig.update_yaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'), title=format_axes_labels(y))
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

	if "heart_rate" in df.columns.tolist():
		max_hr = sql.get_list("SELECT max_hr FROM user_info")[0][0]
		x_values = df.duration.tolist()
		y_values = [max_hr]*len(x_values)
		fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines', line_color="red", name='Max')) # Add line for max heart rate
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

	fig.update_xaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'), title=format_axes_labels(x))
	fig.update_xaxes(gridcolor='#7fc37e', zerolinecolor='#7fc37e', zerolinewidth=3)
	fig.update_yaxes(title_font=dict(color='#f3dfc1'), tickfont=dict(color='#f3dfc1'), title=format_axes_labels(y))
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


def format_axes_labels(label: str) -> str:
	if '_' in label:
		label = label.split('_')
		new_label = []
		for word in label:
			word = word[0].upper()+word[1:]
			new_label.append(word)
		return " ".join(new_label)
	elif 'RPM' in label:
		return label.upper()
	else:
		return label[0].upper()+label[1:]

def add_units(label: str) -> str:
	if 'Power' in label:
		label += ' (W)'
	elif 'Duration' in label:
		label += ' (s)'
	return label
	