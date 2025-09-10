# 🩺 PCOD Cycle Predictor

A Streamlit-based app that helps predict menstrual cycle dates for users with PCOD (Polycystic Ovarian Disease).  
It uses a **Moving Average (MA) model** to forecast upcoming cycles based on historical cycle start dates.

---

## 📂 Project Structure

```
.
├── startDates.csv          # Input data file with cycle start dates (one column: start_date)
├── helper_functions.py     # Utility functions (data loading, MA forecast, metrics, etc.)
├── app.py                  # Main Streamlit application
└── README.md               # Project documentation
```

---

## ⚙️ Features

- 📊 **Input Data Visualization**: Interactive time series graph of past cycles.  
- 📈 **Model Performance Page**: Evaluate forecast accuracy using metrics like MAE, RMSE, MAPE, and ±3-day accuracy.  
- 🔮 **Forecast Next Cycles**: Predict the next 5 cycles with moving average.  
- ✍️ **Override Cycle Dates**: Manually add a new cycle start date (e.g., if actual differs from prediction).  
- 💾 **Persistent Data**: Overrides are appended to `startDates.csv` so the model always trains on the latest data.  
- 🎨 **User-Friendly UI**: Clean sidebar navigation, interactive Plotly charts.

---

## 📊 Data Format

The input file (`startDates.csv`) must have only one column:

```csv
start_date
2023-01-01
2023-01-28
2023-02-20
...
```

- Each row is the **start date of a cycle**.
- Cycle lengths are automatically computed as the difference between consecutive dates.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pcod-cycle-predictor.git
cd pcod-cycle-predictor
```

### 2. Install dependencies
It’s recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:
```
streamlit
pandas
numpy
scikit-learn
plotly
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open in browser
Navigate to: [http://localhost:8501](http://localhost:8501)

---

## 📑 Pages Overview

### 🔹 Data & Input
- Displays interactive time series of recorded cycles.
- Shows how cycle lengths vary over time.

### 🔹 Model Performance
- Trains a **Moving Average model** on your data.
- Reports metrics:
  - **MAE** (Mean Absolute Error)
  - **RMSE** (Root Mean Squared Error)
  - **MAPE** (Mean Absolute Percentage Error)
  - **±3-day accuracy** (fraction of predictions within 3 days of actual)

### 🔹 Forecast Next Cycles
- Predicts the next 5 cycles based on your history.
- Shows both historical and forecasted cycles on the same chart.

### 🔹 Override Cycle
- Allows you to manually enter the **actual start date** of your latest cycle.
- Appends it to `startDates.csv`.
- Refreshes all charts and forecasts automatically.

---

## 🧠 Model Used

- **Moving Average (MA)** is chosen because:
  - Simple and interpretable.
  - Works well with limited data (~40 data points).
  - Outperformed ARIMA in ±3-day accuracy during testing.

Future versions can integrate:
- ARIMA / Prophet
- Hybrid ML + statistical models
- Personalized seasonal adjustments

---

## 🛠️ Notes & Best Practices

- Always keep `startDates.csv` updated — forecasts depend heavily on data quality.  
- If you override with a new cycle date, the app **automatically retrains** using the latest data.  
- Best accuracy is achieved with a **window size of 3–12** depending on your data variance.  
- This tool is **not medical advice** — it’s a data-driven aid for personal use.

---

## 📌 Example Forecast

If your last cycle was on **2025-09-09**, the app might predict:

```
Cycle 1: 2025-09-09 (actual override)
Cycle 2: 2025-10-14 (35 days)
Cycle 3: 2025-11-16 (33 days)
Cycle 4: 2025-12-20 (34 days)
Cycle 5: 2026-01-23 (34 days)
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgments

- Built with [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/), and [scikit-learn](https://scikit-learn.org/).
- Inspired by the need to help women with **PCOD** better understand and track their cycles.
