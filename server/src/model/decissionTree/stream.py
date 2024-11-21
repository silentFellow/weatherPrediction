import streamlit as st
import pickle
import numpy as np

# Load your trained model
model = pickle.load(open('model.pickle', 'rb'))

# Define a function to make predictions
def predict(input_data):
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)
    return prediction

# Streamlit app
st.title('ML Model Hosting with Streamlit')

# Input fields for the features
feature1 = st.number_input('Feature 1')
feature2 = st.number_input('Feature 2')
# Add more input fields as needed

# Button to make predictions
if st.button('Predict'):
    input_data = [feature1, feature2]  # Add more features as needed
    prediction = predict(input_data)
    st.write(f'Prediction: {prediction}')
