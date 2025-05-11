import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle

# Load dataset
df = pd.read_csv('../data/ev_data.csv')

# Features and target
X = df.drop(['physics_range', 'ml_range'], axis=1)
y = df['physics_range']  # Using physics_range as our target variable

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open('ev_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as ev_model.pkl")
