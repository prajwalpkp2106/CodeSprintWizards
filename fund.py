import matplotlib
import pandas as pd
from seaborn.relational import lineplot
import streamlit as st
import plotly.express as px
from PIL import Image
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
import utils as ut

def fund():
    st.markdown("<h1 style='text-align: center;'>Fundamental Analysis</h1>", unsafe_allow_html=True)
    st.write(" ")
    
    if True:
        df = pd.read_csv("StockRatings-04.05.22.csv")
        remove_vals = ['Ticker', 'Sector', 'Company', 'Market Cap', 'Industry', 'Country', 'Earnings Date', 'Valuation Grade', 'Profitability Grade', 'Growth Grade', 'Performance Grade']
        selectable_values = [ elem for elem in df.columns.tolist() if elem not in remove_vals ]

        values = st.selectbox(
            'Select Values',
            (selectable_values))


        st.markdown("***")

        ticker = st.text_input('Enter a Ticker Symbol', 'AAPL')

        row = df[df['Ticker'] == ticker]

        rating = round(row['Overall Rating'].values[0], 1)

        col1, col2, col3 = st.columns(3)
        col1.metric("Company", row['Company'].values[0])
        col2.metric("Market Cap", row['Market Cap'].values[0])
        col3.metric("Overall Rating", str(rating)[0 : str(rating).find('.')])

        col4, col5, col6 = st.columns(3)
        col4.metric("Price", row['Price'].values[0])
        col5.metric("Sector", row['Sector'].values[0])
        col6.metric("Industry", row['Industry'].values[0])

        # stock_metric = st.selectbox(
        #     'Pick a metric to analyze',
        #     (selectable_values))

        filter_by = st.radio(
            "Analyze by",
            ('Sector', 'Industry'))


        fig, subheader, md = ut.plot_dist(df, ticker, sector=(filter_by=='Sector'), _filter=row[filter_by].values[0], metric=values, metric_val=row[values].values[0])

        st.subheader(subheader)
        st.markdown(md)
        st.pyplot(fig)

        # Valuation Section 

        st.text('')
        st.subheader(f"Valuation Grade: {row['Valuation Grade'].values[0]}")

        val_col1, val_col2, val_col3 = st.columns(3)
        val_cols = [val_col1, val_col2, val_col3]

        val_col4, val_col5, val_col6 = st.columns(3)
        val_cols2 = [val_col4, val_col5, val_col6]

        for i, _metric in enumerate(['Fwd P/E', 'P/S', 'P/FCF']):
            val_fig, val_subheader, val_md = ut.plot_dist(df, ticker, sector=(filter_by=='Sector'), _filter=row[filter_by].values[0], metric=_metric, metric_val=row[_metric].values[0], fig_size=(35, 25), show_ticker=False, show_subheader=False)
            val_cols[i].subheader(val_subheader)
            val_cols[i].pyplot(val_fig)


        for i, _metric in enumerate(['PEG', 'P/C', 'P/B']):
            val_fig, val_subheader, val_md = ut.plot_dist(df, ticker, sector=(filter_by=='Sector'), _filter=row[filter_by].values[0], metric=_metric, metric_val=row[_metric].values[0], fig_size=(35, 25), show_ticker=False, show_subheader=False)
            val_cols2[i].subheader(val_subheader)
            val_cols2[i].pyplot(val_fig)

        # Performance Section 

        st.text('')
        st.subheader(f"Performance Grade: {row['Performance Grade'].values[0]}")

        perf_col1, perf_col2, perf_col3 = st.columns(3)
        perf_cols = [perf_col1, perf_col2, perf_col3]

        perf_col4, perf_col5, perf_col6 = st.columns(3)
        perf_cols2 = [perf_col4, perf_col5, perf_col6]

        for i, _metric in enumerate(['Perf Month', 'Perf Quart', 'Perf Half']):
            perf_fig, perf_subheader, perf_md = ut.plot_dist(df, ticker, sector=(filter_by=='Sector'), _filter=row[filter_by].values[0], metric=_metric, metric_val=row[_metric].values[0], fig_size=(35, 25), show_ticker=False, show_subheader=False)
            perf_cols[i].subheader(perf_subheader)
            perf_cols[i].pyplot(perf_fig)


        for i, _metric in enumerate(['Perf Year', 'Perf YTD', 'Volatility M']):
            perf_fig, perf_subheader, perf_md = ut.plot_dist(df, ticker, sector=(filter_by=='Sector'), _filter=row[filter_by].values[0], metric=_metric, metric_val=row[_metric].values[0], fig_size=(35, 25), show_ticker=False, show_subheader=False)
            perf_cols2[i].subheader(perf_subheader)
            perf_cols2[i].pyplot(perf_fig)