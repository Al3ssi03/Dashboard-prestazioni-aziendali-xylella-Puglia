import numpy as np
import pandas as pd
from datetime import timedelta, datetime

# Impostazione del seed per riproducibilità
def genera_dati_simulati(num_giorni=365):
    date_rng = pd.date_range(start='2024-01-01', periods=num_days, freq='D')

    dati = {
        'Data': date_rng,
        'Provincia': np.random.choice(['Lecce', 'Brindisi', 'Taranto', 'Bari', 'BAT', 'Foggia'], size=num_days),
        'Temperatura (°C)': np.random.normal(20, 5, size=num_days).round(2),
        'Umidità (%)': np.random.uniform(40, 90, size=num_days),
        'Precipitazioni (mm)': np.random.uniform(0, 30, size=num_days).round(2),
        'Alberi_Totali': np.random.randint(1000, 5000, size=num_days),
    }

    df = pd.DataFrame(dati)

    # Simulazione numero alberi infetti (da 5% a 20%)
    df['Alberi_Infetti'] = (df['Alberi_Totali'] * np.random.uniform(0.05, 0.20, size=num_days)).astype(int)

    # Alberi ripiantati (valore randomico, circa il 50-70% degli alberi infetti)
    df['Alberi_Ripiantati'] = (df['Alberi_Totali'] * np.random.uniform(0.05, 0.15, size=num_days)).astype(int)

    # Produzione olio: Riduzione in funzione alberi infetti
    produzione_media = 150  # litri per ettaro senza infezioni
    perdita_percentuale = (df['Alberi_Ripiantati'] / df['Alberi_Totali']) * np.random.uniform(0.2, 0.4, size=num_days)
    df['Produzione_Olio'] = (2000 * (1 - perdita_percentuale)).round(2)

    return df

# Generazione dati simulati
num_days = 365
simulated_data = genera_dati_simulati(num_days)

# Esporta i dati simulati in CSV
simulated_data.to_csv('dati_simulati_xylella.csv', index=False)

# Visualizzazione prime righe del dataset
print(simulated_data.head())
