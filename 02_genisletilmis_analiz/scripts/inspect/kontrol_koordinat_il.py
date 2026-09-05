"""
1) Tüm koordinatların Türkiye bbox içinde olup olmadığını kontrol eder.
2) Koordinattan il tespiti (sjoin ile vektörleştirilmiş):
   - contains ile il bulunursa -> il_koordinat_adi
   - bulunamazsa None -> il_koordinat_adi
3) Her nokta için 5km buffer içine düşen iller (il_koordinat_adi hariç) -> koordinat_ili_komsu
4) Uyuşma:
   - il_plaka_adi == il_koordinat_adi           -> True
   - il_plaka_adi in koordinat_ili_komsu        -> "komsu"
   - il_plaka_adi None                          -> None
   - hiçbiri uyuşmuyorsa                        -> False

Çıktı: hansay_processed_v2.7.csv
"""

import re
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

GIRDI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v2.6.csv"
)
CIKTI = (
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v2.7.csv"
)

IL_ADI = {
    1:"Adana",2:"Adıyaman",3:"Afyonkarahisar",4:"Ağrı",5:"Amasya",
    6:"Ankara",7:"Antalya",8:"Artvin",9:"Aydın",10:"Balıkesir",
    11:"Bilecik",12:"Bingöl",13:"Bitlis",14:"Bolu",15:"Burdur",
    16:"Bursa",17:"Çanakkale",18:"Çankırı",19:"Çorum",20:"Denizli",
    21:"Diyarbakır",22:"Edirne",23:"Elazığ",24:"Erzincan",25:"Erzurum",
    26:"Eskişehir",27:"Gaziantep",28:"Giresun",29:"Gümüşhane",30:"Hakkari",
    31:"Hatay",32:"Isparta",33:"Mersin",34:"İstanbul",35:"İzmir",
    36:"Kars",37:"Kastamonu",38:"Kayseri",39:"Kırklareli",40:"Kırşehir",
    41:"Kocaeli",42:"Konya",43:"Kütahya",44:"Malatya",45:"Manisa",
    46:"Kahramanmaraş",47:"Mardin",48:"Muğla",49:"Muş",50:"Nevşehir",
    51:"Niğde",52:"Ordu",53:"Rize",54:"Sakarya",55:"Samsun",
    56:"Siirt",57:"Sinop",58:"Sivas",59:"Tekirdağ",60:"Tokat",
    61:"Trabzon",62:"Tunceli",63:"Şanlıurfa",64:"Uşak",65:"Van",
    66:"Yozgat",67:"Zonguldak",68:"Aksaray",69:"Bayburt",70:"Karaman",
    71:"Kırıkkale",72:"Batman",73:"Şırnak",74:"Bartın",75:"Ardahan",
    76:"Iğdır",77:"Yalova",78:"Karabük",79:"Kilis",80:"Osmaniye",81:"Düzce",
}

