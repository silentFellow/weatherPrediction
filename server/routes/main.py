from fastapi import FastAPI
import pickle
import numpy as np
import pandas as pd

app = FastAPI()

with open("C:/Users/thegr/OneDrive/Desktop/MLMiniProject/model/model.pickle", "rb") as pickleModel:
  model = pickle.load(pickleModel)

file = pd.read_csv("C:/Users/thegr/OneDrive/Desktop/MLMiniProject/data/preprocessedData.csv")

print(model.predict([[26.7,28.9,984.0,76.0,80.0,2.01,148.0,2.01]]))