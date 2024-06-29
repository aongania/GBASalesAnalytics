from dash import html, dcc, Input, Output, callback, no_update
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from pages import resultados, financeiro, comercial
from app import app

# import from folders/theme changer
from dash_bootstrap_templates import ThemeSwitchAIO

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

#----------- Navbar ------------#
pages_list = [{'name': 'Resultados', 'path': '/', 'disabled': False},
              {'name': 'Comercial', 'path': '/Comercial', 'disabled': True},
              {'name': 'Financeiro', 'path': '/Financeiro', 'disabled': True}]

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
                ], href=page['path'], active="exact", className='dbc sidebar-label text-light', disabled=page['disabled'])
                for page in pages_list
            ],
            vertical=True,
            pills=True,
            )
        ], className="dbc sidebar bg-secondary text-white p-2 mb-2")

layout = html.Div([
    sidebar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H4(id='home-actual-page', className='bdc home-actual-page')
            ], xs=12, md=6, className='bdc d-flex align-items-center'),
            dbc.Col([
                #html.Label(id='selected-filters', className='bdc w-100 pe-md-5 pe-xs-0 text-center text-md-end text-xs-1')
                html.Label(id='selected-filters', className='bdc selected-filters')
            ], xs=12, md=6, className='bdc d-flex align-items-center')
        ], className='page-title dbc bg-secondary text-white fixed-top'),
        dbc.Row([
            dbc.Col(
                [
                    html.Div(id='page-contents', children=[resultados.layout]),
                    dcc.Location(id='url', refresh=False)
                ])
        ])
    ], fluid=True, className='dbc bg-secondary', style={'margin-top': '47px'})
], className='dbc dbc-ag-grid')

#========== Callbacks ===========#
@app.callback(
    Output('home-actual-page', 'children'),
    Output('page-contents', 'children'),
    Input('url', 'pathname')
)
def change_page(pathname):
    #print('EJECUTANDO CHANGE PAGE')  
   
    if pathname == '/':
        page_contents = resultados.layout
        title = 'Dashboard Resultados'
    elif pathname == '/Financeiro':
        page_contents = financeiro.layout
        title = 'Dashboard Financeiro'
    elif pathname == '/Comercial':
        page_contents = comercial.layout
        title = 'Dashboard Comercial'
    else:
        page_contents = '404'
        title = 'Page Not Found'

    return title, page_contents

@callback(
        Output('selected-filters', 'children'),
        Input('url', 'pathname'),
        Input('month-range-slider', 'value'),
        Input('select-empresa', 'value'),
        Input('select-receita', 'value'),
)
def selected_filters(pathname, months, empresa, receita):
    # Selected Filters
    if pathname == '/':
        start_month = months[0]
        end_month = months[1]
        start_month_txt = resultados.month_to_text(start_month)
        end_month_txt = resultados.month_to_text(end_month)
        selected_filters = [
            html.Strong('Periodo: '),
            html.Span(f'{start_month_txt} a {end_month_txt}'),
            html.Strong('  |  Empresa: '),
            html.Span(empresa),
            html.Strong('  |  Receita: '),
            html.Span(receita)
        ]
    else:
        selected_filters = []
    
    return selected_filters

@app.callback(
    Input(ThemeSwitchAIO.ids.switch('themes'), 'value')
)
def change_theme(toggle):
    template = template_theme1 if toggle else template_theme2 # Changes theme
    load_figure_template(template)
