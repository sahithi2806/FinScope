import html

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import streamlit as st

from finscope_core import (
    analyze_history,
    average_sentiment,
    build_explanation,
    fetch_relevant_news,
    fetch_stock_history,
)


st.set_page_config(page_title="FinScope AI", page_icon="FS", layout="wide")


st.markdown(
    """
    <style>
    :root {
        --bg: #07111f;
        --panel: #0d1b2d;
        --panel-strong: #10243a;
        --text: #e6edf6;
        --muted: #8ea4bc;
        --line: rgba(148, 163, 184, 0.24);
        --accent: #14b8a6;
        --accent-2: #38bdf8;
        --warning: #fb923c;
    }
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(20, 184, 166, 0.16), transparent 34rem),
            linear-gradient(180deg, #07111f 0%, #0a1728 100%);
        color: var(--text);
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stSidebar"] {
        background: #081524;
        border-right: 1px solid var(--line);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }
    h1, h2, h3, p, li, label, span {
        color: var(--text);
    }
    .eyebrow {
        color: var(--accent);
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08rem;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .title {
        font-size: 2.8rem;
        line-height: 1.08;
        font-weight: 800;
        margin: 0;
    }
    .subtitle {
        color: var(--muted);
        font-size: 1.05rem;
        max-width: 760px;
        margin-top: 0.8rem;
    }
    .metric-card {
        background: rgba(13, 27, 45, 0.9);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem;
        min-height: 116px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
    }
    .metric-label {
        color: var(--muted);
        font-size: 0.8rem;
        margin-bottom: 0.45rem;
    }
    .metric-value {
        color: var(--text);
        font-size: 1.65rem;
        font-weight: 750;
    }
    .metric-note {
        color: var(--muted);
        font-size: 0.85rem;
        margin-top: 0.35rem;
    }
    .panel {
        background: rgba(13, 27, 45, 0.88);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1.25rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.22);
    }
    .insight {
        background: linear-gradient(135deg, rgba(20, 184, 166, 0.15), rgba(56, 189, 248, 0.08));
        border: 1px solid rgba(20, 184, 166, 0.34);
        border-radius: 8px;
        padding: 1.2rem;
        color: var(--text);
        font-size: 1.05rem;
        line-height: 1.65;
    }
    .news-card {
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        background: rgba(16, 36, 58, 0.72);
    }
    .news-title {
        font-weight: 700;
        line-height: 1.45;
    }
    .news-meta {
        color: var(--muted);
        font-size: 0.84rem;
        margin-top: 0.5rem;
    }
    .positive {
        color: #2dd4bf;
        font-weight: 700;
    }
    .negative {
        color: #fb923c;
        font-weight: 700;
    }
    .neutral {
        color: #93c5fd;
        font-weight: 700;
    }
    div.stButton > button {
        background: #14b8a6;
        color: #04111d;
        border: 0;
        border-radius: 8px;
        font-weight: 800;
        width: 100%;
        padding: 0.75rem 1rem;
    }
    div.stButton > button:hover {
        background: #2dd4bf;
        color: #04111d;
        border: 0;
    }
    a {
        color: #67e8f9 !important;
    }
    @media (max-width: 720px) {
        .title {
            font-size: 2rem;
        }
        .metric-value {
            font-size: 1.35rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def money(value):
    return f"Rs. {value:,.2f}"


def pct(value):
    return f"{value:+.2f}%"


def metric_card(label, value, note):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(label)}</div>
            <div class="metric-value">{html.escape(value)}</div>
            <div class="metric-note">{html.escape(note)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sentiment_class(label):
    return label.lower()


def render_price_chart(history, symbol):
    fig, ax = plt.subplots(figsize=(11, 5.8))
    fig.patch.set_facecolor("#0d1b2d")
    ax.set_facecolor("#0d1b2d")

    ax.plot(history.index, history["Close"], label="Close", color="#38bdf8", linewidth=2.5)
    ax.plot(history.index, history["Moving Average"], label="Moving average", color="#14b8a6", linewidth=2)
    ax.fill_between(history.index, history["Close"], alpha=0.12, color="#38bdf8")

    ax.set_title(f"{symbol.upper()} price action", color="#e6edf6", fontsize=15, pad=18, weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Price", color="#8ea4bc")
    ax.tick_params(colors="#8ea4bc")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#25405f")
    ax.spines["bottom"].set_color("#25405f")
    ax.grid(color="#1f334d", alpha=0.75, linewidth=0.8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.legend(facecolor="#10243a", edgecolor="#25405f", labelcolor="#e6edf6")
    fig.autofmt_xdate()
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)


st.sidebar.markdown("### Inputs")
stock_symbol = st.sidebar.text_input("Stock symbol", value="TCS.NS", placeholder="TCS.NS")
period = st.sidebar.selectbox("History range", ["1mo", "3mo", "6mo", "1y", "2y"], index=1)
moving_average_window = st.sidebar.slider("Moving average window", min_value=5, max_value=50, value=5, step=5)
news_limit = st.sidebar.slider("News headlines", min_value=3, max_value=10, value=5)
run_analysis = st.sidebar.button("Analyze Stock")


st.markdown('<div class="eyebrow">FinScope AI</div>', unsafe_allow_html=True)
st.markdown('<h1 class="title">Market signals, news sentiment, and explainable stock insights.</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Enter a stock symbol such as TCS.NS, INFY.NS, RELIANCE.NS, or AAPL. '
    "FinScope AI connects price behavior with volatility, trend strength, and headline sentiment.</p>",
    unsafe_allow_html=True,
)


if run_analysis or stock_symbol:
    symbol = stock_symbol.strip().upper()

    if not symbol:
        st.warning("Enter a stock symbol to begin.")
        st.stop()

    with st.spinner(f"Analyzing {symbol}..."):
        history = fetch_stock_history(symbol, period=period, moving_average_window=moving_average_window)

        if history.empty:
            st.error("No market data found. Check the stock symbol and try again.")
            st.stop()

        metrics = analyze_history(symbol, history, moving_average_window=moving_average_window)
        news_items = fetch_relevant_news(symbol, page_size=news_limit)
        metrics.average_sentiment = average_sentiment(news_items)
        explanation = build_explanation(metrics)

    st.markdown("")
    first, second, third, fourth = st.columns(4)
    with first:
        metric_card("Latest price", money(metrics.latest_price), f"Range high: {money(metrics.highest_price)}")
    with second:
        metric_card("Period change", pct(metrics.percent_change), f"From {money(metrics.start_price)} to {money(metrics.end_price)}")
    with third:
        metric_card("Volatility", f"{metrics.volatility:.2f}%", metrics.risk)
    with fourth:
        metric_card("Trend", metrics.trend, f"{moving_average_window}-day moving average")

    st.markdown("")
    chart_column, insight_column = st.columns([1.6, 1])
    with chart_column:
        render_price_chart(history, symbol)

    with insight_column:
        st.markdown("### AI Explanation")
        st.markdown(f'<div class="insight">{html.escape(explanation)}</div>', unsafe_allow_html=True)
        st.markdown("### Sentiment Pulse")
        sentiment = "Positive" if metrics.average_sentiment > 0.05 else "Negative" if metrics.average_sentiment < -0.05 else "Neutral"
        st.markdown(
            f"""
            <div class="panel">
                <div class="{sentiment_class(sentiment)}">{sentiment}</div>
                <div class="metric-note">Average headline polarity: {metrics.average_sentiment:+.3f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Relevant News")
    if news_items:
        for item in news_items:
            label_class = sentiment_class(item["sentiment_label"])
            source = html.escape(item["source"])
            title = html.escape(item["title"])
            published = html.escape(item["published_at"] or "Publication time unavailable")
            link = f'<a href="{html.escape(item["url"], quote=True)}" target="_blank">Open article</a>' if item["url"] else ""
            st.markdown(
                f"""
                <div class="news-card">
                    <div class="news-title">{title}</div>
                    <div class="news-meta">{source} | {published} | <span class="{label_class}">{item["sentiment_label"]}</span> {link}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No relevant headlines found or NEWS_API_KEY is missing. Market analysis is still available.")
