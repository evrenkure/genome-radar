import pandas as pd
import os

# --- GÜVENLİK KONTROLÜ ---
if os.path.exists("makaleler.xlsx"):
    print("⚠️ DİKKAT: 'makaleler.xlsx' zaten var! Eski verilerinin silinmemesi için işlem İPTAL EDİLDİ.")
    print("Yeni makaleleri eklemek için lütfen doğrudan Excel dosyasını açıp düzenleyin.")
else:
    # Dosya yoksa ilk kez oluşturur (Güvenli Alan)
    ILK_VERILER = [
        {
            "gen": "TP53, BRCA1",
            "mutasyon": "Exon 5",
            "metot": "In Vitro",
            "skor": "8/10",
            "orijinal_baslik": "A novel compound overcoming cisplatin resistance in lung cancer...",
            "link": "https://pubmed.ncbi.nlm.nih.gov/",
            "mikro_ozet": "Buraya yazdığın eski özet duruyor, Excel'de bunu göreceksin."
        }
    ]
    df = pd.DataFrame(ILK_VERILER)
    df.to_excel("makaleler.xlsx", index=False, engine="openpyxl")
    print("🎯 İlk Excel dosyası sıfırdan temizce kuruldu!")