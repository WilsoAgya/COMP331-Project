import pandas as pd

def check_accuracy(row):
    if row['majority_sentiment'] == 'Bullish' and row['price_change'] > 0:
        return 1
    elif row['majority_sentiment'] == 'Bearish' and row['price_change'] < 0:
        return 1
    else:
        return 0

