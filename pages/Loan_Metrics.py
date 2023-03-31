import streamlit as st
import plotly.express as px
from enums.data_app_enum import LoanType, LoanMetric
from utils.utils import compute_loan_metric, compute_yield_group

st.sidebar.subheader('For Loan Metrics:')
loan_options = [LoanType.DEFAULTED.value, LoanType.LATE.value,  
                LoanType.PREPAID.value, LoanType.PROFITABLE.value]
loan_types = st.sidebar \
                .multiselect('Select Loan:', options=loan_options, default=loan_options)

if len(loan_types) == 0:
    loan_types = [LoanType.DEFAULTED.value]
    
st.markdown('### Loan Metrics')
col_interest, col_tenure = st.columns(2)

with col_interest:
    df = compute_loan_metric(loan_types=loan_types, loan_metric=LoanMetric.INTEREST_RATE.value)
    df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.INTEREST_RATE.value: 'Mean Annualised Interest Rate (in %)'}, axis=1, inplace=True)
    title = 'Mean Annualised Interest Rate by Loan Types'
    fig = px.bar(df, x='Loan Types', y='Mean Annualised Interest Rate (in %)',
                  color='Loan Types', title=title, width=400, height=500,
                  color_discrete_map={
                    "Defaulted loans": "red",
                    "Prepaid loans": "grey",
                    "Late loans": "salmon",
                    "Profitable loans": "limegreen"})
    st.plotly_chart(fig)
    
with col_tenure:
    df = compute_loan_metric(loan_types=loan_types, loan_metric=LoanMetric.TENURE.value )
    df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.TENURE.value: 'Mean Loan Tenure (in Months)'}, axis=1, inplace=True)
    title = 'Mean Tenure by Loan Types'
    fig = px.bar(df, x='Loan Types', y='Mean Loan Tenure (in Months)', 
                 color='Loan Types', title=title, width=400, height=500,
                color_discrete_map={
                    "Defaulted loans": "red",
                    "Prepaid loans": "grey",
                    "Late loans": "salmon",
                    "Profitable loans": "limegreen"})
    st.plotly_chart(fig)
    
col_yield_grp, _ = st.columns(2)

with col_yield_grp:
    df = compute_yield_group(loan_types=loan_types)
    title = 'Composition of Yield Group by Credit Worthiness'
    fig = px.bar(df, x=df.columns, y=df.index,
                     title=title, width=400, height=500,color_discrete_map={
                    "high": "red",
                    "middle": "blue",
                    "low_action": "darkgreen",
                    "low_normal": "limegreen"})
    st.plotly_chart(fig)