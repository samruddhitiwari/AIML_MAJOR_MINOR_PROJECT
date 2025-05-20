import zipfile
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# -------------------- Step 1: Extract ZIP and Read CSV -------------------- #

# Replace with your actual zip file name
zip_path = "your_dataset.zip"
extract_path = "extracted_data"

# Extract ZIP file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)
print("✅ ZIP Extracted Successfully!")

# List all extracted files
files = os.listdir(extract_path)
print("📂 Extracted Files:", files)

# Detect CSV file in the extracted folder
csv_file = [f for f in files if f.endswith('.csv')][0]
csv_path = os.path.join(extract_path, csv_file)

# Load CSV data into a DataFrame
df = pd.read_csv(csv_path)
print("📊 CSV Data Sample:\n", df.head())

# -------------------- Step 2: Data Preprocessing -------------------- #

# Select only 'Date' and 'Close' columns
df = df[['Date', 'Close']]
df['Date'] = pd.to_datetime(df['Date'])        # Convert 'Date' to datetime format
df.set_index('Date', inplace=True)             # Set 'Date' as index

# Normalize the close prices
scaler = MinMaxScaler(feature_range=(0, 1))
df_scaled = scaler.fit_transform(df)

# Split the data into training and testing sets
train_size = int(len(df_scaled) * 0.8)
train_data = df_scaled[:train_size]
test_data = df_scaled[train_size:]

# Function to create sequences for LSTM input
def create_sequences(data, seq_length=50):
    sequences = []
    labels = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i + seq_length])
        labels.append(data[i + seq_length])
    return np.array(sequences), np.array(labels)

# Prepare training and testing sequences
seq_length = 50
X_train, y_train = create_sequences(train_data, seq_length)
X_test, y_test = create_sequences(test_data, seq_length)

# -------------------- Step 3: Build and Train LSTM Model -------------------- #

model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(seq_length, 1)),
    LSTM(50, return_sequences=False),
    Dense(25),
    Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')
print("🛠️ Training Model...")
model.fit(X_train, y_train, batch_size=16, epochs=10)

# -------------------- Step 4: Make Predictions and Plot -------------------- #

# Make predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Inverse transform predictions and actual values
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
y_test_original = scaler.inverse_transform(y_test.reshape(-1, 1))

# Plot actual vs predicted prices
plt.figure(figsize=(14, 6))
plt.plot(df.index[train_size + seq_length:], y_test_original, label="Actual Price", color='blue')
plt.plot(df.index[train_size + seq_length:], test_predict, label="Predicted Price", color='red')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('Stock Market Price Prediction using LSTM')
plt.legend()
plt.show()
