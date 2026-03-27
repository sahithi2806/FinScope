import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("NEWS_API_KEY")

stock = input("Enter stock symbol : ")

data = yf.Ticker(stock)
hist = data.history(period="3mo")

if hist.empty:
    print(" Invalid stock symbol or no data found.")
else:
    latest_price = hist["Close"].iloc[-1]
    highest_price = hist["High"].max()
    lowest_price = hist["Low"].min()

    print("\n Stock Summary:\n")
    print("Stock:", stock)
    print("Latest Price: ₹", round(latest_price, 2))
    print("Highest Price : ₹", round(highest_price, 2))
    print("Lowest Price : ₹", round(lowest_price, 2))

    #percentage change
    start_price = hist["Close"].iloc[0]
    end_price = hist["Close"].iloc[-1]
    percent_change = ((end_price - start_price) / start_price) * 100
    print(f"Percentage Change: {percent_change:.2f}%")

    if percent_change > 0:
        movement = "increased "
    else:
        movement = "decreased "
    
    #volatility-how unstable stock is
    volatility = hist["Close"].std()
    if volatility > 50:
        risk = "High Risk "
    elif volatility > 20:
        risk = "Moderate Risk"
    else:
        risk = "Low Risk"

    print(f"Volatility: {volatility:.2f} ({risk})")

    hist["MA"] = hist["Close"].rolling(window=5).mean()
    recent_ma = hist["MA"].iloc[-5:]
    if recent_ma.is_monotonic_increasing:
        trend = "Strong Uptrend "
    elif recent_ma.is_monotonic_decreasing:
        trend = "Strong Downtrend "
    else:
        trend = "Sideways Trend "
    print(f"\nInsight: The stock has {movement} over the selected period, showing {trend.lower()} with {risk.lower()}.")

    # Fetch news
    newsapi =NewsApiClient(api_key="api_key")
    company =stock.split('.')[0]
    articles = newsapi.get_everything(
        q=f"{company} stock India OR {company} earnings OR {company} results",
        language='en',sort_by='relevancy',page_size=3)
    print("\n Latest News:")
    print("\n📰 Relevant News:")

    keywords = ["stock", "shares", "earnings", "results", "market", "revenue"]
    for article in articles['articles']:
        title = article['title'].lower()
        if company.lower() in title and any(word in title for word in keywords):
            print("-", article['title'])

# Simple AI-style explanation
    if percent_change > 0:
        reason = "positive sentiment or strong performance"
    else:
        reason = "negative sentiment or weak performance"
    print(f"\nAI Explanation: The stock movement may be due to {reason},as reflected in recent news trends.\n")

#Ploting Graph
    plt.figure()
    plt.plot(hist.index, hist["Close"], label="Price")
    plt.plot(hist.index, hist["MA"], label="5-Day MA")

    plt.title(f"{stock} Price + Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y'))
    plt.xticks(rotation=45)

    plt.legend()
    plt.tight_layout()
    plt.show()