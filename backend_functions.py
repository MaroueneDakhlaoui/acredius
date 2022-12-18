import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
import plotly.express as px
import re
import webbrowser
from IPython.display import display, HTML


def data_reader():
    """ Reads the excel file from the data folder, makes sure its is just one file and that
    it's not open and notifies the user"""
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
    """ Shows the first 8 rows of the dataframe"""
    return df_param.head(8)


def columns_rename(df_param):
    """ Rename the columns to more significant and less complex strings"""
    df_param = df_param.rename(columns={"Chiffre d'Affaires 15": 'CA15', "Chiffre d'Affaires 16": 'CA16',
                                        "Chiffre d'Affaires 17": 'CA17', "Chiffre d'Affaires 18": 'CA18',
                                        "Evolution du Chiffre d'Affaires 15": 'EV_CA15',
                                        "Evolution du Chiffre d'Affaires 16": 'EV_CA16',
                                        "Evolution du Chiffre d'Affaires 17": 'EV_CA17',
                                        "Evolution du Chiffre d'Affaires 18": 'EV_CA18', })
    return df_param


def describe_data_pipeline(df_param):
    """ This is a pipeline function to provide information about the columns that contain more than 30% missing rows"""
    df_param = df_param.replace(r'^\s*$', np.nan, regex=True)  # <--- Replace empty values with null values
    null_percent = df_param.isnull().sum() / df_param.shape[0]  # <--- Get the percentage of
    # null values for each column
    over_30_null = round(100 * (null_percent[null_percent >= 0.3]), 2)  # <--- columns with 30% or more null values
    under_30_null = round(100 * (null_percent[null_percent < 0.3]), 2)  # <--- columns with less than 30% null values
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(over_30_null.size, " Columns with 30% or more missing values")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(under_30_null.size, " Columns with less than 30% missing values")
    returned_dataframes = {
        'over_30': over_30_null,
        'under_30': under_30_null
    }
    return returned_dataframes


def size_of_series(entry_series):
    """ Get the size of a pandas series and print a custom message for a html"""
    sr_size = entry_series.size
    out = "The number of columns that have more than 30% is " + str(sr_size)
    return out


def unique_stats(param_column):
    """ Display the unique values for a colum along with their occurrences, this will be used a lot for data exploration"""
    pd.options.display.max_rows = 1000
    return param_column.value_counts()


def null_in_four_years(param_df, param_column1, param_column2, param_column3, param_column4):
    """ get the number of rows that are null in 4 specific columns together and print a custom message"""
    temp_df = param_df[
        param_df[param_column1].isnull() & param_df[param_column2].isnull() & param_df[param_column3].isnull() &
        param_df[param_column4].isnull()]
    occurences = len(temp_df)
    occ_percent = round(100 * occurences / len(param_df), 2)
    output_message = "These 4 fields are null together in " + str(occurences) + " Occurrences, meaning in " + str(
        occ_percent) + "% Of the data "
    return output_message


def keep_not_null_together(param_df, param_column1, param_column2, param_column3, param_column4):
    """ For 4 specific columns, keep only the dataframe rows that are not nulll in at least one of them"""
    temp_df = param_df[param_df[[param_column1, param_column2, param_column3,
                                 param_column4]].notnull().any(axis=1)]
    return temp_df


