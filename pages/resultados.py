from dash import html, dcc, Input, Output, State, ctx, callback, no_update
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import datetime
import pathlib
import os

from pages import home

# import from folders/theme changer
from dash_bootstrap_templates import ThemeSwitchAIO

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

# ========== Defining global variables ============ #
now = datetime.datetime.now() # get time of last update

# ========== Reading DATA ============ #
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.parent.joinpath("data").resolve()
data_file = DATA_PATH.joinpath('Vendas2023.xlsx')

df = pd.read_excel(data_file, sheet_name='Dados')
df_targets = pd.read_excel(data_file, sheet_name='Metas')
mod_time = os.path.getmtime(data_file)

# ========= Função dos Filtros ========= #
start_month = 1
end_month = 12

def df_filter(start_month, end_month, empresa, receita):
    #print(f'df_ filter: start_month es {start_month} y end_month es {end_month}')
    if empresa == 'Grupo':
        empresa = '.*'
    if receita == 'Total':
        receita = '.*'
    
    mask = df[df['Mês'].between(start_month, end_month) & df['Empresa'].str.contains(empresa) & df['Tipo Receita'].str.contains(receita)]
    return mask

def meta_filter(start_month, end_month, empresa):
    #print(f'meta_ filter: start_month es {start_month} y end_month es {end_month}')
    if empresa == 'Grupo':
        empresa = '.*'
    
    mask = df_targets[df_targets['Mês'].between(start_month, end_month) & df_targets['Empresa'].str.contains(empresa)]
    return mask

# ========== Criando opções pros filtros que virão ============ # 
def get_selects(df):
    options_month = [{'label': 'Full Year', 'value': 0}]
    for i, j in zip(['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'], sorted(df['Mês'].unique())):
        options_month.append({'label': i, 'value': j})
    
    options_empresas = [{'label': 'Grupo', 'value': 'Grupo'}]
    for i in df['Empresa'].unique():
        options_empresas.append({'label': i, 'value': i})
    
    options_receita = [{'label': 'Total', 'value': 'Total'}]
    for i in df['Tipo Receita'].unique():
        options_receita.append({'label': i, 'value': i})

    return options_month, options_empresas, options_receita

# ========== Months to text ===============#
def month_to_text(month_number):
    match month_number:
        case 1:
            month_text = 'Jan'
        case 2:
            month_text = 'Fev'
        case 3:
            month_text = 'Mar'
        case 4:
            month_text = 'Abr'
        case 5:
            month_text = 'Mai'
        case 6:
            month_text = 'Jun'
        case 7:
            month_text = 'Jul'
        case 8:
            month_text = 'Ago'
        case 9:
            month_text = 'Set'
        case 10:
            month_text = 'Out'
        case 11:
            month_text = 'Nov'
        case 12:
            month_text = 'Dez'

    return month_text
        

# ========== Defining de NavBar ============ #
options_month, options_empresa, options_receita = get_selects(df)

sidebar = html.Div(
    [
        html.Div(
            [
                html.H4(" Filters", className='bi bi-funnel'),
            ],
            className="dbc sidebar-page-header",
        ),
        html.Hr(className='dbc sidebar-page-hr'),
        html.Div([
            dbc.Label('Janela de tempo (Meses)', class_name='dbc sidebar-page-label'),
            dcc.RangeSlider(1, 12, 1, value=[1, 12], id='month-range-slider', className='dbc px-2 sidebar-range-slider'),
            dbc.Label('Empresa', class_name='sidebar-page-label dbc'),
            dbc.Select(
                id='select-empresa',
                options=options_empresa,
                value='Grupo',
                placeholder='Grupo',
                class_name='sidebar-select-control dbc'
            ),
            dbc.Label('Receita', class_name='sidebar-page-label dbc'),
            dbc.Select(
                id='select-receita',
                options=options_receita,
                value='Total',
                placeholder='Total',
                class_name='sidebar-select-control dbc'
            )
        ], className='bdc slider-selectors')
    ], className="dbc sidebar-page bg-secondary text-white p-2 mb-2")

