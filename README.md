# 📖 Kaili Ledo Dictionary — Digital Language Preservation

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Entries](https://img.shields.io/badge/Entries-301+-orange)

An interactive digital dictionary for preserving the **Kaili Ledo language** — a regional tongue spoken by the Kaili people in the Palu Valley, Central Sulawesi, Indonesia.

---

## 🌿 About the Project

Kaili Ledo is one of the dialects within the Kaili language family, spoken by tens of thousands of people in Central Sulawesi. This project digitizes the printed *Kamus Kaili-Ledo Indonesia Inggris* (Donna Evans, 2003) to make it more accessible to younger generations, language researchers, and the general public.

**Database Origin:**  
Started from a Microsoft Access database (~500 selected words), now expanded into a full interactive web application with search, browsing, statistics, and community contribution features.

---

## ✨ Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Dashboard with summary stats, Word of the Day, and random word explorer |
| 🔍 **Search** | Bidirectional search: Kaili Ledo → Indonesian or Indonesian → Kaili Ledo, with result highlighting |
| 📚 **Browse** | Browse all entries by starting letter, with 20-word pagination |
| ➕ **Add Word** | Contribution form that saves new entries directly to the database |
| 📊 **Statistics** | Interactive Plotly charts: letter distribution, example coverage, definition length |
| ℹ️ **About** | Project background, source credits, and deployment guide |

---

## 🚀 Getting Started

### Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/kaili-ledo-dictionary.git
cd kaili-ledo-dictionary

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "🌿 Initial release: Kaili Ledo Digital Dictionary"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/kaili-ledo-dictionary.git
   git push -u origin main
   ```

2. **Deploy:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click **New app**
   - Select your repository, branch `main`, and file `app.py`
   - Click **Deploy!** ✅ — live in minutes

---

## 📁 Project Structure

```
kaili-ledo-dictionary/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── .gitignore
└── data/
    ├── kamus.json      # Dictionary data (JSON format)
    └── kamus.csv       # Dictionary data (CSV backup)
```

---

## 📊 Database Summary

| Metric | Value |
|--------|-------|
| Total entries | 301 words |
| Entries with example sentences | 200+ |
| Starting letters covered | A, B, E, K, M, N, O, P, R, S, T, U, Y |
| Source | Kamus Kaili-Ledo Indonesia Inggris (2003) |

---

## 🗂️ Data Format

Each entry in `data/kamus.json` follows this structure:

```json
{
  "id": 2,
  "kaili_ledo": "Abalaa",
  "indonesia": "Kecelakaan, musibah, malapetaka",
  "contoh": "Nee hau ri kandalana, mbelaka maria abala manggava iko ngena!"
}
```

| Field | Description |
|-------|-------------|
| `id` | Unique numeric identifier |
| `kaili_ledo` | Word in Kaili Ledo |
| `indonesia` | Meaning in Indonesian |
| `contoh` | Example sentence (may be empty) |

---

## 🤝 Contributing

We welcome contributions to expand this dictionary:

**Via the App:** Use the **➕ Add Word** page in the running application.

**Via GitHub:**
1. Fork this repository
2. Edit `data/kamus.json` following the data format above
3. Open a Pull Request with a description of the word(s) added

---

## 📚 Reference

Evans, Donna. (2003). *Kamus Kaili-Ledo Indonesia Inggris* (First Edition). Palu: Dinas Kebudayaan dan Pariwisata Propinsi Sulawesi Tengah & SIL International.

- [SIL International](https://www.sil.org)

---

## 📜 License

- **Source code:** MIT License  
- **Dictionary data:** © 2003 SIL International — used for educational and preservation purposes

---

<div align="center">
  <em>Preserving language is preserving identity. 🌺</em>
</div>
