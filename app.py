import streamlit as st
import plost
from utils import compute_fin_metric, compute_loan_metric, compute_yield_group
from data_app_enum import (ComputeMode, CreditStats, DisplayMode, FinMetric,
                           LoanMetric)



st.set_page_config(layout='wide', 
                   initial_sidebar_state='expanded')

st.sidebar.header('Completed Cash Loans Information')
st.sidebar.subheader('Input to Dashboard:')

display_mode = st.sidebar \
                    .selectbox('Select Display Mode:', (DisplayMode.ALL.value, DisplayMode.DECOMPOSED.value))


if display_mode == DisplayMode.ALL.value:
    st.session_state.disabled = True

elif display_mode == DisplayMode.DECOMPOSED.value:
    st.session_state.disabled = False

credit_stats = st.sidebar \
                    .multiselect('Select Credit Status:', \
                                 options=[CreditStats.DEFAULT.value, CreditStats.NO_DEFAULT.value], 
                                 default=[CreditStats.DEFAULT.value, CreditStats.NO_DEFAULT.value],
                                disabled=st.session_state.disabled)


compute_mode = st.sidebar \
                    .selectbox('Select Compute Mode:', (ComputeMode.SUM.value, ComputeMode.MEAN.value))

#First Row
st.markdown('### Financial Metrics')

with st.container():
    if display_mode == DisplayMode.ALL.value:
        df = compute_fin_metric(credit_stats=None, compute_mode=compute_mode, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Financials', 'VALUE': '$ (in thousands)'}, axis=1, inplace=True)
        plost.bar_chart(
            df, bar='Financials', 
            value='$ (in thousands)', color='Financials', legend='right', width=900, height=600)
    
    elif display_mode == DisplayMode.DECOMPOSED.value:
        df = compute_fin_metric(credit_stats=credit_stats, compute_mode=compute_mode, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Financials', 
                   'VALUE': '$ (in thousands)', 
                   'CREDIT_STATUS': 'Credit Worthiness'}, axis=1, inplace=True)
        plost.bar_chart(
            df, bar='Financials', 
            value='$ (in thousands)', color='Credit Worthiness', legend='right', width=900, height=600)

#2nd Row
st.markdown('### Loan Metrics')
col_interest, col_tenure, col_yield_grp = st.columns(3)

with col_interest:
    if display_mode == DisplayMode.ALL.value:
        df = compute_loan_metric(credit_stats=None, loan_metric=LoanMetric.INTEREST_RATE.value ,display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.INTEREST_RATE.value: 'Mean Annualised Interest Rate (in %)'}, axis=1, inplace=True)
        plost.bar_chart(
            df, bar='Loan Types', 
            value='Mean Annualised Interest Rate (in %)', color='Loan Types', legend='right', width=400, height=500)
    
    elif display_mode == DisplayMode.DECOMPOSED.value:
        df = compute_loan_metric(credit_stats=credit_stats, loan_metric=LoanMetric.INTEREST_RATE.value, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', 
                   LoanMetric.INTEREST_RATE.value: 'Mean Annualised Interest Rate (in %)', 
                   'CREDIT_STATUS': 'Credit Worthiness'}, axis=1, inplace=True)
        plost.bar_chart(
            df, bar='Loan Types', 
            value='Mean Annualised Interest Rate (in %)', color='Credit Worthiness', legend='right', width=400, height=500)
    

with col_tenure:
    if display_mode == DisplayMode.ALL.value:
        df = compute_loan_metric(credit_stats=None, loan_metric=LoanMetric.TENURE.value ,display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.TENURE.value: 'Mean Loan Tenure (in Months)'}, axis=1, inplace=True)
        plost.bar_chart(
            df, bar='Loan Types', 
            value='Mean Loan Tenure (in Months)', color='Loan Types', legend='right', width=400, height=500)
    
    elif display_mode == DisplayMode.DECOMPOSED.value:
        df = compute_loan_metric(credit_stats=credit_stats, loan_metric=LoanMetric.TENURE.value, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', 
                   LoanMetric.TENURE.value: 'Mean Loan Tenure (in Months)', 
                   'CREDIT_STATUS': 'Credit Worthiness'}, axis=1, inplace=True)
        plost.bar_chart(
            df, bar='Loan Types', 
            value='Mean Loan Tenure (in Months)', color='Credit Worthiness', legend='right', width=400, height=500)