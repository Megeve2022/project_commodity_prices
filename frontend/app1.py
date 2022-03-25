import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

'''
# Project Soy Bean Commodity Prediction Price
'''
df_fut_price = pd.read_csv("soybean_daily_price.csv")
df_predc_price = pd.read_csv("predicted_soybean_prices.csv")


st.write("This is inside the container")

fig = go.Figure()
    # You can call any Streamlit command, including custom components:
fig.add_trace(
go.Scatter(x=list(df_fut_price.Date), y=list(df_fut_price.Close), name= 'Real Price'))
fig.add_trace(
go.Scatter(x=list(df_predc_price['Date']), y=list(df_predc_price['Predicted Price']), name= 'Prediction Model'))

    # Set title
fig.update_layout(
    title_text="Historical Futures Prices for Soybeans"
)

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                    label="1m",
                    step="month",
                    stepmode="backward"),
                dict(count=6,
                    label="6m",
                    step="month",
                    stepmode="backward"),
                dict(count=1,
                    label="YTD",
                    step="year",
                    stepmode="todate"),
                dict(count=1,
                    label="1y",
                    step="year",
                    stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

st.plotly_chart(fig)










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

url = 'https://soybean-price-prediction-ts7i4cg3ha-ew.a.run.app/predict'

resposta = requests.get(url).json()


if url == 'https://soybean-price-prediction-ts7i4cg3ha-ew.a.run.app/predict':
    for keys,values in resposta.items():
        st.markdown(f'{keys} : {round(values,2)}')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
