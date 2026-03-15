import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Social Media Analytics", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('social_media_data.csv')
        df['Post_Date'] = pd.to_datetime(df['Post_Date'])
        # Calculating KPI Ratios
        df['ER_%'] = (df['Engagement'] / df['Reach']) * 100
        df['CR_%'] = (df['Conversions'] / df['Engagement']) * 100
        return df
    except FileNotFoundError:
        st.error("Data file not found! Please run 'python data_generator.py' first.")
        return None

df = load_data()

if df is not None:
    # --- SIDEBAR FILTERS ---
    st.sidebar.title("🔍 Filters")
    selected_platform = st.sidebar.multiselect("Select Platform", options=df['Platform'].unique(), default=df['Platform'].unique())
    selected_campaign = st.sidebar.multiselect("Select Campaign", options=df['Campaign_Name'].unique(), default=df['Campaign_Name'].unique())

    # Filtering Data
    filtered_df = df[(df['Platform'].isin(selected_platform)) & (df['Campaign_Name'].isin(selected_campaign))]

    # --- MAIN HEADER ---
    st.title("📊 Social Media Marketing Analytics")
    st.markdown(f"Currently analyzing **{len(filtered_df)}** posts performance.")
    st.divider()

    # --- TOP KPI CARDS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Reach", f"{filtered_df['Reach'].sum():,}")
    with col2:
        st.metric("Total Impressions", f"{filtered_df['Impressions'].sum():,}")
    with col3:
        st.metric("Avg Engagement Rate", f"{filtered_df['ER_%'].mean():.2f}%")
    with col4:
        st.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,}")

    st.divider()

    # --- CHARTS SECTION ---
    row1_c1, row1_c2 = st.columns(2)

    with row1_c1:
        st.subheader("📈 Reach Trend Over Time")
        trend_data = filtered_df.groupby('Post_Date')['Reach'].sum().reset_index()
        fig_line = px.line(trend_data, x='Post_Date', y='Reach', template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

    with row1_c2:
        st.subheader("🎯 Conversions by Platform")
        fig_pie = px.pie(filtered_df, values='Conversions', names='Platform', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- PLATFORM COMPARISON ---
    st.subheader("📊 Platform Comparison: Metrics Breakdown")
    comparison_data = filtered_df.groupby('Platform')[['Reach', 'Engagement', 'Conversions']].sum().reset_index()
    fig_bar = px.bar(comparison_data, x='Platform', y=['Reach', 'Engagement', 'Conversions'], barmode='group')
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- DATA TABLE ---
    with st.expander("📄 View Detailed Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)