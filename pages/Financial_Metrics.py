import streamlit as st
import plotly.express as px
from enums.data_app_enum import LoanType
from utils.utils import compute_fin_metric, show_composition

st.set_page_config(layout='wide', 
                   initial_sidebar_state='expanded')

loan_options = [LoanType.DEFAULTED.value, LoanType.LATE.value,  
                LoanType.PREPAID.value, LoanType.PROFITABLE.value]

st.sidebar.subheader('To decompose Loan by Yield Group:')
loan_types = st.sidebar \
                .selectbox('Select Loan:', loan_options)

#First Row
st.markdown('### Financial Metrics')

col_fin_metric, col_loan_composition = st.columns(2)
with col_fin_metric:
    df = compute_fin_metric()
    df.rename({'FIN_METRIC': 'Financials', 'VALUE': '$ (in thousands)'}, axis=1, inplace=True)

    title = 'Mean Profit/Loss'
    fig = px.bar(
                df, x='Financials', 
                y='$ (in thousands)', color='Financials', title=title, 
                width=600, height=600, color_discrete_sequence=['red', 'red', 'green', 'green'], text_auto=True)
    st.plotly_chart(fig)

with col_loan_composition:
    df = show_composition(loan_type=loan_types)
    title = f'Composition of Yield Group for {loan_types}'
    df = df.sort_values(by='Yield Group')
    fig = px.bar(df, y="% of Each Yield Group", x='Yield Group', color="Yield Group", title=title, color_discrete_map={
                "high": "red",
                "middle": "blue",
                "low_action": "darkgreen",
                "low_normal": "limegreen"}, text_auto=True)
    st.plotly_chart(fig)