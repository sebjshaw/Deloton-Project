from dash import Dash
import index
import callbacks

app = Dash(__name__, suppress_callback_exceptions=True)

if __name__ == "__main__":
	index.app.run_server(debug=True, port=8080)
