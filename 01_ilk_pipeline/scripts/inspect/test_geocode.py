"""
Shapefile sütunlarını göster, sonra birkaç koordinatı test et.
"""
import geopandas as gpd
from shapely.geometry import Point

SHP = r"D:\_Development\Datasets\Turkey Shapefile\gadm41_TUR_shp\gadm41_TUR_1.shp"

# Shapefile'ı yükle
iller = gpd.read_file(SHP)
print("=== SÜTUNLAR ===")
print(iller.columns.tolist())
print(f"\nToplam il sayısı: {len(iller)}")
print("\n=== İLK 5 SATIR (ad sütunları) ===")
ad_sutunlari = [c for c in iller.columns if 'name' in c.lower() or 'NAME' in c]
print(iller[ad_sutunlari].head())

# Test koordinatları (merged CSV'den aldık)
test_noktalari = [
    ("0101 2km 143.xlsx - 01=Adana?",     37.8349,  35.40379),
    ("0103 291.xlsx - 01=Adana?",          36.43467, 35.15009),
    ("0201 3.xlsx - 02=Adıyaman?",         37.435578, 38.201192),
    ("0202 2KM 8.xlsx - 02=Adıyaman?",    37.425034, 38.213598),
    ("0904 67.xlsx - 09=Aydın? (şüpheli)", 31.541735, 28.340063),
    ("6335 3km 224.xlsx - 63=Şanlıurfa?", 27.160289, 38.932941),
]

print("\n=== KOORDINAT - IL TESTI ===")
print(f"{'Dosya':<45} {'Koordinat Il':<20}")
print("-" * 70)

for aciklama, lat, lon in test_noktalari:
    nokta = Point(lon, lat)  # shapely: (x=lon, y=lat)
    eslesme = iller[iller.geometry.contains(nokta)]
    if len(eslesme) > 0:
        il_adi = eslesme.iloc[0]['NAME_1']
    else:
        il_adi = "TÜRKİYE DIŞI"
    print(f"{aciklama:<45} {il_adi:<20}")
