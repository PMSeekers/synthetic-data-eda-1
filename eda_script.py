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
    
# --- 4. EKSPORT DO EXCELA Z FORMATOWANIEM ---
def export_to_excel(df, filename="Raport_ICQA.xlsx"):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Audyt', index=False)
    
    workbook  = writer.book
    worksheet = writer.sheets['Audyt']

    # Definiujemy formaty kolorów
    red_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    orange_format = workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C6500'})

    # Automatyczne kolorowanie wierszy na podstawie statusu
    for row_num in range(1, len(df) + 1):
        status = df.iloc[row_num-1]['audit_status']
        if any(err in status for err in ["NEGATIVE", "MISSING"]):
            worksheet.set_row(row_num, None, red_format)
        elif "ANOMALY" in status:
            worksheet.set_row(row_num, None, orange_format)

    writer.close()
    print(f"\n[SUKCES] Raport został zapisany jako: {filename}")

# --- 5. PODSUMOWANIE DLA MANAGERA ---
def print_business_summary(df):
    total_risk = df[df['audit_status'] != 'CLEAN']['risk_value'].sum()
    issue_count = len(df[df['audit_status'] != 'CLEAN'])
    
    print("-" * 30)
    print(f"PODSUMOWANIE OPERACYJNE:")
    print(f"Liczba wykrytych problemów: {issue_count}")
    print(f"Wartość towaru objęta ryzykiem błędu: {total_risk:.2f} PLN")
    print("-" * 30)
    
# --- URUCHOMIENIE PROGRAMU ---
if __name__ == "__main__":
    # 1. Pobierz dane
    df_inventory = get_data()
    
    # 2. Oblicz ryzyko finansowe (tutaj, żeby dane były gotowe dla audytu)
    df_inventory['risk_value'] = df_inventory['stock_count'].fillna(0) * df_inventory['unit_price']
    
    # 3. Przeprowadź analizę audytową
    df_audited = audit_logic(df_inventory)
    
    # 4. Wyświetl analizę biznesową w konsoli
    print_business_summary(df_audited)
    
    # 5. Wygeneruj wykres
    visualize_anomalies(df_audited)
    
    # 6. Wyślij raport do pliku Excel
    export_to_excel(df_audited)