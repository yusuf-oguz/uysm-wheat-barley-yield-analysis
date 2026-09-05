"""
Bolum 1: Tanimlayici Istatistikler
- 1.1 Ozet istatistik tablosu
- 1.2 C21/D21 dagilim (histogram+KDE)
- 1.3 C21 vs D21 scatter
- 1.4 Basak olcum ortalamalar boxplot
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

CSV  = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\vAnaliz1.0.csv'
OUT  = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\output\tanim'

df = pd.read_csv(CSV, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir")

# ── 1.1 Ozet istatistik ───────────────────────────────────────────────────────
sayisal = df.select_dtypes(include='number').columns.tolist()
rows = []
for col in sayisal:
    s = df[col].dropna()
    if len(s) == 0:
        continue
    rows.append({
        'sutun': col,
        'n_dolu': len(s),
        'n_null': df[col].isna().sum(),
        'mean':   round(s.mean(), 3),
        'std':    round(s.std(), 3),
        'min':    round(s.min(), 3),
        'Q1':     round(s.quantile(0.25), 3),
        'median': round(s.median(), 3),
        'Q3':     round(s.quantile(0.75), 3),
        'max':    round(s.max(), 3),
        'skewness': round(float(s.skew()), 3),
    })
ozet = pd.DataFrame(rows)
ozet.to_csv(f'{OUT}/ozet_istatistik.csv', index=False, encoding='utf-8-sig')
print("1.1 ozet_istatistik.csv kaydedildi")

# ── 1.2 C21 / D21 dagilim ────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, col, label, color in zip(
        axes,
        ['dane_m2_hesap_gram__C21', 'dane_m2_gercek_gram__D21'],
        ['C21 — Basak Sayisi Bazli Verim (g/m²)', 'D21 — Tartim Bazli Verim (g/m²)'],
        ['steelblue', 'darkorange']):
    s = df[col].dropna()
    ax.hist(s, bins=40, density=True, alpha=0.55, color=color, edgecolor='white', linewidth=0.4)
    kde_x = np.linspace(s.min(), s.max(), 300)
    kde = stats.gaussian_kde(s)
    ax.plot(kde_x, kde(kde_x), color=color, linewidth=2)
    ax.axvline(s.median(), color='red', linestyle='--', linewidth=1.2, label=f'Medyan={s.median():.0f}')
    ax.axvline(s.mean(),   color='green', linestyle=':', linewidth=1.2, label=f'Ortalama={s.mean():.0f}')
    ax.set_title(f'{label}\nn={len(s)}, std={s.std():.0f}, skew={s.skew():.2f}', fontsize=10)
    ax.set_xlabel('g/m²', fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/verim_dagilim.png', dpi=130, bbox_inches='tight')
plt.close()
print("1.2 verim_dagilim.png kaydedildi")

# ── 1.3 C21 vs D21 scatter ───────────────────────────────────────────────────
both = df[['dane_m2_hesap_gram__C21','dane_m2_gercek_gram__D21']].dropna()
x, y = both['dane_m2_hesap_gram__C21'], both['dane_m2_gercek_gram__D21']
r, p = stats.pearsonr(x, y)
slope, intercept, *_ = stats.linregress(x, y)
xline = np.linspace(x.min(), x.max(), 200)

fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(x, y, s=18, alpha=0.45, color='steelblue', zorder=3)
ax.plot(xline, slope*xline+intercept, color='red', linewidth=1.5, label=f'Regresyon (r={r:.3f}, p={p:.2e})')
ax.plot([0, max(x.max(), y.max())], [0, max(x.max(), y.max())],
        'k--', linewidth=1, alpha=0.4, label='y=x (esit)')
ax.set_xlabel('C21 — Basak Sayisi Bazli (g/m²)', fontsize=10)
ax.set_ylabel('D21 — Tartim Bazli (g/m²)', fontsize=10)
ax.set_title(f'C21 vs D21 Verim Karsilastirmasi\nn={len(both)}, r={r:.3f}', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/c21_vs_d21.png', dpi=130, bbox_inches='tight')
plt.close()
print("1.3 c21_vs_d21.png kaydedildi")

# ── 1.4 Basak olcum ortalamalari boxplot ─────────────────────────────────────
olcum_cols = [
    ('ort_basak_uzunluk_cm__B40',              'Uzunluk\n(cm)'),
    ('ort_basak_agirlik_mg__C40',              'Agirlik\n(mg)'),
    ('ort_dane_sayisi__D40',                   'Dane\nSayisi'),
    ('bir_basaktaki_ort_dane_agirlik_gram__C20','Dane Ag.\n(g)'),
    ('ort_sap_basak_boyu__H39',                'Sap Basak\n(cm)'),
    ('ort_sap_basak_alti_boyu__I39',           'Sap Alt\n(cm)'),
    ('ort_sap_boy_cm__J39',                    'Sap Boy\n(cm)'),
]
fig, axes = plt.subplots(1, len(olcum_cols), figsize=(16, 5))
for ax, (col, label) in zip(axes, olcum_cols):
    s = df[col].dropna()
    ax.boxplot(s, patch_artist=True,
               boxprops=dict(facecolor='steelblue', alpha=0.6),
               medianprops=dict(color='red', linewidth=2),
               flierprops=dict(marker='.', markersize=3, alpha=0.4))
    ax.set_title(label, fontsize=9)
    ax.tick_params(labelsize=8)
    ax.set_xticks([])
    n_null = df[col].isna().sum()
    ax.set_xlabel(f'n={len(s)}\nnull={n_null}', fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')
plt.suptitle('10 Basak Olcum Ortalamalar — Boxplot', fontsize=12, y=1.01)
plt.tight_layout()
plt.savefig(f'{OUT}/basak_olcum_boxplot.png', dpi=130, bbox_inches='tight')
plt.close()
print("1.4 basak_olcum_boxplot.png kaydedildi")
print("Bolum 1 tamamlandi.")
