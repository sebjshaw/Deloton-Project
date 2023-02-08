from dash import html, dcc

recent_layout = html.Div(
	children=[
		html.Div(
			children = [
				html.Div(
					children = [
						html.Div(
							children = [
								html.Div(
									html.H2('DURATION',id='time_text', className='bit_title'),
								),
								html.H2('00:00:00',id='time_value')
							],
							id="time",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('HEART RATE',id='heart_rate_text', className='bit_title'),
								),
								html.H2('BPM',id='heart_rate_value')
							],
							id="heart_rate",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('Total Power',id='total_power_text', className='bit_title'),
								),
								html.H2('Watts',id='total_power_value')
							],
							id="rpm_recent",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('Average Power',id='avg_power_text', className='bit_title'),
								),
								html.H2('Watts',id='average_power_value')
							],
							id='resistance',
							className='bit'
						),
					],
					id='bit_container'
				),
			],
			id='upper_recent_body'
		),
		html.Div(
			children = [
				html.Div(
					children = [
						html.Div(
							children = [
								dcc.Graph(id="gender_age_avg_graph", className='recent_graph'),
							],
							className='demo_graphs'
						)
					],
					id="avg_ride_share",
					className='shares'
				),
				html.Div(
					children = [
						html.Div(
							children = [
								dcc.Graph(id="gender_age_total_graph", className='recent_graph'),
							],
							className='demo_graphs'
						),
					],
					id="total_ride_share",
					className='shares'
				),
				html.Div(
					children = [
						html.Div(
							children = [
								dcc.Graph(id="avg_power_age_gender_graph", className='recent_graph'),
							],
							className='demo_graphs'
						),
					],
					id="avg_power_share",
					className='shares'
				),
			],
			id='lower_recent_body'
		)
	],
	id="body"
)
