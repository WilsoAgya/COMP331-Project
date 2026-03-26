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


# Raw baseline data

raw_df = merged_df[merged_df['sentiment_clean'].isin(['Bullish', 'Bearish'])].copy()

raw_daily = raw_df.groupby('date').agg(
    majority_sentiment=('sentiment_clean', lambda x: x.mode()[0]),
    price_change=('Price_Change', 'first')
).dropna()

raw_daily['correct_prediction'] = raw_daily.apply(check_accuracy, axis=1)

raw_total = len(raw_daily)
raw_correct = raw_daily['correct_prediction'].sum()
raw_accuracy = (raw_correct / raw_total) * 100

print(f"\nRAW Baseline — Trading Days: {raw_total}, Correct: {raw_correct}, Accuracy: {raw_accuracy:.2f}%")


# cleaned and labled data

final_cleaned_df['date'] = pd.to_datetime(final_cleaned_df['date']).dt.date

clean_daily = final_cleaned_df.groupby('date').agg(
    majority_sentiment=('sentiment_clean', lambda x: x.mode()[0]),
    price_change=('Price_Change', 'first')
).dropna()

clean_daily['correct_prediction'] = clean_daily.apply(check_accuracy, axis=1)

clean_total = len(clean_daily)
clean_correct = clean_daily['correct_prediction'].sum()
clean_accuracy = (clean_correct / clean_total) * 100

print(f"CLEANED Data — Trading Days: {clean_total}, Correct: {clean_correct}, Accuracy: {clean_accuracy:.2f}%")


# Final Comparison
print("\n" + "=" * 50)
print("      DATA QUALITY IMPROVEMENT RESULTS")
print("=" * 50)
print(f"  Raw data accuracy:     {raw_accuracy:.2f}%")
print(f"  Cleaned data accuracy: {clean_accuracy:.2f}%")
print(f"  Improvement:           {clean_accuracy - raw_accuracy:+.2f}%")
print("=" * 50)
if clean_accuracy > raw_accuracy:
    print("  Result: Cleaning IMPROVED predictive accuracy.")
else:
    print("  Result: Cleaning did NOT improve predictive accuracy.")
print("=" * 50)