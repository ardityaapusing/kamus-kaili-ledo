import streamlit as st
import pandas as pd
import json
import re
from pathlib import Path
from datetime import date

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kaili Ledo Dictionary",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",   # sidebar not used anymore
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

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

/* Hide sidebar toggle button completely */
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"]  { display: none !important; }

.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── App background ── */
.stApp {
  background-color: #f5efe6;
  background-image:
    radial-gradient(circle at 15% 50%, rgba(193,127,66,.07) 0%, transparent 45%),
    radial-gradient(circle at 85% 15%, rgba(45,80,22,.05)  0%, transparent 45%);
}

/* ── Top navbar ── */
.topnav {
  background: linear-gradient(135deg, #1a1410 0%, #2d1f12 60%, #1e2d10 100%);
  padding: .85rem 2.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(193,127,66,.3);
  position: sticky;
  top: 0;
  z-index: 999;
}
.topnav-brand {
  display: flex;
  align-items: center;
  gap: .75rem;
}
.topnav-logo { font-size: 1.6rem; line-height: 1; }
.topnav-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #e8c898;
  line-height: 1.2;
}
.topnav-sub {
  font-size: .62rem;
  color: rgba(255,255,255,.38);
  text-transform: uppercase;
  letter-spacing: .1em;
}
.topnav-count {
  font-size: .75rem;
  color: rgba(255,255,255,.38);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 20px;
  padding: 3px 12px;
}
.topnav-count span { color: #e8c898; font-weight: 600; }

/* ── Page wrapper ── */
.page-wrap {
  max-width: 1380px;
  margin: 0 auto;
  padding: 1.5rem 2rem 3rem;
}

/* ── Streamlit tab navigation (main nav) ── */
.stTabs [data-baseweb="tab-list"] {
  background: #1a1410 !important;
  gap: 0 !important;
  border-bottom: none !important;
  padding: 0 2.5rem;
  overflow-x: auto;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-bottom: 3px solid transparent !important;
  color: rgba(255,255,255,.45) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: .84rem !important;
  font-weight: 500 !important;
  padding: .75rem 1.3rem !important;
  transition: color .2s, border-color .2s !important;
  white-space: nowrap;
}
.stTabs [data-baseweb="tab"]:hover {
  color: #e8c898 !important;
}
.stTabs [aria-selected="true"] {
  color: #e8c898 !important;
  border-bottom: 3px solid #c17f42 !important;
  font-weight: 600 !important;
}
/* Tab content area */
.stTabs [data-baseweb="tab-panel"] {
  padding: 0 !important;
}

/* ── Streamlit native widgets ── */
.stTextInput  label,
.stTextArea   label,
.stSelectbox  label,
.stNumberInput label,
[data-testid="stWidgetLabel"] {
  color: #4a3f35 !important;
  font-size: .85rem !important;
  font-weight: 500 !important;
}
.stTextInput  input,
.stTextArea   textarea,
.stNumberInput input {
  color: #1a1410 !important;
  background: #fdfaf6 !important;
  border: 1.5px solid #e2d5c8 !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput  input:focus,
.stTextArea   textarea:focus,
.stNumberInput input:focus {
  border-color: #c17f42 !important;
  box-shadow: 0 0 0 3px rgba(193,127,66,.12) !important;
  outline: none !important;
}
.stTextInput  input::placeholder,
.stTextArea   textarea::placeholder {
  color: #b0a090 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] {
  background: #fdfaf6 !important;
  border-color: #e2d5c8 !important;
  border-radius: 10px !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stSelectbox"] span {
  color: #1a1410 !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── Buttons ── */
.stButton > button {
  background: #8a5a2a !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  padding: .55rem 1.6rem !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: .88rem !important;
  font-weight: 500 !important;
  transition: background .2s, transform .15s, box-shadow .2s !important;
}
.stButton > button:hover {
  background: #c17f42 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 18px rgba(138,90,42,.28) !important;
}
.stFormSubmitButton > button {
  background: #2d5016 !important;
  color: #fff !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  transition: background .2s, transform .15s !important;
}
.stFormSubmitButton > button:hover {
  background: #4a7c2f !important;
  transform: translateY(-2px) !important;
}

/* ── Custom HTML components ── */
.word-card {
  background: #fdfaf6;
  border: 1px solid #e2d5c8;
  border-left: 4px solid #c17f42;
  border-radius: 12px;
  padding: 1.1rem 1.4rem;
  margin-bottom: .75rem;
  transition: border-left-color .2s, box-shadow .2s, transform .2s;
  box-shadow: 0 1px 6px rgba(0,0,0,.04);
}
.word-card:hover {
  border-left-color: #2d5016;
  box-shadow: 0 4px 18px rgba(0,0,0,.09);
  transform: translateY(-2px);
}
.word-kaili {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #7a4f26;
  margin: 0 0 .18rem 0;
  line-height: 1.3;
}
.word-meaning {
  font-size: .93rem;
  color: #3d342c;
  margin: 0 0 .3rem 0;
  line-height: 1.55;
}
.word-example {
  font-size: .8rem;
  color: #8a7a6e;
  font-style: italic;
  border-left: 2px solid #e8c898;
  padding-left: .7rem;
  margin-top: .45rem;
  line-height: 1.6;
}
.word-badge {
  display: inline-block;
  background: #f0ddb0;
  color: #7a4f26;
  font-size: .64rem;
  font-weight: 700;
  padding: 2px 9px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: .06em;
  margin-bottom: .35rem;
}

.hero-banner {
  background: linear-gradient(135deg, #1a1410 0%, #3d2410 45%, #2d5016 100%);
  border-radius: 16px;
  padding: 2.8rem 3.2rem;
  margin-bottom: 1.6rem;
  position: relative;
  overflow: hidden;
}
.hero-banner::before {
  content: "K";
  position: absolute; right: -10px; top: -40px;
  font-size: 240px; color: rgba(255,255,255,.035);
  font-family: 'Playfair Display', serif; line-height: 1;
}
.hero-tag   { color: #e8c898; font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .7rem; }
.hero-title { font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 700; color: #fff; margin: 0; line-height: 1.15; }
.hero-desc  { color: rgba(255,255,255,.62); font-size: .88rem; margin-top: .9rem; max-width: 580px; line-height: 1.7; }

.stat-card   { background: #fdfaf6; border: 1px solid #e2d5c8; border-radius: 12px; padding: 1.25rem 1rem; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,.03); }
.stat-number { font-family: 'Playfair Display', serif; font-size: 2.1rem; font-weight: 700; color: #8a5a2a; line-height: 1; }
.stat-label  { font-size: .73rem; color: #9c8878; text-transform: uppercase; letter-spacing: .09em; margin-top: .3rem; }

.wotd-card    { background: linear-gradient(135deg, #2d5016 0%, #4a7c2f 100%); border-radius: 14px; padding: 1.8rem 2rem; margin-bottom: 1rem; }
.wotd-label   { font-size: .7rem; text-transform: uppercase; letter-spacing: .13em; color: rgba(255,255,255,.55); margin-bottom: .7rem; }
.wotd-word    { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #fff; margin: 0; }
.wotd-meaning { font-size: .93rem; color: rgba(255,255,255,.88); margin-top: .45rem; line-height: 1.55; }
.wotd-example { font-size: .8rem; color: rgba(255,255,255,.6); font-style: italic; margin-top: .85rem; border-top: 1px solid rgba(255,255,255,.15); padding-top: .75rem; line-height: 1.6; }

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.35rem; color: #1a1410;
  margin: 1.4rem 0 .9rem;
  display: flex; align-items: center; gap: .5rem;
}
.section-title::after { content: ''; flex: 1; height: 1px; background: #e2d5c8; margin-left: .8rem; }

.info-box { background: rgba(193,127,66,.07); border: 1px solid #e8c898; border-radius: 10px; padding: .85rem 1.1rem; font-size: .85rem; color: #4a3f35; margin: .6rem 0 1rem; line-height: 1.6; }
.info-box strong { color: #7a4f26; }

.result-tag { display: inline-block; font-size: .78rem; color: #9c8878; background: #fdfaf6; border: 1px solid #e2d5c8; padding: 3px 12px; border-radius: 20px; margin-bottom: .9rem; }

hr { border: none; border-top: 1px solid #e2d5c8; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── TOP NAVBAR (always visible) ──────────────────────────────────────────────
st.markdown(f"""
<div class="topnav">
  <div class="topnav-brand">
    <div class="topnav-logo">📖</div>
    <div>
      <div class="topnav-name">Kaili Ledo Dictionary</div>
      <div class="topnav-sub">Digital Preservation Project</div>
    </div>
  </div>
  <div class="topnav-count">
    <span>{len(df):,}</span> entries
  </div>
</div>
""", unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def highlight(text, query):
    if not query:
        return text
    return re.sub(
        f"({re.escape(query)})",
        r'<mark style="background:#f0ddb0;border-radius:3px;padding:0 2px;">\1</mark>',
        text, flags=re.I
    )

def word_card(row, query=""):
    kaili   = highlight(row["kaili_ledo"], query)
    meaning = highlight(row["indonesia"],  query)
    example = (f'<div class="word-example">📝 {row["contoh"]}</div>'
               if row["contoh"] else "")
    st.markdown(f"""
    <div class="word-card">
      <div class="word-kaili">{kaili}</div>
      <div class="word-meaning">{meaning}</div>
      {example}
    </div>""", unsafe_allow_html=True)

def get_wotd():
    pool = df[(df["kaili_ledo"] != "") & (df["contoh"] != "")]
    if pool.empty:
        pool = df[df["kaili_ledo"] != ""]
    return pool.iloc[date.today().toordinal() % len(pool)]

# ─── MAIN TABS (navigation) ───────────────────────────────────────────────────
tab_home, tab_search, tab_browse, tab_add, tab_stats, tab_about = st.tabs([
    "🏠  Home",
    "🔍  Search",
    "📚  Browse",
    "➕  Add Word",
    "📊  Statistics",
    "ℹ️  About",
])

# ═══════════════════════════════════════════════════════════════════════════════
#  HOME
# ═══════════════════════════════════════════════════════════════════════════════
with tab_home:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-banner">
      <div class="hero-tag">🌿 Regional Language · Central Sulawesi, Indonesia</div>
      <div class="hero-title">Kaili Ledo<br>Digital Dictionary</div>
      <div class="hero-desc">
        A language preservation initiative for Kaili Ledo — the mother tongue of the Kaili
        people in the Palu Valley. Entries are drawn from conversations, oral stories, and
        written texts compiled by SIL International.
      </div>
    </div>""", unsafe_allow_html=True)

    has_ex  = (df["contoh"] != "").sum()
    letters = df[df["kaili_ledo"] != ""]["first_letter"].nunique()
    pct     = round(has_ex / len(df) * 100)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in [
        (c1, len(df),      "Total Entries"),
        (c2, has_ex,       "With Example Sentences"),
        (c3, letters,      "Starting Letters"),
        (c4, f"{pct}%",    "Example Coverage"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-number">{val}</div>
              <div class="stat-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown('<div class="section-title">✨ Word of the Day</div>', unsafe_allow_html=True)
        w = get_wotd()
        ex_html = f'<div class="wotd-example">📝 {w["contoh"]}</div>' if w["contoh"] else ""
        st.markdown(f"""
        <div class="wotd-card">
          <div class="wotd-label">Word of the Day &mdash; {date.today().strftime("%B %d, %Y")}</div>
          <div class="wotd-word">{w["kaili_ledo"]}</div>
          <div class="wotd-meaning">{w["indonesia"]}</div>
          {ex_html}
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title">🎲 Random Word</div>', unsafe_allow_html=True)
        if st.button("Show a Random Word", use_container_width=True):
            word_card(df[df["kaili_ledo"] != ""].sample(1).iloc[0])

    with right:
        st.markdown('<div class="section-title">📋 Recent Entries</div>', unsafe_allow_html=True)
        for _, row in df[df["kaili_ledo"] != ""].tail(8).iloc[::-1].iterrows():
            word_card(row)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SEARCH
# ═══════════════════════════════════════════════════════════════════════════════
with tab_search:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔍 Search the Dictionary</div>', unsafe_allow_html=True)

    s1, s2 = st.tabs(["  Kaili Ledo → Indonesian  ", "  Indonesian → Kaili Ledo  "])

    with s1:
        q = st.text_input("Enter a Kaili Ledo word", placeholder="e.g.  Nangala,  Baju,  Ada …",
                          key="search_kl")
        if q:
            res = df[df["kaili_ledo"].str.contains(q, case=False, na=False)]
            st.markdown(f'<span class="result-tag">{len(res)} result(s) found</span>',
                        unsafe_allow_html=True)
            if res.empty:
                st.info("No entries found — try a different spelling or keyword.")
            else:
                for _, row in res.iterrows():
                    word_card(row, q)

    with s2:
        q2 = st.text_input("Enter an Indonesian word or meaning",
                           placeholder="e.g.  Mengambil,  Agama,  Dagu …", key="search_id")
        if q2:
            res2 = df[df["indonesia"].str.contains(q2, case=False, na=False)]
            st.markdown(f'<span class="result-tag">{len(res2)} result(s) found</span>',
                        unsafe_allow_html=True)
            if res2.empty:
                st.info("No entries found — try a synonym or related term.")
            else:
                for _, row in res2.iterrows():
                    word_card(row, q2)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  BROWSE
# ═══════════════════════════════════════════════════════════════════════════════
with tab_browse:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📚 Browse by Starting Letter</div>', unsafe_allow_html=True)

    all_letters = ["All"] + sorted(df[df["kaili_ledo"] != ""]["first_letter"].dropna().unique())
    sel = st.selectbox("Choose a starting letter", options=all_letters,
                       format_func=lambda x: "📖  Show All Entries" if x == "All" else f"Letter  {x}")

    filtered = (df[df["kaili_ledo"] != ""].sort_values("kaili_ledo")
                if sel == "All"
                else df[df["first_letter"] == sel].sort_values("kaili_ledo"))

    PAGE  = 20
    total = max(1, (len(filtered) - 1) // PAGE + 1)
    ci, cp = st.columns([3, 1])
    with ci:
        st.markdown(f'<span class="result-tag">{len(filtered)} entries</span>',
                    unsafe_allow_html=True)
    with cp:
        page = st.number_input("Page", min_value=1, max_value=total, value=1, step=1)

    start = (page - 1) * PAGE
    for _, row in filtered.iloc[start : start + PAGE].iterrows():
        word_card(row)

    if total > 1:
        st.markdown(
            f'<p style="text-align:center;color:#9c8878;font-size:.82rem;margin-top:.5rem;">'
            f'Page {page} of {total}</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  ADD WORD
# ═══════════════════════════════════════════════════════════════════════════════
with tab_add:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">➕ Contribute a New Word</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
      💡 <strong>Help grow the dictionary.</strong> Every word contributed helps preserve
      Kaili Ledo as a living language for future generations. Fields marked * are required.
    </div>""", unsafe_allow_html=True)

    with st.form("add_word_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_kaili   = st.text_input("Kaili Ledo Word *", placeholder="e.g. Nobose")
        with col2:
            new_meaning = st.text_input("Indonesian Meaning *",
                                        placeholder="e.g. Berenang (Swimming)")
        new_example = st.text_area(
            "Example Sentence (optional)",
            placeholder="A sentence in Kaili Ledo followed by its Indonesian translation…",
            height=110)
        submitted = st.form_submit_button("💾  Save Word", use_container_width=True)

    if submitted:
        if not new_kaili.strip() or not new_meaning.strip():
            st.error("⚠️  Both the Kaili Ledo word and its Indonesian meaning are required.")
        else:
            dup = df[df["kaili_ledo"].str.lower() == new_kaili.strip().lower()]
            if not dup.empty:
                st.warning(f"⚠️  **{new_kaili}** already exists: _{dup.iloc[0]['indonesia']}_")
            else:
                entry = {
                    "id":         int(df["id"].max()) + 1,
                    "kaili_ledo": new_kaili.strip(),
                    "indonesia":  new_meaning.strip(),
                    "contoh":     new_example.strip(),
                }
                data_path = Path(__file__).parent / "data" / "kamus.json"
                with open(data_path, encoding="utf-8") as f:
                    all_data = json.load(f)
                all_data.append(entry)
                with open(data_path, "w", encoding="utf-8") as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)

                import csv
                with open(Path(__file__).parent / "data" / "kamus.csv",
                          "a", encoding="utf-8", newline="") as f:
                    csv.writer(f).writerow([entry["id"], entry["kaili_ledo"],
                                            entry["indonesia"], entry["contoh"]])
                st.success(f"✅  **{new_kaili}** has been added to the dictionary!")
                st.cache_data.clear()
                ex_html = (f'<div class="word-example">📝 {new_example}</div>'
                           if new_example else "")
                st.markdown(f"""
                <div class="word-card">
                  <div class="word-badge">Newly Added</div>
                  <div class="word-kaili">{new_kaili}</div>
                  <div class="word-meaning">{new_meaning}</div>
                  {ex_html}
                </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">📋 Last 5 Entries in Database</div>',
                unsafe_allow_html=True)
    for _, row in df.tail(5).iloc[::-1].iterrows():
        word_card(row)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_stats:
    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Dictionary Statistics</div>', unsafe_allow_html=True)

    BG  = "#fdfaf6"
    INK = "#1a1410"
    PAL = ["#e8c898","#c17f42","#8a5a2a","#4a7c2f","#2d5016"]

    lc = (df[df["kaili_ledo"] != ""]
          .groupby("first_letter").size()
          .reset_index(name="count")
          .sort_values("first_letter"))

    fig1 = px.bar(lc, x="first_letter", y="count",
                  title="Word Count by Starting Letter",
                  color="count",
                  color_continuous_scale=["#e8c898","#c17f42","#8a5a2a","#2d5016"],
                  labels={"first_letter":"Starting Letter","count":"Words"})
    fig1.update_layout(font_family="DM Sans", font_color=INK,
                       plot_bgcolor=BG, paper_bgcolor=BG,
                       coloraxis_showscale=False,
                       title_font=dict(size=15, color=INK),
                       margin=dict(t=52,b=24,l=12,r=12))
    fig1.update_traces(marker_line_width=0)
    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(gridcolor="#e2d5c8")
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        has_ex = (df["contoh"] != "").sum()
        fig2 = go.Figure(go.Pie(
            labels=["Has Example","No Example"],
            values=[has_ex, len(df)-has_ex],
            hole=.58, marker_colors=["#2d5016","#e8c898"],
            textinfo="percent+label", textfont=dict(size=12, color=INK)))
        fig2.update_layout(
            title=dict(text="Example Sentence Coverage", font=dict(size=15,color=INK)),
            font_family="DM Sans", font_color=INK,
            plot_bgcolor=BG, paper_bgcolor=BG,
            showlegend=False, margin=dict(t=52,b=24,l=12,r=12),
            annotations=[dict(text=f"{round(has_ex/len(df)*100)}%",
                              x=.5, y=.5, font=dict(size=24,color="#2d5016"),
                              showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        dv = df[df["kaili_ledo"] != ""].copy()
        dv["def_len"] = dv["indonesia"].str.len()
        dv["bucket"]  = pd.cut(dv["def_len"], bins=[0,20,50,100,200,999],
                               labels=["Very Short","Short","Medium","Long","Very Long"])
        bc = dv["bucket"].value_counts().reset_index()
        bc.columns = ["Length","count"]
        fig3 = px.bar(bc, x="Length", y="count", title="Definition Length Distribution",
                      color="Length", color_discrete_sequence=PAL,
                      labels={"Length":"Definition Length","count":"Words"})
        fig3.update_layout(font_family="DM Sans", font_color=INK,
                           plot_bgcolor=BG, paper_bgcolor=BG, showlegend=False,
                           title_font=dict(size=15,color=INK),
                           margin=dict(t=52,b=24,l=12,r=12))
        fig3.update_traces(marker_line_width=0)
        fig3.update_xaxes(showgrid=False)
        fig3.update_yaxes(gridcolor="#e2d5c8")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">📝 Longest Definitions</div>', unsafe_allow_html=True)
    dv["def_len"] = dv["indonesia"].str.len()
    for _, row in dv.nlargest(5, "def_len").iterrows():
        word_card(row)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_about:
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">ℹ️ About This Project</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="word-card" style="border-left-color:#2d5016;">
      <div class="word-kaili" style="color:#2d5016;">The Kaili Ledo Language</div>
      <div class="word-meaning">
        Kaili Ledo is one of the dialects spoken by the Kaili people in the Palu Valley,
        Central Sulawesi, Indonesia. It is part of the Austronesian language family and
        serves as a regional lingua franca. Like many regional languages, it faces pressure
        from national and global languages — making digital preservation efforts critical.
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">📖 Source</div>
          <div class="word-meaning">
            Based on the <strong style="color:#7a4f26;">Kamus Kaili-Ledo Indonesia Inggris</strong>
            (First Edition, 2003), compiled by <strong style="color:#7a4f26;">Donna Evans</strong>
            and published by the Department of Culture &amp; Tourism of Central Sulawesi Province
            in collaboration with <strong style="color:#7a4f26;">SIL International</strong>.
          </div>
        </div>
        <div class="word-card">
          <div class="word-kaili">🎯 Project Goal</div>
          <div class="word-meaning">
            Make Kaili Ledo accessible to younger generations, researchers, and the general public.
            Started from a Microsoft Access database of ~500 selected words, designed to expand
            continuously through community contributions.
          </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">⚙️ Tech Stack</div>
          <div class="word-meaning">
            <table style="width:100%;border-collapse:collapse;font-size:.88rem;">
              <tr><td style="color:#9c8878;padding:4px 0;width:42%;">Framework</td>
                  <td style="color:#3d342c;font-weight:500;">Python + Streamlit</td></tr>
              <tr><td style="color:#9c8878;padding:4px 0;">Data</td>
                  <td style="color:#3d342c;font-weight:500;">JSON + CSV (from MS Access)</td></tr>
              <tr><td style="color:#9c8878;padding:4px 0;">Charts</td>
                  <td style="color:#3d342c;font-weight:500;">Plotly Express</td></tr>
              <tr><td style="color:#9c8878;padding:4px 0;">Hosting</td>
                  <td style="color:#3d342c;font-weight:500;">Streamlit Community Cloud</td></tr>
              <tr><td style="color:#9c8878;padding:4px 0;">Version Control</td>
                  <td style="color:#3d342c;font-weight:500;">GitHub</td></tr>
            </table>
          </div>
        </div>
        <div class="word-card">
          <div class="word-kaili">🚀 Deploy in 5 Steps</div>
          <div class="word-meaning">
            <ol style="padding-left:1.1rem;margin:0;line-height:2.1;font-size:.88rem;color:#3d342c;">
              <li>Push all files to a new GitHub repository</li>
              <li>Visit <strong style="color:#7a4f26;">share.streamlit.io</strong></li>
              <li>Connect your GitHub account</li>
              <li>Select the repo &amp; <code style="background:#f0ddb0;padding:1px 5px;border-radius:4px;color:#7a4f26;">app.py</code></li>
              <li>Click <strong style="color:#2d5016;">Deploy</strong> — live in minutes! 🎉</li>
            </ol>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
      🤝 <strong>Contribute:</strong> Use the <em>Add Word</em> tab to submit new entries directly.
      Every contribution helps keep Kaili Ledo alive for future generations.
    </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
