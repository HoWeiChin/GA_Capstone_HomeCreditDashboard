import streamlit as st
import plost
from utils import compute_fin_metric, compute_loan_metric
from data_app_enum import FinMetric, ComputeMode, CreditStats, LoanMetric

st.set_page_config(layout='wide', 
                   initial_sidebar_state='expanded')

st.sidebar.header('Completed Cash Loans Information')
st.sidebar.subheader('Input to Dashboard:')

credit_stats = st.sidebar \
                    .multiselect('Select Credit Status:', \
                                 options=[CreditStats.DEFAULT.value, CreditStats.NO_DEFAULT.value], 
                                 default=[CreditStats.DEFAULT.value, CreditStats.NO_DEFAULT.value])

compute_mode = st.sidebar \
                    .selectbox('Select Compute Mode:', (ComputeMode.SUM.value, ComputeMode.MEAN.value))

#First Row
st.markdown('### Financial Metrics')
col_prepaid, col_default, col_penalty = st.columns(3)

with col_prepaid:
    prepaid_loss_df = compute_fin_metric(credit_stats, FinMetric.PREPAID_LOSSES.value, compute_mode)
    y_axis_name = 'Prepaid Losses ($ in Thousands)'
    prepaid_loss_df.rename(
        {FinMetric.PREPAID_LOSSES.value: y_axis_name}, 
         axis=1, inplace=True)
    
    plost.bar_chart(
        prepaid_loss_df, bar='CREDIT_STATUS', 
        value=y_axis_name, color='CREDIT_STATUS', legend=None)

with col_default:
    default_loss_df = compute_fin_metric(credit_stats, FinMetric.DEFAULT_LOSSES.value, compute_mode)
    y_axis_name = 'Default Losses ($ in Thousands)'
    default_loss_df.rename(
        {FinMetric.DEFAULT_LOSSES.value: y_axis_name}, 
         axis=1, inplace=True)
    
    plost.bar_chart(
        default_loss_df, bar='CREDIT_STATUS', 
        value=y_axis_name, color='CREDIT_STATUS', legend=None)

with col_penalty:
    penalty_df = compute_fin_metric(credit_stats, FinMetric.PENALTY_IMPOSED.value, compute_mode)
    y_axis_name = 'Penalty Imposed ($ in Thousands)'
    penalty_df.rename(
        {FinMetric.PENALTY_IMPOSED.value: y_axis_name}, 
         axis=1, inplace=True)
    
    plost.bar_chart(
        penalty_df, bar='CREDIT_STATUS', 
        value=y_axis_name, color='CREDIT_STATUS', legend=None)
    
#2nd Row
st.markdown('### Loan Metrics')
col_interest, col_tenure = st.columns(2)


with col_interest:
    IR_df = compute_loan_metric(credit_stats, loan_metric=LoanMetric.INTEREST_RATE.value)
    y_axis_name = 'Mean Annualised Interest Rate (in %)'
    IR_df.rename(
        {LoanMetric.INTEREST_RATE.value: y_axis_name}, 
         axis=1, inplace=True)
    
    plost.bar_chart(
        IR_df, bar='FIN_METRIC_TYPE', 
        value=y_axis_name, color='CREDIT_STATUS', legend=None)

with col_tenure:
    tenure_df = compute_loan_metric(credit_stats, loan_metric=LoanMetric.TENURE.value)
    y_axis_name = 'Mean Tenure of Loans (in Months)'
    tenure_df.rename(
        {LoanMetric.TENURE.value: y_axis_name}, 
         axis=1, inplace=True)
    
    plost.bar_chart(
        tenure_df, bar='FIN_METRIC_TYPE', 
        value=y_axis_name, color='CREDIT_STATUS', legend=None)