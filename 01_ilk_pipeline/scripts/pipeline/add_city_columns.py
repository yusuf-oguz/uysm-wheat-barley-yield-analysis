"""
Merged CSV'ye iki il sütunu ekler:
  - il_etiket : dosya adındaki 2 haneli il kodundan gelen il adı
  - il_koordinat : koordinatın shapefile üzerinde denk geldiği il
  - il_uyusum : eşleşip eşleşmediği
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

MERGED_CSV = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"
SHP        = r"D:\_Development\Datasets\Turkey Shapefile\gadm41_TUR_shp\gadm41_TUR_1.shp"
CIKTI      = r"D:\_Development\Projects\UYSM_Projects\data\processed\UYSM_merged.csv"

# Türkiye resmi il kodları (01-81)
IL_KODLARI = {
    "01": "Adana",        "02": "Adiyaman",     "03": "Afyonkarahisar",
    "04": "Agri",         "05": "Amasya",        "06": "Ankara",
    "07": "Antalya",      "08": "Artvin",        "09": "Aydin",
    "10": "Balikesir",    "11": "Bilecik",       "12": "Bingol",
    "13": "Bitlis",       "14": "Bolu",          "15": "Burdur",
    "16": "Bursa",        "17": "Canakkale",     "18": "Cankiri",
    "19": "Corum",        "20": "Denizli",       "21": "Diyarbakir",
    "22": "Edirne",       "23": "Elazig",        "24": "Erzincan",
    "25": "Erzurum",      "26": "Eskisehir",     "27": "Gaziantep",
    "28": "Giresun",      "29": "Gumushane",     "30": "Hakkari",
    "31": "Hatay",        "32": "Isparta",       "33": "Mersin",
    "34": "Istanbul",     "35": "Izmir",         "36": "Kars",
    "37": "Kastamonu",    "38": "Kayseri",       "39": "Kirklareli",
    "40": "Kirsehir",     "41": "Kocaeli",       "42": "Konya",
    "43": "Kutahya",      "44": "Malatya",       "45": "Manisa",
    "46": "Kahramanmaras","47": "Mardin",        "48": "Mugla",
    "49": "Mus",          "50": "Nevsehir",      "51": "Nigde",
    "52": "Ordu",         "53": "Rize",          "54": "Sakarya",
    "55": "Samsun",       "56": "Siirt",         "57": "Sinop",
    "58": "Sivas",        "59": "Tekirdag",      "60": "Tokat",
    "61": "Trabzon",      "62": "Tunceli",       "63": "Sanliurfa",
    "64": "Usak",         "65": "Van",           "66": "Yozgat",
    "67": "Zonguldak",    "68": "Aksaray",       "69": "Bayburt",
    "70": "Karaman",      "71": "Kirikkale",     "72": "Batman",
    "73": "Sirnak",       "74": "Bartin",        "75": "Ardahan",
    "76": "Igdir",        "77": "Yalova",        "78": "Karabuk",
    "79": "Kilis",        "80": "Osmaniye",      "81": "Duzce",
}

def il_kodundan_ad(dosya_adi):
    """Dosya adının ilk 2 hanesinden il adını döner."""
    kod = str(dosya_adi)[:2]
    return IL_KODLARI.get(kod, f"Bilinmiyor ({kod})")

def koordinattan_il(geometri, enlem, boylam):
    """Koordinatın düştüğü il adını döner."""
    if pd.isna(enlem) or pd.isna(boylam):
        return "Koordinat Yok"
    try:
        nokta = Point(float(boylam), float(enlem))
        eslesme = geometri[geometri.geometry.contains(nokta)]
        if len(eslesme) > 0:
            return eslesme.iloc[0]["NAME_1"]
        return "Turkiye Disi"
    except Exception:
        return "Hata"

# --- Ana akış ---
print("Shapefile yukleniyor...")
iller = gpd.read_file(SHP)
print(f"  {len(iller)} il yuklendi.")

print("Merged CSV yukleniyor...")
df = pd.read_csv(MERGED_CSV)
print(f"  {len(df)} satir yuklendi.")

print("Il etiketleri hesaplaniyor...")
df["il_etiket"] = df["dosya_adi"].apply(il_kodundan_ad)

print("Koordinat -> il eslestirmesi yapiliyor (291 nokta)...")
il_koord_listesi = []
for i, row in df.iterrows():
    il = koordinattan_il(iller, row["enlem"], row["boylam"])
    il_koord_listesi.append(il)
    if (i + 1) % 50 == 0:
        print(f"  {i+1}/{len(df)} islendi...")

df["il_koordinat"] = il_koord_listesi

# Uyuşum kontrolü (büyük/küçük harf ve Türkçe karakter farkını yok say)
def normalize(s):
    return str(s).lower().strip()

df["il_uyusum"] = df.apply(
    lambda r: normalize(r["il_etiket"]) == normalize(r["il_koordinat"]),
    axis=1
)

# --- Özet ---
print("\n=== OZET ===")
print(f"Toplam: {len(df)}")
print(f"Koordinat Turkiye disi: {(df['il_koordinat'] == 'Turkiye Disi').sum()}")
print(f"Koordinat yok: {(df['il_koordinat'] == 'Koordinat Yok').sum()}")
print(f"Eslesme var (gecerli koordinatlarda): {df['il_uyusum'].sum()}")
print(f"Uyusmazlik: {(~df['il_uyusum']).sum()}")

print("\n=== UYUSMAZLIKLAR ===")
uyusmazlik = df[~df["il_uyusum"]][["dosya_adi", "enlem", "boylam", "il_etiket", "il_koordinat"]]
print(uyusmazlik.to_string(index=False))

# CSV'ye kaydet
df.to_csv(CIKTI, index=False, encoding="utf-8-sig")
print(f"\nDosya guncellendi: {CIKTI}")
