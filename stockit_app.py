#!/usr/bin/env python
# coding: utf-8

# In[10]:


import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(page_title="Stockit", layout="centered")
st.title("📊 Stockit - Interactive Stock Price Viewer")

st.sidebar.header("🔎 Select Stock & Settings")
ticker_input = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper().strip()

timeframes = {
    "1 Day": "1d",
    "5 Days": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "YTD": "ytd",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "Max": "max"
}

selected_tf_label = st.sidebar.selectbox("Select Timeframe", list(timeframes.keys()))
selected_tf = timeframes[selected_tf_label]

interval_map = {
    "1d": "5m",
    "5d": "15m",
    "1mo": "30m",
    "3mo": "1h",
    "6mo": "1d",
    "ytd": "1d",
    "1y": "1d",
    "2y": "1d",
    "5y": "1wk",
    "max": "1mo"
}

selected_interval = interval_map.get(selected_tf, "1d")

try:
    stock = yf.Ticker(ticker_input)
    hist = stock.history(period=selected_tf, interval=selected_interval)

    if hist.empty:
        st.error("No data found for this ticker and timeframe.")
    else:
        st.subheader(f"{ticker_input} Price Chart ({selected_tf_label})")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], mode='lines', name="Close"))
        fig.update_layout(
            title=f"{ticker_input} Closing Prices",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📄 Company Info"):
            info = stock.info
            st.write(f"**Name:** {info.get('longName', 'N/A')}")
            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
            st.write(f"**Summary:** {info.get('longBusinessSummary', 'N/A')}")
except Exception as e:
    st.error(f"⚠️ Error fetching stock data: {e}")


# In[ ]:




