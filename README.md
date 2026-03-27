# FinScope AI
FinScope AI is an end-to-end financial data analysis and insight generation system designed to help users understand stock market behavior through data-driven techniques.

The platform integrates real-time market data, statistical analysis, and contextual news to provide a comprehensive view of stock performance. Instead of merely displaying price trends, FinScope AI interprets market movements by combining quantitative indicators such as moving averages, volatility, and percentage change with qualitative signals from financial news.

The system follows a layered architecture:

* **Data Layer**: Fetches historical stock data using financial APIs
* **Analysis Layer**: Computes indicators like moving average, volatility, and trend classification
* **Insight Layer**: Generates human-readable interpretations of stock performance
* **Context Layer**: Retrieves and filters relevant financial news to explain possible causes of price movements
* **Visualization Layer**: Displays trends and indicators through graphical plots

This approach transforms raw financial data into actionable insights, making the platform useful for beginners learning the stock market as well as users seeking quick analytical summaries.


## Problem Statement
Most beginner investors struggle to interpret stock market data due to:

* Lack of structured explanations for price movements
* Difficulty connecting numerical data with real-world events
* Over-reliance on raw charts without contextual understanding

FinScope AI addresses this gap by providing an integrated system that not only analyzes stock data but also explains *why* certain trends may be occurring using relevant news and indicators.

## Key Highlights

* Combines **data analysis + contextual information**
* Bridges gap between **raw numbers and meaningful insights**
* Demonstrates **real-world application of Python in fintech**
* Built with a scalable structure that can be extended to AI/ML models

## Features

* Fetches real-time stock data using Yahoo Finance
* Displays price trends with graphs
* Calculates moving averages for trend analysis
* Detects trend (Uptrend / Downtrend / Sideways)
* Computes percentage change over time
* Measures volatility (risk level classification)
* Fetches relevant financial news
* Generates AI-style explanations for stock movement

## Flow of Code
1. User inputs stock symbol (e.g., `TCS.NS`)
2. System retrieves historical price data
3. Performs analysis:
   * Trend detection
   * Volatility calculation
   * Percentage change
4. Fetches related financial news
5. Generates insights and explanation
6. Visualizes stock performance


## 🛠️ Tech Stack
* Python
* yfinance
* matplotlib
* NewsAPI
* python-dotenv

## 🔐 Environment Setup

Create a `.env` file in the root directory:

NEWS_API_KEY=your_api_key_here

Install dependencies:

pip install yfinance matplotlib newsapi-python python-dotenv


## ▶️ Usage

Run the program: python main.py

Enter stock symbol: TCS.NS (Sample input)

## 📈 Example Output

* Stock summary (price, high, low)
* Trend detection
* Volatility classification
* Insight statement
* Relevant news headlines
* Price + Moving Average graph

## 🔮 Future Improvements

* Sentiment analysis using NLP
* AI-based explanation generation
* Web-based dashboard
* Portfolio analysis


## Project Status
✔ Version 1 — Data fetching & visualization
✔ Version 2 — Analysis (trend, volatility, insights)
✔ Version 3 — News integration + explanation

## 👩‍💻 Author
Sahithi Singh
