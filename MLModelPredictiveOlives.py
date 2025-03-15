import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import dash_leaflet as dl
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

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

# Modello predittivo (RandomForestRegressor)
from sklearn.ensemble import RandomForestRegressor
features = ['Temperatura (°C)', 'Umidità (%)', 'Precipitazioni (mm)', 'Alberi_Ripiantati', 'Alberi_Infetti']
target = 'Produzione_Olio'
X = simulated_data[features]
y = simulated_data[target]
model = RandomForestRegressor()
model.fit(X, y)

# App Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Monitoraggio Xylella in Puglia", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_provincia",
                 options=[{"label": prov, "value": prov} for prov in simulated_data['Provincia'].unique()],
                 multi=False,
                 value='Lecce',
                 style={'width': "50%"}),

    html.Br(),

    dcc.Graph(id='grafico_temperatura'),
    dcc.Graph(id='grafico_umidita'),
    dcc.Graph(id='grafico_alberi_infetti'),

    html.H2("Mappa della diffusione della Xylella"),
    dl.Map(id="mappa_xylella", style={'width': '100%', 'height': '500px'}, center=[40.9, 16.6], zoom=8, children=[
        dl.TileLayer(),
        dl.LayerGroup(id="layer_province")
    ]),

    html.H2("Predizione produzione olio"),
    html.Div([
        dcc.Input(id='input_temp', type='number', placeholder="Temperatura (°C)", style={'margin': '5px'}),
        dcc.Input(id='input_umid', type='number', placeholder="Umidità (%)", style={'margin': '5px'}),
        dcc.Input(id='input_precipitazioni', type='number', placeholder="Precipitazioni (mm)", style={'margin': '5px'}),
        dcc.Input(id='input_alberi_ripiantati', type='number', placeholder="Alberi Ripiantati", style={'margin': '5px'}),
        dcc.Input(id='input_alberi_infetti', type='number', placeholder="Alberi Infetti", style={'margin': '5px'}),
        html.Button('Calcola Predizione', id='submit-val', n_clicks=0),
        html.Div(id='output_predizione')
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

    markers = [dl.Marker(position=provincia_coords[prov], children=dl.Popup(prov)) for prov in provincia_coords]

    return fig_temp, fig_umid, fig_infetti, markers

@app.callback(
    Output('output_predizione', 'children'),
    [Input('submit_button', 'n_clicks')],
    [Input('input_temp', 'value'),
     Input('input_umidita', 'value'),
     Input('input_alberi_ripiantati', 'value'),
     Input('input_alberi_infetti', 'value')]
)
def calcola_predizione(temp, umidita, alberi_ripiantati, alberi_infetti):
    dati_input = pd.DataFrame({
        'Temperatura (°C)': [temp],
        'Umidità (%)': [umid],
        'Alberi_Ripiantati': [alberi_ripiantati],
        'Alberi_Infetti': [alberi_infetti]
    })
    predizione = model.predict(dati_input)[0]
    return f'Produzione di olio prevista: {predizione:.2f} litri per ettaro'

if __name__ == '__main__':
    app.run_server(debug=True)
