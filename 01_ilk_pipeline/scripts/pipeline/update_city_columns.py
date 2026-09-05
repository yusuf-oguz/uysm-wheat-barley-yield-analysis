"""
Merged CSV'yi günceller:
  - il_koordinat_buffersiz : mevcut il_koordinat (shapefile tam sınır)
  - il_koordinat_bufferli  : ~11 km buffer uygulanmış shapefile ile bulunan il
  - il_uyusum              : il_etiket, buffersiz VEYA bufferli sonuçtan biriyle eşleşiyorsa True
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

MERGED_CSV = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"
SHP_L1     = r"D:\_Development\Datasets\Turkey Shapefile\gadm41_TUR_shp\gadm41_TUR_1.shp"
CIKTI      = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"

BUFFER_DERECE = 0.10  # ~11 km (Türkiye enlemlerinde)


def nokta_il_bul(gdf, lon, lat):
    """Koordinatın düştüğü ili döner. Eşleşme yoksa 'Turkiye Disi'."""
    if pd.isna(lon) or pd.isna(lat):
        return "Koordinat Yok"
    try:
        nokta = Point(float(lon), float(lat))
        eslesme = gdf[gdf.geometry.contains(nokta)]
        if len(eslesme) > 0:
            return eslesme.iloc[0]["NAME_1"]
        return "Turkiye Disi"
    except Exception:
        return "Hata"


def normalize(s):
    return str(s).lower().strip()


# --- Yükle ---
print("Shapefile yukleniyor...")
iller = gpd.read_file(SHP_L1)

print("Buffer uygulanıyor (%.2f derece)..." % BUFFER_DERECE)
iller_bufferli = iller.copy()
iller_bufferli["geometry"] = iller_bufferli.geometry.buffer(BUFFER_DERECE)

print("Merged CSV yukleniyor...")
df = pd.read_csv(MERGED_CSV)
print(f"  {len(df)} satir yuklendi.")

# --- Hesapla ---
print("Buffersiz eslesme yapiliyor...")
buffersiz = []
for _, row in df.iterrows():
    buffersiz.append(nokta_il_bul(iller, row["boylam"], row["enlem"]))

print("Bufferli eslesme yapiliyor...")
bufferli = []
for i, row in df.iterrows():
    il = nokta_il_bul(iller_bufferli, row["boylam"], row["enlem"])
    bufferli.append(il)
    if (i + 1) % 50 == 0:
        print(f"  {i+1}/{len(df)} islendi...")

df["il_koordinat_buffersiz"] = buffersiz
df["il_koordinat_bufferli"]  = bufferli

# il_uyusum: il_etiket, iki sonuçtan biriyle eşleşiyorsa True
df["il_uyusum"] = df.apply(
    lambda r: (
        normalize(r["il_etiket"]) == normalize(r["il_koordinat_buffersiz"]) or
        normalize(r["il_etiket"]) == normalize(r["il_koordinat_bufferli"])
    ),
    axis=1
)

# Eski il_koordinat sütununu kaldır (artık ikiye ayrıldı)
if "il_koordinat" in df.columns:
    df.drop(columns=["il_koordinat"], inplace=True)

# --- Özet ---
print("\n=== OZET ===")
print(f"Toplam: {len(df)}")

disi_buffersiz = (df["il_koordinat_buffersiz"] == "Turkiye Disi").sum()
disi_bufferli  = (df["il_koordinat_bufferli"]  == "Turkiye Disi").sum()
koord_yok      = (df["il_koordinat_buffersiz"] == "Koordinat Yok").sum()

print(f"Koordinat yok              : {koord_yok}")
print(f"Turkiye disi (buffersiz)   : {disi_buffersiz}")
print(f"Turkiye disi (bufferli)    : {disi_bufferli}")
print(f"  -> Buffer ile kurtarilan : {disi_buffersiz - disi_bufferli}")
print(f"Il uyusum True             : {df['il_uyusum'].sum()}")

print("\n=== BUFFER ILE KURTARILAN KOORDINATLAR ===")
kurtarilan = df[
    (df["il_koordinat_buffersiz"] == "Turkiye Disi") &
    (df["il_koordinat_bufferli"]  != "Turkiye Disi")
][["dosya_adi", "enlem", "boylam", "il_koordinat_bufferli"]]
print(kurtarilan.to_string(index=False))

print("\n=== BUFFERLI DE TURKIYE DISI KALANLAR ===")
hala_disi = df[
    (df["il_koordinat_bufferli"] == "Turkiye Disi") &
    (df["il_koordinat_buffersiz"] != "Koordinat Yok")
][["dosya_adi", "enlem", "boylam"]]
print(hala_disi.to_string(index=False))

# --- Kaydet ---
df.to_csv(CIKTI, index=False, encoding="utf-8-sig")
print(f"\nDosya guncellendi: {CIKTI}")
