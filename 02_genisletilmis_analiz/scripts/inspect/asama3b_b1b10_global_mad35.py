"""
ASAMA 3b: b1-b10 Global MAD 3.5 + Turetilmis Sutun Yeniden Hesaplama
Kaynak: hansay_processed_v7.4.csv
Cikti:  hansay_processed_v7.5.csv

Her olcum tipi icin tum b1-b10 sutunlari duzlestirilir (~6390 deger),
global median ve MAD hesaplanir,
|0.6745*(x-median)|/MAD > 3.5 kosulunu saglayan hucreler null yapilir.
sap_boy (J) kurali: H veya I null yapilirsa J de null yapilir.
Null yapilan her hucre kismi_not sutununa kaydedilir.
Son olarak tum turetilmis sutunlar (Katman 3-5) yeniden hesaplanir.
"""

import pandas as pd
import numpy as np
import os

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.4.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.5.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir, {len(df.columns)} sutun")

sap_basak_cols = [f'b{i}_sap_basak_boyu_cm__H{28+i}' for i in range(1, 11)]
sap_alt_cols   = [f'b{i}_sap_alt_cm__I{28+i}'        for i in range(1, 11)]
sap_boy_cols   = [f'b{i}_sap_boy_cm__J{28+i}'        for i in range(1, 11)]

olcum_tipleri = [
    ('uzunluk',      [f'b{i}_uzunluk_cm__B{28+i}'        for i in range(1, 11)]),
    ('agirlik',      [f'b{i}_agirlik_mg__C{28+i}'         for i in range(1, 11)]),
    ('dane_sayisi',  [f'b{i}_dane_sayisi__D{28+i}'        for i in range(1, 11)]),
    ('dane_agirlik', [f'b{i}_dane_agirlik_mg__E{28+i}'    for i in range(1, 11)]),
    ('sap_basak',    [f'b{i}_sap_basak_boyu_cm__H{28+i}'  for i in range(1, 11)]),
    ('sap_alt',      [f'b{i}_sap_alt_cm__I{28+i}'         for i in range(1, 11)]),
    ('sap_boy',      [f'b{i}_sap_boy_cm__J{28+i}'         for i in range(1, 11)]),
]

toplam_null = 0

for tip, cols in olcum_tipleri:
    cols = [c for c in cols if c in df.columns]
    if not cols:
        print(f"  [ATLA] {tip}: sutun bulunamadi")
        continue

    all_vals = df[cols].values.flatten()
    all_vals = all_vals[~np.isnan(all_vals)]

    median_val = np.median(all_vals)
    mad = np.median(np.abs(all_vals - median_val))

    if mad == 0:
        print(f"  [ATLA] {tip}: MAD=0, atlaniyor")
        continue

    threshold = 3.5 / 0.6745  # ~5.189

    print(f"\n{tip}: n_valid={len(all_vals)}, median={median_val:.2f}, MAD={mad:.2f}")
    print(f"  Sinir: [{median_val - threshold*mad:.2f}, {median_val + threshold*mad:.2f}]")

    tip_null = 0
    for col in cols:
        mask = df[col].notna() & (np.abs(df[col] - median_val) / mad > threshold)
        n = mask.sum()
        if n == 0:
            continue
        tip_null += n

        for idx in df[mask].index:
            val = df.at[idx, col]
            mz  = 0.6745 * abs(val - median_val) / mad
            not_str = f"[ASAMA3b MAD3.5] {col}={val:.2f} MZ={mz:.2f}"
            if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
                df.at[idx, 'kismi_not'] = not_str
            else:
                df.at[idx, 'kismi_not'] += ' | ' + not_str
            df.at[idx, col] = np.nan

            # sap_boy kurali
            if col in sap_basak_cols or col in sap_alt_cols:
                b_no = (sap_basak_cols.index(col) if col in sap_basak_cols
                        else sap_alt_cols.index(col))
                j_col = sap_boy_cols[b_no]
                if j_col in df.columns and pd.notna(df.at[idx, j_col]):
                    not_j = f"[ASAMA3b MAD3.5] {j_col} null (kaynak {col} null yapildi)"
                    if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
                        df.at[idx, 'kismi_not'] = not_j
                    else:
                        df.at[idx, 'kismi_not'] += ' | ' + not_j
                    df.at[idx, j_col] = np.nan

        print(f"  {col}: {n} null")

    print(f"  Toplam null bu tip: {tip_null}")
    toplam_null += tip_null

print(f"\nGenel toplam null (MAD3.5): {toplam_null}")

# ── Turetilmis sutunlar yeniden hesapla ──────────────────────────────────────
print("\nTuretilmis sutunlar yeniden hesaplaniyor...")

# Grup A: sap_boy = sap_basak + sap_alt
for i in range(1, 11):
    h = f'b{i}_sap_basak_boyu_cm__H{28+i}'
    ii = f'b{i}_sap_alt_cm__I{28+i}'
    j = f'b{i}_sap_boy_cm__J{28+i}'
    if h in df.columns and ii in df.columns and j in df.columns:
        df[j] = df[h] + df[ii]  # NaN propagation otomatik

# Grup B: toplamlar (sum)
uzunluk_cols     = [f'b{i}_uzunluk_cm__B{28+i}'        for i in range(1, 11)]
agirlik_cols     = [f'b{i}_agirlik_mg__C{28+i}'         for i in range(1, 11)]
dane_sayisi_cols = [f'b{i}_dane_sayisi__D{28+i}'        for i in range(1, 11)]
dane_ag_cols     = [f'b{i}_dane_agirlik_mg__E{28+i}'    for i in range(1, 11)]

if 'toplam_basak_uzunluk__B39' in df.columns:
    df['toplam_basak_uzunluk__B39'] = df[[c for c in uzunluk_cols if c in df.columns]].sum(axis=1, skipna=True)
