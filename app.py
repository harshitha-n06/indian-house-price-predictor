import streamlit as st
import joblib
import pandas as pd
import time

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Indian House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# PROFESSIONAL DARK LUXURY UI
# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ===== ROOT VARIABLES ===== */
:root {
    --bg-deep:       #0B0F1A;
    --bg-card:       #111827;
    --bg-card2:      #161D2E;
    --accent-gold:   #F5A623;
    --accent-teal:   #00C9A7;
    --accent-blue:   #3B82F6;
    --text-primary:  #F1F5F9;
    --text-muted:    #94A3B8;
    --border:        rgba(255,255,255,0.06);
    --glow-gold:     0 0 30px rgba(245,166,35,0.18);
    --glow-teal:     0 0 30px rgba(0,201,167,0.15);
    --radius:        16px;
    --transition:    0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ===== BACKGROUND MESH ===== */
.stApp {
    background: var(--bg-deep);
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%, rgba(245,166,35,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(0,201,167,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(59,130,246,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ===== ALL TEXT ===== */
body, p, span, label, div {
    color: var(--text-primary);
    font-family: 'DM Sans', sans-serif;
}

/* ===== HIDE STREAMLIT CHROME ===== */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 3rem 3rem;
    max-width: 1400px;
}

/* ===== ANIMATED TITLE ===== */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 4vw, 56px);
    font-weight: 800;
    background: linear-gradient(135deg, #F5A623 0%, #F9D423 40%, #00C9A7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin: 0;
    animation: fadeSlideDown 0.8s ease forwards;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 17px;
    font-weight: 300;
    color: var(--text-muted) !important;
    margin-top: 10px;
    letter-spacing: 0.3px;
    animation: fadeSlideDown 0.8s 0.15s ease both;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,201,167,0.12);
    border: 1px solid rgba(0,201,167,0.25);
    color: #00C9A7 !important;
    font-size: 13px;
    font-weight: 500;
    padding: 5px 14px;
    border-radius: 100px;
    margin-top: 14px;
    animation: fadeSlideDown 0.8s 0.3s ease both;
}

/* ===== INFO BANNER ===== */
.stAlert {
    background: rgba(59,130,246,0.08) !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-radius: 12px !important;
    color: #93C5FD !important;
    animation: fadeSlideDown 0.8s 0.45s ease both;
}
.stAlert p { color: #93C5FD !important; font-size: 14px !important; }

/* ===== SECTION CARDS ===== */
.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 20px;
    position: relative;
    overflow: hidden;
    transition: var(--transition);
    animation: cardReveal 0.7s ease both;
}

.section-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-gold), var(--accent-teal));
    opacity: 0;
    transition: var(--transition);
}

.section-card:hover {
    border-color: rgba(245,166,35,0.2);
    transform: translateY(-2px);
    box-shadow: var(--glow-gold), 0 20px 40px rgba(0,0,0,0.3);
}

.section-card:hover::before { opacity: 1; }

.card-1 { animation-delay: 0.2s; }
.card-2 { animation-delay: 0.35s; }
.card-3 { animation-delay: 0.5s; }

/* ===== SECTION HEADINGS ===== */
.section-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}

.section-head .icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.icon-gold { background: rgba(245,166,35,0.15); }
.icon-teal { background: rgba(0,201,167,0.15); }
.icon-blue { background: rgba(59,130,246,0.15); }

.section-head h3 {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary) !important;
    margin: 0;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ===== ALL STREAMLIT LABELS ===== */
.stSelectbox label,
.stSlider label,
.stNumberInput label {
    color: var(--text-muted) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
    text-transform: uppercase !important;
}

/* ===== SELECTBOX ===== */
.stSelectbox > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    transition: var(--transition) !important;
}

.stSelectbox > div > div:hover,
.stSelectbox > div > div:focus-within {
    border-color: rgba(245,166,35,0.4) !important;
    box-shadow: 0 0 0 2px rgba(245,166,35,0.1) !important;
}

/* ===== NUMBER INPUT ===== */
.stNumberInput > div > div > input {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: var(--transition) !important;
}

.stNumberInput > div > div > input:focus {
    border-color: rgba(245,166,35,0.4) !important;
    box-shadow: 0 0 0 2px rgba(245,166,35,0.1) !important;
}

/* ===== SLIDER ===== */
.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"],
.stSlider [data-baseweb="slider"] {
    color: var(--text-muted) !important;
}

