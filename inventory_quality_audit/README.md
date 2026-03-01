📦 Inventory Quality Audit (ICQA) & Anomaly Detection
🎯 Project Overview
Ten projekt to zautomatyzowany system audytu stanów magazynowych, inspirowany standardami Amazon ICQA (Inventory Control & Quality Assurance). Skrypt przekłada moją wiedzę operacyjną na skalowalne rozwiązanie programistyczne, które identyfikuje błędy techniczne w danych logistycznych i przygotowuje je do dalszej analizy lub trenowania modeli AI.

🚀 Key Features
🔍 Automated Anomaly Detection
Z-Score Analysis: Statystyczne wykrywanie odchyleń w ilościach towaru (Outliers).

Logical Validation: Natychmiastowe flagowanie stanów ujemnych oraz nadstanów (Critical Issues).

Missing Data Recovery: Automatyczna imputacja brakujących rekordów na podstawie mediany kategorii, zapewniająca ciągłość zbioru danych.

📊 Business Intelligence & Reporting
ABC Analysis: Klasyfikacja asortymentu według zasady Pareto (Kluczowe vs Niskie zapasy).

DOH (Days on Hand): Prognozowanie trendów wyczerpania zapasów i wykrywanie "martwego towaru".

Excel Automation: Generowanie raportu z automatycznym kolorowaniem rekordów wymagających pilnej interwencji.

💼 Business Context: From Amazon to Code
W latach 2025-2026 w Amazon odpowiadałem za identyfikację błędów technicznych w systemach magazynowych. Ten skrypt to cyfrowa transformacja tamtych procesów:

Manual Logic → Python Script: Zamiast ręcznego filtrowania, algorytm wykonuje audyt w milisekundy.

Scalability: Narzędzie radzi sobie z tysiącami rekordów, które mogą służyć jako czyste dane wejściowe dla modeli LLM.

🛠️ Tech Stack
Language: Python 3.x

Core Libraries: Pandas (Data manipulation), NumPy (Stats), XlsxWriter (Reporting).

Visualization: Seaborn, Matplotlib.

Environment: VS Code.

⚙️ How to Run
Upewnij się, że masz zainstalowane biblioteki:

Bash
pip install pandas numpy openpyxl xlsxwriter
Uruchom skrypt główny:

Bash
python eda_script.py
Sprawdź wygenerowany plik Raport_Magazynowy_Final.xlsx.