if 'toplam_basak_agirlik_mg__C39' in df.columns:
    df['toplam_basak_agirlik_mg__C39'] = df[[c for c in agirlik_cols if c in df.columns]].sum(axis=1, skipna=True)
if 'toplam_dane_sayisi__D39' in df.columns:
    df['toplam_dane_sayisi__D39'] = df[[c for c in dane_sayisi_cols if c in df.columns]].sum(axis=1, skipna=True)
if 'toplam_dane_agirlik_mg__E39' in df.columns:
    df['toplam_dane_agirlik_mg__E39'] = df[[c for c in dane_ag_cols if c in df.columns]].sum(axis=1, skipna=True)

# Grup C: ortalamalar (mean skipna)
def mean_cols(df, cols):
    existing = [c for c in cols if c in df.columns]
    return df[existing].mean(axis=1, skipna=True)

if 'ort_basak_uzunluk_cm__B40' in df.columns:
    df['ort_basak_uzunluk_cm__B40'] = mean_cols(df, uzunluk_cols)
if 'ort_basak_agirlik_mg__C40' in df.columns:
    df['ort_basak_agirlik_mg__C40'] = mean_cols(df, agirlik_cols)
if 'ort_dane_sayisi__D40' in df.columns:
    df['ort_dane_sayisi__D40'] = mean_cols(df, dane_sayisi_cols)
if 'ort_dane_agirlik_mg__E40' in df.columns:
    df['ort_dane_agirlik_mg__E40'] = mean_cols(df, dane_ag_cols)
if 'ort_sap_basak_boyu__H39' in df.columns:
    df['ort_sap_basak_boyu__H39'] = mean_cols(df, sap_basak_cols)
if 'ort_sap_basak_alti_boyu__I39' in df.columns:
    df['ort_sap_basak_alti_boyu__I39'] = mean_cols(df, sap_alt_cols)
if 'ort_sap_boy_cm__J39' in df.columns:
    df['ort_sap_boy_cm__J39'] = mean_cols(df, sap_boy_cols)

# Grup D: kopya/ozet
if 'ort_kilcikli_basak_agirlik_mg__C18' in df.columns:
    df['ort_kilcikli_basak_agirlik_mg__C18'] = df['ort_basak_agirlik_mg__C40']
if 'ort_dane_sayisi_copy__C19' in df.columns:
    df['ort_dane_sayisi_copy__C19'] = df['ort_dane_sayisi__D40']
if 'bir_basaktaki_ort_dane_agirlik_gram__C20' in df.columns:
    df['bir_basaktaki_ort_dane_agirlik_gram__C20'] = df['ort_dane_agirlik_mg__E40'] / 1000
if 'bin_dane_agirlik_gram__C22' in df.columns:
    df['bin_dane_agirlik_gram__C22'] = df['ort_dane_agirlik_mg__E40'] / df['ort_dane_sayisi__D40']
if 'ort_sap_boy_cm_copy__C23' in df.columns:
    df['ort_sap_boy_cm_copy__C23'] = df['ort_sap_boy_cm__J39']
if 'ort_basak_uzunluk_cm_copy__C24' in df.columns:
    df['ort_basak_uzunluk_cm_copy__C24'] = df['ort_basak_uzunluk_cm__B40']
if 'basak_dane_oran__D41' in df.columns:
    df['basak_dane_oran__D41'] = df['ort_dane_agirlik_mg__E40'] / df['ort_basak_agirlik_mg__C40']

# Grup E: alan ve verim zincirleri
if 'm2_basak_sayisi__C12' in df.columns:
    df['m2_basak_sayisi__C12'] = df['olcum_alani_basak__C11'] * df['olcum_alani_carpani__E13']
if 'm2_basaksiz_bitki__C14' in df.columns:
    e14_col = 'olcum_alani_carpani2__E14' if 'olcum_alani_carpani2__E14' in df.columns else 'olcum_alani_carpani__E13'
    df['m2_basaksiz_bitki__C14'] = df['basaksiz_bitki_sayisi__C13'] * df[e14_col]
if 'm2_toplam_bitki__C15' in df.columns:
    df['m2_toplam_bitki__C15'] = df['m2_basak_sayisi__C12'] + df['m2_basaksiz_bitki__C14']
if 'dane_m2_hesap_gram__C21' in df.columns:
    df['dane_m2_hesap_gram__C21'] = df['bir_basaktaki_ort_dane_agirlik_gram__C20'] * df['m2_basak_sayisi__C12']
if 'olcum_basak_dane_agirlik_hesap__E41' in df.columns:
    df['olcum_basak_dane_agirlik_hesap__E41'] = df['olcum_basak_agirlik_ham__C41'] * df['basak_dane_oran__D41']
if 'dane_m2_tartim_hesap__E42' in df.columns:
    e14_col = 'olcum_alani_carpani2__E14' if 'olcum_alani_carpani2__E14' in df.columns else 'olcum_alani_carpani__E13'
    df['dane_m2_tartim_hesap__E42'] = df['olcum_basak_dane_agirlik_hesap__E41'] * df[e14_col]
if 'dane_m2_gercek_gram__D21' in df.columns:
    df['dane_m2_gercek_gram__D21'] = df['dane_m2_tartim_hesap__E42'] / 1000

# c41_m2_norm guncelle
if 'c41_m2_norm' in df.columns:
    df['c41_m2_norm'] = df['olcum_basak_agirlik_ham__C41'] * df['olcum_alani_carpani__E13']

print("Turetilmis sutunlar guncellendi.")

df.to_csv(DST, index=False, encoding='utf-8-sig')
print(f"Kaydedildi: {DST}")
print(f"Sutun sayisi: {len(df.columns)}")