.stSlider [role="slider"] {
    background: var(--accent-gold) !important;
    border: 2px solid var(--bg-deep) !important;
    box-shadow: 0 0 10px rgba(245,166,35,0.5) !important;
    width: 18px !important;
    height: 18px !important;
}

.stSlider [data-testid="stSliderTrackFill"] {
    background: linear-gradient(90deg, var(--accent-gold), var(--accent-teal)) !important;
}

/* ===== DIVIDER ===== */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent) !important;
    margin: 1.5rem 0 !important;
}

/* ===== PREDICT BUTTON ===== */
.stButton > button {
    background: linear-gradient(135deg, #F5A623 0%, #F9D423 50%, #F5A623 100%) !important;
    background-size: 200% 100% !important;
    color: #0B0F1A !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 1rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: all 0.4s ease !important;
    box-shadow: 0 4px 20px rgba(245,166,35,0.35) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    background-position: right center !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(245,166,35,0.5) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ===== SPINNER ===== */
.stSpinner > div {
    border-top-color: var(--accent-gold) !important;
}

/* ===== RESULT BOX ===== */
.result-wrap {
    animation: resultReveal 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    margin-top: 1.5rem;
}

.result-box {
    background: linear-gradient(135deg, #0B0F1A 0%, #111827 100%);
    border: 1px solid rgba(245,166,35,0.3);
    border-radius: 20px;
    padding: 32px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 50px rgba(245,166,35,0.12), 0 20px 60px rgba(0,0,0,0.5);
}

.result-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-gold), var(--accent-teal), var(--accent-gold));
    background-size: 200%;
    animation: shimmer 2s linear infinite;
}

.result-box::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 60% 40% at 50% 0%, rgba(245,166,35,0.08), transparent);
    pointer-events: none;
}

.result-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin-bottom: 8px;
}

.result-price {
    font-family: 'Playfair Display', serif;
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 800;
    background: linear-gradient(135deg, #F5A623, #F9D423, #00C9A7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin: 4px 0;
}

.result-sub {
    font-size: 14px;
    color: var(--text-muted) !important;
    margin-top: 6px;
}

.result-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0,201,167,0.12);
    border: 1px solid rgba(0,201,167,0.25);
    color: #00C9A7 !important;
    font-size: 13px;
    font-weight: 500;
    padding: 5px 14px;
    border-radius: 100px;
    margin-top: 14px;
}

/* ===== FOOTER ===== */
.footer-text {
    text-align: center;
    color: var(--text-muted) !important;
    font-size: 13px;
    letter-spacing: 0.3px;
    padding: 8px 0;
}

/* ===== KEYFRAMES ===== */
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-16px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes cardReveal {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes resultReveal {
    from { opacity: 0; transform: scale(0.92); }
    to   { opacity: 1; transform: scale(1); }
}

@keyframes shimmer {
    from { background-position: 0% center; }
    to   { background-position: 200% center; }
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
}

.live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #00C9A7;
    border-radius: 50%;
    animation: pulse-dot 1.5s ease infinite;
}

