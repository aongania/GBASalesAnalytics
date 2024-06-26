import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# import from folders/theme changer
from dash_bootstrap_templates import ThemeSwitchAIO

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP, dbc_css])
server = app.server

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

#----------- Navbar ------------#

options_dashboard = []
for page in dash.page_registry.values():
    options_dashboard.append({'label': page['name'], 'value': page['path']})

sidebar = html.Div([
            html.Div([
                    html.H4("  Menu", style={"color": "white"}, className='dbc bi bi-list'),
                ], className="dbc sidebar-header"),
            html.Div([
                html.Img(src='assets/Logo-black.png', alt='image', style={'width': '100%', 'max-width': '200px'})
            ], className='dbc sidebar-logo'),
            html.Hr(className='dbc sidebar-hr'),
            html.Legend('Trocar o tema', style={'font-size': '0.8em'}, className='dbc sidebar-label'),
            html.Div([ThemeSwitchAIO(aio_id="themes", themes=[url_theme1, url_theme2])], className='dbc switch-theme'),
            html.Hr(className='dbc sidebar-hr'),
            dbc.Label('Dashboards', className='dbc sidebar-label text-decoration-bold'),
            dbc.Nav([
                dbc.NavLink([
                    html.Div(page['name'], className='dbc')
                ], href=page['path'], active="exact", className='dbc sidebar-label text-light')
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            )
        ], className="dbc sidebar bg-secondary text-white p-2 mb-2")

# navbar = html.Div([
#         html.Div([
#                 html.H4()
#             ]
#         ),
#         html.Hr(),
#         dbc.Nav(
#             [
#                 dbc.NavLink(
#                     [
#                         html.Div(page["name"], className="ms-2"),
#                     ],
#                     href=page["path"],
#                     active="exact",
#                     className='navbar-linnks'
#                 )
#                 for page in dash.page_registry.values()
#             ],
#             vertical=False,
#             pills=True,
#             className="bg-light fixed-top",
#             style={'justify-content': 'right'}
#         ),
#         ],
#     className="navbar",
#     style={'padding-bottom': '0px', 'padding-top': '10px', 'padding-right': '10px'}
# )

app.layout = html.Div([
    sidebar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4(id='actual_page', className='bdc')
            ])
        ], className='page-title dbc bg-secondary text-white p-2 text-center fixed-top'),
        dbc.Row([
            dbc.Col(
                [
                    dash.page_container,
                    dcc.Location(id='url')
                ])
        ])
    ], fluid=True, className='dbc bg-secondary', style={'margin-top': '47px'})
], className='dbc dbc-ag-grid')

#========== Callbacks ===========#
@app.callback(
    Output('actual_page', 'children'),
    Input('url', 'href')
)
def change_page(href):
    #print('EJECUTANDO CHANGE PAGE')  
    title = f"Dashboard {href.split('/')[3]}"
    if title == 'Dashboard ':
        title = 'Dashboard Resultados'
    return title

@callback(
    Input(ThemeSwitchAIO.ids.switch('themes'), 'value')
)
def change_theme(toggle):
    template = template_theme1 if toggle else template_theme2 # Changes theme
    load_figure_template(template)

if __name__ == "__main__":
    app.run(debug=False)
    #app.run_server(host="0.0.0.0", port="8080")
