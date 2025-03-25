
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import dash_leaflet as dl
from MLModelPredictiveOlives import calcola_predizione

# Caricamento dati simulati
simulated_data = pd.read_csv('dati_simulati_xylella.csv')

# Coordinate delle province pugliesi e valori soglia per aree rosse
provincia_coords = {
    'Lecce': [40.3515, 18.1750],
    'Brindisi': [40.6327, 17.9418],
    'Taranto': [40.4644, 17.2470],
    'Bari': [41.1171, 16.8719],
    'BAT': [41.2279, 16.2956],
    'Foggia': [41.4622, 15.5446]
}

# Funzione per generare marker con colore in base al numero di alberi infetti

def crea_marker(provincia, coord, infetti_medi):
    color = 'red' if infetti_medi > 50 else 'green'
    return dl.CircleMarker(center=coord, radius=15, color=color, fill=True, fillOpacity=0.6, children=[
        dl.Tooltip(f"{provincia}: {infetti_medi} alberi infetti")
    ])

# Creazione applicazione Dash
app = dash.Dash(__name__)

# Layout con UI migliorata
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'background-color': '#f0f4f8', 'padding': '30px'}, children=[
    html.H1("🌿 Dashboard Monitoraggio Xylella in Puglia", style={'text-align': 'center', 'color': '#1B4F72', 'margin-bottom': '40px', 'font-size': '40px'}),

    html.Div([
        dcc.Dropdown(id="select_provincia",
                     options=[{"label": prov, "value": prov} for prov in simulated_data['Provincia'].unique()],
                     multi=False,
                     value='Lecce',
                     style={'width': "60%", 'margin': 'auto', 'border-radius': '12px', 'padding': '10px', 'font-size': '16px', 'box-shadow': '0 0 5px rgba(0,0,0,0.1)'}
                     ),
    ], style={'text-align': 'center', 'margin-bottom': '40px'}),

    html.Div([
        dcc.Graph(id='grafico_temperatura', config={'displayModeBar': False}),
        dcc.Graph(id='grafico_umidita', config={'displayModeBar': False}),
        dcc.Graph(id='grafico_alberi_infetti', config={'displayModeBar': False}),
    ], style={'background-color': 'white', 'border-radius': '16px', 'padding': '30px', 'box-shadow': '0 0 15px rgba(0,0,0,0.1)', 'margin-bottom': '50px'}),

    html.H2("🗺️ Mappa con aree rosse dove si concentrano gli alberi infetti", style={'text-align': 'center', 'color': '#21618C', 'margin-bottom': '30px', 'font-size': '28px'}),
    dl.Map(id="mappa_xylella", style={'width': '100%', 'height': '500px', 'border-radius': '12px', 'box-shadow': '0 0 10px rgba(0,0,0,0.1)', 'margin-bottom': '50px'}, center=[40.9, 16.6], zoom=8, children=[
        dl.TileLayer(),
        dl.LayerGroup(id="layer_province")
    ]),

    html.H2("📊 Calcola la previsione di produzione olio d'oliva", style={'text-align': 'center', 'color': '#21618C', 'margin-bottom': '30px', 'font-size': '28px'}),

    html.Div([
        dcc.Input(id='input_temp', type='number', placeholder="🌡️ Temperatura (°C)", style={'margin': '8px', 'padding': '12px', 'width': '18%', 'border-radius': '10px', 'border': '1px solid #ccc', 'font-size': '15px'}),
        dcc.Input(id='input_umidita', type='number', placeholder="💧 Umidità (%)", style={'margin': '8px', 'padding': '12px', 'width': '18%', 'border-radius': '10px', 'border': '1px solid #ccc', 'font-size': '15px'}),
        dcc.Input(id='input_precipitazioni', type='number', placeholder="☔ Precipitazioni (mm)", style={'margin': '8px', 'padding': '12px', 'width': '18%', 'border-radius': '10px', 'border': '1px solid #ccc', 'font-size': '15px'}),
        dcc.Input(id='input_alberi_ripiantati', type='number', placeholder="🌱 Alberi Ripiantati", style={'margin': '8px', 'padding': '12px', 'width': '18%', 'border-radius': '10px', 'border': '1px solid #ccc', 'font-size': '15px'}),
        dcc.Input(id='input_alberi_infetti', type='number', placeholder="🦠 Alberi Infetti", style={'margin': '8px', 'padding': '12px', 'width': '18%', 'border-radius': '10px', 'border': '1px solid #ccc', 'font-size': '15px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'flex-wrap': 'wrap', 'margin-bottom': '30px'}),

    html.Div([
        html.Button('⚡ Calcola Predizione', id='calcola_predizione', n_clicks=0,
                    style={'background-color': '#28B463', 'color': 'white', 'border': 'none',
                           'padding': '14px 36px', 'font-size': '18px', 'border-radius': '10px',
                           'cursor': 'pointer', 'margin-top': '10px', 'box-shadow': '0 4px 6px rgba(0,0,0,0.1)'}),
    ], style={'text-align': 'center'}),

    html.Div(id='output_predizione', style={'margin-top': '40px', 'font-size': '22px', 'font-weight': 'bold', 'color': '#1B4F72', 'text-align': 'center'})
])

@app.callback(
    [Output('grafico_temperatura', 'figure'),
     Output('grafico_umidita', 'figure'),
     Output('grafico_alberi_infetti', 'figure'),
     Output('layer_province', 'children')],
    [Input('select_provincia', 'value')]
)
def update_dashboard(selected_provincia):
    filtered_df = simulated_data[simulated_data['Provincia'] == selected_provincia]

    fig_temp = px.line(filtered_df, x='Data', y='Temperatura (°C)', title='📈 Andamento della Temperatura')
    fig_umid = px.line(filtered_df, x='Data', y='Umidità (%)', title='💧 Andamento Umidità')
    fig_infetti = px.bar(filtered_df, x='Data', y='Alberi_Infetti', title='🌳 Numero di Alberi Infetti')

    # Calcolo media infetti per provincia per visualizzare le zone rosse
    province_avg_infetti = simulated_data.groupby('Provincia')['Alberi_Infetti'].mean().to_dict()
    markers = [crea_marker(prov, provincia_coords[prov], infetti_medi) for prov, infetti_medi in province_avg_infetti.items()]

    return fig_temp, fig_umid, fig_infetti, markers

@app.callback(
    Output('output_predizione', 'children'),
    Input('calcola_predizione', 'n_clicks'),
    State('input_temp', 'value'),
    State('input_umidita', 'value'),
    State('input_precipitazioni', 'value'),
    State('input_alberi_ripiantati', 'value'),
    State('input_alberi_infetti', 'value')
)
def aggiorna_predizione(n_clicks, temp, umid, precipitazioni, ripiantati, infetti):
    if n_clicks == 0 or None in [temp, umid, precipitazioni, ripiantati, infetti]:
        return "⚠️ Inserisci tutti i valori e premi il pulsante per la predizione."

    try:
        prediction = calcola_predizione(temp, umid, precipitazioni, ripiantati, infetti)
        return f'✅ Produzione di olio prevista: {prediction:.2f} litri per ettaro!'
    except Exception as e:
        return f'❗ Errore durante la predizione: {str(e)}'

if __name__ == '__main__':
    app.run_server(debug=True)
