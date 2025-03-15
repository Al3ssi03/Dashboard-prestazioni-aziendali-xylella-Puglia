import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import dash_leaflet as dl
from MLModelPredictiveOlives import model, calcola_predizione

# Caricamento dati simulati
simulated_data = pd.read_csv('dati_simulati_xylella.csv')

# Coordinate delle province pugliesi
provincia_coords = {
    'Lecce': [40.3515, 18.1750],
    'Brindisi': [40.6327, 17.9418],
    'Taranto': [40.4644, 17.2470],
    'Bari': [41.1171, 16.8719],
    'BAT': [41.2279, 16.2956],
    'Foggia': [41.4622, 15.5446]
}

# App Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Monitoraggio Xylella in Puglia", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_provincia",
                 options=[{"label": prov, "value": prov} for prov in simulated_data['Provincia'].unique()],
                 multi=False,
                 value='Lecce',
                 style={'width': "50%"}
                 ),

    html.Br(),

    dcc.Graph(id='grafico_temperatura'),
    dcc.Graph(id='grafico_umidita'),
    dcc.Graph(id='grafico_alberi_infetti'),

    html.H2("Mappa della diffusione della Xylella"),
    dl.Map(id="mappa_xylella", style={'width': '100%', 'height': '500px'}, center=[40.9, 16.6], zoom=8, children=[
        dl.TileLayer(),
        dl.LayerGroup(id="layer_province", children=[
            dl.Marker(position=coord, children=[dl.Popup(prov)]) for prov, coord in provincia_coords.items()
        ])
    ]),

    html.H2("🔍 Previsione produzione olio d'oliva", style={'text-align': 'center', 'color': '#2C3E50', 'margin-top': '20px'}),
    
    html.Div([
        dcc.Input(id='input_temp', type='number', placeholder="🌡️ Temperatura (°C)", style={'margin': '10px', 'padding': '10px', 'width': '18%'}),
        dcc.Input(id='input_umidita', type='number', placeholder="💧 Umidità (%)", style={'margin': '10px', 'padding': '10px', 'width': '18%'}),
        dcc.Input(id='input_precipitazioni', type='number', placeholder="☔ Precipitazioni (mm)", style={'margin': '10px', 'padding': '10px', 'width': '18%'}),
        dcc.Input(id='input_alberi_ripiantati', type='number', placeholder="🌱 Alberi Ripiantati", style={'margin': '10px', 'padding': '10px', 'width': '18%'}),
        dcc.Input(id='input_alberi_infetti', type='number', placeholder="🦠 Alberi Infetti", style={'margin': '10px', 'padding': '10px', 'width': '18%'}),
    ], style={'display': 'flex', 'justify-content': 'center'}),

    html.Div([
        html.Button('⚡ Calcola Predizione', id='calcola_predizione', n_clicks=0,
                    style={'background-color': '#27AE60', 'color': 'white', 'border': 'none',
                           'padding': '12px 24px', 'font-size': '16px', 'border-radius': '5px',
                           'cursor': 'pointer', 'margin-top': '10px'}),
    ], style={'text-align': 'center'}),

    html.Div(id='output_predizione', style={'margin-top': '20px', 'font-size': '18px', 'font-weight': 'bold', 'text-align': 'center'})
])

@app.callback(
    [Output('grafico_temperatura', 'figure'),
     Output('grafico_umidita', 'figure'),
     Output('grafico_alberi_infetti', 'figure')],
    [Input('select_provincia', 'value')]
)
def update_grafici(selected_provincia):
    filtered_df = simulated_data[simulated_data['Provincia'] == selected_provincia]

    fig_temp = px.line(filtered_df, x='Data', y='Temperatura (°C)', title='Andamento Temperatura')
    fig_umid = px.line(filtered_df, x='Data', y='Umidità (%)', title='Andamento Umidità')
    fig_infetti = px.bar(filtered_df, x='Data', y='Alberi_Infetti', title='Numero Alberi Infetti')

    return fig_temp, fig_umid, fig_infetti

if __name__ == '__main__':
    app.run_server(debug=True)
