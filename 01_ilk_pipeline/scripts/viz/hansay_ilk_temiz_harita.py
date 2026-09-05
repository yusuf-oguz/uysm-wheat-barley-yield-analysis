import pandas as pd, re
import folium
import branca.colormap as cm

with open(r"D:\_Development\Projects\UYSM_Projects\data\source\hansay_ilk.xls", "r", encoding="utf-8-sig") as f:
    hl = f.readline().rstrip("\n"); sl = f.readline().rstrip("\n")
colspecs = [(m.start(), m.end()) for m in re.finditer(r"-+", sl)]
cols = [hl[s:e].strip() or f"col_{i}" for i,(s,e) in enumerate(colspecs)]
df = pd.read_fwf(r"D:\_Development\Projects\UYSM_Projects\data\source\hansay_ilk.xls",
                 colspecs=colspecs, names=cols, skiprows=2, encoding="utf-8-sig")
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
df["lat"] = pd.to_numeric(df["Enlem_O"],  errors="coerce")
df["lon"] = pd.to_numeric(df["Boylam_O"], errors="coerce")
df["GercekVerim"] = pd.to_numeric(df["GercekVerim"], errors="coerce")
df["Bitki"] = df["Bitki"].str.lower().str.strip()

# Buğday + IQR filtresi
bugday = df[(df["Bitki"] == "bugday") & df["lat"].notna() & df["lon"].notna() & df["GercekVerim"].notna()].copy()
q1, q3 = bugday["GercekVerim"].quantile(0.25), bugday["GercekVerim"].quantile(0.75)
ust = q3 + 1.5 * (q3 - q1)
temiz = bugday[bugday["GercekVerim"] <= ust].copy()

print(f"Haritaya eklenecek: {len(temiz)} nokta  (anomali siniri: {ust:.0f} g/m2)")

# Google Maps sutunu
def gm(row):
    try:
        return str(row["Enlem"]).strip().rstrip('"') + '"N  ' + str(row["Boylam"]).strip().rstrip('"') + '"E'
    except: return ""
temiz["google_maps"] = temiz.apply(gm, axis=1)

vmin = temiz["GercekVerim"].quantile(0.02)
vmax = temiz["GercekVerim"].quantile(0.98)
colormap = cm.LinearColormap(
    colors=["#313695","#4575b4","#74add1","#abd9e9",
            "#fee090","#fdae61","#f46d43","#d73027","#a50026"],
    vmin=vmin, vmax=vmax,
    caption="Gercek Verim — bugday (g/m2)"
)

harita = folium.Map(location=[39.0, 35.0], zoom_start=6, tiles="CartoDB positron")
colormap.add_to(harita)

for _, row in temiz.iterrows():
    gv = row["GercekVerim"]
    popup_html = f"""
    <div style="font-family:monospace;font-size:12px;min-width:210px">
      <b>{str(row.get('DosyaAdi','')).strip()}</b><br>
      <hr style="margin:4px 0">
      Istasyon : {str(row.get('Istasyon','')).strip()}<br>
      Tarih    : {str(row.get('Tarih','')).strip()}<br>
      <hr style="margin:4px 0">
      <b>Gercek Verim : {gv:.1f} g/m2</b><br>
      <hr style="margin:4px 0">
      {row['google_maps']}
    </div>
    """
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color="white", weight=0.8,
        fill=True, fill_color=colormap(gv), fill_opacity=0.85,
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"{str(row.get('Istasyon','')).strip()} — {gv:.0f} g/m2"
    ).add_to(harita)

harita.save(r"D:\_Development\Projects\UYSM_Projects\output\maps\hansay_ilk_temiz_harita.html")
print("Kaydedildi: hansay_ilk_temiz_harita.html")
