import yfinance as yf
import kagglehub


#search_results = yf.Search("apple")
#print(search_results)

ticker = yf.Ticker("AAPL")
print(ticker.recommendations)

