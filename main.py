from backend_functions import *

df = data_reader()
df
for value in df["Chiffre d'Affaires 16"].unique():
    print(type(value))
print("//////////////////////")
print(df.shape[0])
null_percent = df["Chiffre d'Affaires 16"].isnull().sum() / df.shape[0]
print(null_percent)
'''
wa = df[df["Chiffre d'Affaires 15"].isnull() & df["Chiffre d'Affaires 16"].isnull() & df["Chiffre d'Affaires 17"].isnull() & df["Chiffre d'Affaires 18"].isnull()]
print(len(wa))
ze = df[df["Evolution du Chiffre d'Affaires 15"].isnull() & df["Evolution du Chiffre d'Affaires 16"].isnull() & df["Evolution du Chiffre d'Affaires 17"].isnull() & df["Evolution du Chiffre d'Affaires 18"].isnull()]
print(len(ze))
'''
df = df[df[["Chiffre d'Affaires 15", "Chiffre d'Affaires 16", "Chiffre d'Affaires 17", "Chiffre d'Affaires 18"]].notnull().any(axis=1)]
print(df.shape[0])
total_null = df["Chiffre d'Affaires 16"].isnull().sum()
print(total_null)

data = {
    'column1': [1, 2, 3, None, 2],
    'column2': [5, 6, None, None, None],
    'column3': [None, 11, 12, None, None],
    'column4': [15, None, None, None, None]
}

# create the dataframe
df = pd.DataFrame(data)
print(df)
print("///////////////////////")
df['new_column'] = np.where(
    df['column4'].notnull(),
    df['column4'],
    np.where(
        df['column3'].notnull(),
        df['column3'],
        np.where(
            df['column2'].notnull(),
            df['column2'],
            df['column1'],
        )
    )
)

# print the dataframe
print(df)

