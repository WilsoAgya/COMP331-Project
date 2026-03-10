import pandas as pd
import glob
import os
import zipfile

path = 'data'

files = glob.glob(os.path.join(path, "*"))

dataframes = []

for f in files:
    if f.endswith('.zip'):
        with zipfile.ZipFile(f, 'r') as z:
         
            for filename in z.namelist():
                if filename.endswith('.csv'):
                    with z.open(filename) as csv_file:
                        dataframes.append(pd.read_csv(csv_file))
    elif f.endswith('.csv'):
        dataframes.append(pd.read_csv(f))

if not dataframes:
    print("No data found! Make sure the CSVs are extracted or the Zips contain CSVs.")
else:
    combined_df = pd.concat(dataframes, ignore_index=True)
    print(f"Success! Combined {len(dataframes)} data sources.")
    print(combined_df.head())
