import sqlite3
import pandas as pd
import re
from tqdm import tqdm
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory 

# Aktifkan progress bar untuk Pandas
tqdm.pandas()

DB_NAME = "surabaya_news_pipeline.db"

print("=== MEMULAI TAHAP PREPROCESSING DATA ===")

# ---------------------------------------------------------
# TAHAP 1 & 3: Ingestion Awal & Penanganan Missing Values
# ---------------------------------------------------------
print("1. Menarik data dan menangani Missing Values...")
conn = sqlite3.connect(DB_NAME)
# IS NOT NULL adalah cara ampuh menangani Missing Values di database
df = pd.read_sql_query("SELECT url, sumber, tanggal, judul, isi_berita FROM artikel_berita WHERE isi_berita IS NOT NULL AND isi_berita != ''", conn)
print(f"Data awal ditarik: {len(df)} baris")

# ---------------------------------------------------------
# TAHAP 3: Filter Duplikasi Dataset
# ---------------------------------------------------------
print("2. Memfilter duplikasi data (Duplicate Removal)...")
# Menghapus baris jika judul dan isi beritanya sama persis
df = df.drop_duplicates(subset=['judul', 'isi_berita'], keep='first')
print(f"Data setelah filter duplikasi: {len(df)} baris tersisa")

# ---------------------------------------------------------
# PERSIAPAN NLP (Sastrawi)
# ---------------------------------------------------------
print("\nMenyiapkan mesin NLP (Stopword & Stemmer). Mohon tunggu sebentar...")
factory_stop = StopWordRemoverFactory()
stopword = factory_stop.create_stop_word_remover()

factory_stem = StemmerFactory()
stemmer = factory_stem.create_stemmer()

# ---------------------------------------------------------
# TAHAP 1 & 2: Text Cleaning & Normalisasi NLP
# ---------------------------------------------------------
def bersihkan_teks(teks):
    # 1. Normalisasi: Case Folding
    teks = teks.lower()
    
    # 2. Text Cleaning: Derau HTML, URL, dan Simbol
    teks = re.sub(r'http\S+|www\S+|https\S+', '', teks, flags=re.MULTILINE)
    teks = re.sub(r'<.*?>', '', teks)
    teks = re.sub(r'[^a-z ]', ' ', teks) # Hanya menyisakan huruf alfabet
    teks = re.sub(r'\s+', ' ', teks).strip() # Merapikan spasi
    
    # 3. Normalisasi: Stopwords Removal
    teks = stopword.remove(teks)
    
    # 4. Normalisasi: Stemming (Mengubah ke kata dasar)
    teks = stemmer.stem(teks)
    
    return teks

print("\n3. Memulai proses Pembersihan, Stopword, dan STEMMING...")
print("PERINGATAN: Karena ada proses Stemming, ini bisa memakan waktu berjam-jam!")
df['isi_bersih'] = df['isi_berita'].progress_apply(bersihkan_teks)

print("\n4. Membersihkan kolom judul...")
df['judul_bersih'] = df['judul'].progress_apply(bersihkan_teks)

# ---------------------------------------------------------
# TAHAP 4: Data Ingestion Dataset Bersih ke SQLite
# ---------------------------------------------------------
print("\n5. Ingestion (Menyimpan) dataset bersih ke repositori SQLite...")
df.to_sql('artikel_bersih', conn, if_exists='replace', index=False)

conn.close()

print("\n==================================================")
print("selesai!")
print("==================================================")