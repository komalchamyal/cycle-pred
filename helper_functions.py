import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

# Load and preprocess data
def load_cycle_data(file_path):
    if str(file_path).endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df = df.sort_values('start_date').reset_index(drop=True)
    df['cycle_length'] = df['start_date'].diff().dt.days
    return df

# Compute train-test split
def train_test_split(cycle_lengths, train_ratio=0.8):
    train_size = int(len(cycle_lengths) * train_ratio)
    train = cycle_lengths[:train_size]
    test = cycle_lengths[train_size:]
    return train, test

# Moving Average forecast
def moving_average_forecast(train, test, window=12):
    ma_forecast = []
    train_list = train.tolist()
    for i in range(len(test)):
        ma_pred = np.mean(train_list[-window:])
        ma_forecast.append(ma_pred)
        train_list.append(test.iloc[i])  # update sequence
    return np.array(ma_forecast)

# Compute metrics
def compute_metrics(y_true, y_pred, tol=3):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    accuracy = 100 - mape
    within_tol = (np.abs(y_true - y_pred) <= tol).mean() * 100
    return mae, rmse, mape, accuracy, within_tol

# Predict next N cycles with optional override
def predict_next_cycles(cycle_lengths, last_start, window=12, n_cycles=5, override_date=None):
    next_cycles = []
    last_cycles = cycle_lengths.tolist()

    if override_date is not None:
        override_date = pd.to_datetime(override_date)
        first_length = (override_date - last_start).days
        next_cycles.append((override_date.date(), first_length))
        last_cycles.append(first_length)
        last_start = override_date

    for i in range(n_cycles if override_date is None else n_cycles-1):
        next_length = np.mean(last_cycles[-window:])
        next_start = last_start + pd.Timedelta(days=round(next_length))
        next_cycles.append((next_start.date(), round(next_length)))
        last_cycles.append(next_length)
        last_start = next_start

    return next_cycles