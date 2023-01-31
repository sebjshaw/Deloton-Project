from dash import Dash
import index

app = Dash(__name__)

if __name__ == "__main__":
	index.app.run_server(debug=True, port=8897)