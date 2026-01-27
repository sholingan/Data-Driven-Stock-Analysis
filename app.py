import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# ------------------ APP BACKGROUND COLOR ------------------
st.markdown(
    """
    <style>
    /* Full app background */
    .stApp {
        background-color: #A8D8B9 ;  /* Light grey background */
    }

    /* Optional: make all section titles darker */
    h1, h2, h3 {
        color: #111827;
    }
    </style>
    """,
    unsafe_allow_html=True
)


import streamlit as st

st.set_page_config(
    page_title="Data Driven Stock Analysis",
    layout="wide"
)

# -------------------------------
# 🎨 CSS (Ribbon Color Updated)
# -------------------------------
st.markdown("""
<style>
.ribbon-container {
    background: linear-gradient(135deg, #0050EB, #003bb3);
    padding: 28px 30px;
    border-radius: 14px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.35);
    margin-bottom: 30px;
}

/* Main title */
.ribbon-title {
    font-size: clamp(22px, 3vw, 32px);
    font-weight: 800;
    color: #ffffff;
    text-align: center;
    margin-bottom: 12px;
}

/* Long subtitle */
.ribbon-subtitle {
    font-size: clamp(13px, 1.5vw, 16px);
    color: #E6ECFF;
    text-align: center;
    line-height: 1.7;
    max-width: 95%;
    margin: auto;
    word-break: break-word;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧾 Ribbon Header
# -------------------------------
st.markdown("""
<div class="ribbon-container">
    <div class="ribbon-title">
        📊 Data-Driven Stock Analysis
    </div>
    <div class="ribbon-subtitle">
        Most Volatile Stocks • Cumulative Return • Sector Wise Performance •
        Stock Price Correlation • Top Gainers & Losers
    </div>
</div>
""", unsafe_allow_html=True)



# ------------------ LOAD DATA ------------------
df = pd.read_csv("test_data.csv")

# Clean column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)
# ------------------ DATE FIX (VERY IMPORTANT) ------------------
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

# ------------------ FILTERS ------------------
st.subheader("🔍 Filters")

col1, col2, col3 = st.columns(3)

# Date filter
with col1:
    min_date = df["date"].min().to_pydatetime()
    max_date = df["date"].max().to_pydatetime()

    date_range = st.slider(
        "🗓 Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

# Sector filter
with col2:
    sectors = sorted(df["sector"].dropna().unique())
    selected_sectors = st.multiselect(
        "🏭 Sector",
        options=sectors,
        default=sectors
    )

# Stock filter
with col3:
    stocks = sorted(df["ticker"].dropna().unique())
    selected_stocks = st.multiselect(
        "📈 Stock",
        options=stocks,
        default=stocks
    )

# ------------------ APPLY FILTERS ------------------
df = df[
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1])) &
    (df["sector"].isin(selected_sectors)) &
    (df["ticker"].isin(selected_stocks))
]

# Date parsing (INDIAN FORMAT SAFE)
df["date"] = pd.to_datetime(
    df["date"],
    dayfirst=True,
    errors="coerce"
)

df = df.dropna(subset=["date"])

# Sort
df = df.sort_values(["ticker", "date"])

# ------------------ KPI SECTION ------------------
st.markdown("### 🔑 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📈 Total Stocks", df["ticker"].nunique())

with col2:
    st.metric("🏭 Total Sectors", df["sector"].nunique())

with col3:
    st.metric(
        "🗓 Date Range",
        f"{df['date'].min().date()} → {df['date'].max().date()}"
    )

st.divider()

# ------------------ COMMON CALCULATIONS ------------------
df["daily_return"] = df.groupby("ticker")["close"].pct_change()

# ================== QUESTION 1 ==================
st.subheader("Q - 1. Top 10 Most Volatile Stocks (%)")

volatility = (
    df.groupby("ticker")["daily_return"]
    .std()
    .dropna()
    .sort_values(ascending=False)
    .head(10) * 100
)

colors = [
    "#61056E", "#48BC66", "#12239E", "#E645AB", "#115751",
    "#E66C37", "#3097C3", "#7B4730", "#1ABBB3", "#666666"
]

fig, ax = plt.subplots(figsize=(10, 5))
volatility.sort_values().plot(
    kind="barh",
    ax=ax,
    color=colors
)

ax.set_xlabel("Volatility (%)")

for i, v in enumerate(volatility.sort_values()):
    ax.text(v + 0.1, i, f"{v:.2f}%", va="center")

st.pyplot(fig)

st.divider()


# ================== QUESTION 2 ==================
st.subheader("Q - 2. Cumulative Return – Top 5 Stocks (%)")

# ---- Filters for Cumulative Return ----
col_f1, col_f2 = st.columns(2)

with col_f1:
    top_n = st.selectbox(
        "Select Top N Stocks",
        options=[3, 5, 10],
        index=1   # default = Top 5
    )

with col_f2:
    sector_filter = st.multiselect(
        "Filter by Sector (Optional)",
        options=sorted(df["sector"].dropna().unique()),
        default=[]
    )

# ---- Apply sector filter if selected ----
df_cum = df.copy()
if sector_filter:
    df_cum = df_cum[df_cum["sector"].isin(sector_filter)]

# ---- Cumulative Return Calculation ----
df_cum["cumulative_return"] = (
    df_cum.groupby("ticker")["daily_return"]
    .transform(lambda x: (1 + x).cumprod() - 1)
)

# ---- Get Top N Stocks ----
top_stocks = (
    df_cum.groupby("ticker")["cumulative_return"]
    .last()
    .sort_values(ascending=False)
    .head(top_n)
    .index
)

# ---- Plot ----
fig, ax = plt.subplots(figsize=(12, 5))

for stock in top_stocks:
    temp = df_cum[df_cum["ticker"] == stock].copy()
    temp["cumulative_return_pct"] = temp["cumulative_return"] * 100

    ax.plot(
        temp["date"],
        temp["cumulative_return_pct"],
        label=stock
    )

    ax.text(
        temp["date"].iloc[-1],
        temp["cumulative_return_pct"].iloc[-1],
        f"{temp['cumulative_return_pct'].iloc[-1]:.2f}%",
        fontsize=9
    )

ax.set_ylabel("Cumulative Return (%)")
ax.set_title(f"Cumulative Return – Top {top_n} Stocks")
ax.legend()
st.pyplot(fig)

st.divider()

# ================== QUESTION 3 ==================
st.subheader("Q - 3. Sector-wise Performance")

sector_perf = (
    df.groupby("sector")["yearly_return"]
    .mean()
    .div(100)
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))
sector_perf.plot(kind="bar", ax=ax)

# Axis labels
ax.set_xlabel("Sector")
ax.set_ylabel("Average Yearly Return (%)")

# Percentage formatter
import matplotlib.ticker as mtick
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=1))

# ✅ Multi colors
colors = plt.cm.tab20.colors
for bar, color in zip(ax.patches, colors):
    bar.set_color(color)

st.pyplot(fig)


# ================== QUESTION 4 ==================
st.subheader("Q - 4. Stock Price Correlation Heatmap ")

# Load full stock data
df_full = pd.read_csv(r"D:\Py_start\Python\project_SN\DDSA\DDSA_Updated\test_data.csv")

# Clean columns
df_full.columns = df_full.columns.str.strip().str.lower()
df_full["date"] = pd.to_datetime(df_full["date"], dayfirst=True)

# Keep only needed columns
df_full = df_full[["date", "ticker", "close"]]

# Handle duplicates: one price per ticker per date
df_full = df_full.groupby(["date", "ticker"])["close"].mean().reset_index()

# Pivot to get tickers as columns
price_matrix = df_full.pivot(index="date", columns="ticker", values="close")

# Compute correlation matrix
corr = price_matrix.corr()

# --- HEATMAP SETTINGS (TEXT SIZE FIX ONLY) ---
fig, ax = plt.subplots(figsize=(15, 12), dpi=150)

sns.heatmap(
    corr,
    cmap="RdYlGn",
    center=0,
    linewidths=0.3,
    linecolor="gray",
    annot=True,
    fmt=".2f",
    annot_kws={"size": 5},        # 🔽 reduced from 7 → 5
    cbar_kws={"shrink": 0.8},
    ax=ax
)

# 🔽 Smaller axis label text
plt.xticks(rotation=45, ha="right", fontsize=6)
plt.yticks(rotation=0, fontsize=6)

ax.set_title(
    "Stock Price Correlation Heatmap (All Stocks)",
    fontsize=12                # 🔽 reduced from 14
)

st.pyplot(fig)

# ================== QUESTION 5 ==================

st.subheader("Q - 5. Top 5 Gainers & Losers (Monthly %)")

df["month"] = df["date"].dt.to_period("M")

df_month = df.dropna(subset=["monthly_return"])
df_month = (
    df_month.groupby(["month", "ticker"])["monthly_return"]
    .mean()
    .reset_index()
)

# ✅ FIX SCALE for plotting
df_month["monthly_return_scaled"] = df_month["monthly_return"] / 100

month_selected = st.selectbox(
    "Select Month",
    df_month["month"].astype(str).sort_values().unique()
)

month_df = df_month[df_month["month"].astype(str) == month_selected]

top5 = month_df.sort_values("monthly_return_scaled", ascending=False).head(5)
bottom5 = month_df.sort_values("monthly_return_scaled").head(5)

fig, ax = plt.subplots(figsize=(10,6))
ax.bar(top5["ticker"], top5["monthly_return_scaled"], color="#48BC66", label="Top 5 Gainers")
ax.bar(bottom5["ticker"], bottom5["monthly_return_scaled"], color="#E64545", label="Top 5 Losers")

ax.set_ylabel("Monthly Return (%)")
ax.set_title(f"Top 5 Gainers & Losers for {month_selected}")

import matplotlib.ticker as mtick
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

ax.legend()

# Labels (multiply by 100 to show actual %)
for i, val in enumerate(top5["monthly_return_scaled"]):
    ax.text(i, val, f"{val*100:.0f}%", ha="center", va="bottom", fontsize=9)

for i, val in enumerate(bottom5["monthly_return_scaled"]):
    ax.text(i + len(top5), val, f"{val*100:.0f}%", ha="center", va="top", fontsize=9)

# 🔧 FIX X-AXIS OVERLAP
ax.tick_params(axis="x", labelsize=8)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

st.pyplot(fig)


import streamlit as st

import streamlit as st
import streamlit as st

# ===== Footer Section =====
st.markdown(
    """
    <div style="
        text-align: center; 
        color: #111827; 
        font-size: 20px;  
        font-weight: 600;
        margin-top: 30px;
        padding: 10px 0;
    ">
        <div style="
            width: 120px; 
            height: 4px; 
            background: linear-gradient(90deg, #2563EB, #10B981); 
            margin: 0 auto 10px auto;
            border-radius: 2px;
        "></div>
        Created by Sholingan
    </div>
    """,
    unsafe_allow_html=True
)

# ===== Session State =====
if "rating_counts" not in st.session_state:
    st.session_state.rating_counts = {1:0,2:0,3:0,4:0,5:0}
if "likes" not in st.session_state:
    st.session_state.likes = 0
if "dislikes" not in st.session_state:
    st.session_state.dislikes = 0

# ===== Feedback Row =====
col_left, col_right = st.columns([1,1])

# -------- LEFT : Like / Dislike --------
with col_left:
    st.markdown("### 👍 Like / 👎 Dislike")

    if st.button("👍 Like"):
        st.session_state.likes += 1
        st.success("Thanks for your feedback! 👍")

    if st.button("👎 Dislike"):
        st.session_state.dislikes += 1
        st.warning("Thanks for your honesty! We'll improve.")

    st.markdown(
        f"**👍 Likes:** {st.session_state.likes} &nbsp;&nbsp; "
        f"**👎 Dislikes:** {st.session_state.dislikes}"
    )

# -------- RIGHT : Rating + COUNT (SIDE BY SIDE) --------
with col_right:
    st.markdown("### ⭐ Rate this Dashboard")

    rate_col, count_col = st.columns([2,1])

    # ⭐ Rating
    with rate_col:
        rating = st.radio(
            "",
            [1,2,3,4,5],
            format_func=lambda x: "⭐"*x,
            key="rating_radio"
        )

        if st.button("Submit Rating"):
            st.session_state.rating_counts[rating] += 1
            st.success(f"Rated {rating} ⭐")

    # 📊 Rating Counts (RIGHT SIDE)
    with count_col:
        st.markdown("**Counts**")
        for i in range(1,6):
            st.markdown(f"{'⭐'*i} : {st.session_state.rating_counts[i]}")

# ===== Comment Section =====
st.markdown("### 💬 Leave a Comment")
comment = st.text_area("", placeholder="Type your feedback here...")

if st.button("Submit Comment"):
    if comment.strip():
        st.success("Thanks for your comment! ✅")
    else:
        st.warning("Please type a comment before submitting.")

# ===== Follow Buttons =====
st.markdown("### 🔗 Follow Me")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <a href="https://twitter.com/YOUR_TWITTER_HANDLE" target="_blank">
    <button style="background:#1DA1F2;color:white;padding:10px 20px;
    border-radius:8px;border:none;font-weight:600;">🐦 Twitter</button>
    </a>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <a href="https://www.linkedin.com/in/sholingans/" target="_blank">
    <button style="background:#0A66C2;color:white;padding:10px 20px;
    border-radius:8px;border:none;font-weight:600;">💼 LinkedIn</button>
    </a>
    """, unsafe_allow_html=True)


