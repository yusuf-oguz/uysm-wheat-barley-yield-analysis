"""
Bolum 7: Enlem / Boylam Korelasyon Analizi
Tum sayisal analiz sutunlari ile enlem ve boylam arasindaki
Spearman korelasyonlarini hesapla, anlamlilarini gorsellestir.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

CSV = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\vAnaliz1.0.csv'
OUT = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\output'

import os
os.makedirs(f'{OUT}/koordinat', exist_ok=True)

df = pd.read_csv(CSV, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir")

# Analiz edilecek sutunlar (b1-b10 ham haric, yorumlamasi zor)
analiz_cols = [
    ('dane_m2_hesap_gram__C21',              'C21 Verim (g/m²)'),
    ('dane_m2_gercek_gram__D21',             'D21 Verim (g/m²)'),
    ('ort_basak_uzunluk_cm__B40',            'Ort. Basak Uzunlugu (cm)'),
    ('ort_basak_agirlik_mg__C40',            'Ort. Basak Agirligi (mg)'),
    ('ort_dane_sayisi__D40',                 'Ort. Dane Sayisi'),
    ('ort_dane_agirlik_mg__E40',             'Ort. Dane Agirligi (mg)'),
    ('bir_basaktaki_ort_dane_agirlik_gram__C20', 'Tek Basak Dane Ag. (g)'),
    ('bin_dane_agirlik_gram__C22',           'Tek Dane Agirligi (mg)'),
    ('basak_dane_oran__D41',                 'Dane Orani (D41)'),
    ('ort_sap_basak_boyu__H39',              'Sap Basak Boyu (cm)'),
    ('ort_sap_basak_alti_boyu__I39',         'Sap Alt Boyu (cm)'),
    ('ort_sap_boy_cm__J39',                  'Toplam Sap Boyu (cm)'),
    ('olcum_alani_basak__C11',               'Olcum Alani Basak Sayisi'),
    ('m2_basak_sayisi__C12',                 '1m2 Basak Sayisi'),
    ('olcum_basak_agirlik_ham__C41',         'Lab Tartim C41 (mg)'),
    ('m2_sap_agirlik_kg__C17',               'Sap Agirligi (kg/m2)'),
]

# ── Korelasyon hesapla ────────────────────────────────────────────────────────
results = []
for col, label in analiz_cols:
    if col not in df.columns:
        continue
    sub = df[['enlem_dd_final', 'boylam_dd_final', col]].dropna()
    if len(sub) < 30:
        continue

    r_enl, p_enl = stats.spearmanr(sub['enlem_dd_final'],  sub[col])
    r_boy, p_boy = stats.spearmanr(sub['boylam_dd_final'], sub[col])

    results.append({
        'sutun': col,
        'label': label,
        'n': len(sub),
        'enlem_r':  round(r_enl, 3),
        'enlem_p':  round(p_enl, 4),
        'boylam_r': round(r_boy, 3),
        'boylam_p': round(p_boy, 4),
        'enlem_sig':  abs(r_enl) >= 0.3 and p_enl < 0.05,
        'boylam_sig': abs(r_boy) >= 0.3 and p_boy < 0.05,
    })

res = pd.DataFrame(results).sort_values('enlem_r', key=abs, ascending=False)
res.to_csv(f'{OUT}/koordinat/koordinat_korelasyon.csv', index=False, encoding='utf-8-sig')
print("koordinat_korelasyon.csv kaydedildi")
print("\nTum korelasyonlar:")
for _, row in res.iterrows():
    enl_flag = '***' if row['enlem_sig'] else '   '
    boy_flag = '***' if row['boylam_sig'] else '   '
    print(f"  {row['label']:<35} enlem r={row['enlem_r']:+.3f} {enl_flag}  boylam r={row['boylam_r']:+.3f} {boy_flag}  n={row['n']}")

# ── 1. Ozet heatmap: tum korelasyonlar ───────────────────────────────────────
labels_short = [r['label'] for _, r in res.iterrows()]
enlem_r  = res['enlem_r'].values
boylam_r = res['boylam_r'].values
enlem_p  = res['enlem_p'].values
boylam_p = res['boylam_p'].values

matrix = np.array([enlem_r, boylam_r]).T  # (n_vars, 2)

fig, ax = plt.subplots(figsize=(7, max(6, len(labels_short) * 0.45)))
im = ax.imshow(matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
plt.colorbar(im, ax=ax, shrink=0.6, label='Spearman r')

ax.set_xticks([0, 1])
ax.set_xticklabels(['Enlem', 'Boylam'], fontsize=11)
ax.set_yticks(range(len(labels_short)))
ax.set_yticklabels(labels_short, fontsize=8.5)

for i, (r_e, p_e, r_b, p_b) in enumerate(zip(enlem_r, enlem_p, boylam_r, boylam_p)):
    sig_e = '*' if p_e < 0.05 else ''
    sig_b = '*' if p_b < 0.05 else ''
    ax.text(0, i, f'{r_e:+.2f}{sig_e}', ha='center', va='center', fontsize=8,
            color='white' if abs(r_e) > 0.5 else 'black', fontweight='bold' if p_e < 0.01 else 'normal')
    ax.text(1, i, f'{r_b:+.2f}{sig_b}', ha='center', va='center', fontsize=8,
            color='white' if abs(r_b) > 0.5 else 'black', fontweight='bold' if p_b < 0.01 else 'normal')

ax.set_title('Enlem / Boylam Korelasyonlari (Spearman)\n* p<0.05, kalin p<0.01', fontsize=10)
plt.tight_layout()
plt.savefig(f'{OUT}/koordinat/koordinat_korelasyon_heatmap.png', dpi=130, bbox_inches='tight')
plt.close()
print("koordinat_korelasyon_heatmap.png kaydedildi")

# ── 2. Anlamli sutunlar icin scatter grafikleri ───────────────────────────────
sig_rows = res[(res['enlem_sig']) | (res['boylam_sig'])].copy()
print(f"\nAnlamli (|r|>=0.3, p<0.05) sutun sayisi: {len(sig_rows)}")

if len(sig_rows) > 0:
    # Enlem scatterlar
    enl_sig = sig_rows[sig_rows['enlem_sig']].sort_values('enlem_r', key=abs, ascending=False)
    boy_sig = sig_rows[sig_rows['boylam_sig']].sort_values('boylam_r', key=abs, ascending=False)

    for coord, coord_col, coord_label, sig_df in [
        ('enlem',  'enlem_dd_final',  'Enlem (°N)',  enl_sig),
        ('boylam', 'boylam_dd_final', 'Boylam (°E)', boy_sig),
    ]:
        if len(sig_df) == 0:
            continue
        n_plots = len(sig_df)
        ncols = min(3, n_plots)
        nrows = (n_plots + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 4.5))
        axes = np.array(axes).flatten() if n_plots > 1 else [axes]

        for ax, (_, row) in zip(axes, sig_df.iterrows()):
            col, label = row['sutun'], row['label']
            sub = df[[coord_col, col]].dropna()
            x, y = sub[coord_col], sub[col]

            # Il ortalamalari ile scatter
            il_grp = df[['il_koordinat_final', coord_col, col]].dropna()
            il_med = il_grp.groupby('il_koordinat_final').agg(
                x_med=(coord_col, 'median'),
                y_med=(col, 'median'),
                n=('il_koordinat_final', 'count')
            ).reset_index()

            # Ham nokta (hafif)
            ax.scatter(x, y, s=8, alpha=0.2, color='steelblue', zorder=2)
            # Il ortalamalari (vurgulu)
            sc = ax.scatter(il_med['x_med'], il_med['y_med'],
                            s=il_med['n'] * 5, alpha=0.85, color='darkorange',
                            edgecolors='white', linewidths=0.5, zorder=4,
                            label='Il medyani (boyut=n)')

            # Regresyon (ham veri)
            slope, intercept, *_ = stats.linregress(x, y)
            xline = np.linspace(x.min(), x.max(), 200)
            ax.plot(xline, slope * xline + intercept, 'r-', linewidth=1.8, zorder=3)

            r_val = row[f'{coord}_r']
            p_val = row[f'{coord}_p']
            ax.set_xlabel(coord_label, fontsize=9)
            ax.set_ylabel(label, fontsize=9)
            ax.set_title(f'{label}\nSpearman r={r_val:+.3f}, p={p_val:.4f}, n={len(sub)}', fontsize=8.5)
            ax.legend(fontsize=7)
            ax.grid(True, alpha=0.3)

        # Bos eksenleri gizle
        for ax in axes[n_plots:]:
            ax.set_visible(False)

        plt.suptitle(f'{coord_label} ile Anlamli Korelasyonlar (|r|>=0.3)', fontsize=12, y=1.01)
        plt.tight_layout()
        plt.savefig(f'{OUT}/koordinat/{coord}_korelasyon_scatter.png', dpi=130, bbox_inches='tight')
        plt.close()
        print(f"{coord}_korelasyon_scatter.png kaydedildi ({n_plots} grafik)")

print("\nBolum 7 tamamlandi.")