# =========  Layout  =========== #
layout = html.Div(children=[
    html.Div(
        dcc.Store(id='mod-time')
    ),
    dbc.Row([
        dbc.Col([
            sidebar
        ], style={'text-align': 'center'})
    ]),
    # Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Img(id='logo-select', src='assets/Logo-white.png', alt='image', style={'width': '100%', 'max-width': '200px'})
                        ])
                    ], style={'margin-top': '0px'}),
                    dbc.Row([
                        dbc.Col([  
                            html.H4("Sales Analytics", className='bdc')
                        ], align='start')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div(id='time-updated',
                                    children= html.Label(f'Última atualização: {str(now.time())[:8]}'),
                                    className='dbc'),
                            dcc.Interval(
                                id='interval-component',
                                interval=10000,
                                n_intervals=0
                            )
                        ], align='center', width=12, style={'text-align': 'center', 'margin-top': '30px'})
                    ], justify='center', style={'margin-top': '0px'})
                ])
            ], style=tab_card)
        ], sm=12, md=4, lg=2, style={'text-align': 'center'}),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Loading([
                                dcc.Graph(id='graph1', className='dbc', config=config_graph)
                            ], delay_hide=500)
                        ], xs=12, sm=4, md=4, lg=4),
                        dbc.Col([
                            dcc.Loading([
                                dcc.Graph(id='graph2', className='dbc', config=config_graph)
                            ], delay_hide=500)
                        ], xs=12, sm=4, md=4, lg=4),
                        dbc.Col([
                            dcc.Loading([
                                dcc.Graph(id='graph3', className='dbc', config=config_graph)
                            ], delay_hide=500)
                        ], xs=12, sm=4, md=4, lg=4)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, md=8, lg=8),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4('Total Receita', style={'text-align': 'center'}, className='bdc'),
                            html.Div(id='receita-total', className='dbc')
                        ], class_name='col-md-12')
                    ], class_name='row align-items-center border-start border-primary border-4', style={'height': '100%', 'text-align': 'center'})
                ])
            ], style={'height': '100%'})
        ], sm=12, md=12, lg=2)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading([
                        dcc.Graph(id='graph4', className='dbc', config=config_graph)
                    ], delay_hide=500)
                ])
            ], style=tab_card)
        ], sm=12, md=6, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading([
                        dcc.Graph(id='graph5', className='dbc', config=config_graph)
                    ], delay_hide=500)
                ])
            ], style=tab_card)
        ], sm=12, md=6, lg=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4('Meta', style={'text-align': 'center'}, className='dbc'),
                            html.Div(id='meta-total', style={'text-align': 'center', 'margin-top': '10px'}, className='dbc')
                        ])
                    ], class_name='border-start border-primary border-4')
                ], style={'text-align': 'center'})
            ], style={'height': '49%'}),
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4('Delta', style={'text-align': 'center'}, className='dbc'),
                            html.Div(id='delta-total', style={'text-align': 'center', 'margin-top': '10px'}, className='dbc')  
                        ])
                    ], class_name='border-start border-primary border-4')
                ], style={'text-align': 'center'})
            ], style={'height': '49%', 'margin-top': '2%'})
        ], sm=12, md=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4('Top 5 Clientes', className='dbc'),
                            dag.AgGrid(id='customer-table',
                                columnSize="responsiveSizeToFit",
                                columnDefs = [{'field': 'Grupo',
                                            'columnStyle': {'justify-content': 'center'}},
                                            {'field': 'Faturamento',
                                            'columnStyle': {'justify-content': 'center'},
                                            'valueFormatter': {'function': "'R$' + (params.value ? Number(params.value/1000000).toFixed(2) + 'M' : 0)"},
                                            'columnSize': 'autoSize'}],
                                dashGridOptions={"animateRows": False, 'domLayout': "autoHeight"})
                        ], md=7, lg=7),
                        dbc.Col([
                            dcc.Loading([
                                dcc.Graph(id='graph6', className='dbc', config=config_graph)
                            ], delay_hide=500)
                        ], md=5, lg=5)
                    ])
                ], style={'text-align': 'center'})
            ], style=tab_card)
        ])
    ], className='g-2 my-auto', style={'margin-top': '7px'})    
], style={'padding-top': '0px'}, className="dbc")


