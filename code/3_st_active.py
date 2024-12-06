import streamlit as st
import pandas as pd
import altair as alt

st.title("PolyMarket: Active Markets")
df_active = pd.read_csv('cache/active_markets.csv')
df_all = pd.read_csv('cache/all_markets.csv')

all_markets_count = len(df_all)
active_markets_count = len(df_active)

col1, col2 = st.columns(2)
col1.metric("Total Markets", all_markets_count)
col2.metric("Active Markets", active_markets_count)

default_columns = [
    "question", "outcomes", "outcomePrices", 
    "bestBid", "bestAsk", "lastTradePrice", 
    "spread", "volume", "liquidityNum", 
    "startDateIso", "endDateIso"
]

st.header("Customize Columns to Display")
all_columns = df_active.columns.tolist()
selected_columns = st.multiselect(
    "Select additional columns to display",
    options=all_columns,
    default=default_columns
)

filtered_df = df_active[selected_columns]

st.header("Filtered Active Markets Data")
st.dataframe(filtered_df)

st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name="filtered_active_markets.csv",
    mime="text/csv",
)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Highest Market Durations")
    df_active['duration'] = pd.to_datetime(df_active['endDateIso']) - pd.to_datetime(df_active['startDateIso'])
    df_active['duration_days'] = df_active['duration'].dt.days
    top_duration_markets = df_active.nlargest(10, 'duration_days')[['question', 'duration_days']]
    duration_bar_chart = alt.Chart(top_duration_markets).mark_bar().encode(
        x=alt.X('duration_days:Q', title='Duration (Days)'),
        y=alt.Y('question:N', sort='-x', title=''),
        tooltip=['question', 'duration_days']
    ).properties(height=400)
    st.altair_chart(duration_bar_chart, use_container_width=True)

with col2:
    st.subheader("Market Duration Distribution")
    bins = [
        (0, 50), (50, 100), (100, 150), (150, 200),
        (200, 250), (250, 300), (300, 350), (350, 400),
        (400, 450), (450, 500), (500, float('inf'))
    ]
    bin_labels = [
        "0-50 days", "50-100 days", "100-150 days", 
        "150-200 days", "200-250 days", "250-300 days", 
        "300-350 days", "350-400 days", "400-450 days", 
        "450-500 days", "500+ days"
    ]
    df_active['duration_bin'] = pd.cut(
        df_active['duration_days'], 
        bins=[b[0] for b in bins] + [float('inf')],
        labels=bin_labels,
        right=False
    )
    duration_counts = df_active['duration_bin'].value_counts().reset_index()
    duration_counts.columns = ['Duration Range', 'Market Count']
    duration_dist_chart = alt.Chart(duration_counts).mark_bar().encode(
        x=alt.X('Duration Range:N', sort=bin_labels, title='Duration Range'),
        y=alt.Y('Market Count:Q', title='Number of Markets'),
        tooltip=['Duration Range', 'Market Count']
    ).properties(height=400)
    st.altair_chart(duration_dist_chart, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Active Markets by Volume")
    top_volume_markets = df_active.nlargest(10, 'volume')[['question', 'volume']]
    bar_chart = alt.Chart(top_volume_markets).mark_bar().encode(
        x=alt.X('volume:Q', title='Trading Volume'),
        y=alt.Y('question:N', sort='-x', title=''),
        tooltip=['question', 'volume']
    ).properties(height=400)
    st.altair_chart(bar_chart, use_container_width=True)

with col2:
    st.subheader("Daily Volume")
    daily_volume_chart = alt.Chart(df_active).mark_line().encode(
        x=alt.X('startDateIso:T', title='Date'),
        y=alt.Y('volume24hr:Q', title='Daily Volume'),
        tooltip=['startDateIso', 'volume24hr']
    ).properties(height=400)
    st.altair_chart(daily_volume_chart, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Bid-Ask Spread Distribution")
    df_active['bid_ask_spread'] = df_active['bestAsk'] - df_active['bestBid']
    spread_histogram = alt.Chart(df_active).mark_bar().encode(
        x=alt.X('bid_ask_spread:Q', bin=alt.Bin(maxbins=30), title='Bid-Ask Spread'),
        y=alt.Y('count():Q', title='Count'),
        tooltip=['count()']
    ).properties(height=400)
    st.altair_chart(spread_histogram, use_container_width=True)

with col2:
    st.subheader("Markets with High Bid-Ask Spread")
    df_active['bid_ask_spread'] = df_active['bestAsk'] - df_active['bestBid']
    top_spread_markets = df_active.nlargest(10, 'bid_ask_spread')[['question', 'bid_ask_spread']]
    spread_bar_chart = alt.Chart(top_spread_markets).mark_bar().encode(
        x=alt.X('bid_ask_spread:Q', title='Bid-Ask Spread'),
        y=alt.Y('question:N', sort='-x', title=''),
        tooltip=['question', 'bid_ask_spread']
    ).properties(height=400)
    st.altair_chart(spread_bar_chart, use_container_width=True)

st.divider()

st.subheader("Volume as Percentage of Liquidity")
st.write("to ensure that the markets are liquid enough to handle the volume traded")
df_active['volume_pct_liquidity'] = (df_active['volume'] / df_active['liquidityNum']) * 100
df_active = df_active[df_active['volume_pct_liquidity'].notnull()]
df_active = df_active[df_active['volume_pct_liquidity'] <= 100]
top_volume_pct_markets = df_active.nlargest(10, 'volume_pct_liquidity')[['question', 'volume_pct_liquidity']]
volume_pct_bar_chart = alt.Chart(top_volume_pct_markets).mark_bar().encode(
    x=alt.X('volume_pct_liquidity:Q', title='Volume (% of Liquidity)', scale=alt.Scale(domain=[0, 100])),
    y=alt.Y('question:N', sort='-x', title='Market Question'),
    tooltip=['question', 'volume_pct_liquidity']
).properties(height=400)
st.altair_chart(volume_pct_bar_chart, use_container_width=True)
