# 📖 Kamus Kaili Ledo — Kamus Digital Bahasa Daerah

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Entries](https://img.shields.io/badge/Kata-301+-orange)

Kamus digital interaktif untuk melestarikan **Bahasa Kaili Ledo** — bahasa daerah masyarakat Kaili di lembah Palu, Sulawesi Tengah, Indonesia.

---

## 🌿 Tentang Proyek

Bahasa Kaili Ledo adalah salah satu dialek dari rumpun bahasa Kaili yang dituturkan oleh puluhan ribu penutur di Sulawesi Tengah. Proyek ini adalah upaya digitalisasi kamus cetak *Kamus Kaili-Ledo Indonesia Inggris* (Donna Evans, 2003) agar lebih mudah diakses oleh generasi muda, peneliti bahasa, dan masyarakat umum.

**Asal Database:**  
Diawali dari database Microsoft Access (~500 kata pilihan), dikembangkan menjadi aplikasi web interaktif dengan fitur pencarian, penelusuran, dan penambahan kata baru.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🏠 **Beranda** | Dashboard ringkasan, Kata Hari Ini, statistik cepat |
| 🔍 **Cari Kata** | Cari Kaili Ledo → Indonesia atau sebaliknya, dengan highlight hasil |
| 📚 **Jelajahi** | Telusuri kata per huruf awal, paginasi halaman |
| ➕ **Tambah Kata** | Formulir kontribusi kata baru langsung ke database |
| 📊 **Statistik** | Visualisasi distribusi kata dengan grafik interaktif (Plotly) |
| ℹ️ **Tentang** | Informasi proyek, sumber, dan panduan deploy |

---

## 🚀 Cara Menjalankan

### Lokal (Development)

```bash
# 1. Clone repository
git clone https://github.com/USERNAME/kamus-kaili-ledo.git
cd kamus-kaili-ledo

# 2. Buat virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py
```

Buka browser di `http://localhost:8501`

---

### Deploy ke Streamlit Cloud (Gratis!)

1. **Push ke GitHub:**
   ```bash
   git init
   git add .
   git commit -m "🌿 Initial commit: Kamus Kaili Ledo Digital"
   git branch -M main
   git remote add origin https://github.com/USERNAME/kamus-kaili-ledo.git
   git push -u origin main
   ```

2. **Deploy:**
   - Kunjungi [share.streamlit.io](https://share.streamlit.io)
   - Sign in dengan akun GitHub
   - Klik **New app**
   - Pilih repository, branch `main`, file `app.py`
   - Klik **Deploy!** ✅

---

## 📁 Struktur Proyek

```
kamus-kaili-ledo/
├── app.py                  # Aplikasi utama Streamlit
├── requirements.txt        # Dependencies Python
├── README.md               # Dokumentasi ini
├── .gitignore
└── data/
    ├── kamus.json          # Data kamus (format JSON)
    └── kamus.csv           # Data kamus (format CSV backup)
```

---

## 📊 Statistik Database

- **Total Entri:** 301 kata
- **Dengan Contoh Kalimat:** ~200+ entri
- **Huruf Awal:** A, B, E, K, M, N, O, P, R, S, T, U, Y
- **Sumber:** Kamus Kaili-Ledo Indonesia Inggris (2003)

---

## 🗂️ Format Data

File `data/kamus.json` menggunakan format:

```json
[
  {
    "id": 2,
    "kaili_ledo": "Abalaa",
    "indonesia": "Kecelakaan, musibah, malapetaka",
    "contoh": "Nee hau ri kandalana..."
  }
]
```

---

## 🤝 Kontribusi

Kami sangat mengapresiasi kontribusi untuk memperkaya kamus ini:

1. **Melalui Aplikasi:** Gunakan menu **➕ Tambah Kata** di dalam aplikasi
2. **Melalui GitHub:**
   - Fork repository ini
   - Edit file `data/kamus.json`
   - Buat Pull Request dengan deskripsi kata yang ditambahkan

---

## 📚 Referensi

- Evans, Donna. (2003). *Kamus Kaili-Ledo Indonesia Inggris*. Edisi Perdana. Palu: Dinas Kebudayaan dan Pariwisata Propinsi Sulawesi Tengah, SIL International.
- [SIL International](https://www.sil.org)

---

## 📜 Lisensi

Kode sumber: **MIT License**  
Data kamus: © 2003 SIL International (digunakan untuk tujuan pelestarian dan pendidikan)

---

<div align="center">
  <em>Mobaaa — Selamat belajar Bahasa Kaili Ledo! 🌺</em>
</div>
