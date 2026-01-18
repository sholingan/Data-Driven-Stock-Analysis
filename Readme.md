📊 Data-Driven Stock Market Analysis
Power BI • Python • MySQL • Streamlit

An end-to-end stock market analytics system that transforms raw stock price data into actionable insights using SQL, Python, Power BI, and Streamlit.

This project enables users to analyze market trends, volatility, sector performance, cumulative returns, monthly movers, and correlations between stocks through both BI dashboards and an interactive web app.

🎯 Project Objectives

Store and manage stock market data efficiently using a relational database

Compute financial metrics such as:

Daily returns

Monthly returns

Cumulative returns

Visualize insights through:

Power BI dashboards

Streamlit interactive web app

Help users understand:

Market direction

Risk & volatility

Sector-wise performance

Stock correlations for portfolio analysis

🚀 Features
✅ 1️⃣ SQL Database (MySQL)

A structured relational database designed for time-series financial analysis.

📌 Tables

stocks

Stock symbol

Company name

Sector

prices

Date

Open, High, Low, Close

Volume

Daily return (computed)

⚙️ Capabilities

Indexed for faster queries

Supports advanced analytics

Auto-computes:

Daily returns

Monthly returns

Cumulative returns

Uses window functions (LAG) for return calculations

✅ 2️⃣ Power BI Dashboard

A professionally designed 2-page Power BI report for executive-level and analytical insights.

📄 Page 1 — Market Overview

Top 10 Green Stocks (best yearly returns)

Top 10 Red Stocks (worst yearly returns)

Top 10 Most Volatile Stocks

KPI Cards:

Green stocks count

Red stocks count

Average closing price

Average trading volume

Sector-wise average cumulative return

Cumulative return trend (line chart)

📄 Page 2 — Detailed Analysis

Monthly slicer for time-based filtering

Top 5 Monthly Gainers

Top 5 Monthly Losers

Correlation heatmap of daily returns

Interactive cross-filtering between visuals

🧪 3️⃣ Streamlit Web Application

An interactive Python-based analytics dashboard built with Streamlit.

📈 Overview Module

Green vs Red stocks

Best & worst performers

Quick market snapshot

📉 Volatility Analysis

Standard deviation of daily returns

Volatility bar charts

📊 Cumulative Returns

Log cumulative return calculation

Identifies long-term winners

🏭 Sector Performance

Average cumulative return by sector

Sector comparison visuals

🔥 Monthly Movers

Top 5 monthly gainers

Top 5 monthly losers

Momentum tracking

🔗 Correlation Heatmap

Interactive Plotly heatmap

Shows relationships between stocks

Useful for diversification strategies

🛠️ Technology Stack
🔹 Backend & Processing

Python

Pandas

NumPy

Matplotlib

Plotly

Streamlit

🔹 Database

MySQL

SQL Window Functions (LAG)

🔹 Visualization

Power BI

Streamlit (interactive charts)

🔧 Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/your-username/data-driven-stock-analysis.git
cd data-driven-stock-analysis

2️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows


Install dependencies:

pip install -r requirements.txt

3️⃣ Setup MySQL Database

Import schema and tables:

SOURCE data_driven_stock_analysis.sql;


Load stock data via CSV or API.

4️⃣ Run Streamlit App
streamlit run app_streamlit_simple.py


Access the app at:

http://localhost:8501

5️⃣ Open Power BI Dashboard

Open data_driven_proj.pbix

Refresh data

Ensure MySQL connection is configured

📊 Key Insights You Can Derive

Identify outperforming sectors

Detect high-risk, high-volatility stocks

Track monthly and yearly performance

Analyze stock correlations




👤 Author

Sholingan

LinkedIn: Sholingan
