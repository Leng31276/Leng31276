import pandas as pd

from pathlib import Path

def import_csv(directory):
    dirpath = Path(directory)
    assert dirpath.is_dir()

    df = pd.DataFrame()
    for file in dirpath.glob('*.csv'):
        if file.is_file():
            tmp_df = pd.read_csv(file)
            if df.empty:
                df = tmp_df
            else:    
                df = df.append(tmp_df)
    
    return df.reset_index(drop=True)

def create_pivot(df, index_list=[], value_list=[]):
    """
    Read the DataFrame, create a pivot table and return it as a DataFrame
    """
    return pd.pivot_table(df, index=index_list, values=value_list, fill_value=0)


def save_report(df, outfile):
    """
    Take a report and save it to a single Excel file
    """
    with pd.ExcelWriter(outfile) as writer:
        df.to_excel(writer)
