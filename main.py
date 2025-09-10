import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import plotly.graph_objs as go
import os

# === Functions import ===
from helper_functions import *

# === Streamlit App ===
st.set_page_config(page_title="PCOD Cycle Predictor", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Data & Input", "Model Performance", "Forecast Next Cycles", "Override Cycle"])

# Always use startDates.csv
file_source = 'startDates.csv'

# --- Load data into session ---
if "df" not in st.session_state:
    if os.path.exists(file_source):
        st.session_state.df = load_cycle_data(file_source)
    else:
        st.error("startDates.csv not found. Please make sure the file exists in the app directory.")
        st.stop()

# Work with session dataframe
df = st.session_state.df
cycle_lengths = df['cycle_length'].dropna().reset_index(drop=True)
train, test = train_test_split(cycle_lengths, train_ratio=0.8)

window = st.sidebar.number_input("Moving Average Window", min_value=1, max_value=20, value=12, step=1)

# === Data & Input Page ===
if page == "Data & Input":
    st.header("Cycle so far")

    fig_input = go.Figure()
    cycle_lengths = df['cycle_length'].dropna().reset_index(drop=True)
    dates_for_lengths = df['start_date'].iloc[1:].reset_index(drop=True)

    fig_input.add_trace(go.Scatter(
        x=dates_for_lengths,
        y=cycle_lengths,
        mode='lines+markers',
        name='Cycle Lengths'
    ))

    fig_input.update_layout(
        title='Input Cycle Lengths',
        xaxis_title='Date',
        yaxis_title='Cycle Length (days)'
    )
    st.plotly_chart(fig_input, use_container_width=True)


# === Model Performance Page ===
elif page == "Model Performance":
    ma_forecast_test = moving_average_forecast(train, test, window=window)
    mae, rmse, mape, acc, tol3 = compute_metrics(test, ma_forecast_test)
    st.header("Model Performance on Test Data")
    st.write(f"MAE: {mae:.2f}")
    st.write(f"RMSE: {rmse:.2f}")
    st.write(f"MAPE: {mape:.2f}%")
    st.write(f"Accuracy: {acc:.2f}%")
    st.write(f"±3-day Accuracy: {tol3:.2f}%")

# === Forecast Page ===
elif page == "Forecast Next Cycles":
    next_cycles = predict_next_cycles(
        cycle_lengths,
        df['start_date'].iloc[-1],
        window=window,
        n_cycles=5,
        override_date=None
    )
    st.header("Predicted Next 5 Cycles")
    for i, (date, length) in enumerate(next_cycles, 1):
        st.write(f"Cycle {i}: {date} ({length} days)")

    # Align input cycle lengths with dates (skip first date for diff)
    cycle_lengths = df['cycle_length'].dropna().reset_index(drop=True)
    dates_for_lengths = df['start_date'].iloc[1:].reset_index(drop=True)

    # Forecast series
    forecast_dates = [dates_for_lengths.iloc[-1]]  # last input cycle date
    forecast_values = [cycle_lengths.iloc[-1]]
    for date, length in next_cycles:
        forecast_dates.append(pd.to_datetime(date))
        forecast_values.append(length)

    # Plot
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=dates_for_lengths,
        y=cycle_lengths,
        mode='lines+markers',
        name='Input Cycle Lengths'
    ))
    fig_forecast.add_trace(go.Scatter(
        x=forecast_dates,
        y=forecast_values,
        mode='lines+markers',
        name='Forecasted Cycles'
    ))
    fig_forecast.update_layout(
        title='Cycle Length Time Series with Forecast',
        xaxis_title='Date',
        yaxis_title='Cycle Length (days)'
    )
    st.plotly_chart(fig_forecast, use_container_width=True)


# === Override Page ===
elif page == "Override Cycle":
    if "override_success" in st.session_state:
        st.success(st.session_state.override_success)
        del st.session_state["override_success"]  # clear after showing once

    st.header("Override Cycle Start Date")
    last_date = df['start_date'].iloc[-1]
    st.write(f"Last recorded cycle start date: **{last_date.date()}**")

    override_date_input = st.text_input("Enter new cycle start date (YYYY-MM-DD)")
    if override_date_input:
        try:
            override_date = pd.to_datetime(override_date_input)
            new_cycle_length = (override_date - last_date).days
            st.write(f"Computed cycle length: **{new_cycle_length} days**")

            if st.button("Confirm and Save Override"):
                new_row = pd.DataFrame({"start_date": [override_date]})
                df_save = pd.concat([st.session_state.df[['start_date']], new_row], ignore_index=True)
                df_save.to_csv(file_source, index=False)

                st.session_state.df = load_cycle_data(file_source)
                # set a flag so next run shows success
                st.session_state["override_success"] = f"Override saved! Added {override_date.date()} as new cycle start date."
                st.rerun()

        except Exception as e:
            st.error(f"Invalid date format: {e}")