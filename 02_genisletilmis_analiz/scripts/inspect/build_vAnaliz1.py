"""
vAnaliz1.0 olusturma scripti
- v8.2'den False satirlari cikar (617 satir kalir)
- Gecici/ara hesap sutunlari cikar
- Sonuc: vAnaliz1.0.csv
"""
import pandas as pd

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v8.2.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\vAnaliz1.0.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Ham: {len(df)} satir, {len(df.columns)} sutun")

# 1. False satirlari cikar
df = df[df['vld_genel'] == True].copy()
print(f"False cikarildi: {len(df)} satir kaldi")

# 2. Cikarilacak sutunlar
# - vld_genel / vld_genel_neden: artik anlamsiz (hepsi True)
# - _copy__ sutunlari: ana sutunun kopyasi, redundant
# - toplam_* sutunlari: ara toplam, ort_* zaten var
# - E41 (olcum_basak_dane_agirlik_hesap): D21 hesabinda kullanilan ara deger
# - E42 (dane_m2_tartim_hesap): D21 hesabinda kullanilan ara deger
# - c41_m2_norm: outlier tespiti icin olusturulan normalize sutun, analizde gerek yok
cikar = [
    'vld_genel',
    'vld_genel_neden',
    'ort_basak_uzunluk_cm_copy__C24',
    'ort_dane_sayisi_copy__C19',
    'ort_sap_boy_cm_copy__C23',
    'ort_kilcikli_basak_agirlik_mg__C18',
    'toplam_basak_uzunluk__B39',
    'toplam_basak_agirlik_mg__C39',
    'toplam_dane_sayisi__D39',
    'toplam_dane_agirlik_mg__E39',
    'olcum_basak_dane_agirlik_hesap__E41',
    'dane_m2_tartim_hesap__E42',
    'c41_m2_norm',
]
cikar_mevcut = [c for c in cikar if c in df.columns]
cikar_eksik  = [c for c in cikar if c not in df.columns]
if cikar_eksik:
    print(f"  [UYARI] Bazi sutunlar zaten mevcut degil: {cikar_eksik}")

df = df.drop(columns=cikar_mevcut)
print(f"Gecici sutunlar cikarildi ({len(cikar_mevcut)} adet): {cikar_mevcut}")
print(f"Sonuc: {len(df)} satir, {len(df.columns)} sutun")

# 3. Index sifirla
df = df.reset_index(drop=True)

# 4. Kaydet
df.to_csv(DST, index=False, encoding='utf-8-sig')
print(f"\nKaydedildi: {DST}")

# 5. Kalan sutunlar
print("\nKalan sutunlar:")
for i, c in enumerate(df.columns):
    print(f"  {i:3d}  {c}")
