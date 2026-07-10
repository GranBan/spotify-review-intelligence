# Page 4

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Priority Matrix")

@st.cache_data
def load_data():
    topic_stats = pd.read_csv('data/spotify_priority_matrix.csv')
    return topic_stats

topic_stats = load_data()

st.title("Priority Matrix")
st.markdown("Complaint topics ranked by frequency, sentiment severity, and recent trend.")

st.markdown("---")

# Methodology explanation
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 12px; padding: 1rem;'>
            <p style='color: #1DB954; font-weight: 700; margin-bottom: 0.25rem;'>Frequency (50%)</p>
            <p style='color: #888; font-size: 0.9rem; margin: 0;'>Number of reviews mentioning 
            this issue. More affected users means higher priority.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 12px; padding: 1rem;'>
            <p style='color: #ff4444; font-weight: 700; margin-bottom: 0.25rem;'>Severity (30%)</p>
            <p style='color: #888; font-size: 0.9rem; margin: 0;'>Average star rating of reviews 
            in this topic. Lower rating means more severe user impact.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 12px; padding: 1rem;'>
            <p style='color: #ffcc00; font-weight: 700; margin-bottom: 0.25rem;'>Trend (20%)</p>
            <p style='color: #888; font-size: 0.9rem; margin: 0;'>Prominence in the 5 most recent 
            app versions. Still occurring recently means immediate attention needed.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Priority score chart
st.markdown("### Priority Score by Topic")

df_chart = topic_stats[topic_stats['topic_label'] != 'Noise'].sort_values('priority_score').tail(15)

fig = go.Figure(go.Bar(
    x=df_chart['priority_score'],
    y=df_chart['topic_label'],
    orientation='h',
    marker=dict(
        color=df_chart['priority_score'],
        colorscale=[[0, '#1DB954'], [0.5, '#ffcc00'], [1, '#ff4444']],
        showscale=True,
        colorbar=dict(title="Priority Score")
    ),
    text=df_chart['priority_score'].round(3),
    textposition='outside'
))

fig.update_layout(
    plot_bgcolor='#1e1e2e',
    paper_bgcolor='#1e1e2e',
    font=dict(color='white'),
    xaxis=dict(title="Priority Score", gridcolor='#333', color='white'),
    yaxis=dict(gridcolor='#333', color='white'),
    height=550,
    margin=dict(l=280)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Full ranked table
st.markdown("### Full Priority Matrix")

df_display = topic_stats[topic_stats['topic_label'] != 'Noise'][[
    'rank', 'topic_label', 'review_count', 'avg_star_rating', 
    'priority_score', 'recommended_action'
]].copy()

df_display.columns = ['Rank', 'Issue', 'Reviews', 'Avg Rating', 'Priority Score', 'Recommended Action']
df_display['Priority Score'] = df_display['Priority Score'].round(3)
df_display['Avg Rating'] = df_display['Avg Rating'].round(2)

st.dataframe(df_display, use_container_width=True, hide_index=True)

# Download button
csv = df_display.to_csv(index=False)
st.download_button(
    label="Download Priority Matrix as CSV",
    data=csv,
    file_name="spotify_priority_matrix.csv",
    mime="text/csv"
)

st.markdown("---")

st.markdown("### Scoring Methodology")
st.markdown("""
Priority Score = (0.5 x Frequency Score) + (0.3 x Severity Score) + (0.2 x Trend Score)

- **Frequency Score:** Review count normalized by maximum topic count
- **Severity Score:** (5 - avg star rating) / 4, so 1-star reviews score 1.0
- **Trend Score:** Topic share in the 5 most recent app versions

Weights reflect product team priorities: widespread issues affect more users (frequency dominates), 
severely unhappy users are at highest churn risk (severity second), 
and recent issues need immediate attention (trend as tiebreaker).
""")