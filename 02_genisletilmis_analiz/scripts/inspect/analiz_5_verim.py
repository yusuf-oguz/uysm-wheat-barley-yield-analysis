"""
Bolum 5: Verim Bileseni Analizleri
- 5.1 C21 bilesenleri scatter matris (C20, C12, C21)
- 5.2 C41 vs D21 scatter
- 5.3 C21-D21 normalize fark dagilimi
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
OUT = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\output\verim'

df = pd.read_csv(CSV, encoding='utf-8-sig', low_memory=False)

# ── 5.1 C21 bilesenleri ───────────────────────────────────────────────────────
cols5 = ['bir_basaktaki_ort_dane_agirlik_gram__C20',
         'm2_basak_sayisi__C12',
         'dane_m2_hesap_gram__C21']
labels5 = ['C20 — Tek Basak Dane Ag. (g)', 'C12 — m² Basak Sayisi (adet)', 'C21 — Verim (g/m²)']

sub5 = df[cols5].dropna()
fig, axes = plt.subplots(len(cols5), len(cols5), figsize=(11, 10))

for i, (coli, li) in enumerate(zip(cols5, labels5)):
    for j, (colj, lj) in enumerate(zip(cols5, labels5)):
        ax = axes[i][j]
        if i == j:
            s = sub5[coli]
            ax.hist(s, bins=30, color='steelblue', alpha=0.7, edgecolor='white', linewidth=0.3)
            ax.set_title(li, fontsize=7.5)
        else:
            x, y = sub5[colj], sub5[coli]
            ax.scatter(x, y, s=8, alpha=0.3, color='steelblue')
            r, p = stats.pearsonr(x, y)
            ax.set_title(f'r={r:.3f}', fontsize=7.5, color='red' if abs(r) > 0.5 else 'black')
        if i == len(cols5)-1:
            ax.set_xlabel(lj, fontsize=7)
        if j == 0:
            ax.set_ylabel(li, fontsize=7)
        ax.tick_params(labelsize=6)

plt.suptitle('C21 Verim Bilesenleri — Scatter Matris\n(C21 = C20 × C12)', fontsize=11, y=1.01)
plt.tight_layout()
plt.savefig(f'{OUT}/c21_bilesenleri.png', dpi=130, bbox_inches='tight')
plt.close()
print("5.1 c21_bilesenleri.png kaydedildi")

# ── 5.2 C41 vs D21 ───────────────────────────────────────────────────────────
both = df[['olcum_basak_agirlik_ham__C41','dane_m2_gercek_gram__D21']].dropna()
x, y = both['olcum_basak_agirlik_ham__C41'], both['dane_m2_gercek_gram__D21']
r, p = stats.spearmanr(x, y)

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(x/1000, y, s=18, alpha=0.45, color='darkorange')
slope, intercept, *_ = stats.linregress(x, y)
xline = np.linspace(x.min(), x.max(), 200)
ax.plot(xline/1000, slope*xline+intercept, 'k--', linewidth=1.5,
        label=f'Trend (Spearman r={r:.3f}, p={p:.2e})')
ax.set_xlabel('C41 — Lab Tartim (gram)', fontsize=10)
ax.set_ylabel('D21 — Tartim Bazli Verim (g/m²)', fontsize=10)
ax.set_title(f'C41 (Ham Tartim) vs D21 (Tartim Verimi)\nn={len(both)}', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/c41_vs_d21.png', dpi=130, bbox_inches='tight')
plt.close()
print("5.2 c41_vs_d21.png kaydedildi")

# ── 5.3 C21-D21 normalize fark ───────────────────────────────────────────────
both2 = df[['dane_m2_hesap_gram__C21','dane_m2_gercek_gram__D21']].dropna()
ort = (both2['dane_m2_hesap_gram__C21'] + both2['dane_m2_gercek_gram__D21']) / 2
fark_norm = (both2['dane_m2_hesap_gram__C21'] - both2['dane_m2_gercek_gram__D21']) / ort * 100

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Histogram
ax = axes[0]
ax.hist(fark_norm, bins=50, color='steelblue', alpha=0.7, edgecolor='white', linewidth=0.4)
ax.axvline(0,  color='black', linestyle='-', linewidth=1, alpha=0.5, label='Sifir fark')
ax.axvline(fark_norm.median(), color='red', linestyle='--', linewidth=1.5,
           label=f'Medyan={fark_norm.median():.1f}%')
ax.axvline(fark_norm.mean(), color='green', linestyle=':', linewidth=1.5,
           label=f'Ortalama={fark_norm.mean():.1f}%')
ax.set_xlabel('(C21 - D21) / Ortalama × 100 (%)', fontsize=9)
ax.set_ylabel('Frekans', fontsize=9)
ax.set_title(f'C21-D21 Normalize Fark Dagilimi\nn={len(fark_norm)}', fontsize=10)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Bland-Altman benzeri
ax2 = axes[1]
ax2.scatter(ort, fark_norm, s=14, alpha=0.4, color='steelblue')
ax2.axhline(0, color='black', linewidth=1, alpha=0.5)
ax2.axhline(fark_norm.mean(), color='red', linestyle='--', linewidth=1.5,
            label=f'Bias={fark_norm.mean():.1f}%')
loa_upper = fark_norm.mean() + 1.96 * fark_norm.std()
loa_lower = fark_norm.mean() - 1.96 * fark_norm.std()
ax2.axhline(loa_upper, color='red', linestyle=':', linewidth=1,
            label=f'+1.96 SD={loa_upper:.1f}%')
ax2.axhline(loa_lower, color='red', linestyle=':', linewidth=1,
            label=f'-1.96 SD={loa_lower:.1f}%')
ax2.set_xlabel('Ortalama (C21+D21)/2 (g/m²)', fontsize=9)
ax2.set_ylabel('(C21 - D21) / Ortalama × 100 (%)', fontsize=9)
ax2.set_title('Bland-Altman Grafigi\n(C21 vs D21 Uyum Analizi)', fontsize=10)
ax2.legend(fontsize=7.5)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/c21_d21_fark.png', dpi=130, bbox_inches='tight')
plt.close()
print("5.3 c21_d21_fark.png kaydedildi")
print("Bolum 5 tamamlandi.")
