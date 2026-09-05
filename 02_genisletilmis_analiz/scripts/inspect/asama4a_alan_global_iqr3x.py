"""
ASAMA 4a: C11 ve C41 Global IQR 3x
Kaynak: hansay_processed_v7.5.csv
Cikti:  hansay_processed_v7.6.csv

C11 (basak sayimi): direkt IQR 3x
C41 (lab tartim): c41_m2_norm sutunu uzerinden IQR 3x, outlier tespiti
  C41 hucresine null yansitilir, C41 ile baglantili turetilmis sutunlar guncellenir.
"""

import pandas as pd
import numpy as np

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.5.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.6.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir, {len(df.columns)} sutun")

def apply_iqr3x(df, col, label):
    vals = df[col].dropna()
    q1 = vals.quantile(0.25)
    q3 = vals.quantile(0.75)
    iqr = q3 - q1
    low  = q1 - 3 * iqr
    high = q3 + 3 * iqr
    mask = df[col].notna() & ((df[col] < low) | (df[col] > high))
    n = mask.sum()
    print(f"\n{label}: Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}, sinir=[{low:.2f},{high:.2f}]")
    print(f"  Outlier: {n}")
    return mask, low, high

# ── C11 ──────────────────────────────────────────────────────────────────────
mask_c11, low_c11, high_c11 = apply_iqr3x(df, 'olcum_alani_basak__C11', 'C11')
for idx in df[mask_c11].index:
    val = df.at[idx, 'olcum_alani_basak__C11']
    not_str = f"[ASAMA4a IQR3x] C11={val:.1f} sinir=[{low_c11:.1f},{high_c11:.1f}]"
    if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
        df.at[idx, 'kismi_not'] = not_str
    else:
        df.at[idx, 'kismi_not'] += ' | ' + not_str
    df.at[idx, 'olcum_alani_basak__C11'] = np.nan

# C11 null olursa C12 ve zinciri de null
if mask_c11.sum() > 0:
    for idx in df[mask_c11].index:
        for col in ['m2_basak_sayisi__C12', 'm2_toplam_bitki__C15', 'dane_m2_hesap_gram__C21']:
            if col in df.columns:
                df.at[idx, col] = np.nan

# ── C41 (c41_m2_norm uzerinden) ──────────────────────────────────────────────
mask_c41, low_c41, high_c41 = apply_iqr3x(df, 'c41_m2_norm', 'C41 (c41_m2_norm)')
for idx in df[mask_c41].index:
    val = df.at[idx, 'c41_m2_norm']
    not_str = f"[ASAMA4a IQR3x] c41_m2_norm={val:.1f} sinir=[{low_c41:.1f},{high_c41:.1f}]"
    if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
        df.at[idx, 'kismi_not'] = not_str
    else:
        df.at[idx, 'kismi_not'] += ' | ' + not_str
    df.at[idx, 'olcum_basak_agirlik_ham__C41'] = np.nan
    df.at[idx, 'c41_m2_norm'] = np.nan
    # C41 zincirleme: E41, E42, D21
    for col in ['olcum_basak_dane_agirlik_hesap__E41', 'dane_m2_tartim_hesap__E42', 'dane_m2_gercek_gram__D21']:
        if col in df.columns:
            df.at[idx, col] = np.nan

print(f"\nToplam C11 null: {mask_c11.sum()}, C41 null: {mask_c41.sum()}")

# Turetilmis sutunlar yeniden hesapla (C11 ve C41 baglantili)
e14_col = 'olcum_alani_carpani2__E14' if 'olcum_alani_carpani2__E14' in df.columns else 'olcum_alani_carpani__E13'

if 'm2_basak_sayisi__C12' in df.columns:
    df['m2_basak_sayisi__C12'] = df['olcum_alani_basak__C11'] * df['olcum_alani_carpani__E13']
if 'm2_basaksiz_bitki__C14' in df.columns:
    df['m2_basaksiz_bitki__C14'] = df['basaksiz_bitki_sayisi__C13'] * df[e14_col]
if 'm2_toplam_bitki__C15' in df.columns:
    df['m2_toplam_bitki__C15'] = df['m2_basak_sayisi__C12'] + df['m2_basaksiz_bitki__C14']
if 'dane_m2_hesap_gram__C21' in df.columns:
    df['dane_m2_hesap_gram__C21'] = df['bir_basaktaki_ort_dane_agirlik_gram__C20'] * df['m2_basak_sayisi__C12']
if 'olcum_basak_dane_agirlik_hesap__E41' in df.columns:
    df['olcum_basak_dane_agirlik_hesap__E41'] = df['olcum_basak_agirlik_ham__C41'] * df['basak_dane_oran__D41']
if 'dane_m2_tartim_hesap__E42' in df.columns:
    df['dane_m2_tartim_hesap__E42'] = df['olcum_basak_dane_agirlik_hesap__E41'] * df[e14_col]
if 'dane_m2_gercek_gram__D21' in df.columns:
    df['dane_m2_gercek_gram__D21'] = df['dane_m2_tartim_hesap__E42'] / 1000
if 'c41_m2_norm' in df.columns:
    df['c41_m2_norm'] = df['olcum_basak_agirlik_ham__C41'] * df['olcum_alani_carpani__E13']

print("Turetilmis sutunlar guncellendi.")
df.to_csv(DST, index=False, encoding='utf-8-sig')
print(f"Kaydedildi: {DST}")
