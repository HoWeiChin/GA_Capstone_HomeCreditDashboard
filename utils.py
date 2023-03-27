import pandas as pd
from pathlib import Path
from data_app_enum import FinMetric, ComputeMode, DisplayMode, LoanMetric, LoanType

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

def compute_loan_metric(credit_stats: list[str], loan_types: list[str],
                       loan_metric:str, display_mode:str) -> pd.DataFrame:
    
    result_dict = { loan_metric: [], 
                   'FIN_METRIC': []}
    
    if display_mode == DisplayMode.DECOMPOSED.value:
        result_dict['CREDIT_STATUS'] = []

    loan_to_fin_data = [loan_to_metric(loan_type) for loan_type in loan_types]

    for fin_metric, df in _df_dict.items():

        if fin_metric not in loan_to_fin_data:
            continue

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
        
        elif fin_metric_type == FinMetric.PROFIT.value:
            return 'Profitable Loans'
        
        return 'Late Loans'
        
    df = pd.DataFrame.from_dict(result_dict)
    df['FIN_METRIC'] = df['FIN_METRIC'].apply(mapper)

    return df

def compute_yield_group(credit_stats: list[str], loan_types: list[str],
                       display_mode:str) -> pd.DataFrame:
    
    loan_metric = LoanMetric.YIELD_GRP.value
    dfs = []

    loan_to_fin_data = [loan_to_metric(loan_type) for loan_type in loan_types]

    for fin_metric, df in _df_dict.items():
        if fin_metric not in loan_to_fin_data:
            continue

        if display_mode == DisplayMode.ALL.value:
            result = df \
                    .groupby([loan_metric])['SK_ID_PREV'] \
                    .count() \
                    .reset_index()
                
            result.rename({'SK_ID_PREV': 'Count'}, axis=1, inplace=True)
            result['FIN_METRIC'] = fin_metric
            dfs.append(result)
        
        elif display_mode == DisplayMode.DECOMPOSED.value:

            if 'Default' in credit_stats:
                dfs.append(df[df.TARGET == 1])


            if 'No Default' in credit_stats:
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
    if display_mode == DisplayMode.ALL.value:
        df['FIN_METRIC'] = df['FIN_METRIC'].apply(mapper)
    
    if display_mode == DisplayMode.DECOMPOSED.value:
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