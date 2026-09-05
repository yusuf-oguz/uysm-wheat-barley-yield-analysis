"""
hansay_processed_v2.10.csv — tüm koordinatları interaktif HTML haritasına döker.
Hover: il_koordinat_final + dosya adı + bitki.
Renk: bugday=mavi, arpa=turuncu, koordinat_gecerli=False -> kırmızı.
Çıktı: output/maps/koordinat_harita_v2_10.html
"""

import pandas as pd
import folium

GIRDI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v2.10.csv"
)
CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\output\maps\koordinat_harita_v2_10.html"
)

df = pd.read_csv(GIRDI, encoding="utf-8-sig")

gecersiz = df[df["koordinat_gecerli"].astype(str) == "False"]
if len(gecersiz):
    print(f"UYARI: {len(gecersiz)} satir koordinat_gecerli=False, haritaya eklenmiyor:")
    print(gecersiz[["dosya_adi__dosyaadi", "koordinat_gecersiz_neden"]].to_string(index=False))

df_harita = df[df["koordinat_gecerli"].astype(str) == "True"].copy()
print(f"Haritaya eklenecek nokta: {len(df_harita)}")

RENKLER = {"bugday": "blue", "arpa": "orange"}

m = folium.Map(location=[38.5, 35.0], zoom_start=6, tiles="CartoDB positron")

for _, row in df_harita.iterrows():
    bitki = str(row.get("bitki_adi__C9", "")).strip()
    renk = RENKLER.get(bitki, "gray")
    tooltip = f"{row['dosya_adi__dosyaadi']} | {row['il_koordinat_final']} | {bitki}"

    folium.CircleMarker(
        location=[row["enlem_dd_final"], row["boylam_dd_final"]],
        radius=5,
        color=renk,
        fill=True,
        fill_color=renk,
        fill_opacity=0.7,
        tooltip=tooltip,
    ).add_to(m)

legend = """
<div style="position:fixed;bottom:30px;left:30px;z-index:1000;
            background:white;padding:10px;border-radius:6px;
            border:1px solid #ccc;font-size:13px;">
  <b>Bitki</b><br>
  <span style="color:blue;">●</span> bugday<br>
  <span style="color:orange;">●</span> arpa<br>
  <br><i>Kaynak: v2.10</i>
</div>
"""
m.get_root().html.add_child(folium.Element(legend))

m.save(CIKTI)
print(f"Harita kaydedildi: {CIKTI}")
