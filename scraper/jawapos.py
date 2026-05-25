import sqlite3
import time
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# 1. Setup Database
DB_NAME = "surabaya_news_pipeline.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS url_queue (
    url TEXT PRIMARY KEY,
    tanggal TEXT,
    sumber TEXT,
    status TEXT DEFAULT 'PENDING'
)
""")
conn.commit()

print("=== MEMULAI PANEN URL JAWA POS VIA NEXT.JS HYBRID ===")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

batas_awal = datetime(2025, 1, 1)
batas_akhir = datetime(2026, 4, 30)

start_page = 1
end_page = 500  

for page in range(start_page, end_page + 1):
    url = f"https://www.jawapos.com/surabaya-raya?page={page}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        next_data_script = soup.find('script', id='__NEXT_DATA__')
        
        if not next_data_script or not next_data_script.string:
            print(f"Halaman {page}: Script Next.js kosong/tidak ditemukan. Selesai.")
            break
            
        data = json.loads(next_data_script.string)
        
        try:
            articles = data['props']['pageProps']['dataCategory']['articles']['data']
        except KeyError:
            print(f"Halaman {page}: Struktur JSON habis/berbeda. Selesai.")
            break
            
        if not articles:
            print(f"Halaman {page}: Artikel kosong. Selesai.")
            break

        page_saved_count = 0
        last_date = "Tidak Diketahui"
        sudah_lewat_batas = False
        
        for item in articles:
            # --- PERBAIKAN PENCARIAN URL ---
            # Kita coba tangkap format 'url', 'link', atau rakit manual jika yang ada hanya 'slug'
            full_url = item.get('url') or item.get('link')
            if not full_url and item.get('slug'):
                # Format Jawa Pos: https://www.jawapos.com/surabaya-raya/[ID]/[slug]
                article_id = item.get('id', '')
                slug = item.get('slug', '')
                full_url = f"https://www.jawapos.com/surabaya-raya/{article_id}/{slug}"
                
            raw_date = item.get('published_at') 
            
            # Jika masih kosong, lewati artikel ini
            if not full_url or not raw_date:
                continue
                
            # --- PERBAIKAN PARSING TANGGAL ---
            # Menghindari crash jika format string tiba-tiba berubah
            last_date = str(raw_date)[:10] 
            try:
                dt_artikel = datetime.strptime(last_date, "%Y-%m-%d")
            except ValueError:
                # Jika gagal diparsing (misal format "18 Mei 2026"), biarkan dt_artikel kosong
                dt_artikel = None
            
            if dt_artikel:
                # Cek apakah sudah tembus ke tahun 2024
                if dt_artikel < batas_awal:
                    sudah_lewat_batas = True
                    continue
                    
                # Filter rentang skripsi
                if batas_awal <= dt_artikel <= batas_akhir:
                    cursor.execute("""
                        INSERT OR IGNORE INTO url_queue (url, tanggal, sumber)
                        VALUES (?, ?, ?)
                    """, (full_url, last_date, "JawaPosSurabaya"))
                    
                    if cursor.rowcount > 0:
                        page_saved_count += 1
            else:
                # Jika tanggal gagal diparsing, simpan saja untuk jaga-jaga
                cursor.execute("""
                    INSERT OR IGNORE INTO url_queue (url, tanggal, sumber)
                    VALUES (?, ?, ?)
                """, (full_url, last_date, "JawaPosSurabaya"))
                if cursor.rowcount > 0:
                    page_saved_count += 1
                    
        conn.commit()
        print(f"Halaman {page}: Sukses menyaring {page_saved_count} URL. (Record terakhir: {last_date})")
        
        if sudah_lewat_batas and page_saved_count == 0:
            print(f"\n[INFO] Berita Halaman {page} sudah sepenuhnya di bawah 1 Januari 2025.")
            print("Proses panen Jawa Pos dihentikan karena target sudah terpenuhi.")
            break

    except Exception as e:
        # Menangkap error jenis apa pun agar perulangan tidak langsung crash mati total
        print(f"Halaman {page}: Mengalami Error -> {e}")
        time.sleep(3)
        
    time.sleep(1.2)

cursor.execute("SELECT sumber, COUNT(*) FROM url_queue GROUP BY sumber")
summary = cursor.fetchall()
print("\n=== REKAP DATA PIPELINE SAAT INI ===")
for sumber, jumlah in summary:
    print(f"- {sumber}: {jumlah} URL")

conn.close()