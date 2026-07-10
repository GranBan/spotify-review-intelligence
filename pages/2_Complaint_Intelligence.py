# Page 2

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Complaint Intelligence")

@st.cache_data
def load_data():
    df_topics = pd.read_csv('data/spotify_topics_light.csv')
    return df_topics

df_topics = load_data()

st.title("Complaint Intelligence")
st.markdown("BERTopic clustering of 22,000 negative reviews into distinct complaint themes.")

st.markdown("---")

# Filter noise
df_clean = df_topics[df_topics['topic_label'] != 'Noise'].copy()

# Top topics bar chart
st.markdown("### Top Complaint Topics by Volume")

top_topics = df_clean['topic_label'].value_counts().head(15).sort_values()

fig = go.Figure(go.Bar(
    x=top_topics.values,
    y=top_topics.index,
    orientation='h',
    marker_color='#1DB954',
    text=top_topics.values,
    textposition='outside'
))

fig.update_layout(
    plot_bgcolor='#1e1e2e',
    paper_bgcolor='#1e1e2e',
    font=dict(color='white'),
    xaxis=dict(title="Number of Reviews", gridcolor='#333', color='white'),
    yaxis=dict(gridcolor='#333', color='white'),
    height=550,
    margin=dict(l=250)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Topic explorer
st.markdown("### Topic Explorer")
st.markdown("Select a topic to see representative reviews and average star rating.")

topics_list = sorted(df_clean['topic_label'].unique())
selected_topic = st.selectbox("Select a complaint topic", topics_list)

df_selected = df_clean[df_clean['topic_label'] == selected_topic]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Reviews in Topic", f"{len(df_selected):,}")
with col2:
    st.metric("Avg Star Rating", f"{df_selected['score'].mean():.2f}")
with col3:
    st.metric("% of Negative Reviews", f"{len(df_selected)/len(df_clean)*100:.1f}%")

st.markdown("#### Representative Reviews")
sample_reviews = df_selected[['content', 'score', 'appVersion']].sample(
    min(5, len(df_selected)), random_state=42
)

for _, row in sample_reviews.iterrows():
    st.markdown(f"""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 8px; 
                    padding: 1rem; margin-bottom: 0.5rem;'>
            <span style='color: #ffcc00;'>{"★" * int(row["score"])}{"☆" * (5 - int(row["score"]))}</span>
            <span style='color: #888; font-size: 0.8rem; margin-left: 1rem;'>
                Version {row["appVersion"]}</span>
            <p style='color: #ccc; margin-top: 0.5rem;'>{row["content"]}</p>
        </div>
    """, unsafe_allow_html=True)