"""
hansay.xlsx → Folium harita + Google Maps CSV
"""
import pandas as pd
import folium
import branca.colormap as cm

# ── Veriyi oku (satir 1 sahte baslik, satir 2 gercek baslik) ─────────────────
df_raw = pd.read_excel(r"D:\_Development\Projects\UYSM_Projects\data\source\hansay.xlsx", header=1)
df = df_raw.copy()

# Sutun adlarini temizle
df.columns = [c.strip() for c in df.columns]
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# Koordinat sutunlari
df["lat"] = pd.to_numeric(df["Enlem_O"], errors="coerce")
df["lon"] = pd.to_numeric(df["Boylam_O"], errors="coerce")

# Google Maps sutunu: mevcut DMS + N/E eki
def google_maps_fmt(row):
    try:
        enlem  = str(row["Enlem"]).strip().rstrip('"') + '"N'
        boylam = str(row["Boylam"]).strip().rstrip('"') + '"E'
        return f"{enlem} {boylam}"
    except:
        return ""

df["google_maps"] = df.apply(google_maps_fmt, axis=1)

# CSV kaydet
csv_cols = ["ID", "DosyaAdi", "Istasyon", "Tarih", "Bitki",
            "Enlem", "Boylam", "Enlem_O", "Boylam_O", "google_maps"]
mevcut = [c for c in csv_cols if c in df.columns]
df[mevcut].to_csv(r"D:\_Development\Projects\UYSM_Projects\data\processed\hansay_koordinatlar.csv",
                  index=False, encoding="utf-8-sig")
print(f"CSV kaydedildi: {len(df)} satir")

# ── Folium harita ─────────────────────────────────────────────────────────────
df_harita = df[df["lat"].notna() & df["lon"].notna()].copy()

# Renk skalasi: GercekVerim sutunu varsa onu kullan
renk_sutun = "GercekVerim" if "GercekVerim" in df.columns else None
if renk_sutun:
    df_harita[renk_sutun] = pd.to_numeric(df_harita[renk_sutun], errors="coerce")
    df_harita = df_harita[df_harita[renk_sutun].notna()]
    vmin = df_harita[renk_sutun].quantile(0.02)
    vmax = df_harita[renk_sutun].quantile(0.98)
    colormap = cm.LinearColormap(
        colors=["#313695","#4575b4","#74add1","#abd9e9",
                "#fee090","#fdae61","#f46d43","#d73027","#a50026"],
        vmin=vmin, vmax=vmax,
        caption="Gercek Verim (g/m2)"
    )

harita = folium.Map(location=[39.0, 35.0], zoom_start=6, tiles="CartoDB positron")
if renk_sutun:
    colormap.add_to(harita)

for _, row in df_harita.iterrows():
    if renk_sutun:
        renk = colormap(row[renk_sutun])
        tooltip_val = f"{row[renk_sutun]:.0f} g/m2"
    else:
        renk = "#2E86AB"
        tooltip_val = ""

    popup_html = f"""
    <div style="font-family:monospace;font-size:12px;min-width:210px">
      <b>{str(row.get('DosyaAdi','')).strip()}</b><br>
      <hr style="margin:4px 0">
      Istasyon : {str(row.get('Istasyon','')).strip()}<br>
      Tarih    : {str(row.get('Tarih','')).strip()}<br>
      Bitki    : {str(row.get('Bitki','')).strip()}<br>
      <hr style="margin:4px 0">
      <b>Gercek Verim : {f"{row[renk_sutun]:.1f} g/m2" if renk_sutun else "—"}</b><br>
      <hr style="margin:4px 0">
      Koordinat : {row['lat']:.5f}, {row['lon']:.5f}<br>
      Google Maps: {row['google_maps']}
    </div>
    """

    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=6,
        color="white", weight=0.8,
        fill=True, fill_color=renk, fill_opacity=0.85,
        popup=folium.Popup(popup_html, max_width=270),
        tooltip=f"{str(row.get('Istasyon','')).strip()} — {tooltip_val}"
    ).add_to(harita)

harita.save(r"D:\_Development\Projects\UYSM_Projects\output\maps\hansay_harita.html")
print(f"Harita kaydedildi: {len(df_harita)} nokta")
