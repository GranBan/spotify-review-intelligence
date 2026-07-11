# Page 6

# Page 6

import streamlit as st

st.set_page_config(layout="wide", page_title="Pipeline Overview")

st.title("Pipeline Overview")
st.markdown("How 100,000 raw Google Play reviews become prioritized product decisions.")

st.markdown("---")

steps = [
    ("Data Collection", "Scraped 100,000 Spotify reviews directly from Google Play Store using google-play-scraper, including star rating, review text, date, and app version metadata."),
    ("Exploratory Data Analysis", "Examined score distribution, review length, app version coverage, and identified 33% of reviews under 3 words."),
    ("Sentiment Labeling", "Derived initial sentiment labels from star ratings (1-2 Negative, 4-5 Positive), dropping neutral 3-star reviews to focus on binary classification."),
    ("DistilBERT Fine-Tuning", "Fine-tuned a pre-trained DistilBERT model on 56,510 balanced reviews using Google Colab T4 GPU, achieving 93.5% macro F1 on held-out validation data."),
    ("Full Inference", "Ran the fine-tuned model on all 100,000 reviews to produce text-based sentiment predictions, capturing nuance that star ratings alone miss."),
    ("English Filtering", "Filtered non-English reviews using langdetect before topic modeling, since mixed-language text degrades embedding-based clustering quality."),
    ("BERTopic Clustering", "Applied BERTopic with sentence embeddings (all-MiniLM-L6-v2) to 22,629 predicted-negative reviews with 10+ words, discovering 51 distinct complaint themes."),
    ("Manual Topic Labeling", "Reviewed BERTopic's auto-generated keyword clusters and representative documents to assign clean, business-readable topic labels."),
    ("Temporal Trend Analysis", "Tracked negative sentiment rate across 31 app versions, identifying a 77% negative spike at version 9.1.46 linked to App Crashes and Bugs complaints."),
    ("Priority Matrix Construction", "Scored each complaint topic by frequency (50%), severity (30%), and recent trend (20%) to produce a ranked, actionable fix list."),
    ("Streamlit Deployment", "Built a 6-page interactive dashboard deployed on Streamlit Community Cloud, with memory-optimized data loading for production stability."),
]

for i, (step, desc) in enumerate(steps):
    col1, col2, col3 = st.columns([1, 3, 8])
    with col1:
        st.markdown(f"""
            <div style='background: #1DB954; border-radius: 50%; width: 40px; height: 40px;
                        display: flex; align-items: center; justify-content: center;
                        font-weight: 800; color: white; font-size: 1rem;'>
                {i+1}
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"**{step}**")
    with col3:
        st.markdown(f"<span style='color: #888;'>{desc}</span>", unsafe_allow_html=True)

    if i < len(steps) - 1:
        st.markdown("""
            <div style='margin-left: 20px; color: #555; font-size: 1.2rem;'>|</div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## Why These Design Decisions")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 12px; padding: 1.5rem;'>
            <h4 style='color: #1DB954;'>Why Binary Classification, Not 3-Class</h4>
            <p style='color: #888; font-size: 0.9rem;'>Initial 3-class (Negative/Neutral/Positive) training 
            achieved only 71% macro F1 due to the inherent ambiguity of neutral reviews and limited neutral 
            training data (5,565 samples). Switching to binary classification allowed using the full 
            positive and negative review pools, improving macro F1 to 93.5%. Neutral predictions were also 
            never used downstream, making the added complexity unjustified.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 12px; padding: 1.5rem;'>
            <h4 style='color: #1DB954;'>Why BERTopic Over LDA</h4>
            <p style='color: #888; font-size: 0.9rem;'>LDA relies on bag-of-words representations that treat 
            each word independently, missing semantic meaning. BERTopic uses sentence embeddings that capture 
            context, allowing it to distinguish "the app crashes constantly" from "I want to smash my phone" 
            even without shared vocabulary. This matters significantly for short, colloquial app review text.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 12px; padding: 1.5rem;'>
            <h4 style='color: #1DB954;'>Why Filter Short Reviews Before Topic Modeling</h4>
            <p style='color: #888; font-size: 0.9rem;'>33% of all reviews are under 5 words ("peak", "very nice"). 
            These produce generic embeddings that dilute cluster quality. A 10-word minimum threshold retained 
            19,406+ negative reviews, sufficient for stable topic discovery, while removing noise that 
            would otherwise pollute meaningful clusters.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='background: #1e1e2e; border: 1px solid #333; border-radius: 12px; padding: 1.5rem;'>
            <h4 style='color: #1DB954;'>Why Manual Topic Labeling</h4>
            <p style='color: #888; font-size: 0.9rem;'>BERTopic's auto-generated labels (e.g., "1_ads_premium_song_app") 
            are not human-readable. Manual review of representative documents and keyword clusters converts 
            algorithmic output into business language a product team can act on directly, while also catching 
            and excluding non-actionable noise clusters (e.g., non-English text, generic star-rating complaints).</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## Limitations")
st.markdown("""
- **Language coverage:** Only English reviews are included in topic modeling; ~1,375 non-English reviews were filtered out.
- **Version metadata sparsity:** 16.4% of reviews lack app version information and are excluded from temporal analysis.
- **Sample-based search:** The in-app review search feature operates on a representative sample (820 reviews across 41 topics), not the full negative review corpus, for deployment memory efficiency.
- **Topic noise:** Approximately 35% of negative reviews fall into the "Noise" cluster — genuinely ambiguous or too-short text that doesn't fit any discovered theme.
""")