import pandas as pd
from pathlib import Path
from data_app_enum import FinMetric, ComputeMode, DisplayMode, LoanMetric

data_folder = Path('data')

_profit = pd.read_csv(data_folder / 'profit.csv')
_prepaid = pd.read_csv(data_folder / 'prepaid.csv')
_defaulted = pd.read_csv(data_folder / 'defaulted.csv')
_late_but_repaid = pd.read_csv(data_folder / 'late_but_repaid.csv')

_df_dict = {FinMetric.DEFAULT_LOSSES.value: _defaulted, 
            FinMetric.PREPAID_LOSSES.value: _prepaid,
            FinMetric.PENALTY_IMPOSED.value: _late_but_repaid,
            FinMetric.PROFIT.value: _profit}

def load_all_data() -> tuple[pd.DataFrame]:
    return _defaulted, _late_but_repaid, _prepaid

def load_feature(feature:str) -> tuple[str]:

    defaulted, late_but_repaid, prepaid = load_all_data()

    info_set_1 = set(defaulted[feature].unique())
    info_set_2 = set(late_but_repaid[feature].unique())
    info_set_3 = set(prepaid[feature].unique())

    union_set = info_set_1.union(info_set_2).union(info_set_3)
    
    return sorted(tuple(union_set))

def compute_fin_metric(credit_stats:list[str], 
                       compute_mode:str, display_mode:str):
    
    def mapper(fin_metric):
        if fin_metric == FinMetric.DEFAULT_LOSSES.value:
            return 'Default Losses'
        elif fin_metric == FinMetric.PREPAID_LOSSES.value:
            return 'Prepaid Losses'
        elif fin_metric == FinMetric.PENALTY_IMPOSED.value:
            return 'Penalty Imposed'
        return 'Profit'
    
    result_dict = {'FIN_METRIC': [], 'VALUE': []}
    if display_mode == DisplayMode.ALL.value:
        
        for fin_metric, df in _df_dict.items():

            if compute_mode == ComputeMode.MEAN.value:
                result = round(df[fin_metric].mean() / 10**3, 2)
            
            elif compute_mode == ComputeMode.SUM.value:
                result = round(df[fin_metric].sum() / 10**3, 2)
            
            result_dict['FIN_METRIC'].append(fin_metric)
            result_dict['VALUE'].append(result)
        
    elif display_mode == DisplayMode.DECOMPOSED.value:
        result_dict['CREDIT_STATUS'] = []

        for fin_metric, df in _df_dict.items():
        
            if 'Default' in credit_stats:
                default_result = round(df[df.TARGET == 1][fin_metric].sum(), 2)

                if compute_mode == ComputeMode.MEAN.value:
                    default_result = round(df[df.TARGET == 1][fin_metric].mean(), 2)

                result_dict['CREDIT_STATUS'].append('Default')
                result_dict['VALUE'].append(default_result)
                result_dict['FIN_METRIC'].append(fin_metric)
        
            if 'No Default' in credit_stats:
                non_default_result = round(df[df.TARGET == 0][fin_metric].sum(), 2)

                if compute_mode == ComputeMode.MEAN.value:
                    non_default_result = round(df[df.TARGET == 0][fin_metric].mean(), 2)

                result_dict['CREDIT_STATUS'].append('Non-Default')
                result_dict['VALUE'].append(non_default_result)
                result_dict['FIN_METRIC'].append(fin_metric)
    
    result = pd.DataFrame.from_dict(result_dict)
    result['FIN_METRIC'] = result['FIN_METRIC'].apply(mapper)
    return result

def compute_loan_metric(credit_stats: list[str],
                       loan_metric:str, display_mode:str) -> pd.DataFrame:
    
    result_dict = { loan_metric: [], 
                   'FIN_METRIC': []}
    
    if display_mode == DisplayMode.DECOMPOSED.value:
        result_dict['CREDIT_STATUS'] = []

    for fin_metric, df in _df_dict.items():

        if display_mode == DisplayMode.ALL.value:
            result = round(df[loan_metric].mean(), 2)

            result_dict[loan_metric].append(result)
            result_dict['FIN_METRIC'].append(fin_metric)

        elif display_mode == DisplayMode.DECOMPOSED.value:
        
            if 'Default' in credit_stats:

                default_result = round(df[df.TARGET == 1][loan_metric].mean(), 2)
                result_dict['CREDIT_STATUS'].append('Default')
                result_dict[loan_metric].append(default_result)
                result_dict['FIN_METRIC'].append(fin_metric)
        
            if 'No Default' in credit_stats:
                non_default_result = round(df[df.TARGET == 0][loan_metric].mean(), 2)
                result_dict['CREDIT_STATUS'].append('Non-Default')
                result_dict[loan_metric].append(non_default_result)
                result_dict['FIN_METRIC'].append(fin_metric)
    
    def mapper(fin_metric_type):
        if fin_metric_type == FinMetric.DEFAULT_LOSSES.value:
            return 'Defaulted loans'
        
        elif fin_metric_type == FinMetric.PREPAID_LOSSES.value:
            return 'Prepaid loans'
        
        return 'Late Loans'
        
    df = pd.DataFrame.from_dict(result_dict)
    df['FIN_METRIC'] = df['FIN_METRIC'].apply(mapper)

    return df

def compute_yield_group(credit_stats: list[str],
                       loan_metric:str) -> pd.DataFrame:
    
    dfs = []
    for fin_metric, df in _df_dict.items():
        
        if 'Default' in credit_stats:
            default_result = df[df.TARGET == 1] \
                            .groupby([loan_metric])['SK_ID_PREV'] \
                            .count() \
                            .reset_index()
            default_result['CREDIT_STATUS'] = 'Default'
            default_result['FIN_METRIC_TYPE'] = fin_metric
            dfs.append(default_result)
        
        if 'No Default' in credit_stats:
            non_default_result = df[df.TARGET == 0] \
                                .groupby([loan_metric])['SK_ID_PREV']\
                                .count() \
                                .reset_index()
            non_default_result['CREDIT_STATUS'] = 'Non-Default'
            non_default_result['FIN_METRIC_TYPE'] = fin_metric
            dfs.append(non_default_result)
    
    def mapper(fin_metric_type):
        if fin_metric_type == FinMetric.DEFAULT_LOSSES.value:
            return 'Defaulted loans'
        
        elif fin_metric_type == FinMetric.PREPAID_LOSSES.value:
            return 'Prepaid loans'
        
        return 'Late Loans'
    
    df = pd.concat(dfs)
    df['FIN_METRIC_TYPE'] = df['FIN_METRIC_TYPE'].apply(mapper)
    df.rename({'SK_ID_PREV': 'Loan Counts'}, axis=1, inplace=True)

    #df = df.pivot(index=['FIN_METRIC_TYPE', 'CREDIT_STATUS'], 
                  #columns=loan_metric, values='Loan Counts') 
    print(df)
    return df