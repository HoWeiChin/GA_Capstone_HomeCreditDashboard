import pandas as pd
from pathlib import Path
from data_app_enum import FinMetric, ComputeMode

data_folder = Path('data')

_prepaid = pd.read_csv(data_folder / 'prepaid.csv')
_defaulted = pd.read_csv(data_folder / 'defaulted.csv')
_late_but_repaid = pd.read_csv(data_folder / 'late_but_repaid.csv')

_df_dict = {FinMetric.DEFAULT_LOSSES.value: _defaulted, 
            FinMetric.PREPAID_LOSSES.value: _prepaid,
            FinMetric.PENALTY_IMPOSED.value: _late_but_repaid}

def load_all_data() -> tuple[pd.DataFrame]:
    return _defaulted, _late_but_repaid, _prepaid

def load_feature(feature:str) -> tuple[str]:

    defaulted, late_but_repaid, prepaid = load_all_data()

    info_set_1 = set(defaulted[feature].unique())
    info_set_2 = set(late_but_repaid[feature].unique())
    info_set_3 = set(prepaid[feature].unique())

    union_set = info_set_1.union(info_set_2).union(info_set_3)
    
    return sorted(tuple(union_set))

def compute_fin_metric(credit_stats: list[str], 
                       metric:str, compute_mode: str) -> pd.DataFrame:
    df = _df_dict[metric]

    result_dict = {}

    if len(credit_stats) == 2:
        default_result = None
        non_default_result = None

        if compute_mode == ComputeMode.MEAN.value:
            default_result = round(df[df.TARGET == 1][metric].mean() / 10**3, 2)
            non_default_result = round(df[df.TARGET == 0][metric].mean() / 10**3, 2)
        
        elif compute_mode == ComputeMode.SUM.value:
            default_result = round(df[df.TARGET == 1][metric].sum() / 10**3, 2)
            non_default_result = round(df[df.TARGET == 0][metric].sum() / 10**3, 2)
        
        result_dict['CREDIT_STATUS'] = ['Non-Default', 'Default']
        result_dict[metric] = [non_default_result, default_result]
        
    elif 'Default' in credit_stats:
        default_result = None
        if compute_mode == ComputeMode.MEAN.value:
            default_result = round(df[df.TARGET == 1][metric].mean() / 10**3, 2)
        
        elif compute_mode == ComputeMode.SUM.value:
            default_result = round(df[df.TARGET == 1][metric].sum() / 10**3, 2)
        
        result_dict['CREDIT_STATUS'] = ['Default']
        result_dict[metric] = [default_result]

    elif 'No Default' in credit_stats:
        non_default_result = None

        if compute_mode == ComputeMode.MEAN.value:
            non_default_result = round(df[df.TARGET == 0][metric].mean() / 10**3, 2)
        
        elif compute_mode == ComputeMode.SUM.value:
            non_default_result = round(df[df.TARGET == 0][metric].sum() / 10**3, 2)
        
        result_dict['CREDIT_STATUS'] = ['Non-Default']
        result_dict[metric] = [non_default_result]
    
    return pd.DataFrame.from_dict(result_dict)

def compute_loan_metric(credit_stats: list[str],
                       loan_metric:str) -> pd.DataFrame:
    
    result_dict = {'CREDIT_STATUS': [], 
                   loan_metric: [], 
                   'FIN_METRIC_TYPE': []}

    for fin_metric, df in _df_dict.items():
        
        if 'Default' in credit_stats:

            default_result = round(df[df.TARGET == 1][loan_metric].mean(), 2)
            result_dict['CREDIT_STATUS'].append('Default')
            result_dict[loan_metric].append(default_result)
            result_dict['FIN_METRIC_TYPE'].append(fin_metric)
        
        if 'No Default' in credit_stats:
            non_default_result = round(df[df.TARGET == 0][loan_metric].mean(), 2)
            result_dict['CREDIT_STATUS'].append('Non-Default')
            result_dict[loan_metric].append(non_default_result)
            result_dict['FIN_METRIC_TYPE'].append(fin_metric)
    
    def mapper(fin_metric_type):
        if fin_metric_type == FinMetric.DEFAULT_LOSSES.value:
            return 'Defaulted loans'
        
        elif fin_metric_type == FinMetric.PREPAID_LOSSES.value:
            return 'Prepaid loans'
        
        return 'Late but repaid Loans'
        
    df = pd.DataFrame.from_dict(result_dict)
    df['FIN_METRIC_TYPE'] = df['FIN_METRIC_TYPE'].apply(mapper)

    return df