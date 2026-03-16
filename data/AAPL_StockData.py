import pandas as pd
import yfinance as yf


apple_price = yf.download("AAPL", start="2020-01-01", end="2023-01-01")
apple_price = apple_price.reset_index()

# Flatten any multi-level columns
apple_price.columns = [col if isinstance(col, str) else col[0] for col in apple_price.columns]

# Make sure 'Date' is present
print(apple_price.columns)
apple_price['Date'] = pd.to_datetime(apple_price['Date']).dt.date

# Save to CSV
output_csv = "AAPL_stock_data.csv"
apple_price.to_csv(output_csv, index=False)
print(f"Saved data to {output_csv}")

apple_price.head()