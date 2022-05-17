import pandas as pd
import glob

Lang = ['bn', 'gu', 'hi', 'mr', 'kn', 'pa', 'ta', 'te', 'ml', "as", "or"]

for lang in Lang:

    files = glob.glob(f'/home/cs20m050/SWE_data/{lang}/{lang}*.*')

    if 'Samanantar' in files[0]:
            dataframe1 = pd.read_csv(files[0], sep=None, engine='python', header=None, usecols=[0], skiprows=[0])
    else: dataframe1 = pd.read_csv(files[0], sep=None, engine='python', header=None)

    dataframe1 = pd.read_csv(files[0], sep=None, engine='python', header=None, usecols=[0], skiprows=[0])

    for file in files[1:]:
        print(file)
        if 'Samanantar' in file:
            dataframe2 = pd.read_csv(file, sep=None, engine='python', header=None, usecols=[0], skiprows=[0])
        else: dataframe2 = pd.read_csv(file, sep=None, engine='python', header=None)
        dataframe1 = pd.concat([dataframe1, dataframe2]).drop_duplicates(keep='last')

    dataframe1.to_csv(f'/home/cs20m050/SWE_data/{lang}/{lang}_swe.csv', index=None, header=None)
