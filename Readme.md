# 🩺 PCOD Cycle Predictor

A Streamlit-based ML powered application to analyze menstrual cycle data and predict upcoming cycles for PCOD patients.
Access the live app here: [https://pcod-cycle-prediction.streamlit.app/](https://pcod-cycle-prediction.streamlit.app/)

---
---

## 📌 Overview
This project started with exploratory work in **`dev.ipynb`**, where I experimented with multiple forecasting and machine learning models:

- ARIMA  
- Exponential Smoothing  
- Linear Regression  
- Random Forest  
- XGBoost  
- Moving Average (MA)  
- Weighted Moving Average (WMA)  

### 🔍 Why Moving Average?
- **MA performed best for ±3-day accuracy**, which is the most clinically useful metric.  
- Other models (e.g., ARIMA, XGBoost) sometimes gave higher overall accuracy, but MA consistently gave more **reliable short-window predictions**.  
- MA is also interpretable, simple, and robust for the dataset size.  

If more data is collected in the future, advanced models (like ARIMA or XGBoost) could be reconsidered.

---

## 🚀 Features
- Use default **cycle start date data** (`startDates.csv`).  
- Visualize input cycle lengths with interactive Plotly graphs.  
- Evaluate model performance (MAE, RMSE, MAPE, accuracy, ±3-day accuracy).  
- Predict the next **5 upcoming cycles**.  
- Override the predicted next cycle date → retrains forecast automatically.  
- Sidebar navigation with multiple pages:
  - Data & Input  
  - Model Performance  
  - Forecast Next Cycles  
  - Override Cycle  

---

## 🛠️ Tech Stack
- **Python** (pandas, numpy, scikit-learn)  
- **Streamlit** for UI  
- **Plotly** for interactive charts  

---

## 📂 Project Structure
```
├── dev.ipynb              # Experiments with multiple models
├── app.py                 # Streamlit app (final)
├── helper_functions.py    # Reusable functions for preprocessing, metrics, forecast
├── startDates.csv         # Default cycle start dates dataset
└── README.md              # Project documentation
```

---

## ▶️ Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 📈 Future Work
- Incorporate **larger datasets** for advanced models (ARIMA, XGBoost).  
- Add personalized factors (symptoms, lifestyle) for more contextual predictions.  
- Deploy as a **mobile-friendly app** for patient usage.
