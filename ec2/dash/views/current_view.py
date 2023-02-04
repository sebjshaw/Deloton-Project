from dash import html, dcc

current_layout = html.Div(
	children = [
		html.Div(
			children = [	
				html.Div(
					children = [
						dcc.Graph(id='rpm_graph'),
					],
					id='rpm_graph'
				),
				html.Div(
					children =[
						html.Div(
							children = [	
								html.Div(
									children = [
										html.H2('RPM',id='rpm_text', className='bit_title'),
										html.H2(id='rpm_value'),
									],
									id='rpm',
									className='bit'
								),
								html.Div(
									children = [
										html.H2('RESISTANCE',id='resistance_text', className='bit_title'),
										html.H2('',id='resistance_value')
									],
									id='resistance',
									className='bit'
								)
							],
							className="time_resistance"
						),
						html.Div(
							children = [	
								html.Div(
									children = [
										html.H2('DURATION',id='time_text', className='bit_title'),
										html.H2(id='time_value')
									],
									id='time',
									className='bit'
								),
								html.Div(
									children = [
										html.H2('HEART RATE',id='heart_rate_text', className='bit_title'),
										html.H2(id='heart_rate_value'),
									],
									id='heart_rate',
									className='bit'
								)
							],
							className="time_resistance"
						),
					],
					id='current_values'
				)
			],
			id='upper_body'
		),
		html.Div(
			children = [
				html.Div(
					children = [
						dcc.Graph(id="power_graph"),
						html.Div(
							html.H2(id="power_text")
						)
					],
					id="power"
				),
				html.Div(
					children = [
						dcc.Graph(id="heart_rate_graph"),
						html.Div(
							html.H2(id="heart_rate_text")
						)
					],
					id="heart_rate"
				)
			],
			id='lower_body'
		)
	],
	id='body'
)