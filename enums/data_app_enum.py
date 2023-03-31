from enum import Enum

class FinMetric(Enum):
    PREPAID_LOSSES = 'PREPAID_LOSSES'
    DEFAULT_LOSSES = 'DEFAULT_LOSSES'
    PENALTY_IMPOSED = 'PENALTY_IMPOSED'
    PROFIT = 'PROFIT'


class LoanMetric(Enum):
    INTEREST_RATE = 'INTEREST_RATE'
    TENURE = 'FINAL_INSTAL_NUM'
    YIELD_GRP = 'NAME_YIELD_GROUP'

class LoanType(Enum):
    DEFAULTED = 'Defaulted Loan'
    LATE = 'Late Loan'
    PREPAID = 'Prepaid Loan'
    PROFITABLE = 'Profitable Loan'