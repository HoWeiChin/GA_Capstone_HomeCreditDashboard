from enum import Enum

class FinMetric(Enum):
    PREPAID_LOSSES = 'PREPAID_LOSSES'
    DEFAULT_LOSSES = 'DEFAULT_LOSSES'
    PENALTY_IMPOSED = 'PENALTY_IMPOSED'

class ComputeMode(Enum):
    SUM = 'Sum'
    MEAN = 'Mean'

class CreditStats(Enum):
    DEFAULT = 'Default'
    NO_DEFAULT = 'No Default'

class LoanMetric(Enum):
    INTEREST_RATE = 'INTEREST_RATE'
    TENURE = 'FINAL_INSTAL_NUM'