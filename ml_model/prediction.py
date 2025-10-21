import joblib
import pandas as pd

# Load saved model and label encoder
model = joblib.load("plant_recommendation_model.joblib")
label_encoder = joblib.load("label_encoder.joblib")

def predict_from_csv(input_csv, output_csv="Predictions.csv"):
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Ensure the CSV has the required columns
    required_cols = ["Temperature", "Humidity", "Air_Index", "Lux"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    # Extract features
    X = df[required_cols]

    # Predict encoded labels
    preds_encoded = model.predict(X)

    # Decode labels back to plant names
    preds = label_encoder.inverse_transform(preds_encoded)

    # Add predictions to the dataframe
    df["Recommended_Plant"] = preds

    # Save to new CSV
    df.to_csv(output_csv, index=False)
    print(f"Predictions saved to {output_csv}")
    print(df.head())  # Show first few rows with predictions

# Example usage
predict_from_csv("Sensor_Input.csv")