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

# Caricamento dati simulati
simulated_data = pd.read_csv('dati_simulati_xylella.csv')

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
        dl.LayerGroup(id="layer_province")
    ]),

    html.H2("Previsione produzione olio d'oliva"),
    html.Div([
        dcc.Input(id='input_temp', type='number', placeholder="Temperatura (°C)", style={'margin': '5px'}),
        dcc.Input(id='input_umidita', type='number', placeholder="Umidità (%)", style={'margin': '5px'}),
        dcc.Input(id='input_precipitazioni', type='number', placeholder="Precipitazioni (mm)", style={'margin': '5px'}),
        dcc.Input(id='input_alberi_ripiantati', type='number', placeholder="Alberi Ripiantati", style={'margin': '5px'}),
        dcc.Input(id='input_alberi_infetti', type='number', placeholder="Alberi Infetti", style={'margin': '5px'}),
        html.Button('Calcola Predizione', id='calcola_predizione', n_clicks=0),
        html.Div(id='output_predizione', style={'margin-top': '20px', 'font-weight': 'bold'})
    ])
])

@app.callback(
    [Output('grafico_temperatura', 'figure'),
     Output('grafico_umidita', 'figure'),
     Output('grafico_alberi_infetti', 'figure'),
     Output("layer_province", "children")],
    [Input('select_provincia', 'value')]
)
def update_dashboard(selected_provincia):
    filtered_df = simulated_data[simulated_data['Provincia'] == selected_provincia]

    fig_temp = px.line(filtered_df, x='Data', y='Temperatura (°C)', title='Andamento Temperatura')
    fig_umid = px.line(filtered_df, x='Data', y='Umidità (%)', title='Andamento Umidità')
    fig_infetti = px.bar(filtered_df, x='Data', y='Alberi_Infetti', title='Numero Alberi Infetti')

    markers = [
        dl.Marker(position=provincia_coords[prov], children=[
            dl.Popup(html.B(prov))
        ]) for prov in provincia_coords
    ]

    return fig_temp, fig_umid, fig_infetti, markers

@app.callback(
    Output('output_predizione', 'children'),
    Input('input_temp', 'value'),
    Input('input_umid', 'value'),
    Input('input_precipitazioni', 'value'),
    Input('input_alberi_ripiantati', 'value'),
    Input('input_alberi_infetti', 'value')
)
def aggiorna_predizione(temp, umid, precip, ripiantati, infetti):
    if None in [temp, umid, ripiantati, infetti]:
        return "Inserire tutti i valori richiesti per effettuare la predizione."

    dati_input = pd.DataFrame({
        'Temperatura (°C)': [temp],
        'Umidità (%)': [umid],
        'Precipitazioni (mm)': [precip],
        'Alberi_Ripiantati': [ripiantati],
        'Alberi_Infetti': [infetti]
    })

    predizione = calcola_predizione(model, dati_input)
    return f'Produzione di olio prevista: {predizione:.2f} litri per ettaro'

if __name__ == '__main__':
    app.run_server(debug=True)