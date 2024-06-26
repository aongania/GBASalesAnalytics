from dash import html, dcc, Input, Output, State, ctx, callback, no_update
from dash.exceptions import PreventUpdate
import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import datetime
import os

# import from folders/theme changer
from dash_bootstrap_templates import ThemeSwitchAIO

# Regsiter page in dash registry
dash.register_page(__name__,
                   path='/Comercial',
                   name='Comercial',
                   title='Comercial',
                   image='meta_img.png',
                   description='Data Analitycs by GB Advisors')

# ========== Styles ============ #
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "closest",
    "legend": {'orientation': "h",
                "yanchor":"top", 
                "y":-0.8, 
                "xanchor":"center",
                "x":0.5,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.3)"},
    "margin": {"l":10, "r":10, "t":50, "b":10}
}

#config_graph={"displayModeBar": True, "showTips": False, "displaylogo": False}
config_graph={"showTips": False, "displayModeBar": False, "displaylogo": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY



# ========== Defining de NavBar ============ #

# sidebar = html.Div(
#     [
#         html.Div(
#             [
#                 html.H4(" Filters", style={"color": "white"}, className='bi bi-filter-circle-fill'),
#             ],
#             className="sidebar-header",
#         ),
#         html.Hr(),
        
#         ],
#         className="sidebar mb-2"
#     )

# =========  Layout  =========== #
layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            #sidebar
        ], style={'text-align': 'center'})
    ]),
    # Row 1
    dbc.Row([
        dbc.Col([
            'Comercial - Em Construção'
        ])
    ])
], style={'padding-top': '0px'}, className="dbc dbc-ag-grid")

