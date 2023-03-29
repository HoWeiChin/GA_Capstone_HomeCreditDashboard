import streamlit as st
import plotly.express as px
from enums.data_app_enum import CreditStats, DisplayMode, LoanType, LoanMetric
from utils.utils import compute_loan_metric, compute_yield_group

display_mode_loan = st.sidebar \
                    .selectbox('Select Display Mode:', (DisplayMode.ALL.value, DisplayMode.DECOMPOSED.value))

if display_mode_loan == DisplayMode.ALL.value:
    disabled_loan = True

elif display_mode_loan == DisplayMode.DECOMPOSED.value:
    disabled_loan = False


credit_stats_loan = st.sidebar \
                    .multiselect('Select Credit Status:', \
                                 options=[CreditStats.DEFAULT.value, CreditStats.NO_DEFAULT.value], 
                                 default=[CreditStats.DEFAULT.value, CreditStats.NO_DEFAULT.value],
                                disabled=disabled_loan)


st.sidebar.subheader('For Loan Metrics:')
loan_options = [LoanType.DEFAULTED.value, LoanType.LATE.value,  
                LoanType.PREPAID.value, LoanType.PROFITABLE.value]
loan_types = st.sidebar \
                .multiselect('Select Loan:', options=loan_options, default=loan_options)

st.markdown('### Loan Metrics')
col_interest, col_tenure, col_yield_grp = st.columns(3)

with col_interest:
    if display_mode_loan == DisplayMode.ALL.value:
        df = compute_loan_metric(credit_stats=None, loan_types=loan_types, loan_metric=LoanMetric.INTEREST_RATE.value ,display_mode=display_mode_loan)
        df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.INTEREST_RATE.value: 'Mean Annualised Interest Rate (in %)'}, axis=1, inplace=True)
        title = 'Mean Annualised Interest Rate by Loan Types'
        fig = px.bar(df, x='Loan Types', y='Mean Annualised Interest Rate (in %)', color='Loan Types', title=title, width=400, height=500)
        st.plotly_chart(fig)
    
    elif display_mode_loan == DisplayMode.DECOMPOSED.value:
        df = compute_loan_metric(credit_stats=credit_stats_loan , loan_types=loan_types, loan_metric=LoanMetric.INTEREST_RATE.value, display_mode=display_mode_loan)
        df.rename({'FIN_METRIC': 'Loan Types', 
                   LoanMetric.INTEREST_RATE.value: 'Mean Annualised Interest Rate (in %)', 
                   'CREDIT_STATUS': 'Credit Worthiness'}, axis=1, inplace=True)
        title = 'Mean Annualised Interest Rate by Loan Types and Credit Worthiness'
        fig = px.bar(df, x='Loan Types', y='Mean Annualised Interest Rate (in %)', color='Credit Worthiness', title=title, width=400, height=500)
        st.plotly_chart(fig)
    
with col_tenure:
    if display_mode_loan == DisplayMode.ALL.value:
        df = compute_loan_metric(credit_stats=None, loan_types=loan_types, loan_metric=LoanMetric.TENURE.value ,display_mode=display_mode_loan)
        df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.TENURE.value: 'Mean Loan Tenure (in Months)'}, axis=1, inplace=True)
        title = 'Mean Tenure by Loan Types'
        fig = px.bar(df, x='Loan Types', y='Mean Loan Tenure (in Months)', color='Loan Types', title=title, width=400, height=500)
        st.plotly_chart(fig)
    
    elif display_mode_loan == DisplayMode.DECOMPOSED.value:
        df = compute_loan_metric(credit_stats=credit_stats_loan , loan_types=loan_types, loan_metric=LoanMetric.TENURE.value, display_mode=display_mode_loan)
        df.rename({'FIN_METRIC': 'Loan Types', 
                   LoanMetric.TENURE.value: 'Mean Loan Tenure (in Months)', 
                   'CREDIT_STATUS': 'Credit Worthiness'}, axis=1, inplace=True)
        title = 'Mean Tenure by Loan Types and Credit Worthiness'
        fig = px.bar(df, x='Loan Types', y='Mean Loan Tenure (in Months)', color='Credit Worthiness', title=title, width=400, height=500)
        st.plotly_chart(fig)

with col_yield_grp:
    if display_mode_loan == DisplayMode.ALL.value:
        df = compute_yield_group(credit_stats=None, loan_types=loan_types, display_mode=display_mode_loan)
        df.rename({'FIN_METRIC': 'Loan Types', LoanMetric.YIELD_GRP.value: 'Previous Yield Group'}, axis=1, inplace=True)

        title = 'Composition of Yield Group by Loan Type'
        fig = px.bar(df, x='Loan Types', y='Count', 
                     color='Previous Yield Group', color_discrete_sequence=['forestgreen',  'red', 'yellowgreen', 'darkgreen'], 
                     title=title, width=400, height=500)
        st.plotly_chart(fig)

    elif display_mode_loan == DisplayMode.DECOMPOSED.value:
        df = compute_yield_group(credit_stats=credit_stats_loan, loan_types=loan_types, display_mode=display_mode_loan)
        title = 'Composition of Yield Group by Credit Worthiness'
        fig = px.bar(df, x=df.columns, y=df.index, color_discrete_sequence=['forestgreen',  'red', 'yellowgreen', 'darkgreen'],
                     title=title, width=400, height=500)
        st.plotly_chart(fig)