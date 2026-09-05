"""
Koordinat geçerlilik haritası — turkey_stations_map.png için kaynak HTML.
Yeşil: geçerli koordinat, Kırmızı: geçersiz koordinat, Gri: koordinat yok/bozuk
"""

import pandas as pd
import folium

MERGED_CSV = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"
HTML_CIKTI = r"D:\_Development\Projects\UYSM_Projects\output\maps\turkey_validity_map.html"

df = pd.read_csv(MERGED_CSV)
print(f"{len(df)} satır yüklendi.")

harita = folium.Map(location=[39.0, 35.5], zoom_start=6, tiles="CartoDB positron")

sayaclar = {"green": 0, "red": 0, "gray": 0}

for _, row in df.iterrows():
    durum_val = str(row.get("veri_durumu", "")).strip().lower()

    if durum_val == "koordinat_yok" or (pd.isna(row["enlem"]) or pd.isna(row["boylam"])):
        sayaclar["gray"] += 1
        continue
    elif durum_val == "ulke_disi":
        renk = "red"
        durum = "Türkiye Dışı"
    else:
        renk = "green"
        durum = "Geçerli Koordinat"

    sayaclar[renk] += 1

    popup = (
        f"<b>{row['dosya_adi']}</b><br>"
        f"Enlem: {row['enlem']}<br>"
        f"Boylam: {row['boylam']}<br>"
        f"Durum: {durum}<br>"
        f"İl: {row.get('il_etiket', '-')}<br>"
        f"Bitki: {row.get('bitki_adi', '-')}"
    )

    folium.CircleMarker(
        location=[row["enlem"], row["boylam"]],
        radius=6,
        color=renk,
        fill=True,
        fill_color=renk,
        fill_opacity=0.8,
        popup=folium.Popup(popup, max_width=280),
        tooltip=str(row["dosya_adi"]),
    ).add_to(harita)

legend_html = """
<div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000;
     background: white; padding: 12px 16px; border: 1px solid #ccc;
     border-radius: 6px; font-size: 13px; line-height: 2;">
  <b>Coordinate Validity Status</b><br>
  <span style="color:green; font-size:16px;">&#9679;</span> Valid ({green} stations)<br>
  <span style="color:red;   font-size:16px;">&#9679;</span> Invalid ({red} stations)<br>
  <span style="color:gray;  font-size:16px;">&#9679;</span> No coordinates ({gray} stations)
</div>
""".format(**sayaclar)

harita.get_root().html.add_child(folium.Element(legend_html))
harita.save(HTML_CIKTI)

print(f"\nHarita kaydedildi: {HTML_CIKTI}")
print(f"  Yeşil  (geçerli)       : {sayaclar['green']}")
print(f"  Kırmızı (geçersiz)     : {sayaclar['red']}")
print(f"  Gri    (koordinat yok) : {sayaclar['gray']}")
