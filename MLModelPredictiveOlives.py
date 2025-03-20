# Questo file è MLModelPredictiveOlives.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Funzione per caricare e addestrare il modello

def carica_modello():
    simulated_data = pd.read_csv('dati_simulati_xylella.csv')

    # Addestramento modello
    features = ['Temperatura (°C)', 'Umidità (%)', 'Precipitazioni (mm)', 'Alberi_Ripiantati', 'Alberi_Infetti']
    target = 'Produzione_Olio'
    X = simulated_data[features]
    y = simulated_data[target]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model

# Inizializza il modello una sola volta all'import
model = carica_modello()

# Funzione per effettuare la predizione

def calcola_predizione(temp, umid, precipitazioni, ripiantati, infetti):
    try:
        dati_input = pd.DataFrame({
            'Temperatura (°C)': [temp],
            'Umidità (%)': [umid],
            'Precipitazioni (mm)': [precipitazioni],
            'Alberi_Ripiantati': [ripiantati],
            'Alberi_Infetti': [infetti]
        })

        predizione = model.predict(dati_input)[0]
        return predizione
    except Exception as e:
        raise ValueError(f"Errore nel calcolo della predizione: {str(e)}")
