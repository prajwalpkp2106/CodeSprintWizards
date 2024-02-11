import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import yfinance as yf
from datetime import datetime
import plotly.graph_objects as go
from PIL import Image
from fund import fund
from aboutus import about_us

def home():
    html_temp=""" 
<div style="background-color:
#020842
;padding:10px ;margin:8px">
<h2 style="color:white;text-align:center;">Stock price Prediction</h2>
</div>
"""
    st.markdown(html_temp,unsafe_allow_html=True)
    st.write(" ")
    
    start = '2010-01-01'
    end = '2024-02-10'  # Set end date to today's date

    # user_input = st.text_input('Enter Stock Ticker', 'AAPL')
    input_container = st.container()

    with input_container:
        user_input = st.text_input('Enter Stock Ticker', 'GOOG')

    df = yf.download(user_input, start=start, end=end)
    st.write(" ")

    st.subheader('Data from 2010-Till Date')
    st.write(df.describe())


    data_training=pd.DataFrame(df['Close'][0:int(0.7*len(df))])
    data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(0,1))

    data_training=pd.DataFrame(df['Close'][0:int(0.7*len(df))])
    data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(0,1))

    # data_training_array=scaler.fit_transform(data_training)


    #load
    model=load_model('keras_model_new.h5')


    # Testing
    past_100_days = data_training.tail(100)
    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
    input_data = scaler.fit_transform(final_df)

    x_test = []
    y_test = []
    # y_test_indexes = []  # List to store the indexes

    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100:i])
        y_test.append(input_data[i, 0])
    # y_test_indexes.append(df.index[i])

    x_test, y_test = np.array(x_test), np.array(y_test)

    y_predicted = model.predict(x_test)
    scaler = scaler.scale_

    scale_factor = 1 / scaler[0]
    y_predicted = y_predicted * scale_factor
    y_test = y_test * scale_factor

    # st.divider()

    from datetime import datetime, timedelta

    start_date = datetime(2021,3, 13)
    end_date = datetime(2024, 2, 9)

    date_array = []

    current_date = start_date
    while current_date <= end_date:
        date_array.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    st.subheader('Predictions vs Original')

    fig2 = go.Figure()

    # Original Price
    fig2.add_trace(go.Scatter(x=date_array, y=y_test, mode='lines', name='Original Price', line=dict(color='blue')))

    # Predicted Price
    fig2.add_trace(go.Scatter(x=date_array, y=y_predicted.flatten(), mode='lines', name='Predicted Price', line=dict(color='red')))

    fig2.update_layout(title='Predictions vs Original', xaxis_title='Time', yaxis_title='Price')

    st.plotly_chart(fig2)

    # st.divider()

    st.subheader('Closing Price vs Time Chart')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Closing Price'))
    st.plotly_chart(fig)

    # st.divider()
    ma1 = st.slider('Select moving average', 0, 200, 100)
    st.subheader(f'Closing Price vs Time Chart with {ma1}MA')
    ma100 = df.Close.rolling(ma1).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name=ma1))
    fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Closing Price'))
    st.plotly_chart(fig)



    # st.divider()
    st.subheader('Closing Price vs Time Chart with 100MA & 200MA')
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=ma100, mode='lines', name='100MA', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df.index, y=ma200, mode='lines', name='200MA', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df.index, y=df.Close, mode='lines', name='Closing Price', line=dict(color='blue')))
    st.plotly_chart(fig)
    # st.divider()

def main():
    im = Image.open('logo2.png')#Title and App Icon
    st.set_page_config(page_title="Stock Guru", page_icon = im)   


    hide_default_format = """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_default_format, unsafe_allow_html=True)
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image('logo2.png')
    
    page_bg_img="""
<style>
[data-testid="stAppViewContainer"]{
background: rgb(16,4,4);
background: linear-gradient(18deg, rgba(16,4,4,1) 0%, rgba(0,66,228,1) 100%);
background-position:  10px 0, 10px 0, 0 0, 0 0;
background-size:cover;
background-repeat: no-repeat; 
}

</style>


"""
    st.markdown(page_bg_img,unsafe_allow_html=True)
    menu = ["Stock Price Prediction", "Fundamental Analysis","About Us"]
    choice = st.sidebar.selectbox("Select Page", menu)
    page_bg_img="""
<style>
[data-testid="stSidebarContent"]{
background: rgb(16,4,4);
background: linear-gradient(18deg, rgba(16,4,4,1) 0%, rgba(0,66,228,1) 100%);
background-position:  10px 0, 10px 0, 0 0, 0 0;
background-size:cover;
background-repeat: no-repeat; 
}

</style>


"""
    st.markdown(page_bg_img,unsafe_allow_html=True)

    if choice == "Stock Price Prediction":
        home()
    elif choice == "Fundamental Analysis":
        fund()
    elif choice == "About Us":
        about_us()
    
if __name__ == "__main__":
    main()
