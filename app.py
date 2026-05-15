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
    page_title="Kamus Kaili Ledo",
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
    df["kaili_ledo"] = df["kaili_ledo"].fillna("").str.strip()
    df["indonesia"] = df["indonesia"].fillna("").str.strip()
    df["contoh"] = df["contoh"].fillna("").str.strip()
    df["huruf"] = df["kaili_ledo"].str[0].str.upper().where(df["kaili_ledo"] != "", "")
    return df

df = load_data()

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

  :root {
    --terra: #c17f42;
    --terra-light: #e8c898;
    --terra-dark: #8a5a2a;
    --forest: #2d5016;
    --forest-light: #4a7c2f;
    --earth: #f5efe6;
    --ink: #1a1410;
    --ink-light: #4a3f35;
    --muted: #9c8878;
    --card-bg: #fdfaf6;
    --border: #e2d5c8;
  }

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* Main background */
  .stApp {
    background-color: var(--earth);
    background-image:
      radial-gradient(circle at 20% 50%, rgba(193,127,66,0.06) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(45,80,22,0.04) 0%, transparent 50%);
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1410 0%, #2d1f12 100%);
    border-right: 1px solid var(--terra-dark);
  }
  [data-testid="stSidebar"] * { color: var(--earth) !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stTextInput label,
  [data-testid="stSidebar"] .stRadio label { color: var(--terra-light) !important; }
  [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] {
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

  /* Hide default streamlit elements */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem; max-width: 1400px; }

  /* Cards */
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
  .word-id {
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

  /* Hero banner */
  .hero-banner {
    background: linear-gradient(135deg, #1a1410 0%, #3d2410 50%, #2d5016 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: "𝕂";
    position: absolute;
    right: -20px;
    top: -30px;
    font-size: 220px;
    color: rgba(255,255,255,0.03);
    font-family: serif;
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

  /* Stats cards */
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

  /* Word of the day */
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

  /* Letter index */
  .letter-pill {
    display: inline-block;
    background: var(--terra-light);
    color: var(--terra-dark);
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 2px;
    font-size: 0.82rem;
    cursor: pointer;
  }

  /* Section headings */
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

  /* Form inputs */
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

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid var(--border);
    gap: 0;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent;
    border: none;
    color: var(--muted);
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

  /* Info box */
  .info-box {
    background: rgba(193,127,66,0.08);
    border: 1px solid var(--terra-light);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: var(--ink-light);
    margin: 0.5rem 0;
  }

  /* Success */
  .stSuccess { border-radius: 10px !important; }

  /* Alphabet grid */
  .alpha-grid { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.5rem 0 1rem; }
  .alpha-btn {
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 8px;
    padding: 5px 12px;
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--ink-light);
    cursor: pointer;
    transition: all 0.15s;
  }
  .alpha-btn:hover, .alpha-btn.active {
    background: var(--terra-dark);
    border-color: var(--terra-dark);
    color: white;
  }

  /* Divider */
  hr { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }

  /* Result count badge */
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
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
      <div style="font-size:2.5rem;">📖</div>
      <div style="font-family:'Playfair Display',serif; font-size:1.1rem; color:#e8c898; font-weight:700;">
        Kamus Kaili Ledo
      </div>
      <div style="font-size:0.72rem; color:rgba(255,255,255,0.4); letter-spacing:0.12em; text-transform:uppercase; margin-top:0.2rem;">
        Digital Dictionary
      </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigasi",
        ["🏠 Beranda", "🔍 Cari Kata", "📚 Jelajahi Kamus", "➕ Tambah Kata", "📊 Statistik", "ℹ️ Tentang"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.75rem; color:rgba(255,255,255,0.35); text-align:center; line-height:1.8;">
      Total Kata: <span style="color:#e8c898; font-weight:600;">{len(df):,}</span><br>
      Sumber: Kamus Kaili-Ledo<br>
      Penyusun: Donna Evans (2003)<br>
      SIL International
    </div>
    """, unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def render_word_card(row, highlight_query=""):
    kaili = row["kaili_ledo"]
    indo = row["indonesia"]
    contoh = row["contoh"]

    if highlight_query:
        q = re.escape(highlight_query)
        kaili = re.sub(f"({q})", r'<mark style="background:#e8c898;border-radius:3px;">\1</mark>', kaili, flags=re.I)
        indo = re.sub(f"({q})", r'<mark style="background:#e8c898;border-radius:3px;">\1</mark>', indo, flags=re.I)

    example_html = f'<div class="word-example">📝 {contoh}</div>' if contoh else ""
    st.markdown(f"""
    <div class="word-card">
      <div class="word-kaili">{kaili}</div>
      <div class="word-id">{indo}</div>
      {example_html}
    </div>
    """, unsafe_allow_html=True)


def get_word_of_the_day():
    seed = date.today().toordinal()
    words_with_example = df[df["contoh"] != ""]
    if words_with_example.empty:
        words_with_example = df[df["kaili_ledo"] != ""]
    idx = seed % len(words_with_example)
    return words_with_example.iloc[idx]


# ═══════════════════════════════════════════════════════════════════════════════
#   PAGE: BERANDA
# ═══════════════════════════════════════════════════════════════════════════════
if menu == "🏠 Beranda":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-subtitle">🌿 Bahasa Daerah Sulawesi Tengah</div>
      <div class="hero-title">Kamus Digital<br>Kaili Ledo</div>
      <div class="hero-desc">
        Sebuah upaya pelestarian bahasa daerah Kaili Ledo — bahasa ibu masyarakat
        di lembah Palu, Sulawesi Tengah. Kamus ini memuat entri yang dikumpulkan
        dari percakapan, cerita lisan, dan naskah tertulis masyarakat setempat.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    has_example = (df["contoh"] != "").sum()
    letters_used = df[df["kaili_ledo"] != ""]["huruf"].nunique()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{len(df)}</div>
        <div class="stat-label">Total Entri</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{has_example}</div>
        <div class="stat-label">Punya Contoh Kalimat</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{letters_used}</div>
        <div class="stat-label">Huruf Awal</div></div>""", unsafe_allow_html=True)
    with col4:
        pct = round(has_example / len(df) * 100)
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{pct}%</div>
        <div class="stat-label">Kelengkapan Contoh</div></div>""", unsafe_allow_html=True)

    st.markdown("")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-title">✨ Kata Hari Ini</div>', unsafe_allow_html=True)
        wotd = get_word_of_the_day()
        example_html = f'<div class="wotd-example">📝 {wotd["contoh"]}</div>' if wotd["contoh"] else ""
        st.markdown(f"""
        <div class="wotd-card">
          <div class="wotd-label">Kata Hari Ini — {date.today().strftime("%d %B %Y")}</div>
          <div class="wotd-word">{wotd["kaili_ledo"]}</div>
          <div class="wotd-meaning">{wotd["indonesia"]}</div>
          {example_html}
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">🎲 Kata Acak</div>', unsafe_allow_html=True)
        if st.button("Tampilkan Kata Acak", use_container_width=True):
            rand_word = df[df["kaili_ledo"] != ""].sample(1).iloc[0]
            render_word_card(rand_word)

    with col_right:
        st.markdown('<div class="section-title">📋 Kata Terbaru</div>', unsafe_allow_html=True)
        recent = df[df["kaili_ledo"] != ""].tail(8).iloc[::-1]
        for _, row in recent.iterrows():
            render_word_card(row)


# ═══════════════════════════════════════════════════════════════════════════════
#   PAGE: CARI KATA
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "🔍 Cari Kata":
    st.markdown('<div class="section-title">🔍 Pencarian Kata</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Cari Bahasa Kaili Ledo → Indonesia", "Cari Bahasa Indonesia → Kaili Ledo"])

    with tab1:
        query = st.text_input("Masukkan kata dalam Bahasa Kaili Ledo", placeholder="Contoh: Nangala, Baju, Ada…")
        if query:
            results = df[df["kaili_ledo"].str.contains(query, case=False, na=False)]
            st.markdown(f'<span class="result-count">Ditemukan {len(results)} kata</span>', unsafe_allow_html=True)
            if results.empty:
                st.info("Kata tidak ditemukan. Coba kata lain atau periksa ejaan.")
            else:
                for _, row in results.iterrows():
                    render_word_card(row, highlight_query=query)

    with tab2:
        query_id = st.text_input("Masukkan arti dalam Bahasa Indonesia", placeholder="Contoh: Mengambil, Agama, Dagu…")
        if query_id:
            results = df[df["indonesia"].str.contains(query_id, case=False, na=False)]
            st.markdown(f'<span class="result-count">Ditemukan {len(results)} kata</span>', unsafe_allow_html=True)
            if results.empty:
                st.info("Arti tidak ditemukan. Coba kata lain atau sinonim.")
            else:
                for _, row in results.iterrows():
                    render_word_card(row, highlight_query=query_id)


# ═══════════════════════════════════════════════════════════════════════════════
#   PAGE: JELAJAHI KAMUS
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "📚 Jelajahi Kamus":
    st.markdown('<div class="section-title">📚 Jelajahi Berdasarkan Huruf</div>', unsafe_allow_html=True)

    available_letters = sorted(df[df["kaili_ledo"] != ""]["huruf"].dropna().unique())

    # Letter selector
    selected_letter = st.selectbox(
        "Pilih Huruf Awal",
        options=["Semua"] + available_letters,
        format_func=lambda x: f"Huruf  {x}" if x != "Semua" else "📖 Tampilkan Semua"
    )

    st.markdown("")

    # Filter
    if selected_letter == "Semua":
        filtered = df[df["kaili_ledo"] != ""].sort_values("kaili_ledo")
    else:
        filtered = df[df["huruf"] == selected_letter].sort_values("kaili_ledo")

    st.markdown(f'<span class="result-count">{len(filtered)} kata ditemukan</span>', unsafe_allow_html=True)

    # Paginate
    PAGE_SIZE = 20
    total_pages = max(1, (len(filtered) - 1) // PAGE_SIZE + 1)
    page = st.number_input("Halaman", min_value=1, max_value=total_pages, value=1, step=1)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    page_df = filtered.iloc[start:end]

    for _, row in page_df.iterrows():
        render_word_card(row)

    if total_pages > 1:
        st.markdown(f'<div style="text-align:center;color:var(--muted);font-size:0.82rem;">Halaman {page} dari {total_pages}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#   PAGE: TAMBAH KATA
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "➕ Tambah Kata":
    st.markdown('<div class="section-title">➕ Tambah Kata Baru</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
      💡 Tambahkan kata baru ke dalam kamus untuk memperkaya database bahasa Kaili Ledo.
      Setiap kontribusi sangat berarti bagi pelestarian bahasa daerah kita.
    </div>
    """, unsafe_allow_html=True)

    with st.form("tambah_kata_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_kaili = st.text_input("Kata dalam Bahasa Kaili Ledo *", placeholder="Contoh: Nobose")
        with col2:
            new_indonesia = st.text_input("Arti dalam Bahasa Indonesia *", placeholder="Contoh: Berenang")

        new_contoh = st.text_area(
            "Contoh Kalimat (opsional)",
            placeholder="Contoh kalimat dalam Bahasa Kaili Ledo beserta terjemahannya...",
            height=100
        )
        submitted = st.form_submit_button("💾 Simpan Kata", use_container_width=True)

    if submitted:
        if not new_kaili.strip() or not new_indonesia.strip():
            st.error("⚠️ Kata Kaili Ledo dan arti Bahasa Indonesia wajib diisi.")
        else:
            # Check duplicate
            dup = df[df["kaili_ledo"].str.lower() == new_kaili.strip().lower()]
            if not dup.empty:
                st.warning(f"⚠️ Kata **{new_kaili}** sudah ada dalam kamus dengan arti: _{dup.iloc[0]['indonesia']}_")
            else:
                new_id = int(df["id"].max()) + 1
                new_entry = {
                    "id": new_id,
                    "kaili_ledo": new_kaili.strip(),
                    "indonesia": new_indonesia.strip(),
                    "contoh": new_contoh.strip(),
                    "huruf": new_kaili.strip()[0].upper()
                }
                # Append to JSON
                data_path = Path(__file__).parent / "data" / "kamus.json"
                with open(data_path, encoding="utf-8") as f:
                    all_data = json.load(f)
                all_data.append({k: v for k, v in new_entry.items() if k != "huruf"})
                with open(data_path, "w", encoding="utf-8") as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)

                # Append to CSV
                csv_path = Path(__file__).parent / "data" / "kamus.csv"
                with open(csv_path, "a", encoding="utf-8", newline="") as f:
                    import csv
                    w = csv.writer(f)
                    w.writerow([new_id, new_kaili.strip(), new_indonesia.strip(), new_contoh.strip()])

                st.success(f"✅ Kata **{new_kaili}** berhasil ditambahkan ke kamus!")
                st.cache_data.clear()
                st.markdown(f"""
                <div class="word-card">
                  <div class="word-badge">Baru ditambahkan</div>
                  <div class="word-kaili">{new_kaili}</div>
                  <div class="word-id">{new_indonesia}</div>
                  {"<div class='word-example'>📝 " + new_contoh + "</div>" if new_contoh else ""}
                </div>
                """, unsafe_allow_html=True)

    # Show last 5 entries for context
    st.markdown('<div class="section-title">📋 Entri Terakhir dalam Database</div>', unsafe_allow_html=True)
    for _, row in df.tail(5).iloc[::-1].iterrows():
        render_word_card(row)


# ═══════════════════════════════════════════════════════════════════════════════
#   PAGE: STATISTIK
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "📊 Statistik":
    st.markdown('<div class="section-title">📊 Statistik Kamus</div>', unsafe_allow_html=True)

    import plotly.express as px
    import plotly.graph_objects as go

    COLORS = {
        "terra": "#c17f42",
        "forest": "#2d5016",
        "terra_light": "#e8c898",
        "forest_light": "#4a7c2f",
        "ink": "#1a1410",
        "bg": "#fdfaf6",
    }

    # Distribusi huruf
    letter_counts = df[df["kaili_ledo"] != ""].groupby("huruf").size().reset_index(name="jumlah")
    letter_counts = letter_counts.sort_values("huruf")

    fig1 = px.bar(
        letter_counts,
        x="huruf", y="jumlah",
        title="Distribusi Kata per Huruf Awal",
        color="jumlah",
        color_continuous_scale=["#e8c898", "#c17f42", "#8a5a2a", "#2d5016"],
        labels={"huruf": "Huruf Awal", "jumlah": "Jumlah Kata"},
    )
    fig1.update_layout(
        font_family="DM Sans",
        plot_bgcolor=COLORS["bg"],
        paper_bgcolor=COLORS["bg"],
        coloraxis_showscale=False,
        title_font_size=15,
        title_font_color=COLORS["ink"],
        margin=dict(t=50, b=20, l=20, r=20),
    )
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # Kata dengan vs tanpa contoh
        has_ex = (df["contoh"] != "").sum()
        no_ex = len(df) - has_ex
        fig2 = go.Figure(go.Pie(
            labels=["Punya Contoh", "Tanpa Contoh"],
            values=[has_ex, no_ex],
            hole=0.55,
            marker_colors=[COLORS["forest"], COLORS["terra_light"]],
            textinfo="percent+label",
            textfont_size=12,
        ))
        fig2.update_layout(
            title="Kelengkapan Contoh Kalimat",
            font_family="DM Sans",
            plot_bgcolor=COLORS["bg"],
            paper_bgcolor=COLORS["bg"],
            title_font_size=15,
            showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20),
            annotations=[dict(text=f"{round(has_ex/len(df)*100)}%", x=0.5, y=0.5,
                              font_size=22, font_color=COLORS["forest"], showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # Top 10 most common first syllables
        df_valid = df[df["kaili_ledo"] != ""].copy()
        df_valid["panjang"] = df_valid["indonesia"].str.len()
        df_valid["bucket"] = pd.cut(df_valid["panjang"], bins=[0, 20, 50, 100, 200, 999],
                                    labels=["Sangat Singkat", "Singkat", "Sedang", "Panjang", "Sangat Panjang"])
        bucket_counts = df_valid["bucket"].value_counts().reset_index()
        bucket_counts.columns = ["panjang_arti", "jumlah"]
        bucket_colors = [COLORS["terra_light"], COLORS["terra"], COLORS["terra_dark"],
                        COLORS["forest_light"], COLORS["forest"]]

        fig3 = px.bar(
            bucket_counts,
            x="panjang_arti", y="jumlah",
            title="Distribusi Panjang Definisi",
            color="panjang_arti",
            color_discrete_sequence=bucket_colors,
            labels={"panjang_arti": "Panjang Definisi", "jumlah": "Jumlah Kata"},
        )
        fig3.update_layout(
            font_family="DM Sans",
            plot_bgcolor=COLORS["bg"],
            paper_bgcolor=COLORS["bg"],
            showlegend=False,
            title_font_size=15,
            margin=dict(t=50, b=20, l=20, r=20),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Top words by length
    st.markdown('<div class="section-title">📝 Kata dengan Definisi Terpanjang</div>', unsafe_allow_html=True)
    df_valid["def_len"] = df_valid["indonesia"].str.len()
    top_long = df_valid.nlargest(5, "def_len")[["kaili_ledo", "indonesia", "def_len"]]
    for _, row in top_long.iterrows():
        render_word_card(row)


# ═══════════════════════════════════════════════════════════════════════════════
#   PAGE: TENTANG
# ═══════════════════════════════════════════════════════════════════════════════
elif menu == "ℹ️ Tentang":
    st.markdown('<div class="section-title">ℹ️ Tentang Kamus Kaili Ledo Digital</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="word-card" style="border-left-color: var(--forest);">
      <div class="word-kaili" style="color: var(--forest);">Bahasa Kaili Ledo</div>
      <div class="word-id">
        Bahasa Kaili Ledo adalah salah satu bahasa yang dituturkan oleh masyarakat
        Kaili di lembah Palu, Sulawesi Tengah, Indonesia. Bahasa ini merupakan
        lingua franca di wilayah tersebut dan memiliki beberapa dialek.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">📖 Sumber Kamus</div>
          <div class="word-id">
            Kamus ini dikembangkan berdasarkan <strong>Kamus Kaili-Ledo Indonesia Inggris</strong>
            (Edisi Perdana, 2003) yang disusun oleh <strong>Donna Evans</strong> dan diterbitkan
            oleh Dinas Kebudayaan dan Pariwisata Propinsi Sulawesi Tengah
            bekerja sama dengan SIL International.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">🎯 Tujuan Proyek</div>
          <div class="word-id">
            Kamus digital ini dibuat sebagai upaya pelestarian bahasa daerah Kaili Ledo
            agar lebih mudah diakses oleh generasi muda dan peneliti bahasa.
            Dimulai dengan ~500 kata pilihan dari database Microsoft Access,
            kamus ini terus berkembang dengan kontribusi komunitas.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">⚙️ Teknologi</div>
          <div class="word-id">
            <ul style="padding-left:1rem; margin:0; line-height:2;">
              <li><strong>Backend:</strong> Python + Streamlit</li>
              <li><strong>Data:</strong> JSON + CSV (dari Microsoft Access)</li>
              <li><strong>Visualisasi:</strong> Plotly Express</li>
              <li><strong>Hosting:</strong> Streamlit Community Cloud</li>
              <li><strong>Repository:</strong> GitHub</li>
            </ul>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="word-card">
          <div class="word-kaili">🚀 Cara Deploy ke GitHub</div>
          <div class="word-id">
            <ol style="padding-left:1rem; margin:0; line-height:2; font-size:0.88rem;">
              <li>Push semua file ke repository GitHub baru</li>
              <li>Kunjungi <strong>share.streamlit.io</strong></li>
              <li>Hubungkan akun GitHub</li>
              <li>Pilih repository & file <code>app.py</code></li>
              <li>Deploy otomatis! 🎉</li>
            </ol>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
      🤝 <strong>Kontribusi:</strong> Kamu bisa menambah kata baru melalui menu <em>Tambah Kata</em>.
      Setiap kontribusi akan tersimpan dan membantu memperkaya warisan budaya bahasa Kaili Ledo.
    </div>
    """, unsafe_allow_html=True)
