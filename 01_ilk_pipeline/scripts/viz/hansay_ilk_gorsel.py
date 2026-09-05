"""
hansay_ilk.xls -> Folium harita + Google Maps CSV
"""
import pandas as pd, re
import folium
import branca.colormap as cm

# ── Veriyi oku ────────────────────────────────────────────────────────────────
with open(r"D:\_Development\Projects\UYSM_Projects\data\source\hansay_ilk.xls", "r", encoding="utf-8-sig") as f:
    hl = f.readline().rstrip("\n")
    sl = f.readline().rstrip("\n")

colspecs = [(m.start(), m.end()) for m in re.finditer(r"-+", sl)]
cols = [hl[s:e].strip() or f"col_{i}" for i,(s,e) in enumerate(colspecs)]

df = pd.read_fwf(r"D:\_Development\Projects\UYSM_Projects\data\source\hansay_ilk.xls",
                 colspecs=colspecs, names=cols, skiprows=2, encoding="utf-8-sig")
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

df["lat"] = pd.to_numeric(df["Enlem_O"],  errors="coerce")
df["lon"] = pd.to_numeric(df["Boylam_O"], errors="coerce")

# ── Google Maps sutunu ────────────────────────────────────────────────────────
def google_maps_fmt(row):
    try:
        e = str(row["Enlem"]).strip().rstrip('"')  + '"N'
        b = str(row["Boylam"]).strip().rstrip('"') + '"E'
        return f"{e} {b}"
    except:
        return ""

df["google_maps"] = df.apply(google_maps_fmt, axis=1)

# CSV kaydet
csv_cols = ["ID","DosyaAdi","Istasyon","Tarih","Bitki",
            "Enlem","Boylam","Enlem_O","Boylam_O","google_maps","GercekVerim"]
mevcut = [c for c in csv_cols if c in df.columns]
df[mevcut].to_csv(r"D:\_Development\Projects\UYSM_Projects\data\processed\hansay_ilk_koordinatlar.csv",
                  index=False, encoding="utf-8-sig")
print(f"CSV: {len(df)} satir kaydedildi.")

# ── Folium harita ─────────────────────────────────────────────────────────────
df_h = df[df["lat"].notna() & df["lon"].notna()].copy()
df_h["GercekVerim"] = pd.to_numeric(df_h["GercekVerim"], errors="coerce")
df_renk = df_h[df_h["GercekVerim"].notna()].copy()

vmin = df_renk["GercekVerim"].quantile(0.02)
vmax = df_renk["GercekVerim"].quantile(0.98)
colormap = cm.LinearColormap(
    colors=["#313695","#4575b4","#74add1","#abd9e9",
            "#fee090","#fdae61","#f46d43","#d73027","#a50026"],
    vmin=vmin, vmax=vmax,
    caption="Gercek Verim (g/m2)"
)

harita = folium.Map(location=[39.0, 35.0], zoom_start=6, tiles="CartoDB positron")
colormap.add_to(harita)

for _, row in df_h.iterrows():
    gv = row["GercekVerim"]
    renk = colormap(gv) if pd.notna(gv) else "#888888"

    popup_html = f"""
    <div style="font-family:monospace;font-size:12px;min-width:210px">
      <b>{str(row.get('DosyaAdi','')).strip()}</b><br>
      <hr style="margin:4px 0">
      Istasyon : {str(row.get('Istasyon','')).strip()}<br>
      Tarih    : {str(row.get('Tarih','')).strip()}<br>
      Bitki    : {str(row.get('Bitki','')).strip()}<br>
      <hr style="margin:4px 0">
      <b>Gercek Verim : {f"{gv:.1f} g/m2" if pd.notna(gv) else "—"}</b><br>
      <hr style="margin:4px 0">
      {row['google_maps']}
    </div>
    """
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color="white", weight=0.8,
        fill=True, fill_color=renk, fill_opacity=0.85,
        popup=folium.Popup(popup_html, max_width=260),
        tooltip=f"{str(row.get('Istasyon','')).strip()} — {f'{gv:.0f} g/m2' if pd.notna(gv) else '?'}"
    ).add_to(harita)

harita.save(r"D:\_Development\Projects\UYSM_Projects\output\maps\hansay_ilk_harita.html")
print(f"Harita: {len(df_h)} nokta kaydedildi.")
