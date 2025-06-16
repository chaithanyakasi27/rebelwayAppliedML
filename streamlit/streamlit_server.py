import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

# Title and description
st.write("""
# Iris Flower Classification App 
This app predicts the species of an Iris flower based on user input features or uploaded CSV data.
""")

# Sidebar header
st.sidebar.header("User Input Features")
st.sidebar.markdown("You can upload a CSV file or use the sliders below to input values.")

# File uploader to accept CSV input
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])


# If a file is uploaded, read it as a DataFrame
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    # If no file, use slider input
    def user_input_features():
        # These are the four important features of an Iris flower used for classification
        # Sepal = outer petal-like part of the flower
        # Petal = inner colorful part of the flower

        # Length and width are measured in centimeters
        SepalLengthCm = st.sidebar.slider('Sepal Length (cm)', 4.3, 8.0, 6.0)
        SepalWidthCm = st.sidebar.slider('Sepal Width (cm)', 2.0, 5.0, 3.0)
        PetalLengthCm = st.sidebar.slider('Petal Length (cm)', 1.0, 7.0, 4.0)
        PetalWidthCm = st.sidebar.slider('Petal Width (cm)', 0.1, 3.0, 1.0)

        # Creating a dictionary of input values
        data = {
            "SepalLengthCm": SepalLengthCm,
            "SepalWidthCm": SepalWidthCm,
            "PetalLengthCm": PetalLengthCm,
            "PetalWidthCm": PetalWidthCm
        }

        # Convert to DataFrame (shape: 1 row × 4 columns)
        features = pd.DataFrame(data, index=[0])
        return features

    input_df = user_input_features()

# Load reference iris dataset (assumed to be in the same folder)
iris_raw = pd.read_csv('iris.csv')

# Drop non-feature columns like 'Species' (target) and 'Id' (identifier)
iris = iris_raw.drop(['Species', 'Id'], axis=1)

# Append user input data to iris dataset (only for consistent formatting)
df = pd.concat([input_df, iris], axis=0)

# Keep only the first row — the user's input
df = df[:1]

# Show the input data
st.subheader("User Input Features (Used for Prediction)")
if uploaded_file is not None:
    st.write(df)
else:
    st.write("Using slider input. Upload a CSV file if available.")
    st.write(df)

#Model 
load_clf = pickle.load(open('iris_model.pkl', 'rb'))
prediction = load_clf.predict(df)
prediction_prob = load_clf.predict_proba(df)

st.subheader('prediction')
iris_species = np.array(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
st.write(iris_species[prediction])

st.subheader('Prediction Probability')
st.write(prediction_prob)