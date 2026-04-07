import yfinance as yf
import pandas as pd
import csv
import matplotlib.pyplot  as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#REPLACE WITH PATH OF FOLDER YOU WANT THE FILES TO GO TO
#FOR THE FOLDER YOU WANT TO USE HAVE THE AAPL_Cleaned_Sentiment.csv, AAPL_Final_With_Predictions, and AAPL_stock_data.csv IN THE FOLDER
base_path = 'C:/Users/Wilson/OneDrive/Desktop/COMP331_data'


#merged_df_predicted= []



def clean_final_prediction_join():
    df = pd.read_csv(f"{base_path}/AAPL_Final_With_Predictions.csv", low_memory=False)
    df_yfinance = pd.read_csv(f"{base_path}/AAPL_stock_data.csv", low_memory=False)

    #Gets important columns for join
    df_yfinance['Date'] = pd.to_datetime(df_yfinance['Date']).dt.date
    df['date'] = pd.to_datetime(df['created_at']).dt.date
    df['username'] = df['username'].astype(str).str.strip()

    #Data from StockTwits csv file
    df_sentiment = df[['date', 'username', 'sentiment_clean', 'body']]

    #Match date of sentiments withh yfinance data
    merged_df = pd.merge(df_sentiment, df_yfinance, left_on='date', right_on='Date', how='left')

    #Create Dictionary that gives bullish,and bearish numerical values
    sentiment_map = {'Bullish': 1, 'Bearish': -1, 'Neutral/None': 0}
    merged_df['sentiment_score'] = merged_df['sentiment_clean'].map(sentiment_map)

    #Perform sentiment score calculation
    daily_sentiment = merged_df.groupby('Date')['sentiment_score'].mean().reset_index()
    daily_sentiment.columns = ['Date', 'avg_sentiment_score']

    merged_df = pd.merge(merged_df, daily_sentiment, on='Date', how='left')

    #Puts newly merged dataframe to its own file
    merged_df.to_csv(f'{base_path}/clean_final_prediction_join.csv', index=False)

    print(merged_df)
    #Correlation calculation
    print("\nCorrelation:")
    print(merged_df[['avg_sentiment_score', 'Close', 'High', 'Low', 'Open', 'Volume']].corr())

    daily_df = merged_df.drop_duplicates(subset='Date').sort_values('Date').copy()
    daily_df['Date'] = pd.to_datetime(daily_df['Date'])
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price (USD)', color='steelblue')
    ax1.plot(daily_df['Date'], daily_df['Close'], color='steelblue', label='Close Price', linewidth=1.5)
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Avg Sentiment Score', color='tomato')
    ax2.plot(daily_df['Date'], daily_df['avg_sentiment_score'], color='tomato', label='Avg Sentiment', linewidth=1.5,
             alpha=0.7)
    ax2.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    ax2.tick_params(axis='y', labelcolor='tomato')
    ax2.set_ylim(-1, 1)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('AAPL Close Price vs Avg Daily Sentiment Score')
    plt.tight_layout()
    plt.savefig(f'{base_path}/sentiment_vs_price.png', dpi=150)
    plt.show()

def original_prediction_join():
    df = pd.read_csv(f"{base_path}/AAPL_Cleaned_Sentiment.csv", low_memory=False)
    df_yfinance = pd.read_csv(f"{base_path}/AAPL_stock_data.csv", low_memory=False)

    df_yfinance['Date'] = pd.to_datetime(df_yfinance['Date']).dt.date
    df['date'] = pd.to_datetime(df['created_at']).dt.date
    df['username'] = df['username'].astype(str).str.strip()

    df_sentiment = df[['date', 'username', 'sentiment_clean', 'body']]

    merged_df = pd.merge(df_sentiment, df_yfinance, left_on='date', right_on='Date', how='left')


    sentiment_map = {
        'Bullish': 1,
        'Bearish': -1,
        'Neutral/None': 0
    }
    merged_df['sentiment_score'] = merged_df['sentiment_clean'].map(sentiment_map)

    daily_sentiment = merged_df.groupby('Date')['sentiment_score'].mean().reset_index()
    daily_sentiment.columns = ['Date', 'avg_sentiment_score']


    merged_df = pd.merge(merged_df, daily_sentiment, on='Date', how='left')

    merged_df.to_csv(f'{base_path}/clean_sentiment_prediction_join.csv', index=False)

    print(merged_df)
    print("\nCorrelation:")
    print(merged_df[['avg_sentiment_score', 'Close', 'High', 'Low', 'Open', 'Volume']].corr())

    daily_df = merged_df.drop_duplicates(subset='Date').sort_values('Date').copy()
    daily_df['Date'] = pd.to_datetime(daily_df['Date'])
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price (USD)', color='steelblue')
    ax1.plot(daily_df['Date'], daily_df['Close'], color='steelblue', label='Close Price', linewidth=1.5)
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Avg Sentiment Score', color='tomato')
    ax2.plot(daily_df['Date'], daily_df['avg_sentiment_score'], color='tomato', label='Avg Sentiment', linewidth=1.5,
             alpha=0.7)
    ax2.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    ax2.tick_params(axis='y', labelcolor='tomato')
    ax2.set_ylim(-1, 1)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('AAPL Close Price vs Avg Daily Sentiment Score (Cleaned_Sentiment.csv)')
    plt.tight_layout()
    plt.savefig(f'{base_path}/sentiment_vs_price.png', dpi=150)
    plt.show()




clean_final_prediction_join()
original_prediction_join()

