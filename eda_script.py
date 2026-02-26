import pandas as pd
import numpy as np

# 1. Rozszerzone dane (dodajemy więcej przypadków testowych)
data = {
    'item_id': [101, 102, 103, 104, 105, 106],
    'stock_count': [50, -5, 120, None, 80, 5000],  # Błędy: ujemne, None, outlier (anomalia ilościowa)
    'category': ['Electronics', 'Home', 'Electronics', 'Toys', 'Home', 'Toys'],
    'last_audit': ['2025-01-01', '2025-01-02', None, '2025-01-04', '2025-01-05', '2025-01-06']
}

df = pd.DataFrame(data)

# --- ETAP: AUDYT (IDENTYFIKACJA) ---

# Funkcja do flagowania anomalii (Metoda podobna do systemów ICQA)
def audit_data(row):
    issues = []
    if pd.isnull(row['stock_count']): issues.append("MISSING_DATA")
    if row['stock_count'] is not None and row['stock_count'] < 0: issues.append("NEGATIVE_STOCK")
    if row['stock_count'] is not None and row['stock_count'] > 1000: issues.append("OUTLIER_CHECK")
    return ", ".join(issues) if issues else "CLEAN"

df['audit_status'] = df.apply(audit_data, axis=1)

# --- ETAP: AUTOMATYCZNA KOREKTA (DATA CLEANING) ---

# 2. Inteligentne wypełnianie braków (np. medianą dla danej kategorii zamiast zerem)
df['stock_count_cleaned'] = df.groupby('category')['stock_count'].transform(lambda x: x.fillna(x.median()))

# 3. Korekta ujemnych wartości (Logika biznesowa: błąd systemowy -> ustaw 0 i wymagaj re-countu)
df.loc[df['stock_count'] < 0, 'stock_count_cleaned'] = 0

print("--- RAPORT AUDYTU JAKOŚCI ---")
print(df[['item_id', 'stock_count', 'audit_status']])

print("\n--- DANE PO TRANSFORMACJI (GOTOWE DO ANALIZY/LLM) ---")
print(df[['item_id', 'category', 'stock_count_cleaned', 'audit_status']])