import sqlite3
import pandas as pd
from textblob import TextBlob
from tqdm import tqdm
import os

DB_NAME = "surabaya_news_pipeline.db"

print("=== MEMULAI AUTOMATED SENTIMENT LABELLING (LEXICON INDONESIA) ===")

if not os.path.exists(DB_NAME):
    print(f"[ERROR] Database {DB_NAME} tidak ditemukan!")
    exit()

conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT url, sumber, tanggal_final, judul_bersih, isi_bersih FROM artikel_bersih", conn)

print(f"Total data yang akan dilabeli: {len(df)} artikel.")

# Kamus kata kunci sederhana untuk memperkuat deteksi sentimen khas berita kota (Surabaya)
kata_positif = {'aman', 'sukses', 'prestasi', 'juara', 'bantu', 'membangun', 'bagus', 'lancar', 'menang', 'puji', 'sinergi', 'optimal', 'bersih', 'sehat', 'revitalisasi', 'ramah', 'indah', 'inovasi'}
kata_negatif = {'macet', 'banjir', 'kriminal', 'maling', 'jambret', 'rugi', 'rusak', 'korban', 'tewas', 'kecelakaan', 'demo', 'kecewa', 'gagal', 'kumuh', 'sengketa', 'ditangkap', 'korupsi', 'becek', 'resah'}

hasil_sentimen = []
skor_sentimen = []

print("\nMengeksekusi analisis sentimen cepat...")
for teks in tqdm(df['isi_bersih'], desc="Lexicon Processing"):
    if not teks or len(str(teks).strip()) == 0:
        hasil_sentimen.append("Netral")
        skor_sentimen.append(0.0)
        continue
    
    teks_str = str(teks).lower()
    
    # 1. Hitung skor dasar menggunakan TextBlob
    blob = TextBlob(teks_str)
    score = blob.sentiment.polarity  # default nilainya -1 sampai 1
    
    # 2. Hitung kecenderungan berdasarkan Kamus Lokal (BoW Sentiment)
    words = teks_str.split()
    pos_count = sum(1 for word in words if word in kata_positif)
    neg_count = sum(1 for word in words if word in kata_negatif)
    
    # Gabungkan score TextBlob dengan bobot kamus lokal
    total_score = score + (pos_count * 0.1) - (neg_count * 0.1)
    
    # Tentukan Label
    if total_score > 0.05:
        label = "Positif"
    elif total_score < -0.05:
        label = "Negatif"
    else:
        label = "Netral"
        
    hasil_sentimen.append(label)
    skor_sentimen.append(round(total_score, 4))

# 3. Gabungkan Hasil ke DataFrame
df['sentimen'] = hasil_sentimen
df['skor_kepercayaan'] = skor_sentimen

# Hitung sebaran untuk laporan bimbingan
print("\nHasil Sebaran Sentimen Berita:")
print(df['sentimen'].value_counts())

# 4. Simpan ke Tabel Baru di Database: 'artikel_berlabel'
print("\nMenyimpan hasil pelabelan otomatis ke tabel 'artikel_berlabel'...")
df.to_sql('artikel_berlabel', conn, if_exists='replace', index=False)
conn.close()

print("==================================================")
print("PROSES PELABELAN SELESAI DENGAN METODE LEXICON V2!")
print("Tabel 'artikel_berlabel' siap digunakan untuk Dashboard.")
print("==================================================")