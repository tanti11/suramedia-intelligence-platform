import sqlite3
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

DB_NAME = "surabaya_news_pipeline.db"
BASE_URL = "https://jatim.antaranews.com"
START_URL = "https://jatim.antaranews.com/kabar-jatim/surabaya"

# 1. Setup Database
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

# Bersihkan data Antara lama agar fresh saat ditarik ulang
cursor.execute("DELETE FROM url_queue WHERE sumber = 'AntaraSurabaya'")
conn.commit()

print("=== MEMULAI PANEN URL ANTARA SURABAYA (RENTANG DATA SKRIPSI) ===")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BULAN_INDO = {
    'januari': 1, 'februari': 2, 'maret': 3, 'april': 4, 'mei': 5, 'juni': 6,
    'juli': 7, 'agustus': 8, 'september': 9, 'oktober': 10, 'november': 11, 'desember': 12
}

def parsing_tanggal_pintar(text_date):
    """Mengubah format tanggal Antara menjadi objek datetime untuk filter presisi"""
    sekarang = datetime.now()
    text_clean = text_date.strip().lower()
    
    # 1. Handle format relatif seperti "11 jam lalu" atau "menit lalu"
    if "jam lalu" in text_clean or "menit lalu" in text_clean:
        return sekarang
        
    # 2. Handle format standar berita "16 mei 2026 19:59"
    parts = text_clean.split()
    if len(parts) >= 3:
        try:
            hari = int(parts[0])
            nama_bulan = parts[1]
            tahun = int(parts[2])
            
            if nama_bulan in BULAN_INDO:
                bulan = BULAN_INDO[nama_bulan]
                return datetime(tahun, bulan, hari)
        except ValueError:
            pass
            
    return None

# TENTUKAN BATAS PAGE (Sesuaikan range-nya, misal sampai page 300 atau lebih)
start_page = 1
end_page = 400 

# Batas filter tanggal (1 Jan 2025 - 30 April 2026)
batas_awal = datetime(2025, 1, 1)
batas_akhir = datetime(2026, 4, 30)

inserted = 0

for page in range(start_page, end_page + 1):
    current_url = START_URL if page == 1 else f"{START_URL}/{page}"
    
    try:
        response = requests.get(current_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"Halaman {page}: Skip/Habis (Status Code: {response.status_code})")
            break
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # TARGET SELEKTOR AMAN: Ambi list artikel utama, abaikan top-slider!
        main_container = soup.find("div", class_="wrapper__list__article")
        if not main_container:
            print(f"Halaman {page}: Struktur utama tidak ditemukan. Skip.")
            continue
            
        # Mengambil class card__post-list agar tidak bercampur dengan slider atau pop-up berita lama
        articles = main_container.find_all("div", class_="card__post-list")
        
        if not articles:
            print(f"Halaman {page}: Sudah tidak ada artikel list lagi. Selesai.")
            break
            
        urls_found_in_page = 0
        last_checked_date = "Tidak Diketahui"
        
        for article in articles:
            a_tag = article.find("a", href=True)
            if not a_tag:
                continue
                
            href = a_tag["href"].strip()
            if "/berita/" not in href and "/foto/" not in href:
                continue
                
            full_url = urljoin(BASE_URL, href).split("?")[0]
            
            # Ambil Tanggal Berita
            date_container = article.find("div", class_="card__post__author-info")
            date_text = ""
            if date_container:
                span_tag = date_container.find("span")
                if span_tag:
                    date_text = span_tag.text.strip()
            
            # Konversi tanggal ke bentuk objek datetime
            dt_artikel = parsing_tanggal_pintar(date_text)
            
            if dt_artikel:
                last_checked_date = dt_artikel.strftime("%Y-%m-%d")
                
                # FILTER KETAT: Hanya simpan jika masuk rentang 1 Jan 2025 s.d 30 April 2026
                if batas_awal <= dt_artikel <= batas_akhir:
                    cursor.execute("""
                        INSERT OR IGNORE INTO url_queue (url, tanggal, sumber)
                        VALUES (?, ?, ?)
                    """, (full_url, last_checked_date, "AntaraSurabaya"))
                    if cursor.rowcount > 0:
                        inserted += 1
                        urls_found_in_page += 1
            
        conn.commit()
        print(f"Halaman {page}/{end_page}: Sukses menyaring {urls_found_in_page} URL baru. Tanggal record terakhir: ({last_checked_date})")
        
    except Exception as e:
        print(f"Halaman {page}: Kendala teknis -> {e}")
        time.sleep(3)
        
    # Jeda ramah server
    time.sleep(1.2)

# Cek hasil akhir total database
cursor.execute("SELECT COUNT(*) FROM url_queue")
total_url = cursor.fetchone()[0]
print(f"\n=== PROSES SELESAI! Total Gabungan URL di DB saat ini: {total_url} URL ===")
print(f"Khusus AntaraSurabaya Baru Berhasil Ditambahkan: {inserted} URL")

conn.close()