# Dashboard with Completed Cash Loans Information for Home Credit.

## Links
1. Original dataset from [Home Credit](https://www.kaggle.com/competitions/home-credit-default-risk/data).
2. [Jupyter notebook](https://github.com/HoWeiChin/GA_Capstone/blob/main/extracting-instalment-payment-features.ipynb) to extract the Completed Cash Loans data.
3. The interactive [Dashboard](https://howeichin-ga-capstone-homecreditdashboard-app-hg8136.streamlit.app/) deployed as a streamlit app.

## Background
<p>I created this dashboard to visualise data obtained from completed cash loan. </p>

### Loan Categories
I classifed the completed cash loans into 4 categories:
1. Prepaid Loans.
2. Defaulted Loans.
3. Late Loans with penalty imposed.
4. Profitable Loans.

### Definition

**Fixed Income and Time Value of Money definitions**:
1. **Future Value**: Principal + Interest earned on the Principal.
2. **Total Loan Repaid**: Principal + any Interest paid by a borrower.
3. **Early repayment of principal/prepayment**: Principal is repaid before the full duration of the loan. A lender loses potential interest revenue due to prepayment.
4. **Late repayment of principal**:  Principal is repaid after the full duration of the loan.
5. **Yield Group**: This is a categorical measure of credit risk of a loan.

**Definition of 4 loan categories**:
1. **Prepaid**: Prepayment causes potential interest revenue to be lost, but there are no unpaid oligations: **Total Loan Repaid** < **Future Value**.
2. **Defaulted**: Late repayment with unpaid interest obligations: **Total Loan Repaid** < **Future Value**.
3. **Late**: Late repayment with late penalties paid: **Total Loan Repaid** > **Future Value**.
4. **Profitable**: Loan principals which were prepaid or repaid timely. These loans are profitable because **Total Loan Repaid** > **Principal**.

## Goals
The dashboard answers the following:
1. How much prepayment/default losses were sustained?
2. How much profit were obtained?
3. How much penalty were imposed?
4. What is the average interest rates/loan tenure for each loan category?
5. What is the yield group composition for each loan category?

Note 1: 
1. The dashboard displays information for borrowers who are currently classified as defaulters or non-defaulters.
2. The completed loans represent the current borrowers' histories of borrowing cash loans and repay the principals to Home Credit.

Note 2: 
1. First 3 metrics are related to business profitability. 
2. 4th metrics are related to fixed income risk. 
3. 5th metric visualises credit migration when the dashboard decomposes the data into current defaulters and non-defaulters:
    1. For example, under "Select Display Mode", choose "Decomposed".
    2. The visualisation (rightmost of 2nd row) shows that 92, 000 loans were previously classified as "Middle" risk. But the borrowers of these previous loans were now labelled as "No Default".

## Dashboard Modes
The dashboard has 2 modes currently:
1. **All**: Aggregates the data related to current defaulters and non-defaulters.
2. **Decomposed**: Decomposes the data into current defaulters and/or non-defaulters.
