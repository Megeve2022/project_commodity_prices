import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from dateutil.relativedelta import relativedelta
import joblib



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")
def predict():
    # GET TODO: get model from GCP
    df_soybean = pd.read_csv('gs://commodity-price-storage/dataset_daily_prices_soybean/soybean_daily_price.csv')
    X = df_soybean[-253:].drop(columns = 'Date').to_numpy().reshape(1,253,5)
    soybean_date = pd.to_datetime(df_soybean['Date'])
    date = soybean_date.iloc[-1]
    twelve_months = [date + relativedelta(months=+month) for month in range(1,13)]


    # pipeline = get_model_from_gcp()
    pipeline = joblib.load('model.joblib')

    # make prediction
    results = pipeline.predict(X)
    dicionario = {}
    for result , month in zip(results[0].tolist(), twelve_months):
        date_format = '%Y/%m/%d'
        month_str = month.strftime(date_format)
        dicionario[month_str] = result
    return dicionario
