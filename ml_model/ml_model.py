import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load dataset
df = pd.read_csv("Plant_Dataset.csv")

# 2. Split features and target
X = df[["Temperature", "Humidity", "Air_Index", "Lux"]]
y = df["Best_Plant"]

# 3. Encode target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 4. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# 5. Initialize and train model
# Increased n_estimators for stability, limited max_depth to avoid overfitting
model = RandomForestClassifier(
    n_estimators=300, 
    max_depth=None, 
    min_samples_split=2, 
    random_state=42,
    class_weight="balanced"   # handles any class imbalance
)
model.fit(X_train, y_train)

# 6. Predictions
y_pred = model.predict(X_test)

# 7. Evaluation
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:\n", report)

# 8. Cross-validation (optional, for more reliable accuracy estimate)
cv_scores = cross_val_score(model, X, y_encoded, cv=5)
print(f"Cross-validation Accuracy: {cv_scores.mean():.2f} (+/- {cv_scores.std():.2f})")

# 9. Save model and encoder
joblib.dump(model, "plant_recommendation_model.joblib")
joblib.dump(label_encoder, "label_encoder.joblib")