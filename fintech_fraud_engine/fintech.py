import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# --- 0. PANEL STEROWANIA ---
CONFIG = {
    'num_transactions': 100000,    # Teraz zmiana tej liczby zmieni wszystko
    'user_range': (100, 5000),
    'fraud_threshold': 5000,
    'velocity_limit_min': 60,
    'output_file': "fintech_big_data.json"
}

# --- 1. GENERATOR DANYCH SYNTETYCZNYCH ---
def generate_fintech_data(config):
    np.random.seed(42)
    n = config['num_transactions']
    u_min, u_max = config['user_range']
    start_date = datetime(2026, 1, 1)
    
    data = {
        't_id': [f"TXN-{i:04d}" for i in range(n)],
        'user_id': np.random.randint(u_min, u_max, size=n),
        'amount': np.random.lognormal(mean=4, sigma=1, size=n).round(2),
        'timestamp': [start_date + timedelta(minutes=np.random.randint(1, 10000)) for _ in range(n)],
        'merchant_city': np.random.choice(['Warszawa', 'Kraków', 'Wrocław', 'Londyn', 'Dubaj'], size=n),
        'channel': np.random.choice(['Online', 'POS', 'ATM'], size=n, p=[0.6, 0.3, 0.1])
    }
    
    df = pd.DataFrame(data).sort_values(by=['user_id', 'timestamp'])
    df['is_fraud_ground_truth'] = False

    # --- DYNAMICZNE WSTRZYKIWANIE FRAUDU (np. 0.5% wszystkich transakcji) ---
    fraud_indices = np.random.choice(df.index, size=int(n * 0.005), replace=False)
    
    for idx in fraud_indices:
        # Losujemy typ fraudu
        fraud_type = np.random.choice(['high_amount', 'impossible_travel'])
        
        if fraud_type == 'high_amount':
            # Losowa wysoka kwota powyżej progu
            df.at[idx, 'amount'] = np.random.uniform(5001, 15000)
            df.at[idx, 'is_fraud_ground_truth'] = True
        else:
            # Tworzymy parę "Impossible Travel" dla tego samego usera
            uid = df.at[idx, 'user_id']
            df.at[idx, 'merchant_city'] = 'Dubaj'
            df.at[idx, 'is_fraud_ground_truth'] = True
            
            # Znajdujemy poprzednią transakcję tego usera i skracamy czas
            user_txs = df[df['user_id'] == uid].index
            if len(user_txs) > 1:
                prev_idx = user_txs[list(user_txs).index(idx) - 1]
                df.at[idx, 'timestamp'] = df.at[prev_idx, 'timestamp'] + timedelta(minutes=5)
                df.at[idx, 'merchant_city'] = 'Londyn' # Zmiana miasta na inne niż poprzednie

    return df

# --- 2. LOGIKA ANALITYCZNA ---
def analyze_transactions(df, config):
    df = df.copy()
    # Sortowanie ważne dla diff()
    df = df.sort_values(by=['user_id', 'timestamp'])
    df['time_delta_min'] = df.groupby('user_id')['timestamp'].diff().dt.total_seconds() / 60
    df['city_change'] = df.groupby('user_id')['merchant_city'].shift(0) != df.groupby('user_id')['merchant_city'].shift(1)
    
    def flag_risk(row):
        if row['amount'] > config['fraud_threshold']: 
            return 'CRITICAL_AMOUNT'
        if 0 < row['time_delta_min'] < config['velocity_limit_min'] and row['city_change']: 
            return 'IMPOSSIBLE_TRAVEL'
        if row['amount'] < 5.00: 
            return 'SMALL_PROBE'
        return 'NORMAL'

    df['predicted_risk'] = df.apply(flag_risk, axis=1)
    return df

# --- 3. RAPORTOWANIE ---
def run_full_audit(df):
    """Generuje kompletny raport techniczny, finansowy i jakościowy."""
    # Definicje
    actual_frauds = df[df['is_fraud_ground_truth'] == True]
    actual_normals = df[df['is_fraud_ground_truth'] == False]
    
    predicted_frauds = df[df['predicted_risk'] != 'NORMAL']
    
    # Metryki
    tp = len(actual_frauds[actual_frauds['predicted_risk'] != 'NORMAL']) # True Positives
    fp = len(actual_normals[actual_normals['predicted_risk'] != 'NORMAL']) # False Positives
    
    recall = (tp / len(actual_frauds)) * 100 if len(actual_frauds) > 0 else 0
    precision = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
    
    total_val = actual_frauds['amount'].sum()
    blocked_val = actual_frauds[actual_frauds['predicted_risk'] != 'NORMAL'] ['amount'].sum()

    print("\n" + "="*45)
    print(f"AUDYT SYSTEMU ANTYFRAUDOWEGO (N={len(df)})")
    print("="*45)
    print(f"SKUTECZNOŚĆ (Recall):    {recall:.1f}%  -> Ile oszustw wykryto")
    print(f"PRECYZJA (Precision):   {precision:.1f}%  -> Ile alertów było trafnych")
    print(f"BŁĘDNE ALERTY (FP):     {fp} szt.  -> Tylu klientów zdenerwowaliśmy")
    print("-" * 45)
    print(f"Wartość zagrożona:      {total_val:,.2f} PLN")
    print(f"Wartość zablokowana:    {blocked_val:,.2f} PLN")
    print(f"Wyciek (Loss):          {total_val - blocked_val:,.2f} PLN")
    print("="*45)

# --- 4. URUCHOMIENIE ---
if __name__ == "__main__":
    raw_data = generate_fintech_data(CONFIG)
    analyzed_data = analyze_transactions(raw_data, CONFIG)
    run_full_audit(analyzed_data)
    
    # Wykres (Poprawiony błąd palette/hue)
    plt.figure(figsize=(10, 5))
    sns.countplot(data=analyzed_data, x='predicted_risk', hue='predicted_risk', palette='coolwarm', legend=False)
    plt.title(f"Rozkład alertów dla N={CONFIG['num_transactions']}")
    plt.show()