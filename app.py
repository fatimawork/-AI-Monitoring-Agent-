# app.py

import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime
import time

st.set_page_config(page_title="AI Infrastructure Monitor", layout="wide")

st.title("🧠 Infrastructure Monitoring Agent")
st.caption("Détection d'anomalies sur des logs CPU simulés en temps réel")

placeholder = st.empty()

def generate_fake_logs():
    data = np.random.normal(50, 5, size=1000)
    data[300:310] += 30  # Anomalie injectée
    timestamps = pd.date_range(end=datetime.now(), periods=1000, freq='s')
    df = pd.DataFrame({'timestamp': timestamps, 'cpu_usage': data})
    return df

def detect_anomalies(df):
    model = IsolationForest(contamination=0.01, random_state=42)
    df['anomaly'] = model.fit_predict(df[['cpu_usage']])
    return df

# Simulation live
while True:
    df = generate_fake_logs()
    df = detect_anomalies(df)

    with placeholder.container():
        st.subheader("📊 Graphique d'utilisation CPU")
        st.line_chart(df.set_index("timestamp")[["cpu_usage"]])

        st.subheader("⚠️ Anomalies détectées")
        anomalies = df[df['anomaly'] == -1]
        st.dataframe(anomalies[['timestamp', 'cpu_usage']].tail(5), use_container_width=True)

    time.sleep(10)  # actualisation toutes les 10s
