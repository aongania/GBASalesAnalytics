from dash import html, dcc, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from pages import home, resultados, financeiro, comercial
from app import app

# import from folders/theme changer
from dash_bootstrap_templates import ThemeSwitchAIO

# Validate layouts
app.validation_layout = html.Div([
    home.layout,
    resultados.layout,
    financeiro.layout,
    comercial.layout
])

app.layout = home.layout



if __name__ == "__main__":
    app.run(debug=False)
    #app.run_server(host="0.0.0.0", port="8080", debug=True)
