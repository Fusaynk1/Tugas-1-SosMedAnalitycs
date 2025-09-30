import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

# URL dasar (Detik terkini)
base_url = "https://news.detik.com/terkini?page="

# Simpan hasil scraping
data = []

# Loop dari page 1 sampai 5
for page in range(1, 6):
    print(f"🔎 Scraping halaman {page}...")
    url = base_url + str(page)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = soup.find_all("article")
    
    for a in articles:
        title_tag = a.find("h2")
        title = title_tag.get_text(strip=True) if title_tag else None

        link = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else None
        
        content_tag = a.find("p")
        content = content_tag.get_text(strip=True) if content_tag else None

        time_tag = a.find("time")
        published = time_tag.get("datetime") if time_tag else None

        data.append({
            "title": title,
            "link": link,
            "content": content,
            "published": published
        })

    # Delay biar nggak dianggap spam server
    time.sleep(2)

# Export ke CSV
df = pd.DataFrame(data)
df.to_csv("berita_detik.csv", index=False, encoding="utf-8-sig")

# Export ke Excel
df.to_excel("berita_detik.xlsx", index=False)

# Export ke JSON
with open("berita_detik.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ Scraping selesai! Data disimpan ke CSV, Excel, dan JSON")
