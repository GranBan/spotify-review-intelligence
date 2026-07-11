# Page 7

# Page 7

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Embedding Visualization")

@st.cache_data
def load_data():
    df_umap = pd.read_csv('data/spotify_umap_final.csv')
    return df_umap

df_umap = load_data()

st.title("Embedding Visualization")
st.markdown("2D projection of review embeddings showing how BERTopic separates complaint themes.")

st.markdown("---")

st.markdown("""
Each point represents one negative review, positioned by its semantic embedding and reduced to 2D 
using UMAP (the same dimensionality reduction BERTopic uses internally for clustering). Reviews that 
are semantically similar appear close together, and the resulting visual clusters correspond to the 
complaint topics discovered by BERTopic.
""")

# Filter to top topics for readability
top_n = st.slider("Number of topics to display", min_value=5, max_value=20, value=10)

top_topics = df_umap[df_umap['topic_label'] != 'Noise']['topic_label'].value_counts().head(top_n).index.tolist()

df_filtered = df_umap[df_umap['topic_label'].isin(top_topics)]

fig = px.scatter(
    df_filtered,
    x='umap_x',
    y='umap_y',
    color='topic_label',
    hover_data={'content': True, 'umap_x': False, 'umap_y': False},
    title=f"Top {top_n} Complaint Topics — Embedding Space"
)

fig.update_traces(marker=dict(size=5, opacity=0.6))

fig.update_layout(
    plot_bgcolor='#1e1e2e',
    paper_bgcolor='#1e1e2e',
    font=dict(color='white'),
    xaxis=dict(title="UMAP Dimension 1", gridcolor='#333', color='white'),
    yaxis=dict(title="UMAP Dimension 2", gridcolor='#333', color='white'),
    height=650,
    legend=dict(font=dict(size=9))
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
Points that overlap or lie close together in this space represent reviews with similar language, even 
if they don't share exact keywords. This is the key advantage of embedding-based topic modeling over 
traditional keyword-matching approaches — semantic similarity is captured directly in the geometry.
""")