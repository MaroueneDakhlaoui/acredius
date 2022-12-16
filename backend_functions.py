import os
import pandas as pd
import numpy as np
import webbrowser
from IPython.display import display, HTML


def data_reader():
    folder = 'Data/'  # <--- find the folder
    files = os.listdir(folder)  # <--- find all the files inside the folder
    nb_files = len(files)  # <--- How many files inside the folder ? (should be just one)
    if nb_files != 1:  # <--- If more than one file in the world we can't proceed, so we stop the process and notify
        # the user
        raise Exception(
            "Process stopped!, Make sure you have just one file in the folder, AND THAT IT IS NOT CURRENTLY "
            "OPENED")
    file = files[0]  # <--- Get the only file inside the folder
    if not file.endswith("xlsx"):  # <--- Make sure it has the correct extension
        raise Exception("Process stopped!, Make sure your file extension is xlsx")
    file_path = str(folder) + str(file)  # <--- Get the full file path
    initial_df = pd.read_excel(file_path)  # <--- Read it as a python dataframe to return it
    return initial_df


def data_head(df_param):
    return df_param.head(8)


def columns_rename(df_param):
    df_param = df_param.rename(columns={"Chiffre d'Affaires 15": 'CA15', "Chiffre d'Affaires 16": 'CA16',
                                        "Chiffre d'Affaires 17": 'CA17', "Chiffre d'Affaires 18": 'CA18',
                                        "Evolution du Chiffre d'Affaires 15": 'EV_CA15',
                                        "Evolution du Chiffre d'Affaires 16": 'EV_CA16',
                                        "Evolution du Chiffre d'Affaires 17": 'EV_CA17',
                                        "Evolution du Chiffre d'Affaires 18": 'EV_CA18', })
    return df_param


def describe_data_pipeline(df_param):
    df_param = df_param.replace(r'^\s*$', np.nan, regex=True)  # <--- Replace empty values with null values
    null_percent = df_param.isnull().sum() / df_param.shape[0]  # <--- Get the percentage of
    # null values for each column
    over_30_null = round(100 * (null_percent[null_percent >= 0.3]), 2)  # <--- columns with 30% or more null values
    under_30_null = round(100 * (null_percent[null_percent < 0.3]), 2)  # <--- columns with less than 30% null values
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(over_30_null.size, " Columns with 30% or more missing values")
        print("These Columns are:\n", over_30_null)
    print("/////////////////////////////////////////////////////////////////")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(under_30_null.size, " Columns with less than 30% missing values")
        print("These Columns are:\n", under_30_null)
    returned_dataframes = {
        'over_30': over_30_null,
        'under_30': under_30_null
    }
    return returned_dataframes


def size_of_series(entry_series):
    sr_size = entry_series.size
    out = "The number of columns that have more than 30% is " + str(sr_size)
    return out


def unique_stats(param_column):
    return param_column.value_counts()


def null_in_four_years(param_df, param_column1, param_column2, param_column3, param_column4):
    temp_df = param_df[
        param_df[param_column1].isnull() & param_df[param_column2].isnull() & param_df[param_column3].isnull() &
        param_df[param_column4].isnull()]
    occurences = len(temp_df)
    occ_percent = round(100 * occurences / len(param_df), 2)
    output_message = "These 4 fields are null together in " + str(occurences) + " Occurrences, meaning in " + str(
        occ_percent) + "% Of the data "
    return output_message


def keep_not_null_together(param_df, param_column1, param_column2, param_column3, param_column4):
    temp_df = param_df[param_df[[param_column1, param_column2, param_column3,
                                 param_column4]].notnull().any(axis=1)]
    return temp_df


def create_recent_variable(param_df, param_column1, param_column2, param_column3, param_column4):
    param_df['recent_CA'] = np.where(
        param_df[param_column4].notnull(),
        param_df[param_column4],
        np.where(
            param_df[param_column3].notnull(),
            param_df[param_column3],
            np.where(
                param_df[param_column2].notnull(),
                param_df[param_column2],
                param_df[param_column1],
            )
        )
    )
    return param_df



def clean_column(df, col_name):
    # Cast column to string
    df[col_name] = df[col_name].astype(str)

    # Remove non-int characters
    df[col_name] = df[col_name].replace('[^0-9.]', '', regex=True)

    # Cast column values to floats with 2 decimals
    for i, row in df.iterrows():
        try:
            df.at[i, col_name] = round(float(row[col_name]), 2)
        except ValueError:
            df.at[i, col_name] = None
    return df
