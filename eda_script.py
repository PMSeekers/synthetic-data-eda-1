import pandas as pd

# 1. Tworzymy udawane dane 
data = {
    'item_id': [101, 102, 103, 104, 105],
    'stock_count': [50, -5, 120, None, 80],  # Błędy: ujemna wartość i brak danych
    'category': ['Electronics', 'Home', 'Electronics', 'Toys', 'Home']
}

df = pd.DataFrame(data)

# 2. EDA: Szukamy anomalii 
print("--- Raport jakości danych ---")
missing = df.isnull().sum().sum()
anomalies = df[df['stock_count'] < 0]

print(f"Znalezione braki danych: {missing}")
print(f"Znalezione ujemne stany magazynowe:\n{anomalies}")

# 3. Czyszczenie danych (Automatyzacja)
df['stock_count'] = df['stock_count'].fillna(0) # Naprawa braków
print("\nDane po automatycznej korekcie:")
print(df)