import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import logging
from datetime import datetime, timedelta

# --- KONFIGURACJA LOGOWANIA ---
logging.basicConfig(
    filename='system_run.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# --- 1. GENEROWANIE SYNTETYCZNYCH LOGÓW (SYNTHETIC DATA ENGINEERING) ---
def generate_security_logs(n_entries=2000):
    """Generuje syntetyczny zbiór logów serwera z wstrzykniętą anomalią."""
    np.random.seed(7)
    ips = [f"192.168.1.{i}" for i in range(10, 20)]
    attacker_ip = "10.0.0.66"  # IP "Agresora"
    
    data = []
    start_time = datetime(2025, 5, 20, 10, 0, 0)

    for i in range(n_entries):
        # Normalny ruch - symulacja realnego "szumu"
        current_time = start_time + timedelta(seconds=i * np.random.randint(1, 60))
        ip = np.random.choice(ips)
        status = np.random.choice([200, 404, 500], p=[0.85, 0.12, 0.03])
        data.append([current_time, ip, status, "GET /index.html"])

    # Wstrzyknięcie ataku Brute-Force (Szybkie próby logowania)
    attack_start = start_time + timedelta(minutes=30)
    for i in range(50):
        attack_time = attack_start + timedelta(seconds=i * 2) 
        data.append([attack_time, attacker_ip, 401, "POST /login"])

    df = pd.DataFrame(data, columns=['timestamp', 'ip_address', 'status_code', 'request_path'])
    return df

# --- 2. ANALIZA EDA I WIZUALIZACJA ---
def analyze_logs(df):
    """Przeprowadza analizę statystyczną i generuje wykresy PNG."""
    print("🔍 Analiza logów w toku...")
    
    # Detekcja anomalii: IP z największą liczbą błędów 401
    failed_logins = df[df['status_code'] == 401].groupby('ip_address').size().sort_values(ascending=False)
    
    print("\n[ALERCI BEZPIECZEŃSTWA - WYKRYTE ANOMALIE]")
    print(failed_logins)

    # Wizualizacja 1: Rozkład statusów
    plt.figure(figsize=(10, 5))
    sns.countplot(x='status_code', data=df, hue='status_code', palette='magma', legend=False)
    plt.title('Distribution of HTTP Status Codes (Synthetic Dataset)')
    plt.savefig('status_distribution.png')

    # Wizualizacja 2: Oś czasu ataku
    df['minute'] = df['timestamp'].dt.floor('min')
    if not failed_logins.empty:
        top_ip = failed_logins.index[0]
        attack_timeline = df[df['ip_address'] == top_ip].groupby('minute').size()
        
        plt.figure(figsize=(12, 5))
        attack_timeline.plot(kind='line', color='red', marker='o', linewidth=2)
        plt.title(f'Attack Timeline Insight (IP: {top_ip})')
        plt.ylabel('Requests per Minute')
        plt.grid(True, linestyle='--')
        plt.savefig('attack_timeline.png')
    
    print("\n[SUKCES] Wizualizacje PNG zostały wygenerowane.")
    return failed_logins

# --- 3. GENEROWANIE RAPORTÓW (JSON & TXT) ---
def generate_security_summary(df, failed_logins):
    """Tworzy raport maszynowy w formacie JSON."""
    summary = {
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dataset_info": {
            "total_logs": len(df),
            "time_range": f"{df['timestamp'].min()} to {df['timestamp'].max()}"
        },
        "security_metrics": {
            "critical_401_errors": int(df[df['status_code'] == 401].shape[0]),
            "top_suspicious_origin": failed_logins.index[0] if not failed_logins.empty else "None",
            "threat_level": "High" if not failed_logins.empty and failed_logins.iloc[0] > 20 else "Low"
        }
    }
    
    with open('security_summary.json', 'w') as f:
        json.dump(summary, f, indent=4)
    print("📝 Raport maszynowy security_summary.json został wygenerowany.")

def generate_llm_prompt_task():
    """Tworzy specyfikację zadania dla ewaluacji modeli LLM."""
    task_description = """
### LLM EVALUATION TASK DEFINITION
Project: Synthetic Security Log Analysis

Objective: 
Evaluate the model's ability to identify a low-and-slow brute force attack within a noisy web server log.

Expected Model Output:
1. Identify the suspicious IP address.
2. Characterize the attack type (Brute-Force / Unauthorized Access attempt).
3. Determine the peak time of the attack based on request frequency.

Ground Truth (Context for Evaluator):
- Attacker IP: 10.0.0.66
- Attack Window: Starts 30 minutes after initial log entry.
- Key Indicator: 50 consecutive 401 status codes in a short timeframe.
"""
    with open('llm_task_definition.txt', 'w', encoding='utf-8') as f:
        f.write(task_description)
    print("🤖 Wygenerowano definicję zadania dla LLM (llm_task_definition.txt).")

# --- 4. GŁÓWNA PĘTLA WYKONAWCZA ---
if __name__ == "__main__":
    try:
        logging.info("--- ROZPOCZĘCIE PROCESU SYNTHETIC DATA EDA ---")
        
        # KROK 1: Generowanie danych
        logging.info("Generowanie logów syntetycznych...")
        logs_df = generate_security_logs()
        
        # KROK 2: Analiza i wizualizacja
        logging.info("Uruchomienie modułu analizy wizualnej...")
        anomalies = analyze_logs(logs_df)
        
        # KROK 3: Raportowanie i specyfikacja zadania
        logging.info("Generowanie raportów JSON i TXT...")
        generate_security_summary(logs_df, anomalies)
        generate_llm_prompt_task()
        
        # KROK 4: Eksport danych do CSV
        logging.info("Eksportowanie surowych danych do CSV...")
        logs_df.to_csv("security_logs_synthetic.csv", index=False)
        
        logging.info("--- PROCES ZAKOŃCZONY SUKCESEM ---")
        print("\n🚀 Wszystkie operacje zakończone pomyślnie!")
        print("📁 Pliki wynikowe: PNG (wykresy), JSON (raport), TXT (zadanie LLM), CSV (dane), LOG (system).")
        
    except Exception as e:
        logging.error(f"Błąd krytyczny podczas wykonywania skryptu: {e}", exc_info=True)
        print(f"❌ Wystąpił błąd krytyczny. Sprawdź plik system_run.log po szczegóły.")