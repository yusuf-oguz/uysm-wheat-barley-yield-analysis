import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

csv_path = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\vAnaliz1.0.csv'
fig_dir  = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\docs\figures'

df = pd.read_csv(csv_path, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir")

# 7 olcum tipi ve ilgili b1-b10 sutun prefixleri
olcum_tipleri = [
    ('uzunluk',       'uzunluk_cm__B',    [29,30,31,32,33,34,35,36,37,38], 'cm',    'Basak Uzunlugu (bN_uzunluk_cm)'),
    ('agirlik',       'agirlik_mg__C',    [29,30,31,32,33,34,35,36,37,38], 'mg',    'Basak Agirligi (bN_agirlik_mg)'),
    ('dane_sayisi',   'dane_sayisi__D',   [29,30,31,32,33,34,35,36,37,38], 'adet',  'Dane Sayisi (bN_dane_sayisi)'),
    ('dane_agirlik',  'dane_agirlik_mg__E',[29,30,31,32,33,34,35,36,37,38],'mg',   'Dane Agirligi (bN_dane_agirlik_mg)'),
    ('sap_basak',     'sap_basak_boyu_cm__H',[29,30,31,32,33,34,35,36,37,38],'cm', 'Sap Basak Boyu (bN_sap_basak_boyu_cm)'),
    ('sap_alt',       'sap_alt_cm__I',    [29,30,31,32,33,34,35,36,37,38], 'cm',    'Sap Alt Boyu (bN_sap_alt_cm)'),
    ('sap_boy',       'sap_boy_cm__J',    [29,30,31,32,33,34,35,36,37,38], 'cm',    'Toplam Sap Boyu (bN_sap_boy_cm)'),
]

for tip_kisa, prefix, satirlar, birim, baslik in olcum_tipleri:
    # sutun adlarini bul
    cols = []
    for s in satirlar:
        col = f'b{satirlar.index(s)+1}_{prefix}{s}'
        if col in df.columns:
            cols.append(col)
        else:
            # alternatif arama
            matches = [c for c in df.columns if prefix in c and str(s) in c.split('__')[-1]]
            if matches:
                cols.append(matches[0])
            else:
                print(f"  [UYARI] bulunamadi: b{satirlar.index(s)+1}_{prefix}{s}")

    if not cols:
        print(f"[ATLA] {tip_kisa} icin sutun bulunamadi")
        continue

    print(f"\n{tip_kisa}: {len(cols)} sutun bulundu: {cols[:3]}...")

    # tum degerleri duzlestir: satir sirasiyla b1,b2,...,b10
    # x: 0..N*10-1, her satirin 10 noktasi yan yana
    all_vals = []
    all_x    = []
    null_x   = []

    for row_idx, row in df.iterrows():
        for col_idx, col in enumerate(cols):
            x_pos = row_idx * len(cols) + col_idx
            val = row[col]
            if pd.isna(val):
                null_x.append(x_pos)
            else:
                all_x.append(x_pos)
                all_vals.append(val)

    all_x    = np.array(all_x)
    all_vals = np.array(all_vals)
    null_x   = np.array(null_x)

    n_total = len(df) * len(cols)
    n_valid = len(all_vals)
    n_null  = len(null_x)

    median_val = np.median(all_vals)
    q1 = np.percentile(all_vals, 25)
    q3 = np.percentile(all_vals, 75)
    iqr = q3 - q1
    mad = np.median(np.abs(all_vals - median_val))

    stats_str = (
        f"n_toplam={n_total}  null={n_null}  valid={n_valid}\n"
        f"min={all_vals.min():.2f}  max={all_vals.max():.2f}  "
        f"median={median_val:.2f}  Q1={q1:.2f}  Q3={q3:.2f}  IQR={iqr:.2f}  MAD={mad:.2f}"
    )

    # MAD 3.5 sinirlarini hesapla
    mad_low  = median_val - (3.5 / 0.6745) * mad
    mad_high = median_val + (3.5 / 0.6745) * mad
    n_mad_out = np.sum((all_vals < mad_low) | (all_vals > mad_high))

    fig, ax = plt.subplots(figsize=(20, 5))

    # IQR bandi
    ax.axhspan(q1, q3, alpha=0.10, color='orange', label='IQR (Q1-Q3)')

    # MAD 3.5 sinir cizgileri
    ax.axhline(mad_high, color='purple', linestyle=':', linewidth=1.0, alpha=0.8,
               label=f'MAD 3.5 ust={mad_high:.1f}')
    ax.axhline(mad_low,  color='purple', linestyle=':', linewidth=1.0, alpha=0.8,
               label=f'MAD 3.5 alt={mad_low:.1f}')

    # Medyan
    ax.axhline(median_val, color='red', linestyle='--', linewidth=1.0,
               label=f'Medyan={median_val:.2f}')

    # Scatter (nokta nokta, cizgi yok — 6000 nokta icin daha okunakli)
    ax.scatter(all_x, all_vals, s=2, alpha=0.4, color='steelblue', zorder=3)

    # Null isaretleri
    if len(null_x) > 0:
        y_null = all_vals.min() - iqr * 0.05
        ax.scatter(null_x, [y_null]*len(null_x), marker='x', color='red',
                   s=15, linewidths=0.8, alpha=0.6, label=f'Null={n_null}', zorder=4)

    ax.set_xlabel('Duzlestirmis Indeks (satir×10 + basak_no)', fontsize=9)
    ax.set_ylabel(f'{birim}', fontsize=9)
    ax.set_title(
        f'{baslik}\n{stats_str}\nMAD 3.5 sinir disinda: {n_mad_out} deger ({100*n_mad_out/n_valid:.1f}%)',
        fontsize=8.5, pad=8
    )
    ax.legend(fontsize=7.5, loc='upper right', ncol=2)
    ax.grid(True, alpha=0.25, linewidth=0.4)

    plt.tight_layout()
    out_path = os.path.join(fig_dir, f'b1b10_line_{tip_kisa}.png')
    plt.savefig(out_path, dpi=130, bbox_inches='tight')
    plt.close()
    print(f"  [OK] {out_path}")

print("\nTamamlandi.")
