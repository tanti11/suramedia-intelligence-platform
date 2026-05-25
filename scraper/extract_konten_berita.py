import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import random

DB_NAME = "surabaya_news_pipeline.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Buat tabel baru untuk menampung isi berita
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artikel_berita (
        url TEXT PRIMARY KEY,
        sumber TEXT,
        tanggal TEXT,
        judul TEXT,
        penulis TEXT,
        isi_berita TEXT,
        tags TEXT,
        FOREIGN KEY(url) REFERENCES url_queue(url)
    )
    """)
    conn.commit()
    return conn, cursor

def bersihkan_teks(teks):
    if not teks:
        return ""
    # Hapus spasi berlebih dan enter ganda
    return " ".join(teks.strip().split())

def scrape_artikel(url, sumber):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return None
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        judul = ""
        penulis = ""
        isi = ""
        tags = []

        # ==========================================
        # LOGIKA EKSTRAKSI BERDASARKAN SUMBER
        # (Tag HTML disesuaikan dengan struktur umum media)
        # ==========================================
        
        if "detik" in sumber.lower():
            judul_el = soup.find('h1', class_='detail__title')
            judul = judul_el.get_text() if judul_el else ""
            
            penulis_el = soup.find('div', class_='detail__author')
            penulis = penulis_el.get_text() if penulis_el else ""
            
            # Ambil semua paragraf dalam body teks
            body = soup.find('div', class_='detail__body-text')
            if body:
                paragraf = body.find_all('p')
                isi = " ".join([p.get_text() for p in paragraf])
                
            tags_el = soup.find_all('a', class_='nav__item')
            tags = [t.get_text().strip() for t in tags_el]

        elif "antara" in sumber.lower():
            judul_el = soup.find('h1', class_='post-title')
            judul = judul_el.get_text() if judul_el else ""
            
            # Antara kadang menaruh penulis di span atau strong awal paragraf
            penulis = "Tim Antara" 
            
            body = soup.find('div', class_='post-content')
            if body:
                isi = body.get_text(separator=" ")
                
            tags_el = soup.find_all('ul', class_='tags')
            if tags_el:
                tags = [t.get_text().strip() for t in tags_el[0].find_all('li')]

        elif "jawapos" in sumber.lower():
            judul_el = soup.find('h1')
            judul = judul_el.get_text() if judul_el else ""
            
            # JawaPos modern menggunakan div class tertentu untuk isi
            body = soup.find('div', class_=lambda x: x and ('content' in x.lower() or 'article' in x.lower()))
            if body:
                paragraf = body.find_all('p')
                isi = " ".join([p.get_text() for p in paragraf])
            
            # Jika isi gagal didapat dengan cara di atas
            if not isi:
                paragraf = soup.find_all('p')
                isi = " ".join([p.get_text() for p in paragraf[:15]]) # Ambil 15 paragraf pertama sbg safety

        # Membersihkan teks final
        return {
            "judul": bersihkan_teks(judul),
            "penulis": bersihkan_teks(penulis),
            "isi_berita": bersihkan_teks(isi),
            "tags": ", ".join(tags)
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# ==========================================
# MAIN EXECUTION
# ==========================================
conn, cursor = setup_database()

# Ambil URL yang statusnya masih PENDING
cursor.execute("SELECT url, sumber, tanggal FROM url_queue WHERE status = 'PENDING'")
antrian = cursor.fetchall()
total_antrian = len(antrian)

print(f"=== MEMULAI EKSTRAKSI {total_antrian} ARTIKEL ===")

sukses = 0
gagal = 0

for index, (url, sumber, tanggal) in enumerate(antrian, 1):
    print(f"[{index}/{total_antrian}] Scraping: {url[:60]}...")
    
    hasil = scrape_artikel(url, sumber)
    
    if hasil and hasil['isi_berita']: # Pastikan isinya tidak kosong
        # Masukkan ke tabel artikel_berita
        cursor.execute("""
            INSERT OR REPLACE INTO artikel_berita (url, sumber, tanggal, judul, penulis, isi_berita, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (url, sumber, tanggal, hasil['judul'], hasil['penulis'], hasil['isi_berita'], hasil['tags']))
        
        # Update status di url_queue menjadi DONE
        cursor.execute("UPDATE url_queue SET status = 'DONE' WHERE url = ?", (url,))
        
        sukses += 1
    else:
        # Jika gagal diakses atau teks kosong, tandai error agar bisa dicek nanti
        cursor.execute("UPDATE url_queue SET status = 'ERROR' WHERE url = ?", (url,))
        gagal += 1
        
    if index % 10 == 0:
        conn.commit()
        
    # Jeda acak 1 - 2.5 detik agar server berita tidak memblokir IP 
    time.sleep(random.uniform(1.0, 2.5))

conn.commit()
conn.close()

print("\n" + "=" * 50)
print("EKSTRAKSI SELESAI!")
print(f"Berhasil: {sukses} | Gagal/Kosong: {gagal}")
print("=" * 50)