def create_recent_variable(param_df, param_column1, param_column2, param_column3, param_column4, new_column):
    """ Use 4 Columns and get the most recent available value and generate into a new column, then drop the 4"""
    param_df[new_column] = np.where(
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
    param_df = param_df.drop(labels=[param_column1, param_column2, param_column3, param_column4], axis=1)
    return param_df


def make_float(df, col_name):
    """Remove non int characters and cast string to float, This is developed for cleaning the CA column """
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


def count_invalid_rows(df, column):
    """ Try to cast all rows of a dataframe column to float, and return the number of rows that can not be cast
     This is developed to check the possibility of cleaning the column EBE"""
    invalid_rows = 0
    for index, row in df.iterrows():
        try:
            float(row[column])
        except ValueError:
            invalid_rows += 1
    return invalid_rows


def convert_to_median(value):
    """ Try Changing percentage intervals (if they exist) to a median float (10-15% become 7.5), otherwise keep the
        float and clean it, This is developed to use for the resultat_net column"""
    try:
        value = str(value)
        # Remove leading and trailing spaces
        value = value.strip()

        # Replace all percent signs with an empty string
        value = value.replace('%', '')

        # Split the value on the dash and convert the two resulting values to floats
        values = value.split('-')
        values = [float(v) for v in values]

        # Calculate the median of the range by taking the average of the two values
        median = sum(values) / len(values)

        # Return the median, rounded to 1 decimal place
        return round(median, 1)
    except ValueError:
        # If there is a ValueError, return the original value casted to float
        value = str(value)
        value = value.replace(",", ".")
        value = float(value)
        return value


def process_bilan(s: str) -> float:
    """ Process a string, replace with null if it is just a -, repalace with null if it is empty otherwise
    remove whitespaces, replace ',' with '.' for decimals and only keep digits and . then cast to float and return"""
    if s == '-':
        return None
    # Handle empty or null strings to avoid ValueError
    if not s:
        return None

    # Cast all the column rows into str
    s = str(s)

    # Remove whitespaces with the replace function
    s = s.replace(" ", "")

    # Replace ',' with '.' for decimals
    s = s.replace(",", ".")

    # Remove alphabetical letters and the all symbols except . if they exist
    s = ''.join(c for c in s if c.isdigit() or c == '.')
    # Cast all the column rows into float
    return round(float(s), 2)


def process_FP_TB(s: str) -> float:
    """ Cleaning the Fond propres/total bilan column, cast all to just keep the raw percentage as float """
    # Cast all the column rows into str
    s = str(s)

    # Remove percentage symbol with the replace function
    s = s.replace("%", "")

    # Remove whitespaces with the replace function
    s = s.replace(" ", "")

    # Replace ',' with '.' for decimals
    s = s.replace(",", ".")

    # Remove alphabetical letters and the all symbols except . if they exist
    s = ''.join(c for c in s if c.isdigit() or c in ['.', '-'])
    # Cast all the column rows into float
    return round(float(s), 2)


def process_dette_EBE(s: str) -> int:
    """ Cleaning the Dettes nettes / EBE column ,Remove any whitespaces, currency or non int
     characters in money related columns"""
    if s == '-':
        return None
        # Handle empty or null strings to avoid ValueError
    if not s:
        return None

    # Cast all the column rows into str
    s = str(s)

    # Remove whitespaces with the replace function
    s = s.replace(" ", "")

    # Replace ',' with '.' for decimals
    s = s.replace(",", ".")

    # Remove alphabetical letters and the all symbols except . if they exist
    s = ''.join(c for c in s if c.isdigit() or c in ['.', '-'])
    # Cast all the column rows into float
    return round(float(s), 2)


def process_montant_ou_capital(s: str) -> int:
    """ Clean any column in which we want to keep the raw money value as int eg capital or montant"""
    if s == '-':
        return None
    # Cast all the column rows into str
    s = str(s)

    # Remove whitespaces with the replace function
    s = s.replace(" ", "")

    # Replace ',' with '.' for decimals
    s = s.replace(",", ".")

    # Keep only digits
    s = ''.join(c for c in s if c.isdigit())
    # Cast all the column rows into int
    return int(s)


def process_taux(s: str) -> float:
    """ Process our target variable by keeping the raw float interest rate and removing anything else"""
    # Cast all the column rows into str
    s = str(s)

    # Remove percentage symbol with the replace function
    s = s.replace("%", "")

    # Remove whitespaces with the replace function
    s = s.replace(" ", "")

    # Replace ',' with '.' for decimals
    s = s.replace(",", ".")

    # Remove alphabetical letters and the all symbols except . if they exist
    s = ''.join(c for c in s if c.isdigit() or c == '.')
    # Cast all the column rows into float
    return round(float(s), 2)


def encode_risk_category(df, risk_col):
    """ Ordinal Encoding the risk category to provide bias for the model"""
    # Create a mapping of categories to ordinal values
    ordinal_mapping = {'A+': 1, 'A': 2, 'B+': 3, 'B': 4, 'C': 5}
    # Use the `map` function to apply the mapping to the risk category column
    df[risk_col] = df[risk_col].map(ordinal_mapping)
    return df


def process_head_count(s):
    """ Clean the effectifs column to unify the format to a-b eg (0-5) because many formats existed"""
    s = str(s)
    if not s or s == '':
        s = np.nan
    if s == '-':
        return None
    # Cast all the column rows into str
    s = str(s)

    # Remove percentage symbol with the replace function
    s = s.replace("à", "-")

    # Remove whitespaces with the replace function
    s = s.replace(" ", "")
    # Remove alphabetical letters and the all symbols except . if they exist
    s = ''.join(c for c in s if c.isdigit() or c == '-')
    return s


def process_head_count_2(s):
    """ Decided not to go with the above function and develop a new one, we will Keep the strings available and just
    remove whitespaces and dots for now to unify 1000 with 1.000 and 1 000 for example, this function goes along
    with the next one"""
    s = str(s)
    if not s or s == '':
        s = np.nan
    if s == '-':
        return None
    # Cast all the column rows into str
    s = str(s)

    # Remove whitespaces with the replace function
    s = s.replace(" ", "")
    s = s.replace(".", "")
    # Remove alphabetical letters and the all symbols except . if they exist
    return s

def get_first_number(value):
    """Take the inferior part of the interval meaning if the interval is 1 to 10 we will take 1,
if it's plus de 1000 we will take 1000. Basically the first full number present in the string"""
    if pd.isnull(value) or not isinstance(value, str):
        return np.nan
    # split the value by 'à' and take the first element
    split_value = value.split('à')[0]
    # try to convert the first element to an integer
    try:
        return int(split_value)
    except ValueError:
        # if the value cannot be converted to an integer,
        # check if it starts with 'Plusde'
        if split_value.startswith('Plusde'):
            # if it does, split the string on the 'de' delimiter and take the second element
            number_str = split_value.split('de')[1]
            return int(number_str)
        else:
            # if the value cannot be converted to an integer and does not start with 'Plusde',
            # return nan
            return np.nan

def label_encode(df, col):
    """ Label Encode function for the head count column hence the bins I created"""
    df[col] = pd.cut(df[col], [0, 10, 50, 250, 999, 1000])
    le = preprocessing.LabelEncoder()
    df[col] = le.fit_transform(df[col])

    return df


def one_hot_encode(df, col):
    """ One hot encoding """
    # Select the categorical column
    cat_column = df[col]

    # Use the `get_dummies` function to apply one-hot encoding
    one_hot = pd.get_dummies(cat_column)

    # Join the one-hot encoded columns to the original dataframe
    df = df.join(one_hot)

    return df


def process_pays(s):
    """ Clean the country column by removing some whitespaces"""
    s = str(s)
    # Cast all the column rows into str
    s = str(s)
    s = s.strip()

    # Remove whitespaces with the replace function
    s = s.replace("\n", "")

    # Remove alphabetical letters and the all symbols except . if they exist
    return s

