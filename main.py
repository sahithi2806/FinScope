import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from newsapi import NewsApiClient
from dotenv import load_dotenv
from textblob import TextBlob
import os
from groq import Groq  # Switched from google.genai

# Load environment variables
load_dotenv()
# Initialize Groq Client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
news_api_key = os.getenv("NEWS_API_KEY")

stock = input("Enter stock symbol : ").upper()
data = yf.Ticker(stock)
hist = data.history(period="3mo")

if hist.empty:
    print(" Invalid stock symbol or no data found.")
else:
    # ---------------- STOCK SUMMARY ----------------
    latest_price = hist["Close"].iloc[-1]
    highest_price = hist["High"].max()
    lowest_price = hist["Low"].min()

    print(f"\n Stock Summary: {stock}\n" + "-"*20)
    print(f"Latest Price: ₹{round(latest_price, 2)}")
    print(f"Highest Price: ₹{round(highest_price, 2)}")
    print(f"Lowest Price: ₹{round(lowest_price, 2)}")

    # ---------------- PERCENTAGE CHANGE ----------------
    start_price = hist["Close"].iloc[0]
    percent_change = ((latest_price - start_price) / start_price) * 100
    movement = "increased" if percent_change > 0 else "decreased"
    print(f"Percentage Change: {percent_change:.2f}%")

    # ---------------- VOLATILITY ----------------
    volatility = hist["Close"].pct_change().std() * 100
    risk = "High Risk" if volatility > 3 else "Moderate Risk" if volatility > 1 else "Low Risk"
    print(f"Volatility: {volatility:.2f} ({risk})")

    # ---------------- TREND ----------------
    hist["MA"] = hist["Close"].rolling(window=5).mean()
    if hist["MA"].iloc[-1] > hist["MA"].iloc[-5]:
        trend = "Uptrend"
    elif hist["MA"].iloc[-1] < hist["MA"].iloc[-5]:
        trend = "Downtrend"
    else:
        trend = "Sideways"
    print(f"Insight: {movement.capitalize()} over 3 months, showing {trend.lower()}.")

    # ---------------- NEWS ----------------
    newsapi = NewsApiClient(api_key=news_api_key)
    company = stock.split('.')[0]
    articles = newsapi.get_everything(
        q=f"{company} stock OR {company} earnings",
        language='en',
        sort_by='relevancy',
        page_size=3
    )
    
    sentiments = []
    news_titles = []
    print("\n📰 Relevant News:")
    for article in articles['articles']:
        title = article['title']
        print("-", title)
        news_titles.append(title)
        blob = TextBlob(title)
        sentiments.append(blob.sentiment.polarity)

    # ---------------- SENTIMENT ----------------
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    sentiment_label = "Positive" if avg_sentiment > 0 else "Negative" if avg_sentiment < 0 else "Neutral"
    print(f"\nNews Sentiment: {sentiment_label}")

    # ---------------- RULE-BASED EXPLANATION ----------------
    explanation = f"The stock has {movement} recently. "
    explanation += f"News is {sentiment_label.lower()}, suggesting {('optimism' if avg_sentiment > 0 else 'caution')}."

    # ---------------- GROQ AI (FREE REPLACEMENT) ----------------
    news_context = ", ".join(news_titles[:2]) if news_titles else "No major news"
    
    prompt = f"""
    Analyze {stock} stock.
    Current Trend: {trend}
    Volatility: {risk}
    Change: {percent_change:.2f}%
    News Context: {news_context}
    
    Provide a practical 3-line explanation for a beginner. No jargon.
    """

    print("\n" + "="*30)
    print("Groq AI Explanation:")
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        print(completion.choices[0].message.content.strip())
    except Exception as e:
        print(f"AI Limit reached. Using Rule-Based: {explanation}")

    # ---------------- GRAPH ----------------
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist["Close"], label="Price", color='blue')
    plt.plot(hist.index, hist["MA"], label="5-Day MA", color='orange', linestyle='--')
    plt.title(f"{stock} Analysis (3 Months)")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    plt.legend()
    plt.tight_layout()
    plt.show()