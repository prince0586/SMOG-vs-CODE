import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# --- 1. Page Configuration ---
st.set_page_config(page_title="Smog & Code: Similarity Engine", page_icon="📉", layout="wide")

st.title("🏭 Smog & Code: The Similarity Engine")
st.markdown("""
**The Challenge:** Find similarity between two completely unrelated datasets.
* **Dataset A:** Air Quality (PM 2.5) in your city.
* **Dataset B:** Your coding output (GitHub Commits).
""")

# --- 2. Sidebar Inputs ---
st.sidebar.header("Configure Data Sources")
github_user = st.sidebar.text_input("GitHub Username", "torvalds")
# Default: San Francisco
lat = st.sidebar.number_input("Latitude", value=37.7749) 
lon = st.sidebar.number_input("Longitude", value=-122.4194)

# --- 3. Data Acquisition Engine ---
@st.cache_data
def fetch_and_process_data(username, lat, lon):
    # A. Fetch GitHub Data (Digital Source)
    try:
        gh_url = f"https://api.github.com/users/{username}/events/public"
        gh_data = requests.get(gh_url).json()
        
        commits = []
        for event in gh_data:
            if event['type'] == 'PushEvent':
                date = event['created_at'].split('T')[0]
                count = len(event['payload'].get('commits', []))
                commits.append({'date': date, 'commits': count})
        
        df_commits = pd.DataFrame(commits)
        if df_commits.empty: return None
        
        # Group by day
        df_commits['date'] = pd.to_datetime(df_commits['date'])
        df_commits = df_commits.groupby('date')['commits'].sum().reset_index()
    except:
        return None

    # B. Fetch Air Quality Data (Physical Source)
    try:
        # Match the date range of the commits
        min_date = df_commits['date'].min().strftime("%Y-%m-%d")
        max_date = df_commits['date'].max().strftime("%Y-%m-%d")
        
        aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": lat, "longitude": lon,
            "start_date": min_date, "end_date": max_date,
            "hourly": "pm2_5"
        }
        aqi_resp = requests.get(aqi_url, params=params).json()
        
        df_aqi = pd.DataFrame({
            'time': pd.to_datetime(aqi_resp['hourly']['time']),
            'pm2_5': aqi_resp['hourly']['pm2_5']
        })
        df_aqi['date'] = df_aqi['time'].dt.date
        df_aqi['date'] = pd.to_datetime(df_aqi['date'])
        
        # Average PM2.5 per day
        df_aqi_daily = df_aqi.groupby('date')['pm2_5'].mean().reset_index()
    except:
        return None

    # C. Mash Up (Merge)
    merged = pd.merge(df_commits, df_aqi_daily, on='date')
    return merged

# --- 4. The Similarity Analysis ---
if st.button("Analyze Similarity"):
    with st.spinner("Normalizing unrelated data scales..."):
        df = fetch_and_process_data(github_user, lat, lon)
        
        if df is None or len(df) < 3:
            st.error("Not enough matching data found. Try a more active GitHub user.")
        else:
            # --- THE MAGIC: Normalization ---
            # We scale both 5-20 commits and 10-150 AQI to a 0.0-1.0 range
            # This allows us to visually overlay them perfectly.
            scaler = MinMaxScaler()
            df[['norm_commits', 'norm_aqi']] = scaler.fit_transform(df[['commits', 'pm2_5']])
            
            # --- THE MATH: Correlation ---
            correlation = df['commits'].corr(df['pm2_5'])
            
            # Display Results
            col1, col2, col3 = st.columns(3)
            col1.metric("Data Points", len(df))
            col2.metric("Similarity Score", f"{correlation:.4f}", 
                        help="1.0 = Identical, -1.0 = Opposite, 0.0 = Unrelated")
            
            if abs(correlation) > 0.5:
                col3.success("Strong Similarity Found!")
            elif abs(correlation) > 0.3:
                col3.warning("Weak Similarity Found.")
            else:
                col3.info("No Similarity Detected.")

            # --- Visualization ---
            st.subheader("Normalized Pattern Overlay")
            st.caption("Notice how the axes are removed? We are looking at PURE PATTERNS now.")
            
            fig = go.Figure()
            
            # Line 1: Productivity
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['norm_commits'],
                mode='lines+markers', name='Productivity Pattern',
                line=dict(color='#00CC96', width=3)
            ))
            
            # Line 2: Pollution
            fig.add_trace(go.Scatter(
                x=df['date'], y=df['norm_aqi'],
                mode='lines+markers', name='Pollution Pattern',
                line=dict(color='#EF553B', width=3, dash='dot')
            ))
            
            fig.update_layout(
                hovermode="x unified",
                template="plotly_dark",
                yaxis=dict(showticklabels=False, title="Normalized Intensity (0-1)")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("View Raw Data"):
                st.dataframe(df)