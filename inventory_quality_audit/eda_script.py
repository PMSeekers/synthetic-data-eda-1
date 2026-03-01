import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime

# --- 1. POBIERANIE DANYCH WEJŚCIOWYCH ---
def get_data(file_path="dane_magazynowe.xlsx"):
    """Wczytuje arkusz stanów magazynowych lub generuje szablon operacyjny."""
    if os.path.exists(file_path):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Wczytywanie danych z pliku: {file_path}")
        return pd.read_excel(file_path)
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ALERT: Brak pliku wejściowego. Generowanie szablonu...")
        data = {
            'item_id': [101, 102, 103, 104, 105],
            'stock_count': [50, -5, 120, None, 5000],
            'category': ['Electronics', 'Home', 'Electronics', 'Toys', 'Toys'],
            'unit_price': [100, 20, 100, 15, 10]
        }
        df_template = pd.DataFrame(data)
        df_template.to_excel(file_path, index=False)
        print(f"[OK] Szablon 'dane_magazynowe.xlsx' został utworzony.")
        return df_template

# --- 2. LOGIKA AUDYTU ICQA (Inventory Control & Quality Assurance) ---
def audit_logic(df):
    """Weryfikacja spójności danych i wykrywanie błędów w stanach."""
    def detect_z_score(group):
        std = group.std()
        return (group - group.mean()) / std if (pd.notna(std) and std != 0) else 0

    df['z_score'] = df.groupby('category')['stock_count'].transform(detect_z_score)

    def check_row(row):
        issues = []
        val = row['stock_count']
        if pd.isnull(val): issues.append("BRAK_DANYCH")
        elif val < 0: issues.append("STAN_UJEMNY")
        elif abs(row['z_score']) > 1.5: issues.append("ODCHYLENIE_STAT")
        elif val > 1000: issues.append("NADSTAN")
        return ", ".join(issues) if issues else "POPRAWNY"

    df['audit_status'] = df.apply(check_row, axis=1)

    # Definiowanie wymaganych działań operacyjnych
    df['required_action'] = df['audit_status'].apply(
        lambda x: "PILNE: PRZELICZENIE" if any(err in x for err in ["BRAK_DANYCH", "STAN_UJEMNY"]) 
        else ("WERYFIKACJA_KIEROWNICZA" if "ODCHYLENIE" in x else "BRAK")
    )

    # Przygotowanie danych do procesów analitycznych (czyszczenie)
    df['stock_cleaned'] = df.groupby('category')['stock_count'].transform(lambda x: x.fillna(x.median()))
    df.loc[df['stock_cleaned'] < 0, 'stock_cleaned'] = 0
    
    return df

# --- 3. ANALIZA WARTOŚCIOWA ABC ---
def abc_analysis(df):
    """Klasyfikacja asortymentu według kryterium Pareto (wartość zapasu)."""
    df['total_value'] = df['stock_count'].fillna(0) * df['unit_price']
    df = df.sort_values(by='total_value', ascending=False).reset_index(drop=True)
    
    cumulative_value = df['total_value'].cumsum()
    total_sum = df['total_value'].sum()
    df['cumulative_percentage'] = (cumulative_value / total_sum * 100) if total_sum > 0 else 0

    def classify_abc(percentage):
        if percentage <= 80: return 'A (Kluczowe)'
        elif percentage <= 95: return 'B (Średnie)'
        else: return 'C (Niskie)'

    df['abc_class'] = df['cumulative_percentage'].apply(classify_abc)
    return df

# --- 4. ANALIZA ROTACJI I TRENDÓW (DOH - Days on Hand) ---
def trend_analysis(df):
    """Prognozowanie dostępności zapasów na podstawie średniej sprzedaży."""
    if 'daily_sales' not in df.columns:
        # Symulacja średniej sprzedaży dziennej
        df['daily_sales'] = np.random.uniform(1, 20, size=len(df))
    
    # Obliczanie pokrycia zapasem (DOH)
    df['days_on_hand'] = df['stock_cleaned'] / df['daily_sales']
    
    def detect_trend(row):
        if row['days_on_hand'] < 5: return "RYZYKO_BRAKU"
        elif row['days_on_hand'] > 180: return "MARTWY_ZAPAS"
        else: return "OPTYMALNY"
        
    df['inventory_trend'] = df.apply(detect_trend, axis=1)
    return df

# --- 5. RAPORTOWANIE I EKSPORT ---
def print_business_summary(df):
    """Wyświetla podsumowanie KPI w konsoli."""
    total_risk_val = df[df['audit_status'] != 'POPRAWNY']['risk_value'].sum()
    issue_count = len(df[df['audit_status'] != 'POPRAWNY'])
    
    print("\n" + "="*50)
    print("   RAPORT OPERACYJNY: KONTROLA ZAPASÓW")
    print("="*50)
    print(f"Liczba wykrytych nieścisłości:  {issue_count} pozycji")
    print(f"Wartość zapasu objęta ryzykiem: {total_risk_val:,.2f} PLN")
    print("-" * 50)

def export_to_excel(df, filename="Raport_Magazynowy_Final.xlsx"):
    """Zapisuje dane do pliku Excel z automatycznym formatowaniem warunkowym."""
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Analiza_Audyt', index=False)
    
    workbook  = writer.book
    worksheet = writer.sheets['Analiza_Audyt']

    # Formaty kolorystyczne dla czytelności raportu
    red_fmt = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    yellow_fmt = workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C6500'})

    for row_num in range(1, len(df) + 1):
        status = df.iloc[row_num-1]['audit_status']
        if any(err in status for err in ["BRAK", "UJEMNY"]):
            worksheet.set_row(row_num, None, red_fmt)
        elif "ODCHYLENIE" in status:
            worksheet.set_row(row_num, None, yellow_fmt)

    writer.close()
    print(f"\n[SUKCES] Raport końcowy wygenerowany: {filename}")

# --- URUCHOMIENIE PROCESU ---
if __name__ == "__main__":
    FILE_NAME = "moje_zapas_testowe.xlsx" 
    
    # Przebieg procesu analitycznego
    df_raw = get_data(FILE_NAME)
    df_raw['risk_value'] = df_raw['stock_count'].fillna(0) * df_raw['unit_price']
    
    df_audited = audit_logic(df_raw)
    df_abc = abc_analysis(df_audited)
    df_final = trend_analysis(df_abc)
    
    # Raportowanie wyników
    print_business_summary(df_final)
    
    print("POZYCJE KRYTYCZNE (NISKIE POKRYCIE ZAPASEM):")
    critical_items = df_final[df_final['inventory_trend'] == "RYZYKO_BRAKU"]
    print(critical_items[['item_id', 'abc_class', 'days_on_hand']].head())
    
    export_to_excel(df_final)