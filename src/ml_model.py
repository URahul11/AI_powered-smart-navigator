import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np

class TrafficPredictor:
    def __init__(self, data_path):
        # Load data
        data = pd.read_csv(data_path)
        self.X = data[['hour', 'day_of_week']]
        self.y = data['traffic_multiplier']
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)  # 100 trees for better accuracy
        self.model.fit(self.X, self.y)
        self.feature_names = ['hour', 'day_of_week']

    def predict(self, hour, day_of_week):
        # Predict traffic multiplier using DataFrame to avoid feature name issues
        input_data = pd.DataFrame([[hour, day_of_week]], columns=self.feature_names)
        return max(1.0, self.model.predict(input_data)[0])

# Test the model
if __name__ == "__main__":
    predictor = TrafficPredictor('data/traffic_data.csv')
    test_cases = [(8, 1), (12, 2), (17, 5)]
    for hour, day in test_cases:
        traffic = predictor.predict(hour, day)
        print(f"Hour: {hour}, Day: {day}, Predicted Traffic Multiplier: {traffic:.2f}")