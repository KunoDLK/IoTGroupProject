import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load CSV data
INPUT_CSV = "mock_bin_data.csv"
df_hist = pd.read_csv(INPUT_CSV, parse_dates=['timestamp'])

# Configuration
MAX_WEIGHT = 25  # kg
MIN_PROXIMITY = 1  # cm

# Initialize summaries
summaries = []

# ML-based prediction for each bin
for bin_id, group in df_hist.groupby('bin_id'):
    group = group.sort_values('timestamp')
    group['days'] = (group['timestamp'] - group['timestamp'].min()).dt.days

    X = group[['days']].values
    y_weight = group['weight'].values
    y_proximity = group['proximity'].values

    # Fit linear regression models
    weight_model = LinearRegression().fit(X, y_weight)
    proximity_model = LinearRegression().fit(X, y_proximity)

    current_day = group['days'].iloc[-1]
    current_weight = y_weight[-1]
    current_proximity = y_proximity[-1]

    weight_rate = weight_model.coef_[0]
    proximity_rate = proximity_model.coef_[0]

    # Predict days to full
    days_to_full = (MAX_WEIGHT - current_weight) / weight_rate if weight_rate > 0 else np.inf
    days_to_closure = (MIN_PROXIMITY - current_proximity) / proximity_rate if proximity_rate < 0 else np.inf

    # Summary based on ML prediction
    summary = (
        f"\n📦 {bin_id}:\n"
        f"- Current weight: {current_weight:.1f} kg → Predicted fill rate: {weight_rate:.2f} kg/day.\n"
        f"- Est. time to full (25kg): {days_to_full:.1f} days.\n"
        f"- Current proximity: {current_proximity:.1f} cm → Predicted change rate: {proximity_rate:.2f} cm/day.\n"
        f"- Est. time to lid closure (1 cm): {days_to_closure:.1f} days.\n"
        f"- Summary: {'⚠️ Needs urgent collection.' if min(days_to_full, days_to_closure) <= 3 else '✅ Collection not yet urgent.'}"
    )

    summaries.append(summary)

# Print summaries
for s in summaries:
    print(s)
