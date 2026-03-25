import pandas as pd

# loading files for comparison
merged_df = pd.read_csv('AAPL_Merged_Sentiment_Stock.csv')
final_cleaned_df = pd.read_csv('apple_fully_labeled_sentiment.csv')

print(f"Merged df: {len(merged_df)} rows")
print(f"Final cleaned df: {len(final_cleaned_df)} rows")
def check_accuracy(row):
    if row['majority_sentiment'] == 'Bullish' and row['price_change'] > 0:
        return 1
    elif row['majority_sentiment'] == 'Bearish' and row['price_change'] < 0:
        return 1
    else:
        return 0
    

# Raw baseline data categorizating
raw_df = merged_df[merged_df['sentiment_clean'].isin(['Bullish', 'Bearish'])].copy()