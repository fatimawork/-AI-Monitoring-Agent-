# monitor_agent.py

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import time
import schedule
from datetime import datetime

# 1. Génération de logs simulés
def generate_fake_logs():
    data = np.random.normal(50, 5, size=1000)  # Usage CPU normal
    # Injecter une anomalie (pic CPU) aléatoirement
    data[300:310] += 30
    timestamps = pd.date_range(end=datetime.now(), periods=1000, freq='S')
    df = pd.DataFrame({'timestamp': timestamps, 'cpu_usage': data})
    return df

# 2. Détection d’anomalies
def detect_anomalies(df):
    model = IsolationForest(contamination=0.01, random_state=42)
    df['anomaly'] = model.fit_predict(df[['cpu_usage']])
    anomalies = df[df['anomaly'] == -1]
    return anomalies

# 3. Surveillance périodique
def monitor():
    print(f"🕒 Checking logs at {datetime.now().strftime('%H:%M:%S')}")
    logs = generate_fake_logs()
    anomalies = detect_anomalies(logs)
    
    if not anomalies.empty:
        print("⚠️  Anomalies detected!")
        print(anomalies[['timestamp', 'cpu_usage']].tail())
        # send_alert() # <-- à activer si tu veux envoyer un email
    else:
        print("✅ All good.")

# 4. Scheduler
schedule.every(10).seconds.do(monitor)

print("🔍 Monitoring agent started.")
while True:
    schedule.run_pending()
    time.sleep(1)
