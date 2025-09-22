import pandas as pd

class TrafficPredictor:
    def __init__(self, data_path):
        # Load data
        self.data = pd.read_csv(data_path)
        self.data.set_index(['hour', 'day_of_week'], inplace=True)

    def predict(self, hour, day_of_week):
        # Lookup traffic multiplier, default to 1.0 if not found
        try:
            return max(1.0, self.data.loc[(hour, day_of_week), 'traffic_multiplier'])
        except KeyError:
            return 1.0

# Test the model
if __name__ == "__main__":
    predictor = TrafficPredictor('data/traffic_data.csv')
    test_cases = [(8, 1), (12, 2), (17, 5)]
    for hour, day in test_cases:
        traffic = predictor.predict(hour, day)
        print(f"Hour: {hour}, Day: {day}, Predicted Traffic Multiplier: {traffic:.2f}")