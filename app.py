import streamlit as st
import requests

'''
# Project Commodity Prediction Price
'''

st.markdown('''
Este projeto possui como objetivo prever por meio de uso de redes neurais o preço da soja nos próximos 12 meses
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://soybean-predict-price-project-ts7i4cg3ha-ew.a.run.app/predict'

resposta = requests.get(url).json()


if url == 'https://soybean-predict-price-project-ts7i4cg3ha-ew.a.run.app/predict':
    for keys,values in resposta.items():
        st.markdown(f'{keys} : {round(values,2)}')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
