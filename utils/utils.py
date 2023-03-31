import pandas as pd
import numpy as np
from pathlib import Path
from enums.data_app_enum import FinMetric, LoanMetric, LoanType

data_folder = Path('data')

_profit = pd.read_csv(data_folder / 'profit.csv')
_prepaid = pd.read_csv(data_folder / 'prepaid.csv')
_defaulted = pd.read_csv(data_folder / 'defaulted.csv')
_late_but_repaid = pd.read_csv(data_folder / 'late_but_repaid.csv')

_df_dict = {FinMetric.DEFAULT_LOSSES.value: _defaulted, 
            FinMetric.PREPAID_LOSSES.value: _prepaid,
            FinMetric.PENALTY_IMPOSED.value: _late_but_repaid,
            FinMetric.PROFIT.value: _profit}

def loan_to_metric(loan):
    if loan == LoanType.DEFAULTED.value:
        return FinMetric.DEFAULT_LOSSES.value
    
    elif loan == LoanType.PREPAID.value:
        return FinMetric.PREPAID_LOSSES.value
    
    elif loan == LoanType.PROFITABLE.value:
        return FinMetric.PROFIT.value
    
    return FinMetric.PENALTY_IMPOSED.value

def load_all_data() -> tuple[pd.DataFrame]:
    return _defaulted, _late_but_repaid, _prepaid

def load_feature(feature:str) -> tuple[str]:

    defaulted, late_but_repaid, prepaid = load_all_data()

    info_set_1 = set(defaulted[feature].unique())
    info_set_2 = set(late_but_repaid[feature].unique())
    info_set_3 = set(prepaid[feature].unique())

    union_set = info_set_1.union(info_set_2).union(info_set_3)
    
    return sorted(tuple(union_set))

def compute_fin_metric():
    
    def mapper(fin_metric):
        if fin_metric == FinMetric.DEFAULT_LOSSES.value:
            return 'Default Losses'
        elif fin_metric == FinMetric.PREPAID_LOSSES.value:
            return 'Prepaid Losses'
        elif fin_metric == FinMetric.PENALTY_IMPOSED.value:
            return 'Penalty Imposed'
        return 'Profit'
    
    result_dict = {'FIN_METRIC': [], 'VALUE': []}
 
    for fin_metric, df in _df_dict.items():
        result = round(df[fin_metric].mean() / 10**3, 2)        
        if fin_metric in [FinMetric.DEFAULT_LOSSES.value, FinMetric.PREPAID_LOSSES.value]:
            result = result * -1

        result_dict['FIN_METRIC'].append(fin_metric)
        result_dict['VALUE'].append(result)
        
    result = pd.DataFrame.from_dict(result_dict)
    result['FIN_METRIC'] = result['FIN_METRIC'].apply(mapper)
    return result

def show_composition(loan_type):
    df = _profit
    if loan_type == LoanType.DEFAULTED.value:
        df = _defaulted
    
    elif loan_type == LoanType.LATE.value:
        df = _late_but_repaid
    
    elif loan_type == LoanType.PREPAID.value:
        df = _prepaid

    df_trimmed = df \
                .filter(['NAME_YIELD_GROUP']) \
                
    result = (df_trimmed.groupby('NAME_YIELD_GROUP')['NAME_YIELD_GROUP'].count().rename("% of Each Yield Group") / df_trimmed['NAME_YIELD_GROUP'].count()) * 100
    result = result.reset_index()
    result["% of Each Yield Group"] = np.round(result["% of Each Yield Group"])
    return result.rename({'NAME_YIELD_GROUP': 'Yield Group'}, axis=1)
 
def compute_loan_metric(loan_types: list[str],
                       loan_metric:str) -> pd.DataFrame:
    
    result_dict = { loan_metric: [], 
                   'FIN_METRIC': []}
    
    loan_to_fin_data = [loan_to_metric(loan_type) for loan_type in loan_types]

    for fin_metric, df in _df_dict.items():

        if fin_metric not in loan_to_fin_data:
            continue

        result = round(df[loan_metric].mean(), 2)

        result_dict[loan_metric].append(result)
        result_dict['FIN_METRIC'].append(fin_metric)

    def mapper(fin_metric_type):
        if fin_metric_type == FinMetric.DEFAULT_LOSSES.value:
            return 'Defaulted loans'
        
        elif fin_metric_type == FinMetric.PREPAID_LOSSES.value:
            return 'Prepaid loans'
        
        elif fin_metric_type == FinMetric.PROFIT.value:
            return 'Profitable Loans'
        
        return 'Late Loans'
        
    df = pd.DataFrame.from_dict(result_dict)
    df['FIN_METRIC'] = df['FIN_METRIC'].apply(mapper)

    return df

def compute_yield_group(loan_types: list[str]) -> pd.DataFrame:
    
    loan_metric = LoanMetric.YIELD_GRP.value
    dfs = []

    loan_to_fin_data = [loan_to_metric(loan_type) for loan_type in loan_types]

    for fin_metric, df in _df_dict.items():
        if fin_metric not in loan_to_fin_data:
            continue

        dfs.append(df[df.TARGET == 1])
        dfs.append(df[df.TARGET == 0])
            
    def mapper(fin_metric_type):
        if fin_metric_type == FinMetric.DEFAULT_LOSSES.value:
            return 'Defaulted loans'
        
        elif fin_metric_type == FinMetric.PREPAID_LOSSES.value:
            return 'Prepaid loans'
        
        elif fin_metric_type == FinMetric.PROFIT.value:
            return 'Profitable Loans'
        return 'Late Loans'
    
    df = pd.concat(dfs)

    
    df = df \
        .groupby(['TARGET', loan_metric])['SK_ID_PREV'] \
        .count() \
        .reset_index() \
        .rename({'SK_ID_PREV': 'Count', 'TARGET': 'Credit Worthiness', loan_metric: 'Previous Yield Group'}, axis=1)
        
    def credit_mapper(value):
        if value:
            return 'Default'
        return 'No Default'
        
    df['Credit Worthiness'] = df['Credit Worthiness'].apply(credit_mapper)
    df = df.pivot(index='Credit Worthiness', columns='Previous Yield Group', values='Count')

    return df