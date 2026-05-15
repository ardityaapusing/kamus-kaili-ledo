import streamlit as st
import pandas as pd
import json
import random
from pathlib import Path
from datetime import date
from collections import Counter
import re

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kaili Ledo Dictionary",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "data" / "kamus.json"
    with open(data_path, encoding="utf-8") as f:
        raw = json.load(f)
    df = pd.DataFrame(raw)
    df["kaili_ledo"]   = df["kaili_ledo"].fillna("").str.strip()
    df["indonesia"]    = df["indonesia"].fillna("").str.strip()
    df["contoh"]       = df["contoh"].fillna("").str.strip()
    df["first_letter"] = df["kaili_ledo"].str[0].str.upper().where(df["kaili_ledo"] != "", "")
    return df

df = load_data()

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

  :root {
    --terra:        #c17f42;
    --terra-light:  #e8c898;
    --terra-dark:   #8a5a2a;
    --forest:       #2d5016;
    --forest-light: #4a7c2f;
    --earth:        #f5efe6;
    --ink:          #1a1410;
    --ink-light:    #4a3f35;
    --muted:        #9c8878;
    --card-bg:      #fdfaf6;
    --border:       #e2d5c8;
  }

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

  /* Force all main content text to be dark */
  .stApp, .stApp p, .stApp div, .stApp span, .stApp label,
  .stApp input, .stApp textarea, .stApp select,
  .stMarkdown, .stMarkdown p, .stMarkdown div {
    color: var(--ink) !important;
  }

  /* Input fields in main area — always dark text */
  .stTextInput input, .stTextArea textarea,
  section[data-testid="stMain"] input,
  section[data-testid="stMain"] textarea {
    color: var(--ink) !important;
    background: var(--card-bg) !important;
  }

  /* Tab text */
  .stTabs [data-baseweb="tab"] { color: var(--muted) !important; }
  .stTabs [aria-selected="true"] { color: var(--terra-dark) !important; }

  /* Selectbox text */
  [data-testid="stSelectbox"] div,
  [data-testid="stSelectbox"] span { color: var(--ink) !important; }

  /* Number input */
  .stNumberInput input { color: var(--ink) !important; }

  .stApp {
    background-color: var(--earth);
    background-image:
      radial-gradient(circle at 20% 50%, rgba(193,127,66,0.06) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(45,80,22,0.04) 0%, transparent 50%);
  }

  /* Sidebar — scoped separately, won't bleed out */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1410 0%, #2d1f12 100%);
    border-right: 1px solid var(--terra-dark);
  }
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] div { color: var(--earth) !important; }
  [data-testid="stSidebar"] label { color: var(--terra-light) !important; }
  [data-testid="stSidebar"] [data-baseweb="select"] {
    background: rgba(255,255,255,0.07);
    border: 1px solid var(--terra-dark);
    border-radius: 8px;
  }
  [data-testid="stSidebar"] input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid var(--terra-dark) !important;
    color: var(--earth) !important;
    border-radius: 8px !important;
  }

  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem; max-width: 1400px; }

  .word-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-left: 4px solid var(--terra);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .word-card:hover {
    border-left-color: var(--forest);
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    transform: translateY(-1px);
  }
  .word-kaili {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--terra-dark);
    margin: 0 0 0.2rem 0;
  }
  .word-meaning {
    font-size: 0.95rem;
    color: var(--ink-light);
    margin: 0 0 0.5rem 0;
    line-height: 1.5;
  }
  .word-example {
    font-size: 0.82rem;
    color: var(--muted);
    font-style: italic;
    border-left: 2px solid var(--terra-light);
    padding-left: 0.7rem;
    margin-top: 0.5rem;
    line-height: 1.6;
  }
  .word-badge {
    display: inline-block;
    background: var(--terra-light);
    color: var(--terra-dark);
    font-size: 0.68rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.4rem;
  }

  .hero-banner {
    background: linear-gradient(135deg, #1a1410 0%, #3d2410 50%, #2d5016 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: "K";
    position: absolute;
    right: -20px; top: -30px;
    font-size: 220px;
    color: rgba(255,255,255,0.03);
    font-family: 'Playfair Display', serif;
  }
  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    line-height: 1.2;
  }
  .hero-subtitle {
    color: var(--terra-light);
    font-size: 0.9rem;
    margin-top: 0.4rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
  .hero-desc {
    color: rgba(255,255,255,0.65);
    font-size: 0.9rem;
    margin-top: 1rem;
    max-width: 600px;
    line-height: 1.6;
  }

  .stat-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
  }
  .stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--terra-dark);
    line-height: 1;
  }
  .stat-label {
    font-size: 0.78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
  }

  .wotd-card {
    background: linear-gradient(135deg, var(--forest) 0%, var(--forest-light) 100%);
    border-radius: 14px;
    padding: 1.8rem;
    color: white;
    margin-bottom: 1rem;
  }
  .wotd-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.6);
    margin-bottom: 0.8rem;
  }
  .wotd-word {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
  }
  .wotd-meaning {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.85);
    margin-top: 0.5rem;
    line-height: 1.5;
  }
  .wotd-example {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.65);
    font-style: italic;
    margin-top: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.15);
    padding-top: 0.8rem;
    line-height: 1.5;
  }

  .section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--ink);
    margin: 1.2rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: 1rem;
  }

  .stTextInput input, .stTextArea textarea {
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--card-bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
  }
  .stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--terra) !important;
    box-shadow: 0 0 0 2px rgba(193,127,66,0.15) !important;
  }
  .stButton > button {
    background: var(--terra-dark) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover {
    background: var(--terra) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(138,90,42,0.3) !important;
  }

  .stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid var(--border);
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    border: none;
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    padding: 0.5rem 1.2rem;
  }
  .stTabs [aria-selected="true"] {
    background: transparent !important;
    color: var(--terra-dark) !important;
    border-bottom: 2px solid var(--terra-dark) !important;
    font-weight: 600 !important;
  }

  .info-box {
    background: rgba(193,127,66,0.08);
    border: 1px solid var(--terra-light);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: var(--ink-light);
    margin: 0.5rem 0;
  }

  .result-count {
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 0.8rem;
    display: inline-block;
    background: var(--card-bg);
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid var(--border);
  }

  hr { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
      <div style="font-size:2.5rem;">📖</div>
      <div style="font-family:'Playfair Display',serif; font-size:1.1rem; color:#e8c898; font-weight:700;">
        Kaili Ledo Dictionary
      </div>
      <div style="font-size:0.72rem; color:rgba(255,255,255,0.4); letter-spacing:0.12em; text-transform:uppercase; margin-top:0.2rem;">
        Digital Preservation Project
      </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        ["🏠 Home", "🔍 Search", "📚 Browse", "➕ Add Word", "📊 Statistics", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.75rem; color:rgba(255,255,255,0.35); text-align:center; line-height:1.8;">
      Total Entries: <span style="color:#e8c898; font-weight:600;">{len(df):,}</span><br>
      Source: Kamus Kaili-Ledo<br>
      Author: Donna Evans (2003)<br>
      SIL International
    </div>
    """, unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def render_word_card(row, highlight_query=""):
    kaili   = row["kaili_ledo"]
    meaning = row["indonesia"]
    example = row["contoh"]

    if highlight_query:
        q       = re.escape(highlight_query)
        kaili   = re.sub(f"({q})", r'<mark style="background:#e8c898;border-radius:3px;">\1</mark>', kaili,   flags=re.I)
        meaning = re.sub(f"({q})", r'<mark style="background:#e8c898;border-radius:3px;">\1</mark>', meaning, flags=re.I)

    example_html = f'<div class="word-example">📝 {example}</div>' if example else ""
    st.markdown(f"""
    <div class="word-card">
      <div class="word-kaili">{kaili}</div>
      <div class="word-meaning">{meaning}</div>
      {example_html}
    </div>
    """, unsafe_allow_html=True)


def get_word_of_the_day():
    seed = date.today().toordinal()
    pool = df[(df["kaili_ledo"] != "") & (df["contoh"] != "")]
    if pool.empty:
        pool = df[df["kaili_ledo"] != ""]
    return pool.iloc[seed % len(pool)]


# ═══════════════════════════════════════════════════════════════════════════════
#  HOME
# ═══════════════════════════════════════════════════════════════════════════════
if menu == "🏠 Home":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-subtitle">🌿 Regional Language of Central Sulawesi, Indonesia</div>
      <div class="hero-title">Kaili Ledo<br>Digital Dictionary</div>
      <div class="hero-desc">
        A language preservation initiative for Kaili Ledo — the mother tongue of the Kaili
        people in the Palu Valley, Central Sulawesi. Entries are drawn from conversations,
        oral stories, and written texts of the local community.
      </div>
    </div>
    """, unsafe_allow_html=True)

    has_example  = (df["contoh"] != "").sum()
    letters_used = df[df["kaili_ledo"] != ""]["first_letter"].nunique()
    pct          = round(has_example / len(df) * 100)

    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in [
        (c1, len(df),        "Total Entries"),
        (c2, has_example,    "With Example Sentences"),
        (c3, letters_used,   "Starting Letters"),
        (c4, f"{pct}%",      "Example Coverage"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-number">{num}</div>
              <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-title">✨ Word of the Day</div>', unsafe_allow_html=True)
        wotd         = get_word_of_the_day()
        example_html = f'<div class="wotd-example">📝 {wotd["contoh"]}</div>' if wotd["contoh"] else ""
        st.markdown(f"""
        <div class="wotd-card">
          <div class="wotd-label">Word of the Day — {date.today().strftime("%B %d, %Y")}</div>
          <div class="wotd-word">{wotd["kaili_ledo"]}</div>
          <div class="wotd-meaning">{wotd["indonesia"]}</div>
          {example_html}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">🎲 Random Word</div>', unsafe_allow_html=True)
        if st.button("Show a Random Word", use_container_width=True):
            render_word_card(df[df["kaili_ledo"] != ""].sample(1).iloc[0])

    with col_right:
        st.markdown('<div class="section-title">📋 Recent Entries</div>', unsafe_allow_html=True)
        for _, row in df[df["kaili_ledo"] != ""].tail(8).iloc[::-1].iterrows():
            render_word_card(row)


# ═══════════════════════════════════════════════════════════════════════════════
#  SEARCH
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "🔍 Search":
    st.markdown('<div class="section-title">🔍 Search the Dictionary</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Kaili Ledo → Indonesian", "Indonesian → Kaili Ledo"])

    with tab1:
        query = st.text_input("Enter a Kaili Ledo word", placeholder="e.g. Nangala, Baju, Ada…")
        if query:
            results = df[df["kaili_ledo"].str.contains(query, case=False, na=False)]
            st.markdown(f'<span class="result-count">{len(results)} result(s) found</span>', unsafe_allow_html=True)
            if results.empty:
                st.info("No entries found. Try a different spelling or keyword.")
            else:
                for _, row in results.iterrows():
                    render_word_card(row, highlight_query=query)

    with tab2:
        query_id = st.text_input("Enter an Indonesian word or meaning", placeholder="e.g. Mengambil, Agama, Dagu…")
        if query_id:
            results = df[df["indonesia"].str.contains(query_id, case=False, na=False)]
            st.markdown(f'<span class="result-count">{len(results)} result(s) found</span>', unsafe_allow_html=True)
            if results.empty:
                st.info("No entries found. Try a synonym or related term.")
            else:
                for _, row in results.iterrows():
                    render_word_card(row, highlight_query=query_id)


# ═══════════════════════════════════════════════════════════════════════════════
#  BROWSE
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "📚 Browse":
    st.markdown('<div class="section-title">📚 Browse by Starting Letter</div>', unsafe_allow_html=True)

    available_letters = sorted(df[df["kaili_ledo"] != ""]["first_letter"].dropna().unique())

    selected_letter = st.selectbox(
        "Choose a starting letter",
        options=["All"] + available_letters,
        format_func=lambda x: f"Letter  {x}" if x != "All" else "📖 Show All Entries"
    )

    filtered = (
        df[df["kaili_ledo"] != ""].sort_values("kaili_ledo")
        if selected_letter == "All"
        else df[df["first_letter"] == selected_letter].sort_values("kaili_ledo")
    )

    st.markdown(f'<span class="result-count">{len(filtered)} entries</span>', unsafe_allow_html=True)

    PAGE_SIZE   = 20
    total_pages = max(1, (len(filtered) - 1) // PAGE_SIZE + 1)
    page        = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    start       = (page - 1) * PAGE_SIZE

    for _, row in filtered.iloc[start : start + PAGE_SIZE].iterrows():
        render_word_card(row)

    if total_pages > 1:
        st.markdown(
            f'<div style="text-align:center;color:var(--muted);font-size:0.82rem;">Page {page} of {total_pages}</div>',
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  ADD WORD
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "➕ Add Word":
    st.markdown('<div class="section-title">➕ Contribute a New Word</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
      💡 Help preserve the Kaili Ledo language by contributing new words.
      Every entry matters for keeping this language alive for future generations.
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_word_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_kaili   = st.text_input("Kaili Ledo Word *", placeholder="e.g. Nobose")
        with col2:
            new_meaning = st.text_input("Indonesian Meaning *", placeholder="e.g. Berenang (Swimming)")

        new_example = st.text_area(
            "Example Sentence (optional)",
            placeholder="Provide an example sentence in Kaili Ledo with its Indonesian translation…",
            height=100
        )
        submitted = st.form_submit_button("💾 Save Word", use_container_width=True)

    if submitted:
        if not new_kaili.strip() or not new_meaning.strip():
            st.error("⚠️ Both the Kaili Ledo word and its Indonesian meaning are required.")
        else:
            dup = df[df["kaili_ledo"].str.lower() == new_kaili.strip().lower()]
            if not dup.empty:
                st.warning(f"⚠️ **{new_kaili}** already exists with meaning: _{dup.iloc[0]['indonesia']}_")
            else:
                new_id    = int(df["id"].max()) + 1
                new_entry = {
                    "id":         new_id,
                    "kaili_ledo": new_kaili.strip(),
                    "indonesia":  new_meaning.strip(),
                    "contoh":     new_example.strip(),
                }
                data_path = Path(__file__).parent / "data" / "kamus.json"
                with open(data_path, encoding="utf-8") as f:
                    all_data = json.load(f)
                all_data.append(new_entry)
                with open(data_path, "w", encoding="utf-8") as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)

                import csv
                csv_path = Path(__file__).parent / "data" / "kamus.csv"
                with open(csv_path, "a", encoding="utf-8", newline="") as f:
                    csv.writer(f).writerow([new_id, new_kaili.strip(), new_meaning.strip(), new_example.strip()])

                st.success(f"✅ **{new_kaili}** has been successfully added to the dictionary!")
                st.cache_data.clear()
                example_html = f"<div class='word-example'>📝 {new_example}</div>" if new_example else ""
                st.markdown(f"""
                <div class="word-card">
                  <div class="word-badge">Newly Added</div>
                  <div class="word-kaili">{new_kaili}</div>
                  <div class="word-meaning">{new_meaning}</div>
                  {example_html}
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📋 Last 5 Entries in Database</div>', unsafe_allow_html=True)
    for _, row in df.tail(5).iloc[::-1].iterrows():
        render_word_card(row)


# ═══════════════════════════════════════════════════════════════════════════════
#  STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "📊 Statistics":
    st.markdown('<div class="section-title">📊 Dictionary Statistics</div>', unsafe_allow_html=True)

    import plotly.express as px
    import plotly.graph_objects as go

    C = dict(terra="#c17f42", forest="#2d5016", terra_dark="#8a5a2a",
             terra_light="#e8c898", forest_light="#4a7c2f", ink="#1a1410", bg="#fdfaf6")

    letter_counts = (
        df[df["kaili_ledo"] != ""]
        .groupby("first_letter").size()
        .reset_index(name="count")
        .sort_values("first_letter")
    )
    fig1 = px.bar(
        letter_counts, x="first_letter", y="count",
        title="Word Count by Starting Letter",
        color="count",
        color_continuous_scale=[C["terra_light"], C["terra"], C["terra_dark"], C["forest"]],
        labels={"first_letter": "Starting Letter", "count": "Number of Words"},
    )
    fig1.update_layout(
        font_family="DM Sans", plot_bgcolor=C["bg"], paper_bgcolor=C["bg"],
        coloraxis_showscale=False, title_font_size=15,
        title_font_color=C["ink"], margin=dict(t=50, b=20, l=20, r=20),
    )
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        has_ex = (df["contoh"] != "").sum()
        no_ex  = len(df) - has_ex
        fig2   = go.Figure(go.Pie(
            labels=["Has Example", "No Example"],
            values=[has_ex, no_ex],
            hole=0.55,
            marker_colors=[C["forest"], C["terra_light"]],
            textinfo="percent+label",
            textfont_size=12,
        ))
        fig2.update_layout(
            title="Example Sentence Coverage",
            font_family="DM Sans", plot_bgcolor=C["bg"], paper_bgcolor=C["bg"],
            title_font_size=15, showlegend=False, margin=dict(t=50, b=20, l=20, r=20),
            annotations=[dict(text=f"{round(has_ex/len(df)*100)}%", x=0.5, y=0.5,
                              font_size=22, font_color=C["forest"], showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        df_v = df[df["kaili_ledo"] != ""].copy()
        df_v["def_len"] = df_v["indonesia"].str.len()
        df_v["bucket"]  = pd.cut(
            df_v["def_len"],
            bins=[0, 20, 50, 100, 200, 999],
            labels=["Very Short", "Short", "Medium", "Long", "Very Long"]
        )
        bucket_counts = df_v["bucket"].value_counts().reset_index()
        bucket_counts.columns = ["definition_length", "count"]
        fig3 = px.bar(
            bucket_counts, x="definition_length", y="count",
            title="Definition Length Distribution",
            color="definition_length",
            color_discrete_sequence=[C["terra_light"], C["terra"], C["terra_dark"],
                                     C["forest_light"], C["forest"]],
            labels={"definition_length": "Definition Length", "count": "Number of Words"},
        )
        fig3.update_layout(
            font_family="DM Sans", plot_bgcolor=C["bg"], paper_bgcolor=C["bg"],
            showlegend=False, title_font_size=15, margin=dict(t=50, b=20, l=20, r=20),
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">📝 Entries with the Longest Definitions</div>', unsafe_allow_html=True)
    df_v["def_len"] = df_v["indonesia"].str.len()
    for _, row in df_v.nlargest(5, "def_len").iterrows():
        render_word_card(row)


# ═══════════════════════════════════════════════════════════════════════════════
#  ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "ℹ️ About":
    st.markdown('<div class="section-title">ℹ️ About This Project</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="word-card" style="border-left-color: var(--forest);">
      <div class="word-kaili" style="color: var(--forest);">The Kaili Ledo Language</div>
      <div class="word-meaning">
        Kaili Ledo is one of the dialects spoken by the Kaili people in the Palu Valley,
        Central Sulawesi, Indonesia. It serves as a regional lingua franca and is part of
        the Austronesian language family. Like many regional languages, it faces challenges
        from language shift toward national and global languages.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">📖 Dictionary Source</div>
          <div class="word-meaning">
            Based on the <strong>Kamus Kaili-Ledo Indonesia Inggris</strong> (First Edition, 2003),
            compiled by <strong>Donna Evans</strong> and published by the Department of Culture
            and Tourism of Central Sulawesi Province in collaboration with <strong>SIL International</strong>.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">🎯 Project Goal</div>
          <div class="word-meaning">
            Built as a language preservation effort, making Kaili Ledo accessible to younger
            generations, researchers, and the general public. Started from a Microsoft Access
            database of ~500 selected words, designed to grow through community contributions.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">⚙️ Tech Stack</div>
          <div class="word-meaning">
            <ul style="padding-left:1rem; margin:0; line-height:2.2;">
              <li><strong>Framework:</strong> Python + Streamlit</li>
              <li><strong>Data:</strong> JSON + CSV (migrated from MS Access)</li>
              <li><strong>Charts:</strong> Plotly Express</li>
              <li><strong>Hosting:</strong> Streamlit Community Cloud</li>
              <li><strong>Version Control:</strong> GitHub</li>
            </ul>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">🚀 How to Deploy</div>
          <div class="word-meaning">
            <ol style="padding-left:1rem; margin:0; line-height:2.2; font-size:0.88rem;">
              <li>Push all files to a new GitHub repository</li>
              <li>Go to <strong>share.streamlit.io</strong></li>
              <li>Connect your GitHub account</li>
              <li>Select the repository and <code>app.py</code></li>
              <li>Click <strong>Deploy</strong> — live in minutes! 🎉</li>
            </ol>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
      🤝 <strong>Contribute:</strong> Add new words via the <em>Add Word</em> menu.
      Every contribution helps preserve Kaili Ledo as a living language for future generations.
    </div>
    """, unsafe_allow_html=True)
