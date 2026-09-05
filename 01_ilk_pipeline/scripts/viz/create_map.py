"""
UYSM koordinatlarını interaktif harita olarak görselleştirir.
Çıktı 1: UYSM_harita.html  (Folium - tarayıcıda açılır)
Çıktı 2: UYSM_googlemymaps.csv  (Google My Maps için)

Renk kodları:
  Yeşil  : Türkiye içinde, buffersız eşleşme
  Turuncu: Türkiye içinde, sadece buffer ile yakalanan (kıyı/sınır)
  Kırmızı: Buffer sonrası da Türkiye dışı
  Gri    : Koordinat yok/bozuk
"""

import pandas as pd
import folium

MERGED_CSV = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"
HTML_CIKTI = r"D:\_Development\Projects\UYSM_Projects\output\maps\UYSM_harita.html"
CSV_CIKTI  = r"D:\_Development\Projects\UYSM_Projects\output\maps\UYSM_googlemymaps.csv"


def nokta_kategorisi(row):
    """Her koordinat için renk ve kategori belirler."""
    if pd.isna(row["enlem"]) or pd.isna(row["boylam"]):
        return "gri", "Koordinat Yok"

    bs  = row["il_koordinat_buffersiz"]
    bl  = row["il_koordinat_bufferli"]

    if bs == "Koordinat Yok":
        return "gri", "Koordinat Yok"
    elif bs != "Turkiye Disi":
        return "green", f"Turkiye ici ({bs})"
    elif bl != "Turkiye Disi":
        return "orange", f"Sinir/Kiyi ({bl})"
    else:
        return "red", "Turkiye Disi"


def popup_metni(row):
    """Harita üzerinde tıklandığında gösterilecek bilgi."""
    return (
        f"<b>{row['dosya_adi']}</b><br>"
        f"Enlem: {row['enlem']}<br>"
        f"Boylam: {row['boylam']}<br>"
        f"Il (buffersiz): {row['il_koordinat_buffersiz']}<br>"
        f"Il (bufferli): {row['il_koordinat_bufferli']}<br>"
        f"Il etiket: {row['il_etiket']}<br>"
        f"Dane agirlik (hesap): {row['dane_m2_hesap_gram']} g/m2<br>"
        f"Bitki: {row['bitki_adi']}"
    )


# --- Yükle ---
df = pd.read_csv(MERGED_CSV)
print(f"{len(df)} satir yuklendi.")

# --- Folium haritası ---
harita = folium.Map(
    location=[39.0, 35.0],
    zoom_start=6,
    tiles="OpenStreetMap"
)

# Renk sayaçları
sayaclar = {"green": 0, "orange": 0, "red": 0, "gri": 0}

for _, row in df.iterrows():
    renk, kategori = nokta_kategorisi(row)
    sayaclar[renk] += 1

    if pd.isna(row["enlem"]) or pd.isna(row["boylam"]):
        continue  # Koordinatsızları haritaya ekleyemeyiz

    folium.CircleMarker(
        location=[row["enlem"], row["boylam"]],
        radius=6,
        color=renk,
        fill=True,
        fill_color=renk,
        fill_opacity=0.8,
        popup=folium.Popup(popup_metni(row), max_width=300),
        tooltip=row["dosya_adi"],
    ).add_to(harita)

# Legend (sağ alt köşe)
legend_html = """
<div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000;
     background: white; padding: 12px; border: 1px solid #ccc;
     border-radius: 6px; font-size: 13px; line-height: 1.8;">
  <b>Koordinat Durumu</b><br>
  <span style="color:green;">&#9679;</span> Turkiye ici ({green})<br>
  <span style="color:orange;">&#9679;</span> Sinir/Kiyi - buffer ({orange})<br>
  <span style="color:red;">&#9679;</span> Turkiye disi ({red})<br>
  <span style="color:gray;">&#9679;</span> Koordinat yok ({gri})
</div>
""".format(**sayaclar)

harita.get_root().html.add_child(folium.Element(legend_html))
harita.save(HTML_CIKTI)
print(f"Harita kaydedildi: {HTML_CIKTI}")

# --- Google My Maps CSV ---
gmaps_df = df[[
    "dosya_adi", "enlem", "boylam",
    "il_etiket", "il_koordinat_buffersiz", "il_koordinat_bufferli",
    "bitki_adi", "dane_m2_hesap_gram", "dane_m2_gercek_gram"
]].copy()

gmaps_df.columns = [
    "Dosya Adi", "Latitude", "Longitude",
    "Il Etiket", "Il Buffersiz", "Il Bufferli",
    "Bitki", "Dane Agirlik Hesap g_m2", "Dane Agirlik Gercek g_m2"
]

# Kategori sütunu ekle (My Maps'te renklendirme için)
gmaps_df["Kategori"] = df.apply(
    lambda r: nokta_kategorisi(r)[1], axis=1
)

gmaps_df.to_csv(CSV_CIKTI, index=False, encoding="utf-8-sig")
print(f"Google My Maps CSV kaydedildi: {CSV_CIKTI}")

# --- Özet ---
print(f"\nToplam nokta: {len(df)}")
print(f"  Yeşil  (Turkiye ici)   : {sayaclar['green']}")
print(f"  Turuncu (sinir/kiyi)   : {sayaclar['orange']}")
print(f"  Kirmizi (Turkiye disi) : {sayaclar['red']}")
print(f"  Gri    (koordinat yok) : {sayaclar['gri']}")
