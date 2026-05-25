import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# 1. Inisialisasi Database SQLite
conn = sqlite3.connect('surabaya_news_pipeline.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS url_queue (
        url TEXT PRIMARY KEY,
        tanggal TEXT,
        sumber TEXT,
        status TEXT DEFAULT 'PENDING'
    )
''')
conn.commit()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

print("=== MEMULAI PANEN URL DETIK SURABAYA (LOGIKA HALAMAN STABIL) ===")

start_page = 1
end_page = 1500 

for page in range(start_page, end_page + 1):
    url_tag = f"https://www.detik.com/tag/surabaya/?page={page}"
    
    try:
        # Request dengan timeout agar tidak menggantung jika internet putus
        response = requests.get(url_tag, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Halaman {page}: Skip (Status Code: {response.status_code})")
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        
        # Jika halaman benar-benar kosong/habis beritanya di server Detik
        if not articles:
            print(f"Halaman {page}: Sudah tidak ada artikel lagi di server. Berhenti.")
            break
            
        urls_found = 0
        
        for article in articles:
            link_tag = article.find('a', href=True)
            date_tag = article.find('span', class_='date') or article.find('div', class_='date')
            
            if link_tag:
                url = link_tag['href']
                raw_date = date_tag.text.strip() if date_tag else "Tidak Diketahui"
                
                # Simpan ke SQLite (INSERT OR IGNORE menjamin tidak ada duplikat)
                cursor.execute(
                    "INSERT OR IGNORE INTO url_queue (url, tanggal, sumber) VALUES (?, ?, ?)",
                    (url, raw_date, 'detikTagSurabaya')
                )
                urls_found += 1
                
        conn.commit() # Commit setiap selesai 1 halaman agar data aman tersimpan
        print(f"Halaman {page}/{end_page}: Sukses mengamankan {urls_found} URL. ({raw_date})")
        
    except Exception as e:
        print(f"Halaman {page}: Ada gangguan internet/teknis -> {e}")
        time.sleep(5) # Jika error, istirahat lebih lama sebelum mencoba lagi
        
    # Jeda 1.2 detik agar ramah pada server dan aman dari blokir
    time.sleep(1.2)

# Cek hasil akhir penutupan batch
cursor.execute("SELECT COUNT(*) FROM url_queue")
total_url = cursor.fetchone()[0]
print(f"\n=== PROSES SELESAI! Total URL Berhasil Diamankan: {total_url} URL ===")

conn.close()