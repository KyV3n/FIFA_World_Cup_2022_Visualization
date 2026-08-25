from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from navbar import create_navbar

APP_TITLE = "FIFA World Cup 2022 Visualization"
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"       # font URL

NAVBAR = create_navbar()

# Initializing the application.
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.LUX,     # Dash Themes CSS
        FA621,              # Font Awesome Icons CSS
    ],
    title=APP_TITLE,
    use_pages=True,         # New in Dash 2.7 - Allows us to register pages
)

# Defining the app layout.
app.layout = html.Div([NAVBAR, page_container])

server = app.server

if __name__ == '__main__':
    app.run(debug=True)