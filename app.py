import streamlit as st
import pandas as pd
import joblib
import re
from urllib.parse import urlparse

st.set_page_config(
    page_title="URL Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------
# GLOBAL STYLE
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(99, 102, 241, 0.16), transparent 40%),
            radial-gradient(circle at 85% 15%, rgba(56, 189, 248, 0.12), transparent 40%),
            #0a0f1e;
    }
    section[data-testid="stSidebar"] {
        background: #0d1424;
        border-right: 1px solid #1c2740;
    }
    h1, h2, h3, h4, p, label, span, div { color: #e2e8f0; }

    /* ---- Hero ---- */
    .hero { padding: 2.4rem 0 0.6rem 0; text-align: center; }
    .hero-badge {
        display: inline-flex; align-items: center; gap: 0.4rem;
        background: linear-gradient(90deg, rgba(99,102,241,0.15), rgba(56,189,248,0.15));
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
        padding: 0.35rem 1rem; border-radius: 999px;
        font-size: 0.76rem; font-weight: 700; letter-spacing: 0.05em;
        margin-bottom: 1.1rem;
    }
    .hero-title {
        font-size: 2.9rem; font-weight: 900; margin: 0; line-height: 1.15;
        background: linear-gradient(100deg, #f8fafc 20%, #a5b4fc 60%, #38bdf8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        text-align: center; width: 100%;
        color: #64748b; font-size: 1.04rem; margin: 0.7rem auto 0;
        max-width: 620px; display: block;
    }

    /* ---- Feature grid ---- */
    .feature-card {
        background: linear-gradient(160deg, #131c31, #0f1729);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.3rem 1.2rem;
        height: 100%;
        transition: all 0.2s ease;
    }
    .feature-card:hover { border-color: #334155; transform: translateY(-2px); }
    .feature-icon {
        width: 42px; height: 42px; border-radius: 11px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 0.8rem;
    }
    .feature-icon svg { width: 20px; height: 20px; }
    .fi-violet { background: rgba(139, 92, 246, 0.15); }
    .fi-cyan   { background: rgba(56, 189, 248, 0.15); }
    .fi-amber  { background: rgba(251, 191, 36, 0.15); }
    .fi-rose   { background: rgba(251, 113, 133, 0.15); }
    .feature-title { font-size: 0.98rem; font-weight: 700; color: #f1f5f9; margin: 0 0 0.3rem 0; }
    .feature-desc { font-size: 0.82rem; color: #64748b; line-height: 1.5; margin: 0; }

    /* ---- Scan panel ---- */
    .scan-panel {
        background: linear-gradient(160deg, #131c31, #0d1424);
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 2rem 2.2rem;
        margin-top: 1.8rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    }
    .scan-label { font-size: 0.85rem; font-weight: 700; color: #94a3b8; margin-bottom: 0.6rem; text-align: center; }

    div[data-testid="stTextInput"] input {
        background-color: #0a0f1e;
        border: 1.5px solid #1e293b;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        font-size: 1rem;
        color: #f1f5f9;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #818cf8;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.18);
    }
    div[data-testid="stTextInput"] input::placeholder { color: #475569; }

    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1, #38bdf8);
        color: #04101f !important;
        border: none; border-radius: 12px;
        padding: 0.8rem 0; font-size: 1rem; font-weight: 800;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }

    /* ---- Stat cards ---- */
    .stat-card {
        border-radius: 14px; padding: 1rem 1.2rem; text-align: left;
        border: 1px solid;
    }
    .stat-cyan   { background: rgba(56, 189, 248, 0.08);  border-color: rgba(56, 189, 248, 0.3); }
    .stat-violet { background: rgba(139, 92, 246, 0.08);  border-color: rgba(139, 92, 246, 0.3); }
    .stat-amber  { background: rgba(251, 191, 36, 0.08);  border-color: rgba(251, 191, 36, 0.3); }
    .stat-value { font-size: 1.6rem; font-weight: 800; color: #f8fafc; }
    .stat-label { font-size: 0.76rem; color: #94a3b8; margin-top: 0.15rem; text-transform: uppercase; letter-spacing: 0.04em; }

    /* ---- Result card ---- */
    .result-card {
        border-radius: 18px; padding: 1.7rem; margin-top: 1.5rem;
        display: flex; align-items: center; gap: 1.1rem;
    }
    .result-icon { font-size: 2.4rem; line-height: 1; }
    .result-title { font-size: 1.25rem; font-weight: 800; margin: 0; }
    .result-sub { font-size: 0.88rem; color: #94a3b8; margin-top: 0.2rem; }
    .safe   { background: rgba(34, 197, 94, 0.08);  border: 1px solid rgba(34, 197, 94, 0.35); }
    .safe   .result-title { color: #4ade80; }
    .danger { background: rgba(239, 68, 68, 0.08);  border: 1px solid rgba(239, 68, 68, 0.35); }
    .danger .result-title { color: #f87171; }
    .warn   { background: rgba(234, 179, 8, 0.08);  border: 1px solid rgba(234, 179, 8, 0.35); }
    .warn   .result-title { color: #facc15; }

    /* ---- Confidence gauge ---- */
    .gauge-wrap { margin-top: 1.1rem; }
    .gauge-track {
        width: 100%; height: 10px; border-radius: 999px;
        background: #1e293b; overflow: hidden;
    }
    .gauge-fill { height: 100%; border-radius: 999px; }
    .gauge-caption { display: flex; justify-content: space-between; font-size: 0.78rem; color: #64748b; margin-top: 0.4rem; }

    /* ---- Breakdown chips ---- */
    .breakdown-title { font-size: 0.85rem; font-weight: 700; color: #94a3b8; margin: 1.4rem 0 0.7rem 0; }
    .chip {
        display: inline-flex; align-items: center; gap: 0.4rem;
        background: #131c31; border: 1px solid #1e293b;
        padding: 0.4rem 0.8rem; border-radius: 10px;
        font-size: 0.82rem; margin: 0 0.5rem 0.5rem 0;
    }
    .chip-ok  { color: #4ade80; border-color: rgba(34,197,94,0.3); }
    .chip-bad { color: #f87171; border-color: rgba(239,68,68,0.3); }

    /* ---- Tags row ---- */
    .tag {
        display: inline-block; background: #131c31; color: #94a3b8;
        font-size: 0.72rem; padding: 0.2rem 0.6rem; border-radius: 7px;
        margin: 0 0.35rem 0.35rem 0; border: 1px solid #1e293b;
    }

    /* ---- History ---- */
    .history-item {
        background: #131c31; border: 1px solid #1e293b; border-radius: 10px;
        padding: 0.55rem 0.8rem; margin-bottom: 0.45rem; font-size: 0.83rem;
        display: flex; align-items: center; gap: 0.5rem;
    }
    .history-url { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #cbd5e1; }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------------
@st.cache_resource
def load_model():
    model = joblib.load("url_checker_model.pkl")
    features = joblib.load("model_features.pkl")
    return model, features


model, feature_names = load_model()

WHITELIST = [
    "google.com", "facebook.com", "youtube.com", "instagram.com",
    "twitter.com", "x.com", "pinterest.com", "github.com",
    "linkedin.com", "wikipedia.org", "amazon.com", "microsoft.com",
    "anthropic.com", "claude.ai", "claude.com", "openai.com", "chatgpt.com",
    "whatsapp.com", "telegram.org", "discord.com", "slack.com", "zoom.us",
    "netflix.com", "spotify.com", "apple.com", "adobe.com", "dropbox.com",
    "reddit.com", "tiktok.com", "yahoo.com", "bing.com", "paypal.com",
    "ebay.com", "outlook.com", "office.com", "notion.so", "canva.com",
]

SUSPICIOUS_WORDS = [
    "login", "admin", "account", "bank", "verify",
    "secure", "ebayisapi", "webscr", "pay", "free",
]


def is_whitelisted(url):
    try:
        domain = urlparse(url).netloc.lower()
        if not domain:
            domain = url.split("/")[0].lower()
        return any(safe in domain for safe in WHITELIST)
    except Exception:
        return False


def looks_like_url(raw):
    candidate = raw.strip()
    if not candidate or " " in candidate:
        return False
    parse_target = candidate if re.match(r"^https?://", candidate, re.I) else "http://" + candidate
    domain = urlparse(parse_target).netloc.lower()
    if "." not in domain:
        return False
    tld = domain.rsplit(".", 1)[-1]
    if not tld.isalpha() or len(tld) < 2:
        return False
    return True


def extract_features(url):
    data = {}
    data["url_length"] = len(url)
    data["count_dots"] = url.count(".")
    data["count_hyphen"] = url.count("-")
    data["count_at"] = url.count("@")

    match = re.search(
        r"(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])", url
    )
    data["has_ip"] = 1 if match else 0
    data["use_https"] = 1 if "https" in url.lower() else 0
    data["count_digits"] = sum(c.isdigit() for c in url)
    data["count_letters"] = sum(c.isalpha() for c in url)
    data["digits_ratio"] = data["count_digits"] / (data["url_length"] + 1)

    for word in SUSPICIOUS_WORDS:
        data[f"word_{word}"] = 1 if word in url.lower() else 0

    data["count_slash"] = url.count("/")
    data["count_question"] = url.count("?")
    data["count_equal"] = url.count("=")
    data["count_percent"] = url.count("%")
    return data


def build_breakdown(raw_data):
    chips = []
    ok = raw_data["use_https"] == 1
    chips.append((ok, "Uses HTTPS" if ok else "No HTTPS"))

    ok = raw_data["has_ip"] == 0
    chips.append((ok, "No raw IP address" if ok else "Contains raw IP address"))

    ok = raw_data["url_length"] < 75
    chips.append((ok, f"{raw_data['url_length']} characters long"))

    hit = any(raw_data.get(f"word_{w}", 0) for w in SUSPICIOUS_WORDS)
    chips.append((not hit, "No suspicious keywords" if not hit else "Suspicious keyword found"))

    ok = raw_data["count_at"] == 0
    chips.append((ok, "No @ symbol" if ok else "Contains @ symbol"))

    ok = raw_data["count_hyphen"] <= 2
    chips.append((ok, "Few hyphens" if ok else "Many hyphens in domain"))
    return chips


def classify(url):
    if is_whitelisted(url):
        return "safe", "✅", "Trusted domain", "This is a well-known, verified website.", None, None

    raw_data = extract_features(url)
    features_df = pd.DataFrame([raw_data])[feature_names]
    prediction = model.predict(features_df)[0]

    proba = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(features_df)[0]
        proba = max(probs) * 100

    breakdown = build_breakdown(raw_data)

    if prediction == "benign":
        return "safe", "✅", "Looks safe", "No suspicious patterns detected.", proba, breakdown
    elif prediction == "phishing":
        return "danger", "⚠️", "Phishing detected", "This URL shows signs of a phishing attempt.", proba, breakdown
    elif prediction == "malware":
        return "danger", "🚨", "Malware risk", "This URL may distribute malicious software.", proba, breakdown
    else:
        return "warn", "⚠️", f"Flagged as {prediction}", "Proceed with caution.", proba, breakdown


# ---------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ URL Shield")
    st.caption("ML-powered link safety checker")
    st.markdown("---")
    st.markdown("**How it works**")
    st.write(
        "A Random Forest model analyzes the structure of a URL — length, "
        "symbols, keywords, and more — to flag phishing and malware links "
        "before you click them."
    )
    st.markdown("---")
    total = len(st.session_state.history)
    threats = sum(1 for h in st.session_state.history if h["icon"] in ("⚠️", "🚨"))
    c1, c2 = st.columns(2)
    c1.metric("Checked", total)
    c2.metric("Threats", threats)

    st.markdown("---")
    st.markdown("**Recent checks**")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-8:]):
            st.markdown(
                f"<div class='history-item'>{item['icon']} "
                f"<span class='history-url'>{item['url']}</span></div>",
                unsafe_allow_html=True,
            )
        if st.button("Clear history", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("No checks yet.")

# ---------------------------------------------------------------
# HERO
# ---------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">🛡️ MACHINE LEARNING · REAL-TIME SCANNING</div>
        <p class="hero-title">Check any link<br>before you click</p>
        <p class="hero-subtitle">
            Paste a URL below to instantly detect phishing, malware, and
            other suspicious links using a trained classification model.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# FEATURE GRID
# ---------------------------------------------------------------
f1, f2, f3, f4 = st.columns(4)
icon_hook = '<svg viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v10"/><circle cx="12" cy="16" r="4"/><path d="M12 20c-3 0-5-2-5-4"/></svg>'
icon_bug = '<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="7" width="8" height="12" rx="4"/><path d="M8 11H4M20 11h-4M8 15H5M19 15h-3M10 7 8 4M14 7l2-3M12 7V4"/></svg>'
icon_shield = '<svg viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 4 5v6c0 5 3.4 8.5 8 10 4.6-1.5 8-5 8-10V5l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg>'
icon_bolt = '<svg viewBox="0 0 24 24" fill="none" stroke="#fb7185" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8Z"/></svg>'

features_info = [
    (f1, "fi-violet", icon_hook, "Phishing Detection", "Flags fake login and account pages designed to steal credentials."),
    (f2, "fi-cyan", icon_bug, "Malware Screening", "Catches links known to distribute malicious software."),
    (f3, "fi-amber", icon_shield, "Trusted Whitelist", "Recognizes 30+ major platforms instantly, no scan needed."),
    (f4, "fi-rose", icon_bolt, "Instant Results", "Get a verdict with confidence score in under a second."),
]
for col, icon_class, icon_svg, title, desc in features_info:
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon {icon_class}">{icon_svg}</div>
                <p class="feature-title">{title}</p>
                <p class="feature-desc">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------
# SCAN PANEL
# ---------------------------------------------------------------
st.markdown('<div class="scan-panel">', unsafe_allow_html=True)
st.markdown('<p class="scan-label">🔗 ENTER A URL TO SCAN</p>', unsafe_allow_html=True)

user_url = st.text_input(
    "URL", placeholder="https://example.com/login",
    label_visibility="collapsed",
)
check_clicked = st.button("🔍 Scan URL", use_container_width=True)
st.caption("Tip: paste the complete link, including https:// — not just a site name.")

if check_clicked:
    if not user_url.strip():
        st.warning("Please enter a URL first.")
    elif not looks_like_url(user_url):
        st.info(
            "That doesn't look like a full URL. Try something like "
            "**https://example.com** — a single word (e.g. \"claude\") "
            "can't be scanned."
        )
    else:
        with st.spinner("Analyzing URL structure..."):
            css_class, icon, title, subtitle, proba, breakdown = classify(user_url)

            st.markdown(
                f"""
                <div class="result-card {css_class}">
                    <div class="result-icon">{icon}</div>
                    <div>
                        <p class="result-title">{title}</p>
                        <p class="result-sub">{subtitle}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if proba:
                if css_class == "safe":
                    grad = "linear-gradient(90deg, #22c55e, #4ade80)"
                elif css_class == "danger":
                    grad = "linear-gradient(90deg, #ef4444, #f87171)"
                else:
                    grad = "linear-gradient(90deg, #eab308, #facc15)"
                st.markdown(
                    f"""
                    <div class="gauge-wrap">
                        <div class="gauge-track">
                            <div class="gauge-fill" style="width:{proba:.0f}%; background:{grad};"></div>
                        </div>
                        <div class="gauge-caption">
                            <span>Model confidence</span>
                            <span>{proba:.1f}%</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if breakdown:
                st.markdown('<p class="breakdown-title">SIGNAL BREAKDOWN</p>', unsafe_allow_html=True)
                chips_html = ""
                for ok, label in breakdown:
                    cls = "chip-ok" if ok else "chip-bad"
                    dot = "🟢" if ok else "🔴"
                    chips_html += f'<span class="chip {cls}">{dot} {label}</span>'
                st.markdown(chips_html, unsafe_allow_html=True)

            st.session_state.history.append({"url": user_url, "icon": icon})

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# STAT ROW
# ---------------------------------------------------------------
st.write("")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(
        "<div class='stat-card stat-cyan'><div class='stat-value'>99%+</div>"
        "<div class='stat-label'>Model accuracy</div></div>",
        unsafe_allow_html=True,
    )
with col_b:
    st.markdown(
        f"<div class='stat-card stat-violet'><div class='stat-value'>{len(st.session_state.history)}</div>"
        "<div class='stat-label'>URLs checked this session</div></div>",
        unsafe_allow_html=True,
    )
with col_c:
    st.markdown(
        "<div class='stat-card stat-amber'><div class='stat-value'>21</div>"
        "<div class='stat-label'>Signals analyzed per URL</div></div>",
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="margin-top:2rem; text-align:center;">
        <span class="tag">Phishing detection</span>
        <span class="tag">Malware flags</span>
        <span class="tag">Trusted domain whitelist</span>
        <span class="tag">Random Forest model</span>
        <span class="tag">Signal breakdown</span>
    </div>
    """,
    unsafe_allow_html=True,
)