/* ===== COLUMNS SPACING ===== */
[data-testid="stHorizontalBlock"] > div {
    padding: 0 8px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# MODEL LOAD
# =========================

model = joblib.load("models/house_price_model.pkl")

# =========================
# HERO HEADER
# =========================

st.markdown("""
<div style="padding: 10px 0 8px 0;">
    <div class="hero-title">Indian House Price Predictor</div>
    <p class="hero-sub">Powered by Machine Learning &mdash; get an instant estimated valuation for any property across major Indian cities.</p>
    <div class="hero-badge"><span class="live-dot"></span> ML Model Active &nbsp;·&nbsp; 6 Cities Supported</div>
</div>
""", unsafe_allow_html=True)

st.info("💡 Fill in the property details below. Use 'Doesn't Matter' for flexible fields — the model handles it gracefully.")

st.divider()

# =========================
# THREE COLUMN LAYOUT
# =========================

col1, col2, col3 = st.columns(3)

# =========================
# COLUMN 1 — LOCATION & PROPERTY
# =========================

with col1:
    st.markdown("""
    <div class="section-card card-1">
        <div class="section-head">
            <div class="icon icon-gold">🏙️</div>
            <h3>Location &amp; Property</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    city = st.selectbox("City", ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Nagpur"])
    locality = st.selectbox("Locality Tier", ["Basic", "Mid", "Premium"])

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    bhk = st.slider("BHK", 1, 10, 2)
    bathrooms = st.slider("Bathrooms", 1, 10, 2)
    super_area = st.number_input("Super Area (sqft)", 200, value=1200)
    carpet_area = st.number_input("Carpet Area (sqft)", 100, value=900)

# =========================
# COLUMN 2 — STRUCTURE & AMENITIES
# =========================

with col2:
    st.markdown("""
    <div class="section-card card-2">
        <div class="section-head">
            <div class="icon icon-teal">🏢</div>
            <h3>Structure &amp; Amenities</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    floor_no = st.slider("Floor Number", 0, 50, 2)
    total_floors = st.slider("Total Floors", 1, 60, 10)
    property_age = st.slider("Property Age (Years)", 0, 50, 5)
    parking = st.slider("Parking Spaces", 0, 5, 1)

    furnishing = st.selectbox("Furnishing Status", ["Furnished", "Semi-Furnished", "Unfurnished"])
    lift = st.selectbox("Lift Available", ["Doesn't Matter", "Yes", "No"])
    gated = st.selectbox("Gated Society", ["Doesn't Matter", "Yes", "No"])

# =========================
# COLUMN 3 — NEARBY & ENVIRONMENT
# =========================

with col3:
    st.markdown("""
    <div class="section-card card-3">
        <div class="section-head">
            <div class="icon icon-blue">📍</div>
            <h3>Nearby &amp; Environment</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    metro_distance    = st.slider("Metro Distance (km)", 0.0, 20.0, 2.0)
    city_distance     = st.slider("City Center (km)", 0.0, 50.0, 5.0)
    school_distance   = st.slider("Nearest School (km)", 0.0, 10.0, 1.0)
    hospital_distance = st.slider("Nearest Hospital (km)", 0.0, 10.0, 1.0)
    crime_rate        = st.slider("Crime Index", 0.0, 10.0, 3.0)

# =========================
# ENCODING
# =========================

def encode(x):
    return 1 if x == "Yes" else (0 if x == "No" else 1)

lift_val  = encode(lift)
gated_val = encode(gated)

# =========================
# PREDICT BUTTON
# =========================

st.divider()

colA, colB, colC = st.columns([1, 2, 1])

with colB:
    predict = st.button("⚡  Estimate Property Price", use_container_width=True)

# =========================
# PREDICTION RESULT
# =========================

if predict:

    input_data = pd.DataFrame([{
        'City':                    city,
        'Locality_Tier':           locality,
        'BHK':                     bhk,
        'Bathrooms':               bathrooms,
        'Super_Area_sqft':         super_area,
        'Carpet_Area_sqft':        carpet_area,
        'Floor_No':                floor_no,
        'Total_Floors':            total_floors,
        'Property_Age_years':      property_age,
        'Parking':                 parking,
        'Furnishing':              furnishing,
        'Lift':                    lift_val,
        'Gated_Society':           gated_val,
        'Distance_to_Metro_km':    metro_distance,
        'Distance_to_CityCenter_km': city_distance,
        'Nearby_School_km':        school_distance,
        'Nearby_Hospital_km':      hospital_distance,
        'Crime_Rate_Index':        crime_rate
    }])

    with st.spinner("Running valuation model…"):
        time.sleep(1.2)
        prediction = model.predict(input_data)

    price_lakhs = round(prediction[0] / 100000, 2)
    price_crore = round(price_lakhs / 100, 2)

    colX, colY, colZ = st.columns([1, 2, 1])
    with colY:
        st.markdown(
            f"""
            <div class="result-wrap">
                <div class="result-box">
                    <div class="result-label">Estimated Market Value</div>
                    <div class="result-price">₹ {price_lakhs:,.2f} L</div>
                    <div class="result-sub">≈ ₹ {price_crore:,.2f} Crore &nbsp;·&nbsp; {city}, {locality} Locality</div>
                    <div class="result-pill">✦ AI-Powered Valuation</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# FOOTER
# =========================

st.markdown("---")
st.markdown(
    '<p class="footer-text">Built with Streamlit &amp; Machine Learning &nbsp;·&nbsp; Prices are estimates and may vary from actual market rates</p>',
    unsafe_allow_html=True
)
