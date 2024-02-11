import streamlit as st
from PIL import Image   

def about_us():

    st.header("About Us")
    
    st.markdown("""<div style='border: 1px solid #e6e6e6; padding: 10px; border-radius: 5px;'><h2>Welcome to Stock Guru</h2>


Are you trading Enthusiast but struggle with understanding the stock market and predicting future stock prices, don't stress! Our website is here to make things simple and help you out.
\n Simply enter the stock ticker code and get the prediction of rise and fall of stock and also its fundamental analysis
<h3>Let's go Trading!!!</h3>
                </div>
""", unsafe_allow_html=True)