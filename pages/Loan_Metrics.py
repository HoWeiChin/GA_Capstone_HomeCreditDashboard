import streamlit as st
import plotly.express as px
from enums.data_app_enum import CreditStats, DisplayMode, LoanType, LoanMetric
from utils.utils import compute_loan_metric, compute_yield_group

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

st.sidebar.subheader('For Loan Metrics:')
loan_options = [LoanType.DEFAULTED.value, LoanType.LATE.value,  
                LoanType.PREPAID.value, LoanType.PROFITABLE.value]
loan_types = st.sidebar \
                .multiselect('Select Loan:', options=loan_options, default=loan_options)

st.markdown('### Loan Metrics')
col_interest, col_tenure, col_yield_grp = st.columns(3)

with col_interest:
    if display_mode == DisplayMode.ALL.value:
        df = compute_loan_metric(credit_stats=None, loan_types=loan_types, loan_metric=LoanMetric.INTEREST_RATE.value ,display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.INTEREST_RATE.value: 'Mean Annualised Interest Rate (in %)'}, axis=1, inplace=True)
        
        fig = px.bar(df, x='Loan Types', y='Mean Annualised Interest Rate (in %)', color='Loan Types', width=400, height=500)
        st.plotly_chart(fig)
    
    elif display_mode == DisplayMode.DECOMPOSED.value:
        df = compute_loan_metric(credit_stats=credit_stats, loan_types=loan_types, loan_metric=LoanMetric.INTEREST_RATE.value, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', 
                   LoanMetric.INTEREST_RATE.value: 'Mean Annualised Interest Rate (in %)', 
                   'CREDIT_STATUS': 'Credit Worthiness'}, axis=1, inplace=True)
        
        fig = px.bar(df, x='Loan Types', y='Mean Annualised Interest Rate (in %)', color='Credit Worthiness', width=400, height=500)
        st.plotly_chart(fig)
    
with col_tenure:
    if display_mode == DisplayMode.ALL.value:
        df = compute_loan_metric(credit_stats=None, loan_types=loan_types, loan_metric=LoanMetric.TENURE.value ,display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.TENURE.value: 'Mean Loan Tenure (in Months)'}, axis=1, inplace=True)

        fig = px.bar(df, x='Loan Types', y='Mean Loan Tenure (in Months)', color='Loan Types', width=400, height=500)
        st.plotly_chart(fig)
    
    elif display_mode == DisplayMode.DECOMPOSED.value:
        df = compute_loan_metric(credit_stats=credit_stats, loan_types=loan_types, loan_metric=LoanMetric.TENURE.value, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', 
                   LoanMetric.TENURE.value: 'Mean Loan Tenure (in Months)', 
                   'CREDIT_STATUS': 'Credit Worthiness'}, axis=1, inplace=True)

        fig = px.bar(df, x='Loan Types', y='Mean Loan Tenure (in Months)', color='Credit Worthiness', width=400, height=500)
        st.plotly_chart(fig)

with col_yield_grp:
    if display_mode == DisplayMode.ALL.value:
        df = compute_yield_group(credit_stats=None, loan_types=loan_types, display_mode=display_mode)
        df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.YIELD_GRP.value: 'Previous Yield Group'}, axis=1, inplace=True)

        fig = px.bar(df, x='Loan Types', y='Count', 
                     color='Previous Yield Group', color_discrete_sequence=['forestgreen',  'red', 'yellowgreen', 'darkgreen'], 
                     width=400, height=500)
        st.plotly_chart(fig)

    elif display_mode == DisplayMode.DECOMPOSED.value:
        df = compute_yield_group(credit_stats=credit_stats, loan_types=loan_types, display_mode=display_mode)
        
        fig = px.bar(df, x=df.columns, y=df.index, color_discrete_sequence=['forestgreen',  'red', 'yellowgreen', 'darkgreen'],
                     width=400, height=500)
        st.plotly_chart(fig)