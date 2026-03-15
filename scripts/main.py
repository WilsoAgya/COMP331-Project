import pandas as pd
import glob
import os
import zipfile
import kagglehub

def run_pipeline():
    # Download Dataset
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("frankcaoyun/stocktwits-2020-2022-raw")
    data_folder = os.path.join(path, "StockTwits_2020_2022_Raw")
    files = glob.glob(os.path.join(data_folder, "**", "*"), recursive=True)

    # Load and Merge
    dataframes = []
    print("Merging 4.6 million rows... this may take a minute.")
    for f in files:
        if f.endswith(".zip"):
            with zipfile.ZipFile(f, 'r') as z:
                for filename in z.namelist():
                    if filename.endswith(".csv"):
                        with z.open(filename) as csv_file:
                            dataframes.append(pd.read_csv(csv_file))
        elif f.endswith(".csv"):
            dataframes.append(pd.read_csv(f))

    if not dataframes:
        print("No data found!")
        return

    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Data Quality Logic 
    combined_df['username'] = combined_df['user'].apply(lambda x: eval(x)['username'] if isinstance(x, str) else x.get('username'))
    combined_df['is_low_quality'] = combined_df.duplicated(subset=['username', 'body'], keep=False)
    
    # Filter for Apple
    aapl_clean = combined_df[(combined_df['is_low_quality'] == False) & 
                             (combined_df['body'].str.contains('AAPL', na=False, case=False))]
    
    print(f"Success! Created cleaned dataset with {len(aapl_clean)} Apple posts.")
    aapl_clean.to_csv('AAPL_Cleaned_Sentiment.csv', index=False)

if __name__ == "__main__":
    run_pipeline()
