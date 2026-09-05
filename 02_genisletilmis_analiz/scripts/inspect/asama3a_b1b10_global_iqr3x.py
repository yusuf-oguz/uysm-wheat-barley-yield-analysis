"""
ASAMA 3a: b1-b10 Global IQR 3x
Kaynak: hansay_processed_v7.3.csv
Cikti:  hansay_processed_v7.4.csv

Her olcum tipi icin tum b1-b10 sutunlari duzlestirilir (~6390 deger),
global Q1/Q3/IQR hesaplanir, Q1-3xIQR / Q3+3xIQR disindaki hucreler null yapilir.
sap_boy (J) kurali: H veya I null yapilirsa J de null yapilir.
Null yapilan her hucre kismi_not sutununa kaydedilir.
"""

import pandas as pd
import numpy as np
import os

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.3.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.4.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir, {len(df.columns)} sutun")

# 7 olcum tipi: (kisaad, sutun_prefix_listesi)
olcum_tipleri = [
    ('uzunluk',      [f'b{i}_uzunluk_cm__B{28+i}'        for i in range(1, 11)]),
    ('agirlik',      [f'b{i}_agirlik_mg__C{28+i}'         for i in range(1, 11)]),
    ('dane_sayisi',  [f'b{i}_dane_sayisi__D{28+i}'        for i in range(1, 11)]),
    ('dane_agirlik', [f'b{i}_dane_agirlik_mg__E{28+i}'    for i in range(1, 11)]),
    ('sap_basak',    [f'b{i}_sap_basak_boyu_cm__H{28+i}'  for i in range(1, 11)]),
    ('sap_alt',      [f'b{i}_sap_alt_cm__I{28+i}'         for i in range(1, 11)]),
    ('sap_boy',      [f'b{i}_sap_boy_cm__J{28+i}'         for i in range(1, 11)]),
]

sap_basak_cols = [f'b{i}_sap_basak_boyu_cm__H{28+i}' for i in range(1, 11)]
sap_alt_cols   = [f'b{i}_sap_alt_cm__I{28+i}'        for i in range(1, 11)]
sap_boy_cols   = [f'b{i}_sap_boy_cm__J{28+i}'        for i in range(1, 11)]

toplam_null = 0

for tip, cols in olcum_tipleri:
    # Mevcut sutunlari dogrula
    cols = [c for c in cols if c in df.columns]
    if not cols:
        print(f"  [ATLA] {tip}: sutun bulunamadi")
        continue

    # Tum gecerli degerleri duzlestir
    all_vals = df[cols].values.flatten()
    all_vals = all_vals[~np.isnan(all_vals)]

    q1  = np.percentile(all_vals, 25)
    q3  = np.percentile(all_vals, 75)
    iqr = q3 - q1
    low  = q1 - 3 * iqr
    high = q3 + 3 * iqr

    print(f"\n{tip}: n_valid={len(all_vals)}, Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}")
    print(f"  Sinir: [{low:.2f}, {high:.2f}]")

    tip_null = 0
    for col in cols:
        mask = df[col].notna() & ((df[col] < low) | (df[col] > high))
        n = mask.sum()
        if n == 0:
            continue
        tip_null += n

        for idx in df[mask].index:
            val = df.at[idx, col]
            not_str = f"[ASAMA3a IQR3x] {col}={val:.2f} sinir=[{low:.2f},{high:.2f}]"
            if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
                df.at[idx, 'kismi_not'] = not_str
            else:
                df.at[idx, 'kismi_not'] += ' | ' + not_str
            df.at[idx, col] = np.nan

            # sap_boy kurali: H veya I null olursa J de null
            if col in sap_basak_cols or col in sap_alt_cols:
                b_no = cols.index(col)  # 0-indexed
                j_col = sap_boy_cols[b_no]
                if j_col in df.columns and pd.notna(df.at[idx, j_col]):
                    not_j = f"[ASAMA3a IQR3x] {j_col} null (kaynak {col} null yapildi)"
                    if pd.isna(df.at[idx, 'kismi_not']) or df.at[idx, 'kismi_not'] == '':
                        df.at[idx, 'kismi_not'] = not_j
                    else:
                        df.at[idx, 'kismi_not'] += ' | ' + not_j
                    df.at[idx, j_col] = np.nan

        print(f"  {col}: {n} null")

    print(f"  Toplam null bu tip: {tip_null}")
    toplam_null += tip_null

print(f"\nGenel toplam null: {toplam_null}")

df.to_csv(DST, index=False, encoding='utf-8-sig')
print(f"Kaydedildi: {DST}")
print(f"Sutun sayisi: {len(df.columns)}")
