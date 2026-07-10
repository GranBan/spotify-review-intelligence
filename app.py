# App

import streamlit as st

st.set_page_config(
    page_title="Spotify Review Intelligence",
    layout="wide"
)

st.markdown("""
    <style>
        .hero {
            text-align: center;
            padding: 3rem 2rem 2rem 2rem;
        }
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #1DB954, #191414);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .hero p {
            font-size: 1.25rem;
            color: #888;
            max-width: 700px;
            margin: 0 auto 2rem auto;
        }
        .metric-card {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
            border: 1px solid #333;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .metric-card .value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #1DB954;
        }
        .metric-card .label {
            font-size: 0.9rem;
            color: #888;
            margin-top: 0.25rem;
        }
        .feature-card {
            background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
            border: 1px solid #333;
            border-radius: 16px;
            padding: 1.5rem;
            height: 100%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .feature-card h3 {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #1DB954;
        }
        .feature-card p {
            font-size: 0.9rem;
            color: #888;
        }
        .divider {
            border: none;
            border-top: 1px solid #333;
            margin: 2rem 0;
        }
        .section-title {
            font-size: 1.8rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .insight-box {
            background: linear-gradient(135deg, #1a2e1a, #1e3a1e);
            border: 1px solid #1DB954;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .insight-box p {
            color: #ccc;
            font-size: 1rem;
            margin: 0;
        }
    </style>

    <div class="hero">
        <h1>Spotify Review Intelligence</h1>
        <p>NLP pipeline that transforms 100,000 Google Play reviews into prioritized product decisions.
        Built with DistilBERT, BERTopic, and temporal trend analysis.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.page_link("pages/1_Overview.py", label="Explore Dashboard", use_container_width=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>System at a Glance</div>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

metrics = [
    ("100,000", "Reviews Analyzed"),
    ("93.5%", "Classifier F1"),
    ("51", "Topics Discovered"),
    ("31", "App Versions Tracked"),
    ("77%", "Peak Negative Rate"),
]

for col, (value, label) in zip([col1, col2, col3, col4, col5], metrics):
    with col:
        st.markdown(f"""
            <div class="metric-card">
                <div class="value">{value}</div>
                <div class="label">{label}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Key Finding</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="insight-box">
        <p>Versions 9.1.46 and 9.1.48 show the highest negative sentiment rates in the dataset (77% and 75%), 
        driven primarily by App Crashes and Bugs complaints, suggesting a regression introduced in the 9.1.46 
        update that persisted into 9.1.48. Ads and Premium Upsell is the single largest complaint category 
        with 3,753 reviews, consistently appearing across all tracked versions.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>What Makes This Different</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>Transformer-Based Classification</h3>
            <p>Fine-tuned DistilBERT on 25,565 balanced Spotify reviews. Binary classification 
            (Negative vs Positive) achieves 93.5% macro F1, significantly outperforming 
            rule-based approaches like VADER.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>Embedding-Based Topic Modeling</h3>
            <p>BERTopic clusters complaint themes using sentence embeddings rather than 
            bag-of-words, capturing semantic meaning. 51 distinct complaint topics 
            discovered from 22,000 negative reviews.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>Version-Level Temporal Analysis</h3>
            <p>Tracks negative sentiment rate across 31 app versions, identifying specific 
            updates that caused sentiment spikes. Links version regressions to dominant 
            complaint topics automatically.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>Business Priority Matrix</h3>
            <p>Scores each complaint topic by frequency, sentiment severity, and recent trend 
            to produce a ranked fix list. Translates NLP output into actionable product 
            decisions with recommended actions.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>Real Production Data</h3>
            <p>100,000 reviews scraped directly from Google Play Store using google-play-scraper. 
            Not a Kaggle dataset. Includes app version metadata enabling version-level 
            temporal analysis.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>End-to-End Pipeline</h3>
            <p>Scraping, preprocessing, classification, topic modeling, temporal analysis, 
            and business prioritization in a single cohesive system. Each stage feeds 
            directly into the next.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Explore the Dashboard</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

pages = [
    ("Overview", "Sentiment distribution, review volume trends, and dataset summary statistics."),
    ("Complaint Intelligence", "BERTopic clusters showing top complaint themes with representative reviews."),
    ("Version Trends", "Negative sentiment rate tracked across 31 app versions with spike detection."),
    ("Priority Matrix", "Ranked fix list scoring issues by frequency, severity, and recent trend."),
]

for col, (title, desc) in zip([col1, col2, col3, col4], pages):
    with col:
        st.markdown(f"""
            <div class="feature-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
        """, unsafe_allow_html=True)