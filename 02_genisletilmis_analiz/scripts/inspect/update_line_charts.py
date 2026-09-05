import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import os
import glob

# --- Paths ---
csv_path = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\vAnaliz1.0.csv'
fig_dir  = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\docs\figures'

# --- 1. Delete dag_* and b1b10_dagilim.png ---
deleted = []
for f in glob.glob(os.path.join(fig_dir, 'dag_*.png')):
    os.remove(f)
    deleted.append(os.path.basename(f))
b1b10 = os.path.join(fig_dir, 'b1b10_dagilim.png')
if os.path.exists(b1b10):
    os.remove(b1b10)
    deleted.append('b1b10_dagilim.png')
if deleted:
    print(f"Silindi ({len(deleted)}): {', '.join(deleted)}")
else:
    print("Silinecek dag_* dosyasi yok.")

# --- 2. Load data ---
df = pd.read_csv(csv_path, encoding='utf-8-sig', low_memory=False)
print(f"Veri yuklendi: {len(df)} satir, {len(df.columns)} sutun")

# --- 3. Column list ---
analiz_sutunlari = [
    ('dane_m2_hesap_gram__C21',                     'Verim - Basak Sayisi Bazli (C21)',           'g/m2'),
    ('dane_m2_gercek_gram__D21',                    'Verim - Tartim Bazli (D21)',                 'g/m2'),
    ('ort_basak_uzunluk_cm__B40',                   'Ort. Basak Uzunlugu (B40)',                  'cm'),
    ('ort_basak_agirlik_mg__C40',                   'Ort. Basak Agirligi (C40)',                  'mg'),
    ('ort_dane_sayisi__D40',                        'Ort. Dane Sayisi (D40)',                     'adet'),
    ('ort_dane_agirlik_mg__E40',                    'Ort. Dane Agirligi (E40)',                   'mg'),
    ('bir_basaktaki_ort_dane_agirlik_gram__C20',    'Ort. Dane Agirligi (C20)',                   'g'),
    ('bin_dane_agirlik_gram__C22',                  'Tek Dane Agirligi (C22)',                    'mg'),
    ('basak_dane_oran__D41',                        'Dane Orani (D41)',                           '-'),
    ('ort_sap_boy_cm__J39',                         'Ort. Sap Boyu (J39)',                        'cm'),
    ('ort_sap_basak_boyu__H39',                     'Ort. Sap Basak Boyu (H39)',                  'cm'),
    ('ort_sap_basak_alti_boyu__I39',                'Ort. Sap Alt Boyu (I39)',                    'cm'),
    ('olcum_alani_basak__C11',                      'Olcum Alani Basak Sayisi (C11)',              'adet'),
    ('m2_basak_sayisi__C12',                        '1m2 Basak Sayisi (C12)',                      'adet'),
    ('olcum_basak_agirlik_ham__C41',                'Lab Tartim - Olcum Alani (C41)',              'mg'),
]

# --- 4. Generate line charts ---
generated = []
for col, baslik, birim in analiz_sutunlari:
    if col not in df.columns:
        print(f"  [ATLA] {col} sutunu bulunamadi")
        continue

    series = df[col]
    vals   = series.dropna()

    if len(vals) == 0:
        print(f"  [ATLA] {col} - hic dolu deger yok")
        continue

    median_val = vals.median()
    q1 = vals.quantile(0.25)
    q3 = vals.quantile(0.75)
    iqr = q3 - q1
    n_null = series.isna().sum()
    n_total = len(series)

    stats_str = (
        f"n={n_total}  null={n_null}  "
        f"min={vals.min():.2f}  max={vals.max():.2f}  "
        f"median={median_val:.2f}  "
        f"Q1={q1:.2f}  Q3={q3:.2f}  IQR={iqr:.2f}"
    )

    x_valid = np.where(series.notna())[0]
    y_valid = series.dropna().values
    x_null  = np.where(series.isna())[0]
    y_null_marker = vals.min() - iqr * 0.1 if len(vals) > 0 else 0

    fig, ax = plt.subplots(figsize=(16, 5))

    ax.axhspan(q1, q3, alpha=0.12, color='orange', label='IQR (Q1-Q3)')
    ax.axhline(median_val, color='red', linestyle='--', linewidth=1.2, label=f'Medyan={median_val:.2f}')
    ax.plot(x_valid, y_valid, color='steelblue', linewidth=0.7, alpha=0.8)
    ax.scatter(x_valid, y_valid, color='steelblue', s=8, alpha=0.6, zorder=3)

    if len(x_null) > 0:
        ax.scatter(x_null, [y_null_marker] * len(x_null),
                   marker='x', color='red', s=30, linewidths=1.2,
                   alpha=0.7, label=f'Null={n_null}', zorder=4)

    ax.set_xlabel('Satir Indeksi', fontsize=9)
    ax.set_ylabel(f'{baslik} ({birim})', fontsize=9)
    ax.set_title(f'{baslik}\n[{col}]\n{stats_str}', fontsize=9, pad=8)
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, alpha=0.3, linewidth=0.5)

    plt.tight_layout()
    out_path = os.path.join(fig_dir, f'line_{col}.png')
    plt.savefig(out_path, dpi=130, bbox_inches='tight')
    plt.close()
    generated.append(f'line_{col}.png')
    print(f"  [OK] {out_path}")

print(f"\nTamamlandi. Uretilen: {len(generated)} line chart.")
