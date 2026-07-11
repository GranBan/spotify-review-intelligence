# Page 5

# Page 5

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Misclassification Analysis")

@st.cache_data
def load_data():
    df_mismatch = pd.read_csv('data/spotify_mismatches.csv')
    return df_mismatch

df_mismatch = load_data()

st.title("Misclassification Analysis")
st.markdown("Where the model's predictions disagree with star-rating-derived sentiment, and why.")

st.markdown("---")

st.markdown("""
    <div style='background: linear-gradient(135deg, #1a2e1a, #1e3a1e); 
                border: 1px solid #1DB954; border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem;'>
        <p style='color: #1DB954; font-weight: 700; margin-bottom: 0.5rem;'>Why This Matters</p>
        <p style='color: #ccc; margin: 0;'>Star ratings are a noisy proxy for sentiment. A 5-star review 
        can contain negative text ("great app but too many ads"), and a 1-star review can contain positive 
        text about specific features despite overall frustration. Comparing the model's text-based predictions 
        against star-rating labels reveals where each signal adds unique information.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

high_to_neg = df_mismatch[(df_mismatch['sentiment'] == 'Positive') & 
                            (df_mismatch['predicted_sentiment'] == 'Negative')]
low_to_pos = df_mismatch[(df_mismatch['sentiment'] == 'Negative') & 
                           (df_mismatch['predicted_sentiment'] == 'Positive')]

with col1:
    st.metric("Total Disagreements", f"{len(df_mismatch):,}")
with col2:
    st.metric("High Stars, Negative Text", f"{len(high_to_neg):,}")
with col3:
    st.metric("Low Stars, Positive Text", f"{len(low_to_pos):,}")

st.markdown("---")

# Distribution chart
st.markdown("### Disagreement Breakdown")

fig = go.Figure(go.Bar(
    x=["High Stars → Predicted Negative", "Low Stars → Predicted Positive"],
    y=[len(high_to_neg), len(low_to_pos)],
    marker_color=['#ff4444', '#1DB954'],
    text=[len(high_to_neg), len(low_to_pos)],
    textposition='outside'
))

fig.update_layout(
    plot_bgcolor='#1e1e2e',
    paper_bgcolor='#1e1e2e',
    font=dict(color='white'),
    xaxis=dict(gridcolor='#333', color='white'),
    yaxis=dict(title="Count", gridcolor='#333', color='white'),
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Explorer
st.markdown("### Explore Disagreements")

case_type = st.radio(
    "Select disagreement type",
    ["High Stars, Predicted Negative (model caught hidden negativity)",
     "Low Stars, Predicted Positive (potential model error)"],
    horizontal=False
)

if "High Stars" in case_type:
    df_view = high_to_neg
else:
    df_view = low_to_pos

sample_size = min(8, len(df_view))
display_cases = df_view.sample(sample_size, random_state=42)

for _, row in display_cases.iterrows():
    st.markdown(f"""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 8px; 
                    padding: 1rem; margin-bottom: 0.5rem;'>
            <span style='color: #ffcc00;'>{"★" * int(row["score"])}{"☆" * (5 - int(row["score"]))}</span>
            <span style='color: #888; font-size: 0.8rem; margin-left: 1rem;'>
                Star-derived: {row["sentiment"]} → Model predicted: {row["predicted_sentiment"]}</span>
            <p style='color: #ccc; margin-top: 0.5rem;'>{row["content"]}</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Interpretation")
st.markdown("""
The **3,554 "High Stars, Predicted Negative"** cases are the more common and more informative pattern. 
These are typically reviews where the user gave a high star rating out of overall satisfaction, but the 
written text contains specific complaints ("Love the app but the ads are getting ridiculous"). This is 
exactly the kind of nuance that star ratings alone cannot capture, and represents a case where the model 
adds genuine value over simple rating-based filtering.

The **1,019 "Low Stars, Predicted Positive"** cases are less common and more likely to include genuine 
model errors, sarcasm, or reviews where the star rating reflects a factor unrelated to the review text 
itself (e.g., frustration with pricing despite positive comments about the app's features).
""")