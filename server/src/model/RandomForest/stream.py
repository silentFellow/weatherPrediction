import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import polars as pl

# Load preprocessed data for reference
file = pl.read_csv("data.csv")

# Load the trained model
with open("model.pickle", 'rb') as model_file:
    model = pickle.load(model_file)

# Feature columns
feature_columns = [col for col in file.columns if col != 'result']

# Standard scaler for input transformation
scaler = StandardScaler().fit(file[feature_columns].to_pandas())

# Streamlit UI
st.title("Weather Prediction App")
st.sidebar.header("Input Features")

# User input for all features
user_input = {}
for feature in feature_columns:
    user_input[feature] = st.sidebar.number_input(
        f'{feature}', 
        float(file[feature].min()), 
        float(file[feature].max()), 
        float(file[feature].mean())
    )

user_input_df = pd.DataFrame([user_input])

# Show user input
st.write("### User Input:")
st.write(user_input_df)

# Prediction
if st.button('Predict'):
    scaled_input = scaler.transform(user_input_df)
    prediction = model.predict(scaled_input)
    
    result = "Rain" if prediction[0] == 1 else "No Rain"
    st.write(f"### Predicted Weather Outcome: **{result}**")