# ======== Callbacks ========== #
# When Interval Ends
@callback(
        Output('time-updated', 'children'),
        Output('mod-time', 'data'),
        Input('interval-component', 'n_intervals'),
        State('mod-time', 'data')
)
def update_page(n_intervals, data):
    #print(f'Ejecutada {n_intervals} veces por {ctx.triggered_id}')
    global df
    global df_targets
    new_mod_time = os.path.getmtime(data_file)

    if data:
        #print(f'browser_mod_time es {data['browser_mod_time']}')
        if new_mod_time != data['browser_mod_time']:
            data['browser_mod_time'] = new_mod_time
            # ========== Re-Reading DATA ============ #
            #print('Ejecutando actualizacion')
            df = pd.read_excel(data_file, sheet_name='Dados')
            df_targets = pd.read_excel(data_file, sheet_name='Metas')
            new_time = datetime.datetime.now().time()
            new_label_updated = html.Label(f'Úlltima atualização: {str(new_time)[:8]}')
            #print(f'DATA tenia valor y browser_mod_time es {data['browser_mod_time']}')
            #print(f'DATA tenia valor y new_mod_time es {new_mod_time}')
            return new_label_updated, data
        else:
            return no_update, no_update
    else:
        #print('SE EJECUTA POR PRIMERA VEZ')
        data = {'browser_mod_time': new_mod_time}
        #print(f'BROWSER_MOD_TIME es {data['browser_mod_time']}')
        #print(f'DATA NO tenia valor y browser_mod_time es {data['browser_mod_time']}')
        #print(f'DATA NO tenia valor y new_mod_time es {new_mod_time}')

        return no_update, data

