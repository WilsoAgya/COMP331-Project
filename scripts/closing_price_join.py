import yfinance as yf
import pandas as pd
import csv
import matplotlib

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#REPLACE WITH PATH OF FOLDER YOU WANT THE FILES TO GO TO
#FOR THE FOLDER YOU WANT TO USE HAVE THE AAPL_Cleaned_Sentiment.csv, AAPL_Final_With_Predictions, and AAPL_stock_data.csv IN THE FOLDER
base_path = 'FOLDER PATH'


#Join with cleaned sentiment data
def clean_sentiment_join():
    df = pd.read_csv(f"{base_path}/AAPL_Cleaned_Sentiment.csv", low_memory=False)
    df_yfinance = pd.read_csv(f"{base_path}/AAPL_stock_data.csv", low_memory=False)

    df_yfinance['Date'] = pd.to_datetime(df_yfinance['Date']).dt.date

    df['date'] = pd.to_datetime(df['created_at']).dt.date
    df['username'] = df['username'].astype(str).str.strip()

    df_sentiment = df[['date', 'username', 'sentiment_clean', 'body']]

    merged_df = pd.merge(df_sentiment, df_yfinance, left_on='date', right_on='Date', how='left')

    merged_df.to_csv(f'{base_path}/closing_price_join.csv')

    df = pd.read_csv(f"{base_path}/closing_price_join.csv")

    print(merged_df)


#Join for table with final prediction data
def clean_final_prediction_join():
    df = pd.read_csv(f"{base_path}/AAPL_Final_With_Predictions.csv", low_memory=False)
    df_yfinance = pd.read_csv(f"{base_path}/AAPL_stock_data.csv", low_memory=False)

    df_yfinance['Date'] = pd.to_datetime(df_yfinance['Date']).dt.date
    df['date'] = pd.to_datetime(df['created_at']).dt.date
    df['username'] = df['username'].astype(str).str.strip()

    df_sentiment = df[['date', 'username', 'sentiment_clean', 'body']]

    merged_df = pd.merge(df_sentiment, df_yfinance, left_on='date', right_on='Date', how='left')

    merged_df.to_csv(f'{base_path}/clean_final_prediction_join.csv')

    df = pd.read_csv(f"{base_path}/clean_final_prediction_join.csv")

    print(merged_df)
    print("Correlation:")
    print(df.corr(numeric_only=True))


clean_sentiment_join()
clean_final_prediction_join()
