"""
ASAMA 5a: Turetilmis sutunlara Global IQR 3x
Kaynak: hansay_processed_v7.7.csv
Cikti:  hansay_processed_v7.8.csv

Turetilmis ozet sutunlara (n=639) global IQR 3x uygulanir.
Outlier hucre null yapilir, kismi_not guncellenir.
NOT: Bu sutunlara null uygularsak bunu ham veriye degil, sadece
turetilmis sütuna kayıt olarak dusuruyoruz — ham veri etkilenmez.
"""

import pandas as pd
import numpy as np

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.7.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.8.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir, {len(df.columns)} sutun")

turetilmis_sutunlar = [
    'ort_basak_uzunluk_cm__B40',
    'ort_basak_agirlik_mg__C40',
    'ort_dane_sayisi__D40',
    'ort_dane_agirlik_mg__E40',
    'bir_basaktaki_ort_dane_agirlik_gram__C20',
    'bin_dane_agirlik_gram__C22',
    'basak_dane_oran__D41',
    'ort_sap_boy_cm__J39',
    'ort_sap_basak_boyu__H39',
    'ort_sap_basak_alti_boyu__I39',
    'm2_basak_sayisi__C12',
    'dane_m2_hesap_gram__C21',
    'dane_m2_gercek_gram__D21',
    'olcum_alani_basak__C11',
    'olcum_basak_agirlik_ham__C41',
]

toplam_null = 0

for col in turetilmis_sutunlar:
    if col not in df.columns:
        print(f"  [ATLA] {col} mevcut degil")
        continue

    vals = df[col].dropna()
    if len(vals) < 10:
        print(f"  [ATLA] {col}: yeterli deger yok (n={len(vals)})")
        continue

    q1  = vals.quantile(0.25)
    q3  = vals.quantile(0.75)
    iqr = q3 - q1
    low  = q1 - 3 * iqr
    high = q3 + 3 * iqr

    mask = df[col].notna() & ((df[col] < low) | (df[col] > high))
    n = mask.sum()
    print(f"{col}: Q1={q1:.2f}, IQR={iqr:.2f}, sinir=[{low:.2f},{high:.2f}], outlier={n}")

    if n == 0:
        continue

    toplam_null += n
    for idx in df[mask].index:
        val = df.at[idx, col]
        not_str = f"[ASAMA5a IQR3x] {col}={val:.2f} sinir=[{low:.2f},{high:.2f}]"
        if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
            df.at[idx, 'kismi_not'] = not_str
        else:
            df.at[idx, 'kismi_not'] += ' | ' + not_str
        df.at[idx, col] = np.nan

print(f"\nGenel toplam null: {toplam_null}")
df.to_csv(DST, index=False, encoding='utf-8-sig')
print(f"Kaydedildi: {DST}")