# Update graphs and tables when filters change
@callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('receita-total', 'children'),
    Output('customer-table', 'rowData'),
    Output('logo-select', 'src'),
    Output('graph6', 'figure'),
    Output('graph4', 'figure'),
    Output('graph5', 'figure'),
    Output('meta-total', 'children'),
    Output('delta-total', 'children'),
    Input('time-updated', 'children'),
    Input('month-range-slider', 'value'),
    Input('select-empresa', 'value'),
    Input('select-receita', 'value'),
    Input(ThemeSwitchAIO.ids.switch("themes"), "value")
)
def update_charts(_, month_range, empresa, receita, toggle):
    #print(f'Callback 1 Ejecutada por {ctx.triggered_id}')
    template = template_theme1 if toggle else template_theme2 # Changes theme

    start_month = month_range[0]
    end_month = month_range[1]

    df_1 = df_filter(start_month, end_month, empresa, receita)
    df_2 = df_1.groupby(['Empresa'])['Faturamento'].sum().reset_index()
    
    #fig Faturamento por Empresa
    data = []
    for empresa_temp in df_2['Empresa'].unique():
        df_3 = df_2[df_2['Empresa'].str.contains(empresa_temp)]
        data.append(
            go.Bar(
                x=['Empresa'],
                y=df_3['Faturamento']/1000000,
                hovertemplate="%{data.name}: R%{y:$.2f}M<extra></extra>",
                name = empresa_temp,
                showlegend = True,
                textposition='auto'
                #text=df_3['Faturamento']/1000000
            )
        )
    fig1 = go.Figure(data=data)
    fig1.update_layout(main_config, autosize=True, title='Faturamento por Empresa', height=250, template=template, barmode='stack')

    #fig Dsitribução de receita por empresa
    fig2 = go.Figure(go.Pie(labels=df_2['Empresa'], values=df_2['Faturamento']/1000000, 
                            textposition='auto',
                            text=df_2['Empresa'],
                            hole=.6,
                            hovertemplate='%{label}: R%{value:$.2f}M<br>%{percent}</br><extra></extra>'))
    fig2.update_layout(main_config, height=250, template=template, showlegend=False)

    df_2 = df_1.groupby(['Tipo Receita'])['Faturamento'].sum().reset_index()

    #fig Faturamento por tipo de receita
    data = []
    for receita_temp in df_2['Tipo Receita'].unique():
        df_3 = df_2[df_2['Tipo Receita'].str.contains(receita_temp)]
        data.append(
            go.Bar(
                x=['Receita'],
                y=df_3['Faturamento']/1000000,
                hovertemplate="%{data.name}: R%{y:$.2f}M<extra></extra>",
                name = receita_temp,
                showlegend = True
            )
        )
    fig3 = go.Figure(data=data)
    fig3.update_layout(main_config, autosize=True, title='Por Tipo de Receita', height=250, template=template, barmode='stack', showlegend=True)

    #Select Total Faturamento
    fat_total = df_1['Faturamento'].sum()/1000000
    
    select3 = html.H4(f'R${fat_total:,.2f}M')

    #table Top 5 Clientes
    df_faturamento = df_1.groupby(['Grupo'])['Faturamento'].sum().sort_values(ascending=False).reset_index()
    df_table = df_faturamento.iloc[:5]
    table_data = df_table.to_dict('records')

    #graph Pie Top 5 Clientes vs Others
    #First 5 Top clientes
    value_pie_top_5 = df_table['Faturamento'].sum()
    #Other Clients
    value_pie_others_fat = df_faturamento.iloc[5:]['Faturamento'].sum()
    
    df_pie_data = [['Top 5 Clientes', value_pie_top_5], ['Others', value_pie_others_fat]]
    df_pie = pd.DataFrame(df_pie_data, columns=['Grupo', 'Faturamento'])
    
    fig6 = go.Figure(go.Pie(labels=df_pie['Grupo'], values=df_pie['Faturamento']/1000000, 
                             textposition='auto',
                             text=df_pie['Grupo'],
                             hole=0,
                             showlegend=True,
                             #textinfo='none',
                             hovertemplate='%{label}: R%{value:$.2f}M<br>%{percent}</br><extra></extra>'))
    fig6.update_layout(main_config,
                       legend= {
                                'orientation': "h",
                                "yanchor":"top",
                                "y":-0.1, 
                                "xanchor":"center",
                                "x":0.5,
                                "title": {"text": None},
                                "font" :{"color":"white"},
                                "bgcolor": "rgba(0,0,0,0.3)"},
                        height=300,
                        template=template,
                        autosize=True)

    #select Muda Logo segundo o template
    if template == template_theme1:
        logo = 'Logo-white.png'
    else:
        logo = 'Logo-black.png'

    src_logo = f'assets/{logo}'
    select4 = src_logo

    # Charts Row 2
    df_3 = meta_filter(start_month, end_month, empresa)
    df_4 = df_3.groupby('Mês')['Meta'].sum().reset_index()
    df_5 = df_filter(start_month, end_month, empresa, 'Recorrente')
    df_6 = df_5.groupby(['Mês', 'Empresa'])['Faturamento'].sum().reset_index()

    # Faturamento mensal vs Meta
    fig_data = [go.Scatter(x=df_4['Mês'],
                           y=df_4['Meta']/1000000,
                           mode='lines+markers',
                           hovertemplate="%{data.name}:<br>R%{y:$.2f}M<extra></extra>",
                           name='Meta')]
    for i in df_6['Empresa'].unique():
        df_7 = df_6[df_6['Empresa'] == i]
        fig_data.append(go.Bar(x=df_7['Mês'],
                               y=df_7['Faturamento']/1000000,
                               hovertemplate="%{data.name}:<br>R%{y:$.2f}M<extra></extra>",
                               name=f'Faturamento {i}'))
    
    fig4 = go.Figure(data=fig_data)
    fig4.update_layout(main_config, xaxis={"dtick":1, 'titlefont': {'size': 5}}, title='Receita Recorrente vs Meta', xaxis_title='Meses', yaxis_title='Milhões $R', height=200, template=template, barmode='stack', showlegend=True)

    #fig Atingimento da Meta
    meta_value = df_4['Meta'].sum()/1000000
    fat_value = df_5['Faturamento'].sum()/1000000
    #bar color
    if fat_value < meta_value * 0.7:
        bar_color = '#e74c3c' #red
    elif fat_value < meta_value:
        bar_color = '#f39c12' #orange
    else:
        bar_color = '#18bc9c' #green
    
    fig5 = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = fat_value,
        number = {'prefix': 'R$', 'suffix': 'M'},
        mode = "gauge+number+delta",
        title = {'text': "Atingimento"},
        delta = {'reference': meta_value, 'relative': True, 'valueformat': '.2%'},
        gauge = {'axis': {'range': [None, meta_value * 1.5]},
                 'bar': {'color': bar_color},
                'steps' : [
                    {'range': [0, meta_value * 0.7], 'color': "lightgray"},
                    {'range': [meta_value * 0.7, meta_value], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': meta_value}}
    ))
    fig5.update_layout(main_config,
                       height=200,
                       template=template)

    #select Valor da Meta FY
    select = html.H3(f'R${meta_value:,.2f}M')
    if fat_value-meta_value > 0:
        color = '#18bc9c'
    else:
        color = '#ff1100'
    
    #select Gap para atingir a Meta
    select2 = html.H3(f'R${fat_value - meta_value:,.2f}M', style={'color': color})

    return fig1, fig2, fig3, select3, table_data, select4, fig6, fig4, fig5, select, select2

