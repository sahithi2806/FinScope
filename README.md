# FinScope AI

FinScope AI is an end-to-end financial data analysis and insight generation system designed to help users understand stock market behavior through data-driven techniques.

The platform integrates real-time market data, statistical analysis, and contextual news to provide a comprehensive view of stock performance. Instead of merely displaying price trends, FinScope AI interprets market movements by combining quantitative indicators such as moving averages, volatility, and percentage change with qualitative signals from financial news.

Additionally, the system incorporates **sentiment analysis and multi-factor reasoning** to explain *why* a stock is moving, transforming raw financial data into meaningful, human-readable insights.

---

## 🧩 System Architecture

The system follows a layered architecture:

* **Data Layer**: Fetches historical stock data using financial APIs
* **Analysis Layer**: Computes indicators like moving average, volatility, and trend classification
* **Insight Layer**: Generates human-readable interpretations of stock performance
* **Context Layer**: Retrieves and filters relevant financial news
* **Sentiment Layer**: Analyzes news polarity using NLP (TextBlob)
* **Explanation Layer**: Combines data + sentiment for multi-factor reasoning
* **Visualization Layer**: Displays trends and indicators through graphical plots

---

## 🎯 Problem Statement

Most beginner investors struggle to interpret stock market data due to:

* Lack of structured explanations for price movements
* Difficulty connecting numerical data with real-world events
* Over-reliance on raw charts without contextual understanding

FinScope AI addresses this gap by providing an integrated system that not only analyzes stock data but also explains *why* certain trends may be occurring using relevant news and indicators.

---

## 💡 Key Highlights

* Combines **data analysis + contextual information + NLP**
* Bridges gap between **raw numbers and meaningful insights**
* Demonstrates **real-world application of Python in fintech**
* Implements a **layered system design**
* Generates **multi-factor AI-style explanations**

---

## 📊 Features

* Fetches real-time stock data using Yahoo Finance
* Visualizes stock price trends with moving averages
* Calculates percentage change over time
* Measures volatility using returns-based risk modeling
* Detects trend (Uptrend / Downtrend / Sideways)
* Fetches and filters relevant financial news
* Performs sentiment analysis using NLP (TextBlob)
* Generates AI-style explanations using multi-factor reasoning

---

## 🧠 How It Works

1. User inputs stock symbol (e.g., `TCS.NS`)
2. System retrieves historical price data
3. Performs analysis:

   * Trend detection using moving averages
   * Volatility calculation (risk assessment)
   * Percentage change computation
4. Fetches relevant financial news
5. Applies sentiment analysis on news headlines
6. Combines data + sentiment to generate intelligent explanations
7. Visualizes stock performance

---

## 🛠️ Tech Stack

* Python
* yfinance
* matplotlib
* NewsAPI
* python-dotenv
* TextBlob (NLP sentiment analysis)

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```
NEWS_API_KEY=your_api_key_here
```

Install dependencies:

```
pip install yfinance matplotlib newsapi-python python-dotenv textblob
```

---

## ▶️ Usage

Run the program:

```
python main.py
```

Enter stock symbol:

```
TCS.NS
```

---

## 📈 Example Output

* Stock summary (price, high, low)
* Trend detection
* Volatility classification
* Insight statement
* Relevant news headlines
* News sentiment (Positive / Negative / Neutral)
* AI-generated explanation
* Price + Moving Average graph

---

## 🔮 Future Improvements

* LLM-based explanation generation
* Web-based dashboard (Flask/React)
* Portfolio analysis system
* Advanced sentiment analysis models

---

## 📌 Project Status

* ✔ Version 1 — Data Acquisition & Visualization
* ✔ Version 2 — Analytical Engine (trend, volatility, indicators)
* ✔ Version 3 — News Integration & Context Layer
* ✔ Version 4 — Sentiment Analysis using NLP
* ✔ Version 5 — Multi-factor AI Explanation System

---

## 👩‍💻 Author

Sahithi Singh
