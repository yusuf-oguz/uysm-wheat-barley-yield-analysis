"""
Bolum 6: Sap Boyu Analizleri
- 6.1 Sap bilesenleri boxplot (H39, I39, J39)
- 6.2 Sap boyu vs verim scatter (il bazli)
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
OUT = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\output\sap'

df = pd.read_csv(CSV, encoding='utf-8-sig', low_memory=False)

# ── 6.1 Sap boy bilesenleri boxplot ──────────────────────────────────────────
sap_cols = [
    ('ort_sap_basak_boyu__H39',       'Sap Basak Boyu\n(H39, cm)'),
    ('ort_sap_basak_alti_boyu__I39',  'Sap Alt Boyu\n(I39, cm)'),
    ('ort_sap_boy_cm__J39',           'Toplam Sap Boyu\n(J39 = H+I, cm)'),
]

fig, axes = plt.subplots(1, 3, figsize=(12, 6), sharey=False)
for ax, (col, label) in zip(axes, sap_cols):
    s = df[col].dropna()
    bp = ax.boxplot(s, patch_artist=True,
                    boxprops=dict(facecolor='steelblue', alpha=0.65),
                    medianprops=dict(color='red', linewidth=2.5),
                    flierprops=dict(marker='.', markersize=4, alpha=0.4),
                    widths=0.5)
    ax.set_title(f'{label}\nn={len(s)}, null={df[col].isna().sum()}', fontsize=10)
    ax.set_xticks([])

    # Istatistik kutusu
    textstr = f'Med={s.median():.1f}\nMean={s.mean():.1f}\nStd={s.std():.1f}\nMin={s.min():.1f}\nMax={s.max():.1f}'
    ax.text(0.97, 0.97, textstr, transform=ax.transAxes,
            fontsize=8, va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylabel('cm', fontsize=9)

plt.suptitle('Sap Boyu Bilesenleri — Dagilim Karsilastirmasi', fontsize=12)
plt.tight_layout()
plt.savefig(f'{OUT}/sap_boy_dagilim.png', dpi=130, bbox_inches='tight')
plt.close()
print("6.1 sap_boy_dagilim.png kaydedildi")

# ── 6.2 Sap boyu vs verim (il bazli ozet) ────────────────────────────────────
il_sap = df.groupby('il_koordinat_final').agg(
    sap_median=('ort_sap_boy_cm__J39', 'median'),
    c21_median=('dane_m2_hesap_gram__C21', 'median'),
    n=('dosya_adi__dosyaadi', 'count')
).dropna().reset_index()
il_sap = il_sap[il_sap['n'] >= 5]

r, p = stats.pearsonr(il_sap['sap_median'], il_sap['c21_median'])

fig, ax = plt.subplots(figsize=(9, 6))
sc = ax.scatter(il_sap['sap_median'], il_sap['c21_median'],
                s=il_sap['n'] * 4, alpha=0.7, color='steelblue',
                edgecolors='white', linewidths=0.5)

for _, row in il_sap.iterrows():
    ax.annotate(row['il_koordinat_final'],
                (row['sap_median'], row['c21_median']),
                fontsize=6.5, ha='center', va='bottom',
                xytext=(0, 4), textcoords='offset points', color='#333')

slope, intercept, *_ = stats.linregress(il_sap['sap_median'], il_sap['c21_median'])
xline = np.linspace(il_sap['sap_median'].min(), il_sap['sap_median'].max(), 200)
ax.plot(xline, slope*xline+intercept, 'r--', linewidth=1.5,
        label=f'Trend (r={r:.3f}, p={p:.3f})')

ax.set_xlabel('Il Medyan Sap Boyu — J39 (cm)', fontsize=10)
ax.set_ylabel('Il Medyan C21 Verim (g/m²)', fontsize=10)
ax.set_title(f'Il Bazinda Sap Boyu vs Verim\n(daire buyuklugu = n, min n=5, {len(il_sap)} il)', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/sap_boy_vs_verim.png', dpi=130, bbox_inches='tight')
plt.close()
print("6.2 sap_boy_vs_verim.png kaydedildi")
print("Bolum 6 tamamlandi.")
