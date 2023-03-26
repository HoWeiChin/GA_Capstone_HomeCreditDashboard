from enum import Enum

class FinMetric(Enum):
    PREPAID_LOSSES = 'PREPAID_LOSSES'
    DEFAULT_LOSSES = 'DEFAULT_LOSSES'
    PENALTY_IMPOSED = 'PENALTY_IMPOSED'
    PROFIT = 'PROFIT'

class ComputeMode(Enum):
    SUM = 'Sum'
    MEAN = 'Mean'

class DisplayMode(Enum):
    ALL = 'All'
    DECOMPOSED = 'Decomposed'

class CreditStats(Enum):
    DEFAULT = 'Default'
    NO_DEFAULT = 'No Default'

class LoanMetric(Enum):
    INTEREST_RATE = 'INTEREST_RATE'
    TENURE = 'FINAL_INSTAL_NUM'
    YIELD_GRP = 'NAME_YIELD_GROUP'