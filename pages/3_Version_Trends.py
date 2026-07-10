# Page 3

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Version Trends")

@st.cache_data
def load_data():
    version_sentiment = pd.read_csv('data/spotify_version_sentiment.csv')
    df_topics = pd.read_csv('data/spotify_topics_light.csv')
    return version_sentiment, df_topics

version_sentiment, df_topics = load_data()

st.title("Version Trends")
st.markdown("Negative sentiment rate tracked across 31 app versions with spike detection.")

st.markdown("---")

# Key finding callout
st.markdown("""
    <div style='background: linear-gradient(135deg, #1a2e1a, #1e3a1e); 
                border: 1px solid #1DB954; border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem;'>
        <p style='color: #1DB954; font-weight: 700; margin-bottom: 0.5rem;'>Key Finding</p>
        <p style='color: #ccc; margin: 0;'>Versions 9.1.46 and 9.1.48 show the highest negative sentiment 
        rates in the dataset (77% and 75%), driven primarily by App Crashes and Bugs complaints, suggesting 
        a regression introduced in the 9.1.46 update that persisted into 9.1.48.</p>
    </div>
""", unsafe_allow_html=True)

# Dual axis chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=version_sentiment['appVersion'],
    y=version_sentiment['total_reviews'],
    name='Total Reviews',
    marker_color='rgba(29, 185, 84, 0.3)',
    yaxis='y1'
))

fig.add_trace(go.Scatter(
    x=version_sentiment['appVersion'],
    y=version_sentiment['negative_rate'],
    name='Negative Rate',
    line=dict(color='#ff4444', width=2.5),
    marker=dict(size=7),
    mode='lines+markers',
    yaxis='y2',
    hovertemplate="Version: %{x}<br>Negative Rate: %{y:.1%}<extra></extra>"
))

# Annotate spikes
spike_versions = version_sentiment[version_sentiment['negative_rate'] > 0.65]
for _, row in spike_versions.iterrows():
    fig.add_annotation(
        x=row['appVersion'],
        y=row['negative_rate'],
        text=f"{row['negative_rate']:.0%}",
        showarrow=True,
        arrowhead=2,
        arrowcolor='#ff4444',
        font=dict(color='#ff4444', size=11),
        yref='y2',
        ay=-40
    )

fig.update_layout(
    plot_bgcolor='#1e1e2e',
    paper_bgcolor='#1e1e2e',
    font=dict(color='white'),
    xaxis=dict(
        title="App Version",
        tickangle=90,
        gridcolor='#333',
        color='white',
        tickfont=dict(size=9)
    ),
    yaxis=dict(
        title="Total Reviews",
        gridcolor='#333',
        color='#1DB954'
    ),
    yaxis2=dict(
        title="Negative Rate",
        overlaying='y',
        side='right',
        tickformat='.0%',
        range=[0, 1],
        color='#ff4444'
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    height=500,
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Version drill-down
st.markdown("### Version Drill-Down")
st.markdown("Select a version to see its top complaint topics.")

selected_version = st.selectbox(
    "Select app version",
    version_sentiment['appVersion'].tolist()
)

df_version = df_topics[
    (df_topics['appVersion'] == selected_version) &
    (df_topics['topic_label'] != 'Noise')
]

if len(df_version) == 0:
    st.warning("No labeled topic data available for this version.")
else:
    col1, col2, col3 = st.columns(3)
    
    total = version_sentiment[version_sentiment['appVersion'] == selected_version]['total_reviews'].values[0]
    neg_rate = version_sentiment[version_sentiment['appVersion'] == selected_version]['negative_rate'].values[0]
    top_complaint = df_version['topic_label'].value_counts().index[0]
    
    with col1:
        st.metric("Total Reviews", f"{total:,}")
    with col2:
        st.metric("Negative Rate", f"{neg_rate:.1%}")
    with col3:
        st.metric("Top Complaint", top_complaint)

    topic_counts = df_version['topic_label'].value_counts().head(8).sort_values()
    
    fig2 = go.Figure(go.Bar(
        x=topic_counts.values,
        y=topic_counts.index,
        orientation='h',
        marker_color='#ff4444',
        text=topic_counts.values,
        textposition='outside'
    ))
    
    fig2.update_layout(
        plot_bgcolor='#1e1e2e',
        paper_bgcolor='#1e1e2e',
        font=dict(color='white'),
        xaxis=dict(title="Review Count", gridcolor='#333', color='white'),
        yaxis=dict(gridcolor='#333', color='white'),
        height=400,
        margin=dict(l=250),
        title=dict(
            text=f"Top Complaint Topics — Version {selected_version}",
            font=dict(color='white'),
            x=0.5
        )
    )
    
    st.plotly_chart(fig2, use_container_width=True)