GADM_TO_TR = {
    "Adana":"Adana","Adiyaman":"Adıyaman","Afyon":"Afyonkarahisar",
    "Agri":"Ağrı","Aksaray":"Aksaray","Amasya":"Amasya","Ankara":"Ankara",
    "Antalya":"Antalya","Ardahan":"Ardahan","Artvin":"Artvin","Aydin":"Aydın",
    "Balikesir":"Balıkesir","Bartin":"Bartın","Batman":"Batman","Bayburt":"Bayburt",
    "Bilecik":"Bilecik","Bingol":"Bingöl","Bitlis":"Bitlis","Bolu":"Bolu",
    "Burdur":"Burdur","Bursa":"Bursa","Canakkale":"Çanakkale","Cankiri":"Çankırı",
    "Corum":"Çorum","Denizli":"Denizli","Diyarbakir":"Diyarbakır","Duzce":"Düzce",
    "Edirne":"Edirne","Elazig":"Elazığ","Erzincan":"Erzincan","Erzurum":"Erzurum",
    "Eskisehir":"Eskişehir","Gaziantep":"Gaziantep","Giresun":"Giresun",
    "Gumushane":"Gümüşhane","Hakkari":"Hakkari","Hatay":"Hatay","Igdir":"Iğdır",
    "Isparta":"Isparta","Istanbul":"İstanbul","Izmir":"İzmir","Kahramanmaras":"Kahramanmaraş",
    "Karabuk":"Karabük","Karaman":"Karaman","Kars":"Kars","Kastamonu":"Kastamonu",
    "Kayseri":"Kayseri","Kilis":"Kilis","Kirikkale":"Kırıkkale","Kirklareli":"Kırklareli",
    "Kirsehir":"Kırşehir","Kocaeli":"Kocaeli","Konya":"Konya","Kutahya":"Kütahya",
    "Malatya":"Malatya","Manisa":"Manisa","Mardin":"Mardin","Mersin":"Mersin",
    "Mugla":"Muğla","Mus":"Muş","Nevsehir":"Nevşehir","Nigde":"Niğde",
    "Ordu":"Ordu","Osmaniye":"Osmaniye","Rize":"Rize","Sakarya":"Sakarya",
    "Samsun":"Samsun","Sanliurfa":"Şanlıurfa","Siirt":"Siirt","Sinop":"Sinop",
    "Sirnak":"Şırnak","Sivas":"Sivas","Tekirdag":"Tekirdağ","Tokat":"Tokat",
    "Trabzon":"Trabzon","Tunceli":"Tunceli","Usak":"Uşak","Van":"Van",
    "Yalova":"Yalova","Yozgat":"Yozgat","Zonguldak":"Zonguldak",
    # GADM varyantlari
    "Bartın":"Bartın","Bingöl":"Bingöl","Çanakkale":"Çanakkale",
    "Çankiri":"Çankırı","Çorum":"Çorum","Düzce":"Düzce","Elazığ":"Elazığ",
    "Gümüshane":"Gümüşhane","Iğdır":"Iğdır","K. Maras":"Kahramanmaraş",
    "Karabük":"Karabük","Kinkkale":"Kırıkkale","Kütahya":"Kütahya",
    "Zinguldak":"Zonguldak",
}

TR_ENLEM_MIN, TR_ENLEM_MAX = 35.8, 42.2
TR_BOYLAM_MIN, TR_BOYLAM_MAX = 25.7, 44.8


def dms_to_dd(dms):
    m = re.match(r"""(\d+)°(\d+)'([\d.]+)\"""", str(dms).strip())
    if not m:
        return None
    d, mn, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
    return d + mn / 60 + s / 3600


def il_adi_from_kod(kod):
    try:
        return IL_ADI.get(int(float(kod)))
    except (ValueError, TypeError):
        return None


print("Il sinirları yukleniyor...")
iller = gpd.read_file(
    r"D:\_Development\Projects\UYSM_Project_2"
    r"\yusuf_oguz_calismalari\data\source\gadm41_TUR.gpkg",
    layer=1
)[["NAME_1", "geometry"]].copy()
iller["il_tr"] = iller["NAME_1"].map(GADM_TO_TR)
iller = iller.set_crs("EPSG:4326", allow_override=True).reset_index(drop=True)
print(f"  {len(iller)} il yuklendi.")

# Komşuluk matrisi: touches veya sınır paylaşımı (sjoin ile)
print("Komşuluk matrisi hesaplaniyor...")
komsu_map = {}  # {il_adi: [komsu_il_adi, ...]}
for i, row_i in iller.iterrows():
    il_adi = row_i["il_tr"]
    if pd.isna(il_adi):
        continue
    komsu_map[il_adi] = []
    for j, row_j in iller.iterrows():
        if i == j:
            continue
        il_adi_j = row_j["il_tr"]
        if pd.isna(il_adi_j):
            continue
        if row_i["geometry"].touches(row_j["geometry"]) or row_i["geometry"].intersects(row_j["geometry"]):
            komsu_map[il_adi].append(il_adi_j)
print(f"  Komşuluk matrisi hazir.")

print("Veri okunuyor...")
_raw = pd.read_csv(GIRDI, encoding="utf-8-sig")

# Fragmented DataFrame sorununu onlemek icin tum yeni sutunlari onceden hesapla
enlem_dd  = _raw["enlem_raw__E3"].apply(dms_to_dd)
boylam_dd = _raw["boylam_raw__E4"].apply(dms_to_dd)

gecersiz = enlem_dd.isna() | boylam_dd.isna()
turkiye_ici = pd.array(
    [
        None if gecersiz[i] else
        bool(TR_ENLEM_MIN <= enlem_dd[i] <= TR_ENLEM_MAX and
             TR_BOYLAM_MIN <= boylam_dd[i] <= TR_BOYLAM_MAX)
        for i in _raw.index
    ],
    dtype=pd.BooleanDtype()
)

il_plaka_adi = _raw["dosya_il_kodu__dosyaadi"].apply(il_adi_from_kod)

