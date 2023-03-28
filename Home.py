import streamlit as st

st.markdown("# Goal :goal_net:")

goal_txt = """
The dashboard answers the following:
1. How much prepayment/default losses were sustained?
2. How much profit were obtained?
3. How much penalty were imposed?
4. What is the average interest rates/loan tenure for each loan category?
5. What is the yield group composition for each loan category?

Notes:
1. The dashboard displays information for borrowers who are currently classified as defaulters or non-defaulters.
2. The completed loans represent the current borrowers' histories of borrowing cash loans and repay the principals to Home Credit.
3. First 3 metrics are related to business profitability. 
4. 4th metrics are related to fixed income risk. 
5. 5th metric visualises credit migration when the dashboard decomposes the data into current defaulters and non-defaulters.
"""
st.markdown(goal_txt)

st.subheader('Future Works')
st.write(
    """
    This dashboard is an initial prototype. I plan to enhance the UI/UX of the dashboard.
    """
)

c1, c2, c3 = st.columns(3)
with c1:
    st.info('**Data Analyst: [Ho Wei Chin]**')
with c2:
    st.info('**GitHub: [@HoWeiChin](https://github.com/HoWeiChin/GA_Capstone_HomeCreditDashboard)**')
with c3:
    st.info('**Data: [Home Credit Kaggle Competition](https://www.kaggle.com/competitions/home-credit-default-risk/data)**')