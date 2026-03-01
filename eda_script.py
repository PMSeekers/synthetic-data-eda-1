import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- 1. POBIERANIE DANYCH ---
def get_data():
    data = {
        'item_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'stock_count': [50, -5, 120, None, 80, 5000, 45, 55, 60, 65],
        'category': ['Electronics', 'Home', 'Electronics', 'Toys', 'Home', 'Toys', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
        'unit_price': [100, 20, 100, 15, 20, 10, 100, 105, 95, 90]
    }
    return pd.DataFrame(data)

# --- 2. ANALIZA I LOGIKA AUDYTU ---
def audit_logic(df):
    # Statystyka: Z-Score (wykrywa czy liczba "pasuje" do reszty w kategorii)
    def detect_z_score(group):
        std = group.std()
        return (group - group.mean()) / std if (pd.notna(std) and std != 0) else 0

    df['z_score'] = df.groupby('category')['stock_count'].transform(detect_z_score)

    # Flagowanie błędów
    def check_row(row):
        issues = []
        val = row['stock_count']
        if pd.isnull(val): issues.append("MISSING")
        elif val < 0: issues.append("NEGATIVE")
        elif abs(row['z_score']) > 1.5: issues.append("STAT_ANOMALY")
        elif val > 1000: issues.append("OUTLIER")
        return ", ".join(issues) if issues else "CLEAN"

    df['audit_status'] = df.apply(check_row, axis=1)

    # Akcje biznesowe
    df['required_action'] = df['audit_status'].apply(
        lambda x: "URGENT_RECOUNT" if any(err in x for err in ["MISSING", "NEGATIVE"]) 
        else ("SUPERVISOR_CHECK" if "ANOMALY" in x else "NONE")
    )

    # Czyszczenie danych do analizy
    df['stock_cleaned'] = df.groupby('category')['stock_count'].transform(lambda x: x.fillna(x.median()))
    df.loc[df['stock_cleaned'] < 0, 'stock_cleaned'] = 0
    
    return df

# --- 3. WIZUALIZACJA ---
def visualize_anomalies(df):
    plt.figure(figsize=(10, 6))
    # Przygotowanie danych do wykresu (zastąpienie None zerem tylko dla osi Y)
    plot_df = df.copy()
    plot_df['stock_display'] = plot_df['stock_count'].fillna(0)
    
    sns.scatterplot(data=plot_df, x='item_id', y='stock_display', hue='audit_status', 
                    palette='viridis', size='stock_cleaned', sizes=(50, 300))
    
    plt.axhline(0, color='red', lw=1, ls='--')
    plt.title("System ICQA: Wykrywanie anomalii w zapasach")
    plt.grid(True, alpha=0.3)
    plt.show()

# --- URUCHOMIENIE PROGRAMU ---
if __name__ == "__main__":
    df_inventory = get_data()
    df_audited = audit_logic(df_inventory)
    
    print("\n--- FINALNY RAPORT AUDYTU ---")
    print(df_audited[['item_id', 'category', 'stock_count', 'audit_status', 'required_action']])
    
    visualize_anomalies(df_audited)