# Gecerli satirlari GeoDataFrame'e al
gecerli_idx = _raw.index[~gecersiz]
gdf = gpd.GeoDataFrame(
    {"geometry": gpd.points_from_xy(boylam_dd[gecerli_idx], enlem_dd[gecerli_idx])},
    index=gecerli_idx,
    crs="EPSG:4326"
)

# 1) il_koordinat_adi — sjoin within
print("il_koordinat_adi hesaplaniyor (sjoin)...")
joined = gpd.sjoin(gdf, iller[["il_tr", "geometry"]], how="left", predicate="within")
il_koordinat_adi = joined.groupby(joined.index)["il_tr"].first()
il_koordinat_adi = il_koordinat_adi.reindex(_raw.index)

# 2) koordinat_ili_komsu — komşuluk matrisinden
koordinat_ili_komsu_ser = pd.Series(
    {idx: ", ".join(komsu_map.get(il_koordinat_adi.get(idx), []))
         if pd.notna(il_koordinat_adi.get(idx)) else None
     for idx in _raw.index},
    dtype=object
)

# 3) il_plaka_c6 — C6 degerinden il kodu (sadece XX.YY formatinda)
def c6_plaka(val):
    try:
        s = str(val).strip()
        if '.' not in s:
            return None
        oncesi = s.split('.')[0]
        if len(oncesi) > 2:
            return None
        return IL_ADI.get(int(oncesi))
    except:
        return None

il_plaka_c6 = _raw["istasyon_no__C6"].apply(c6_plaka)

# 4) il_plaka_final — 3 dosya icin C6, digerlerinde dosya adi
C6_OVERRIDE = {"4006 aydınlar 465.xlsx", "3610 300m 403.xlsx", "195 30km 195.xlsx"}

il_plaka_final = pd.Series([
    il_plaka_c6.iloc[i] if _raw["dosya_adi__dosyaadi"].iloc[i] in C6_OVERRIDE
    else il_plaka_adi.iloc[i]
    for i in range(len(_raw))
], index=_raw.index)

# 5) Uyusma (il_plaka_final kullanarak)
def uyusma_hesapla(plaka, koord, komsu):
    if pd.isna(plaka) or plaka is None:
        return None
    if pd.notna(koord) and plaka == koord:
        return True
    if pd.notna(komsu) and komsu:
        if plaka in [k.strip() for k in str(komsu).split(",")]:
            return "komsu"
    if pd.notna(koord):
        return False
    return None

il_uyusma = [
    uyusma_hesapla(p, k, ks)
    for p, k, ks in zip(il_plaka_final, il_koordinat_adi, koordinat_ili_komsu_ser)
]

# Tek seferde DataFrame olustur
df_out = pd.concat([
    _raw,
    pd.DataFrame({
        "enlem_dd":             enlem_dd.values,
        "boylam_dd":            boylam_dd.values,
        "turkiye_ici":          turkiye_ici,
        "il_plaka_adi":         il_plaka_adi.values,
        "il_plaka_c6":          il_plaka_c6.values,
        "il_plaka_final":       il_plaka_final.values,
        "il_koordinat_adi":     il_koordinat_adi.values,
        "koordinat_ili_komsu":  koordinat_ili_komsu_ser.values,
        "il_uyusma":            il_uyusma,
    }, index=_raw.index)
], axis=1)

df_out.to_csv(CIKTI, index=False, encoding="utf-8-sig")

print(f"\nv2.7 kaydedildi: {CIKTI}")
print(f"Toplam satir          : {len(df_out)}")
print(f"turkiye_ici True      : {(df_out['turkiye_ici']==True).sum()}")
print(f"il_koordinat dolu     : {df_out['il_koordinat_adi'].notna().sum()}")
print(f"il_koordinat bos      : {df_out['il_koordinat_adi'].isna().sum()}")
print(f"komsu listesi dolu    : {df_out['koordinat_ili_komsu'].notna().sum()}")
print(f"il_plaka_c6 dolu      : {df_out['il_plaka_c6'].notna().sum()}")
print(f"il_uyusma True        : {(df_out['il_uyusma']==True).sum()}")
print(f"il_uyusma False       : {(df_out['il_uyusma']==False).sum()}")
print(f"il_uyusma komsu       : {(df_out['il_uyusma']=='komsu').sum()}")
print(f"il_uyusma None        : {df_out['il_uyusma'].isna().sum()}")
