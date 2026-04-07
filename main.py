import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from newsapi import NewsApiClient
from dotenv import load_dotenv
from textblob import TextBlob
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
    volatility = hist["Close"].pct_change().std() * 100
    if volatility > 3:
        risk ="High Risk"
    elif volatility > 1:
        risk ="Moderate Risk"
    else:
        risk ="Low Risk"
    print(f"Volatility: {volatility:.2f} ({risk})")

    hist["MA"] = hist["Close"].rolling(window=5).mean()
    recent_ma = hist["MA"].iloc[-5:]
    if hist["MA"].iloc[-1] >hist["MA"].iloc[-5]:
        trend = "Uptrend"
    elif hist["MA"].iloc[-1] <hist["MA"].iloc[-5]:
        trend = "Downtrend"
    else:
        trend = "Sideways"
    print(f"\nInsight: The stock has {movement} over the selected period, showing {trend.lower()} with {risk.lower()}.")

    # Fetch news
    newsapi =NewsApiClient(api_key=api_key)
    company =stock.split('.')[0]
    articles = newsapi.get_everything(
        q=f"{company} stock India OR {company} earnings OR {company} results",
        language='en',sort_by='relevancy',page_size=3)

    keywords = ["stock", "shares", "earnings", "results", "market", "revenue"]
    sentiments = []
    print("\n Relevant News:")

    seen = set()
    for article in articles['articles']:
        title = article['title']
        title_lower = title.lower().strip()

        # take first 8 words as key
        key = " ".join(title_lower.split()[:5])
        if key not in seen:
            seen.add(key)

            if company.lower() in title_lower or any(word in title_lower for word in keywords):
                print("-", title)

                blob = TextBlob(title)
                polarity = blob.sentiment.polarity
                sentiments.append(polarity)
    if sentiments: 
        avg_sentiment = sum(sentiments) / len(sentiments) 
    else: 
        avg_sentiment = 0
    explanation = f"The stock has {movement} over the selected period, showing a {trend.lower()} with {risk.lower()}."

    # sentiment reasoning
    if avg_sentiment > 0:
        explanation += " Recent news sentiment is positive, indicating optimistic market signals."
    elif avg_sentiment < 0:
        explanation += " Recent news sentiment is negative, indicating cautious or weak market outlook."
    else:
        explanation += " News sentiment is neutral, suggesting no strong external influence."

    # deeper reasoning
    if trend == "Uptrend" and percent_change < 0:
        explanation += " This may indicate a potential recovery phase."
    elif trend == "Downtrend" and percent_change > 0:
        explanation += " This may indicate a possible reversal or instability."

    print(f"\nAI Explanation:\n{explanation}")

# Simple AI-style explanation
    if avg_sentiment > 0:
        reason = "positive news sentiment and favorable market signals"
    elif avg_sentiment < 0:
        reason = "negative news sentiment and weak performance signals"
    else:
        reason = "mixed or neutral market signals"
    print(f"\nAI Explanation: The stock movement may be influenced by {reason}.")

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