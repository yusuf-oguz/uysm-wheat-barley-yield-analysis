"""
ASAMA 4b: C11 ve C41 Global MAD 3.5
Kaynak: hansay_processed_v7.6.csv
Cikti:  hansay_processed_v7.7.csv
"""

import pandas as pd
import numpy as np

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.6.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.7.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir, {len(df.columns)} sutun")

THRESHOLD = 3.5 / 0.6745  # ~5.189

def apply_mad35(df, col, label):
    vals = df[col].dropna()
    median_val = vals.median()
    mad = np.median(np.abs(vals - median_val))
    if mad == 0:
        print(f"  {label}: MAD=0, atlaniyor")
        return pd.Series(False, index=df.index)
    low  = median_val - THRESHOLD * mad
    high = median_val + THRESHOLD * mad
    mask = df[col].notna() & ((df[col] < low) | (df[col] > high))
    print(f"\n{label}: median={median_val:.2f}, MAD={mad:.2f}, sinir=[{low:.2f},{high:.2f}]")
    print(f"  Outlier: {mask.sum()}")
    return mask, median_val, mad

# ── C11 ──────────────────────────────────────────────────────────────────────
mask_c11, med_c11, mad_c11 = apply_mad35(df, 'olcum_alani_basak__C11', 'C11')
low_c11 = med_c11 - THRESHOLD * mad_c11
high_c11 = med_c11 + THRESHOLD * mad_c11
for idx in df[mask_c11].index:
    val = df.at[idx, 'olcum_alani_basak__C11']
    mz  = 0.6745 * abs(val - med_c11) / mad_c11
    not_str = f"[ASAMA4b MAD3.5] C11={val:.1f} MZ={mz:.2f}"
    if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
        df.at[idx, 'kismi_not'] = not_str
    else:
        df.at[idx, 'kismi_not'] += ' | ' + not_str
    df.at[idx, 'olcum_alani_basak__C11'] = np.nan
    for col in ['m2_basak_sayisi__C12', 'm2_toplam_bitki__C15', 'dane_m2_hesap_gram__C21']:
        if col in df.columns:
            df.at[idx, col] = np.nan

# ── C41 (c41_m2_norm uzerinden) ──────────────────────────────────────────────
mask_c41, med_c41, mad_c41 = apply_mad35(df, 'c41_m2_norm', 'C41 (c41_m2_norm)')
low_c41 = med_c41 - THRESHOLD * mad_c41
high_c41 = med_c41 + THRESHOLD * mad_c41
for idx in df[mask_c41].index:
    val = df.at[idx, 'c41_m2_norm']
    mz  = 0.6745 * abs(val - med_c41) / mad_c41
    not_str = f"[ASAMA4b MAD3.5] c41_m2_norm={val:.1f} MZ={mz:.2f}"
    if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
        df.at[idx, 'kismi_not'] = not_str
    else:
        df.at[idx, 'kismi_not'] += ' | ' + not_str
    df.at[idx, 'olcum_basak_agirlik_ham__C41'] = np.nan
    df.at[idx, 'c41_m2_norm'] = np.nan
    for col in ['olcum_basak_dane_agirlik_hesap__E41', 'dane_m2_tartim_hesap__E42', 'dane_m2_gercek_gram__D21']:
        if col in df.columns:
            df.at[idx, col] = np.nan

print(f"\nToplam C11 null: {mask_c11.sum()}, C41 null: {mask_c41.sum()}")

# Turetilmis sutunlar yeniden hesapla
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
