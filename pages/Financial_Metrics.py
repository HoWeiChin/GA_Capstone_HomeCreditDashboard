import streamlit as st
import plotly.express as px
from enums.data_app_enum import CreditStats, ComputeMode, DisplayMode
from utils.utils import compute_fin_metric

st.set_page_config(layout='wide', 
                   initial_sidebar_state='expanded')

display_mode = st.sidebar \
                    .selectbox('Select Display Mode:', (DisplayMode.ALL.value, DisplayMode.DECOMPOSED.value))

if display_mode == DisplayMode.ALL.value:
    disabled = True

elif display_mode == DisplayMode.DECOMPOSED.value:
    disabled = False

credit_stats = st.sidebar \
                    .multiselect('Select Credit Status:', \
                                 options=[CreditStats.DEFAULT.value, CreditStats.NO_DEFAULT.value], 
                                 default=[CreditStats.DEFAULT.value, CreditStats.NO_DEFAULT.value],
                                disabled=disabled)

st.sidebar.subheader('For Financial Metrics:')
compute_mode = st.sidebar \
                    .selectbox('Select Compute Mode:', (ComputeMode.SUM.value, ComputeMode.MEAN.value))

#First Row
st.markdown('### Financial Metrics')

with st.container():
    if display_mode == DisplayMode.ALL.value:
        df = compute_fin_metric(credit_stats=None, compute_mode=compute_mode, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Financials', 'VALUE': '$ (in thousands)'}, axis=1, inplace=True)

        title = 'Mean Monetary Losses or Profit'
        if compute_mode == ComputeMode.SUM.value:
            title = 'Total Monetary Losses or Profit'

        fig = px.bar(
                df, x='Financials', 
                    y='$ (in thousands)', color='Financials', title=title, width=950, height=700)
        st.plotly_chart(fig)
    
    elif display_mode == DisplayMode.DECOMPOSED.value:
        df = compute_fin_metric(credit_stats=credit_stats, compute_mode=compute_mode, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Financials', 
                   'VALUE': '$ (in thousands)', 
                   'CREDIT_STATUS': 'Credit Worthiness'}, axis=1, inplace=True)
        
        title = 'Mean Monetary Losses or Profit by Credit Worthiness'
        if compute_mode == ComputeMode.SUM.value:
            title = 'Total Monetary Losses or Profit by Credit Worthiness'

        fig = px.bar(
                df, x='Financials', 
                    y='$ (in thousands)', color='Credit Worthiness', title=title, width=900, height=600)
        st.plotly_chart(fig)
