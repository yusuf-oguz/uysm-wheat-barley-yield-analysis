"""
v2.7 -> v2.8
Her satir icin KMZ'den koordinat ve il bilgisi eklenir.
Eslestirme: istasyon_no__C6 (ornek: 6.09) -> KMZ istasyon_no (ornek: 06.09)
            + dosya adindaki son sayi == KMZ sira_no

Durum (kmz_esleme):
  - "tek"     : KMZ'de sadece 1 kayit var, direkt eslesti
  - "sira"    : birden fazla kayit icinden sira_no ile eslesti
  - "coklu"   : birden fazla kayit var, sira_no eslesemedi -> hepsi virgülle
  - "yok"     : KMZ'de bu istasyon yok
"""

import re
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

GIRDI  = (r"D:\_Development\Projects\UYSM_Project_2"
          r"\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v2.7.csv")
CIKTI  = (r"D:\_Development\Projects\UYSM_Project_2"
          r"\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v2.8.csv")
KMZ_XL = (r"D:\_Development\Projects\UYSM_Project_2"
           r"\yusuf_oguz_calismalari\data\processed\tmp\kmz_ham.xlsx")
GPKG   = (r"D:\_Development\Projects\UYSM_Project_2"
           r"\yusuf_oguz_calismalari\data\source\gadm41_TUR.gpkg")

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
    "Bartın":"Bartın","Bingöl":"Bingöl","Çanakkale":"Çanakkale",
    "Çankiri":"Çankırı","Çorum":"Çorum","Düzce":"Düzce","Elazığ":"Elazığ",
    "Gümüshane":"Gümüşhane","Iğdır":"Iğdır","K. Maras":"Kahramanmaraş",
    "Karabük":"Karabük","Kinkkale":"Kırıkkale","Kütahya":"Kütahya",
    "Zinguldak":"Zonguldak",
}


def son_sayi(s):
    m = re.findall(r'\d+', str(s).replace('.xlsx', ''))
    return m[-1] if m else None


def kmz_to_c6_format(s):
    try:
        parts = str(s).split('.')
        return str(int(parts[0])) + '.' + parts[1]
    except:
        return None


print("Il sinirlari yukleniyor...")
iller = gpd.read_file(GPKG, layer=1)[["NAME_1", "geometry"]].copy()
iller["il_tr"] = iller["NAME_1"].map(GADM_TO_TR)
iller = iller.set_crs("EPSG:4326", allow_override=True)


def hangi_il(lat, lon):
    pt = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")
    j = gpd.sjoin(pt, iller[["il_tr", "geometry"]], how="left", predicate="within")
    v = j["il_tr"].dropna().tolist()
    return v[0] if v else None


print("KMZ verisi yukleniyor...")
kmz = pd.read_excel(KMZ_XL)
kmz["c6_format"] = kmz["istasyon_no"].apply(kmz_to_c6_format)
kmz["sira_no"] = kmz["sira_no"].astype(str).str.strip().replace("nan", None)
# Duplikatlari temizle (ayni istasyon+sira birden fazla geciyor)
kmz = kmz.drop_duplicates(subset=["c6_format", "sira_no"])

# c6_format -> grup sozlugu
kmz_grp = {k: grp for k, grp in kmz.groupby("c6_format")}

print("v2.7 okunuyor...")
df = pd.read_csv(GIRDI, encoding="utf-8-sig")

kmz_enlem_list   = []
kmz_boylam_list  = []
kmz_il_list      = []
kmz_esleme_list  = []

for _, row in df.iterrows():
    c6_raw = str(row["istasyon_no__C6"]).strip()
    # C6 degerini XX.YY formatina getir
    try:
        parts = c6_raw.split(".")
        c6_key = str(int(parts[0])) + "." + parts[1]
    except:
        kmz_enlem_list.append(None)
        kmz_boylam_list.append(None)
        kmz_il_list.append(None)
        kmz_esleme_list.append("yok")
        continue

    grp = kmz_grp.get(c6_key)
    if grp is None or len(grp) == 0:
        kmz_enlem_list.append(None)
        kmz_boylam_list.append(None)
        kmz_il_list.append(None)
        kmz_esleme_list.append("yok")
        continue

    if len(grp) == 1:
        r = grp.iloc[0]
        il = hangi_il(r["enlem_dd"], r["boylam_dd"])
        kmz_enlem_list.append(r["enlem_dd"])
        kmz_boylam_list.append(r["boylam_dd"])
        kmz_il_list.append(il)
        kmz_esleme_list.append("tek")
    else:
        # Sira no ile eslesmeyi dene
        dosya_sira = son_sayi(row["dosya_adi__dosyaadi"])
        eslesen = grp[grp["sira_no"] == dosya_sira]
        if len(eslesen) == 1:
            r = eslesen.iloc[0]
            il = hangi_il(r["enlem_dd"], r["boylam_dd"])
            kmz_enlem_list.append(r["enlem_dd"])
            kmz_boylam_list.append(r["boylam_dd"])
            kmz_il_list.append(il)
            kmz_esleme_list.append("sira")
        else:
            # Hepsini virgülle birlestir
            enlemler = ", ".join(grp["enlem_dd"].astype(str).tolist())
            boylamlar = ", ".join(grp["boylam_dd"].astype(str).tolist())
            iller_list = [hangi_il(r["enlem_dd"], r["boylam_dd"]) for _, r in grp.iterrows()]
            kmz_enlem_list.append(enlemler)
            kmz_boylam_list.append(boylamlar)
            kmz_il_list.append(", ".join(str(x) for x in iller_list))
            kmz_esleme_list.append("coklu")

# Tek seferde ekle
df_out = pd.concat([
    df,
    pd.DataFrame({
        "kmz_enlem_dd":  kmz_enlem_list,
        "kmz_boylam_dd": kmz_boylam_list,
        "kmz_il":        kmz_il_list,
        "kmz_esleme":    kmz_esleme_list,
    }, index=df.index)
], axis=1)

df_out.to_csv(CIKTI, index=False, encoding="utf-8-sig")

print(f"\nv2.8 kaydedildi: {CIKTI}")
print(f"Toplam satir   : {len(df_out)}")
print(f"kmz_esleme tek   : {(df_out['kmz_esleme']=='tek').sum()}")
print(f"kmz_esleme sira  : {(df_out['kmz_esleme']=='sira').sum()}")
print(f"kmz_esleme coklu : {(df_out['kmz_esleme']=='coklu').sum()}")
print(f"kmz_esleme yok   : {(df_out['kmz_esleme']=='yok').sum()}")
