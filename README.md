# 🚀 Operations-Driven Data Engineering Portfolio

Witaj! To repozytorium dokumentuje moją ścieżkę przejścia z operacji logistycznych (**Amazon Operations**) do budowy skalowalnych rozwiązań **Data Engineering**. Tworzę narzędzia inspirowane realnymi wyzwaniami łańcucha dostaw, koncentrując się na generowaniu danych syntetycznych, modelowaniu ryzyka i automatyzacji audytu.

---

## 📂 Przegląd Projektów

### 🛡️ [Cyber-Security Anomaly Detection](./cyber_security_eda/)
**Generowanie syntetycznych logów do ewaluacji modeli AI pod kątem bezpieczeństwa.**
* **Logika biznesowa:** Symulacja ataku typu **Brute-Force** (Status 401) ukrytego w szumie ponad 2000 logów serwera.
* **Impact:** Dostarczanie zbiorów typu "Ground Truth" oraz definicji zadań dla LLM, aby benchmarkować rozumowanie AI w wykrywaniu zagrożeń.
* **Stack:** `Python`, `JSON`, `Seaborn`.

### 🌐 [Global Supply Chain Analytics](./supply_chain_analytics/)
**Modelowanie predykcyjne opóźnień w dostawach dla 50,000 przesyłek międzynarodowych.**
* **Logika biznesowa:** Stochastyczna symulacja kongestii w portach i zakłóceń pogodowych na szlakach morskich.
* **Impact:** Kwantyfikacja **"Total Value at Risk"**, umożliwiająca priorytetyzację ładunków o wysokiej wartości podczas zatorów.
* **Stack:** `Python 3.12+`, `Pandas`, `Seaborn`.

### 💳 [Fintech Fraud Detection Engine](./fintech_fraud_engine/)
**Symulacja 100,000 transakcji w celu testowania wzorców wykrywania anomalii.**
* **Logika biznesowa:** Scenariusze "Impossible Travel" oraz przejęć kont (Account Takeover - ATO).
* **Impact:** Identyfikacja sygnatur oszustw na wolumenie transakcyjnym rzędu **~2.4 mln PLN**.
* **Stack:** `Python`, `NumPy`, `Seaborn`.

### 📦 [Inventory Quality Audit (ICQA) Logic](./inventory_quality_audit/)
**Automatyzacja wykrywania anomalii w logistyce magazynowej (Digitalizacja Quality Workflows).**
* **Logika biznesowa:** Wykrywanie stanów ujemnych, niespójności w lokalizacjach (bins) i wzorców "dirty data".
* **Kontekst:** Pythonowa automatyzacja procesów identyfikacji rozbieżności oparta na doświadczeniu w **Amazon**.
* **Stack:** `Python`, `Pandas`, `XlsxWriter`.

---

## 🛠️ Stack Techniczny i Kompetencje

| Kategoria | Technologie |
| :--- | :--- |
| **Języki** | Python 3.12+ (Zarządzanie przez `uv`) |
| **Data Processing** | Zaawansowany Pandas (operacje wektorowe, Time-series), NumPy |
| **Wizualizacja** | Seaborn, Matplotlib (Heatmapy ryzyka, rozkłady gęstości) |
| **AI/LLM** | Projektowanie specyfikacji promptów do ewaluacji modeli |

---

## ⚙️ Szybki Start (Quick Start)

1.  **Sklonuj repozytorium:**
    ```bash
    git clone [https://github.com/PMSeekers/synthetic-data-eda-1.git](https://github.com/PMSeekers/synthetic-data-eda-1.git)
    cd synthetic-data-eda-1
    ```

2.  **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uruchom wybrany moduł (przykład):**
    ```bash
    python cyber_security_eda/synthetic_security_eda.py
    ```


