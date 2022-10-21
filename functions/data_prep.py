import pandas as pd
import numpy as np

# Forex 
from forex_python.converter import get_rate
from datetime import datetime

def fish_out_col_lst(df, 
                     col_idx = 0,
                     separator = ','
                    ):
    
    """Retrieve list of columns had the df been a nice csv"""

    # Fish out column list
    col_lst = df.columns[col_idx].split(separator)
    col_lst = [col.strip() for col in col_lst if col != '']
    # Replace spaces with underscores in columns' names!!!!!
    col_lst = [col.replace(' ', '_') for col in col_lst]
    
    return col_lst

def data_to_cols(df,
                 merged_col_name, 
                 col_lst,
                 title_col_name = 'name',
                 separator = ',',
                 n_col_with_commas = 2, # The 2nd column has commas
                 title_col_idx = 0, # first column has titles
                ):
    
    """All data in excel condensed in one column, 
    this function to convert one long string column into multiple columns"""
    
    # Create df with all the data with consistent comma separation
    df_right = df[merged_col_name].str.rsplit(separator, 
                                       len(col_lst) - n_col_with_commas, # Because commas are in the second column
                                       expand = True)
    
    # Seperate the column containing the names of the campaign
    title_col = df_right.iloc[:, title_col_idx]

    # Drop first column of dataframe
    df_right = df_right.iloc[:, title_col_idx + 1:]

    # Create df with all the data with consistent comma separation, with maxsplit of 1 to remove indices
    titles = [title.split(separator, 1) for title in title_col]

    # Ditch the index because not informative
    # Would need to make sure they contain no information on the campaign though
    titles = [title[-1] for title in titles]

    # Ensure we've kept all the titles that had commas 
    assert len([title for title in titles if separator in title]) > 0

    # Now name columns on df_right
    df_right.columns = col_lst[n_col_with_commas:]

    # Add the titles back into the df
    df_right[title_col_name] = titles
    # And change df_right to something appropriate
    df_prep = df_right.copy()
    
    return df_prep

def condense_category(col, 
                      df,
                      min_freq = 2.5, 
                      new_name = 'other'):
    
    """Combining extraneous occurences into one other category"""
    series = pd.value_counts(df[col])
    mask = (series/series.sum() * 100).lt(min_freq)
    
    # To replace df['column'] use np.where I.e 
    return np.where(df[col].isin(series[mask].index),'Other', df[col])

def change_dtype(df, 
                 col, 
                 dtype):
    
    if dtype == 'date':
        df[col] = pd.to_datetime(df[col])

    else:
        df[col] = df[col].astype(dtype)

    return df

def create_country_dict(df_prep, 
                        exclude_eur = True):
    
    # From currency and country cols - infer who belongs to what country from currency
    
    # Cannot infer country from currency because well - the EUR, but can infer country from most currencies
    country_dict = dict(zip(df_prep.currency.to_list(),
             df_prep.country.to_list()))
    if exclude_eur == True:
        country_dict = {i:country_dict[i] for i in country_dict if i!= 'EUR'}
    
    return country_dict

def impute_missing_amounts(df_prep,
                           value_to_replace, 
                           country_dict, 
                           currency_col_to_impute, 
                           country_col_to_impute,
                           base_currency = 'USD',
                           substitute_for_eur = 'Other'): 
    
    for row in df_prep.itertuples():
        if row.country == value_to_replace:
            t = datetime(row.deadline.year, row.deadline.month, row.deadline.day)
            fx_rate = get_rate(row.currency, base_currency, t)

            # Impute missing values
            df_prep.at[row.Index, currency_col_to_impute] = float(row.pledged) * fx_rate

            if row.currency != 'EUR':
                df_prep.at[row.Index, country_col_to_impute] = country_dict[row.currency]
            else:
                # Convert the EUR rows to keep it clean
                df_prep.at[row.Index, country_col_to_impute] = substitute_for_eur

    return df_prep