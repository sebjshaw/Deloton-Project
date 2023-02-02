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
									html.H2('⏱️',id='time_text', className='bit_title'),
								),
								html.H2('00:00:00',id='time_value')
							],
							id="time",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('🫀',id='heart_rate_text', className='bit_title'),
								),
								html.H2('BPM',id='heart_rate_value')
							],
							id="heart_rate",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('🔄',id='rpm_text', className='bit_title'),
								),
								html.H2('RPM',id='rpm_value')
							],
							id="rpm_recent",
							className='bit'
						),
						html.Div(
							children = [
								html.Div(
									html.H2('😤',id='resistance_text', className='bit_title'),
								),
								html.H2('RES',id='resistance_value')
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
							html.H2('gender',id="gender_text")
						),
						dcc.Graph(id="gender_share_graph"),
					],
					id="gender_share",
					className='shares'
				),
				html.Div(
					children = [
						html.Div(
							html.H2('age',id="age_text")
						),
						dcc.Graph(id="age_share_graph"),
					],
					id="age_share",
					className='shares'
				),
				html.Div(
					children = [
						html.Div(
							html.H2('power',id="power_text")
						),
						dcc.Graph(id="power_share_graph"),
					],
					id="power_share",
					className='shares'
				),
			],
			id='lower_recent_body'
		)
	],
	id="body"
)
