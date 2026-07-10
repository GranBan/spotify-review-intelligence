# Page 1

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide", page_title="Overview")

@st.cache_data
def load_data():
    df = pd.read_csv('data/spotify_reviews_light.csv')
    return df

df = load_data()

st.title("Overview")
st.markdown("Sentiment distribution, review volume, and dataset summary across 100,000 Spotify reviews.")

st.markdown("---")

# Key stats
col1, col2, col3, col4 = st.columns(4)

neg_count = (df['predicted_sentiment'] == 'Negative').sum()
pos_count = (df['predicted_sentiment'] == 'Positive').sum()
neg_pct = neg_count / len(df) * 100

with col1:
    st.metric("Total Reviews", f"{len(df):,}")
with col2:
    st.metric("Negative Reviews", f"{neg_count:,}")
with col3:
    st.metric("Positive Reviews", f"{pos_count:,}")
with col4:
    st.metric("Negative Rate", f"{neg_pct:.1f}%")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sentiment Distribution")
    sentiment_counts = df['predicted_sentiment'].value_counts()
    fig = go.Figure(go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        hole=0.4,
        marker_colors=['#ff4444', '#1DB954']
    ))
    fig.update_layout(
        plot_bgcolor='#1e1e2e',
        paper_bgcolor='#1e1e2e',
        font=dict(color='white'),
        height=350,
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Score Distribution")
    score_counts = df['score'].value_counts().sort_index()
    fig2 = go.Figure(go.Bar(
        x=score_counts.index,
        y=score_counts.values,
        marker_color=['#ff4444', '#ff7f0e', '#ffcc00', '#1DB954', '#1DB954'],
        text=score_counts.values,
        textposition='outside'
    ))
    fig2.update_layout(
        plot_bgcolor='#1e1e2e',
        paper_bgcolor='#1e1e2e',
        font=dict(color='white'),
        xaxis=dict(title="Star Rating", gridcolor='#333', color='white'),
        yaxis=dict(title="Count", gridcolor='#333', color='white'),
        height=350
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Reviews by Month")
    month_counts = df['month'].value_counts().sort_index()
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 
                   6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 
                   11: 'Nov', 12: 'Dec'}
    fig3 = go.Figure(go.Bar(
        x=[month_names[m] for m in month_counts.index],
        y=month_counts.values,
        marker_color='#1DB954',
        text=month_counts.values,
        textposition='outside'
    ))
    fig3.update_layout(
        plot_bgcolor='#1e1e2e',
        paper_bgcolor='#1e1e2e',
        font=dict(color='white'),
        xaxis=dict(title="Month", gridcolor='#333', color='white'),
        yaxis=dict(title="Number of Reviews", gridcolor='#333', color='white', range=[0, max(month_counts.values) * 1.15]),
        height=350
    )
    
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("### Review Length Distribution")
    fig4 = go.Figure(go.Histogram(
        x=df['word_count'],
        nbinsx=50,
        marker_color='#1DB954',
        opacity=0.8
    ))
    fig4.update_layout(
        plot_bgcolor='#1e1e2e',
        paper_bgcolor='#1e1e2e',
        font=dict(color='white'),
        xaxis=dict(title="Word Count", gridcolor='#333', color='white'),
        yaxis=dict(title="Number of Reviews", gridcolor='#333', color='white'),
        height=350
    )
    st.plotly_chart(fig4, use_container_width=True)