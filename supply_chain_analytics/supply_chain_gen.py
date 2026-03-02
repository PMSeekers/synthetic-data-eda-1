import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# --- 1. KONFIGURACJA SYMULACJI ---
N_SHIPMENTS = 50000
START_DATE = datetime(2025, 1, 1)

def generate_supply_chain_data():
    np.random.seed(42)
    
    # Baza portów i miast docelowych
    origins = ['Shanghai', 'Singapore', 'Shenzhen', 'Busan', 'Dubai']
    destinations = ['Gdańsk', 'Hamburg', 'Rotterdam', 'Antwerp', 'Felixstowe']
    modes = ['Sea', 'Air', 'Rail']
    
    data = {
        'shipment_id': [f"SHP-{100000 + i}" for i in range(N_SHIPMENTS)],
        'origin': np.random.choice(origins, N_SHIPMENTS),
        'destination': np.random.choice(destinations, N_SHIPMENTS),
        'shipping_mode': np.random.choice(modes, N_SHIPMENTS, p=[0.7, 0.1, 0.2]),
        'unit_weight': np.random.uniform(10, 500, N_SHIPMENTS), # kg
        'cargo_value_usd': np.random.uniform(500, 50000, N_SHIPMENTS)
    }

    df = pd.DataFrame(data)

    # --- 2. SYMULACJA CZASU I OPÓŹNIEŃ (LOGIKA BIZNESOWA) ---
    df['shipment_date'] = [START_DATE + timedelta(days=np.random.randint(0, 365)) for _ in range(N_SHIPMENTS)]
    
    conditions = [
        (df['shipping_mode'] == 'Sea'),
        (df['shipping_mode'] == 'Air'),
        (df['shipping_mode'] == 'Rail')
    ]
    choices = [35, 5, 18] 
    df['base_lead_time'] = np.select(conditions, choices)

    df['delay_days'] = 0
    # Symulacja zatoru w Szanghaju
    shanghai_mask = df['origin'] == 'Shanghai'
    df.loc[shanghai_mask, 'delay_days'] += np.random.randint(3, 11, size=shanghai_mask.sum())
    
    # Symulacja pogody na morzu
    sea_weather_delay = (df['shipping_mode'] == 'Sea') & (np.random.random(N_SHIPMENTS) > 0.85)
    df.loc[sea_weather_delay, 'delay_days'] += np.random.randint(2, 7, size=sea_weather_delay.sum())

    df['estimated_arrival'] = df.apply(lambda x: x['shipment_date'] + timedelta(days=x['base_lead_time']), axis=1)
    df['actual_arrival'] = df.apply(lambda x: x['estimated_arrival'] + timedelta(days=x['delay_days']), axis=1)

    # --- 3. ANALIZA RYZYKA ---
    df['is_delayed'] = df['delay_days'] > 0
    df['risk_score'] = (df['delay_days'] * 10) + (df['cargo_value_usd'] / 10000)

    return df

# --- 4. URUCHOMIENIE I RAPORTOWANIE ---
# --- 4. URUCHOMIENIE I RAPORTOWANIE ---
if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Generowanie 50k rekordów Supply Chain...")
    df_logistics = generate_supply_chain_data()
    
    # --- NOWA ANALIZA: KPI BIZNESOWE ---
    total_value_at_risk = df_logistics[df_logistics['is_delayed']]['cargo_value_usd'].sum()
    delayed_count = df_logistics['is_delayed'].sum()
    
    print("-" * 30)
    print(f"💰 TOTAL VALUE AT RISK: ${total_value_at_risk:,.2f}")
    print(f"📦 DELAYED SHIPMENTS: {delayed_count} units")
    print("-" * 30)

    # Eksport danych
    df_logistics.to_csv("global_supply_chain_data.csv", index=False)
    print("[SUKCES] Dane zapisane w 'global_supply_chain_data.csv'.")
    
    # --- WIZUALIZACJA 1: Opóźnienia wg Portów ---
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    sns.barplot(x='origin', y='delay_days', data=df_logistics, palette="viridis", errorbar=None)
    plt.title('Average Shipping Delays by Origin Port (Simulation 2025)')
    plt.savefig('delay_analysis.png')
    print("[WIZUALIZACJA 1] Wykres opóźnień zapisany.")

# --- WIZUALIZACJA 1 ---
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    sns.barplot(x='origin', y='delay_days', data=df_logistics, palette="viridis", errorbar=None)
    plt.title('Average Shipping Delays by Origin Port (Simulation 2025)')
    plt.savefig('delay_analysis.png') # <--- To już masz
    plt.close() # Zamknij wykres, żeby nie nakładał się na następny

    # --- WIZUALIZACJA 2 ---
    plt.figure(figsize=(8, 6))
    numeric_cols = ['unit_weight', 'cargo_value_usd', 'base_lead_time', 'delay_days', 'risk_score']
    numeric_df = df_logistics[numeric_cols].corr()
    sns.heatmap(numeric_df, annot=True, cmap='RdYlGn', center=0)
    plt.title('Correlation Matrix: Logistics Factors vs Risk Score')
    plt.tight_layout()
    plt.savefig('correlation_map.png') # <--- TEGO SZUKAMY
    plt.close()

    # --- WIZUALIZACJA 3 ---
    plt.figure(figsize=(10, 5))
    sns.histplot(df_logistics['cargo_value_usd'], bins=50, kde=True, color='royalblue')
    plt.title('Distribution of Cargo Value (USD)')
    plt.savefig('cargo_distribution.png') # <--- TEGO TEŻ SZUKAMY
    plt.close()

    # --- DODATEK: ANALIZA STRAT PER PORT ---
    print("\n[RAPORT FINANSOWY PER PORT]")
    port_analysis = df_logistics.groupby('origin')['cargo_value_usd'].sum().sort_values(ascending=False)
    for port, value in port_analysis.items():
        print(f"📍 {port}: Total Cargo Value: ${value:,.2f}")

    print("\n" + "="*40)
    print("PROJEKT UKOŃCZONY POMYŚLNIE")
    print("="*40)