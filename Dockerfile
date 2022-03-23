FROM python:3.8-buster

COPY api /api
COPY project_commodity_prices /project_commodity_prices
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt
COPY raw_data/commodity-price-lewagon-af21f5db0b4a.json /google_credentials.json
COPY raw_data/soybean_daily_price.csv /soybean_daily_price.csv

RUN pip install -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=/google_credentials.json

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
