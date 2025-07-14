import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the 3D point data with faction labels
df = pd.read_csv(r"D:\portfolio class\3D\development\ML\rebelwayAppliedML_2\randomforest\point_data_v2.csv")

# Use all 3 dimensions as input features
x = df[['x', 'y', 'z']]
y = df['faction']

# Split into training and test data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# Evaluate
predictions = model.predict(x_test)
print(f"Accuracy: {accuracy_score(y_test, predictions)}")

# Save model
joblib.dump(model, "random_forest_model.pkl")
print("Model saved successfully")
