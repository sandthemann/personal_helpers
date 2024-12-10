import pandas as pd
from shoskar.utils.functions import filter_kwargs

def auto_numeric(df, **kwargs):

    possible_column_kwarg_names = ['cols', 'columns', 'select']
    default_excl = ['int', 'float', 'datetime']
    kwargs['exclude'] = default_excl + (kwargs.get('exclude') or [])
    kwargs['errors'] = kwargs.get('errors') or 'raise'
    base_cols = df.select_dtypes(**filter_kwargs(pd.DataFrame.select_dtypes, kwargs)).columns
    if (kwarg_cols:=list(dict.fromkeys(sum([kwargs.get(i, []) for i in possible_column_kwarg_names], [])))):
         conversion_columns = [col for col in kwarg_cols if col in base_cols]
    else:
         conversion_columns = base_cols

    to_numeric_kwargs = filter_kwargs(pd.to_numeric, kwargs)
    for col in conversion_columns:
            try:
                # convert the column to numeric, coercing errors
                df[col] = pd.to_numeric(df[col], **to_numeric_kwargs).astype(float)
            except Exception as e:
                 print(f'unable to convert column {col} to a numeric type - {e}')
    return df