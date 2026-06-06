import os
from dataclasses import dataclass

import yfinance as yf
from dotenv import load_dotenv
from newsapi import NewsApiClient
from textblob import TextBlob


load_dotenv()


@dataclass
class StockMetrics:
    symbol: str
    latest_price: float
    highest_price: float
    lowest_price: float
    start_price: float
    end_price: float
    percent_change: float
    volatility: float
    risk: str
    trend: str
    movement: str
    average_sentiment: float = 0.0


def fetch_stock_history(symbol, period="3mo", moving_average_window=5):
    stock = yf.Ticker(symbol)
    history = stock.history(period=period)

    if history.empty:
        return history

    history = history.copy()
    history["Moving Average"] = history["Close"].rolling(window=moving_average_window).mean()
    history["Daily Return"] = history["Close"].pct_change()
    return history


def analyze_history(symbol, history, moving_average_window=5):
    latest_price = history["Close"].iloc[-1]
    highest_price = history["High"].max()
    lowest_price = history["Low"].min()
    start_price = history["Close"].iloc[0]
    end_price = history["Close"].iloc[-1]
    percent_change = ((end_price - start_price) / start_price) * 100
    volatility = history["Close"].pct_change().std() * 100

    if volatility > 3:
        risk = "High Risk"
    elif volatility > 1:
        risk = "Moderate Risk"
    else:
        risk = "Low Risk"

    moving_average = history["Moving Average"].dropna()
    if len(moving_average) >= moving_average_window:
        if moving_average.iloc[-1] > moving_average.iloc[-moving_average_window]:
            trend = "Uptrend"
        elif moving_average.iloc[-1] < moving_average.iloc[-moving_average_window]:
            trend = "Downtrend"
        else:
            trend = "Sideways"
    else:
        trend = "Sideways"

    movement = "increased" if percent_change > 0 else "decreased"

    return StockMetrics(
        symbol=symbol.upper(),
        latest_price=latest_price,
        highest_price=highest_price,
        lowest_price=lowest_price,
        start_price=start_price,
        end_price=end_price,
        percent_change=percent_change,
        volatility=volatility,
        risk=risk,
        trend=trend,
        movement=movement,
    )


def fetch_relevant_news(symbol, page_size=5):
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return []

    company = symbol.split(".")[0]
    newsapi = NewsApiClient(api_key=api_key)
    articles = newsapi.get_everything(
        q=f"{company} stock India OR {company} earnings OR {company} results",
        language="en",
        sort_by="relevancy",
        page_size=page_size,
    )

    keywords = ["stock", "shares", "earnings", "results", "market", "revenue"]
    relevant_articles = []
    seen = set()

    for article in articles.get("articles", []):
        title = article.get("title") or ""
        title_lower = title.lower().strip()
        key = " ".join(title_lower.split()[:5])

        if not title_lower or key in seen:
            continue

        seen.add(key)
        if company.lower() in title_lower or any(word in title_lower for word in keywords):
            polarity = TextBlob(title).sentiment.polarity
            relevant_articles.append(
                {
                    "title": title,
                    "source": (article.get("source") or {}).get("name", "Unknown"),
                    "url": article.get("url"),
                    "published_at": article.get("publishedAt"),
                    "sentiment": polarity,
                    "sentiment_label": sentiment_label(polarity),
                }
            )

    return relevant_articles


def sentiment_label(score):
    if score > 0.05:
        return "Positive"
    if score < -0.05:
        return "Negative"
    return "Neutral"


def average_sentiment(news_items):
    if not news_items:
        return 0
    return sum(item["sentiment"] for item in news_items) / len(news_items)


def build_explanation(metrics):
    explanation = (
        f"{metrics.symbol} has {metrics.movement} over the selected period, "
        f"showing a {metrics.trend.lower()} with {metrics.risk.lower()}."
    )

    if metrics.average_sentiment > 0.05:
        explanation += " Recent news sentiment is positive, pointing to optimistic market signals."
    elif metrics.average_sentiment < -0.05:
        explanation += " Recent news sentiment is negative, pointing to a cautious market outlook."
    else:
        explanation += " News sentiment is neutral, suggesting no strong external signal in the latest headlines."

    if metrics.trend == "Uptrend" and metrics.percent_change < 0:
        explanation += " The moving average is improving despite the period loss, which may indicate an early recovery phase."
    elif metrics.trend == "Downtrend" and metrics.percent_change > 0:
        explanation += " The price is higher over the period, but the moving average is weakening, which may indicate instability."

    return explanation
