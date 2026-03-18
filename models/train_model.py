import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load data
data = pd.read_csv("data/business_data.csv")

# Features & target
X = data[["price", "marketing", "customers"]]
y = data["revenue"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
with open("models/revenue_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved!")