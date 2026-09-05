"""
Bolum 4: Morfoloji Analizleri
- 4.1 Korelasyon matrisi isi haritasi
- 4.2 Dane orani dagilimi
- 4.3 Basak agirlik vs verim scatter
- 4.4 Sap boyu vs basak uzunlugu scatter
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
OUT = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\output\morfoloji'

df = pd.read_csv(CSV, encoding='utf-8-sig', low_memory=False)

# ── 4.1 Korelasyon matrisi ────────────────────────────────────────────────────
korel_cols = {
    'Uzunluk\n(B40)':    'ort_basak_uzunluk_cm__B40',
    'Agirlik\n(C40)':    'ort_basak_agirlik_mg__C40',
    'Dane Say.\n(D40)':  'ort_dane_sayisi__D40',
    'Dane Ag.\n(E40)':   'ort_dane_agirlik_mg__E40',
    'Tek Dane\n(C22)':   'bin_dane_agirlik_gram__C22',
    'Dane Oran\n(D41)':  'basak_dane_oran__D41',
    'Sap Basak\n(H39)':  'ort_sap_basak_boyu__H39',
    'Sap Alt\n(I39)':    'ort_sap_basak_alti_boyu__I39',
    'Sap Boy\n(J39)':    'ort_sap_boy_cm__J39',
    'Verim C21':         'dane_m2_hesap_gram__C21',
    'Verim D21':         'dane_m2_gercek_gram__D21',
}
sub = df[[v for v in korel_cols.values() if v in df.columns]].dropna()
corr = sub.corr(method='spearman')
corr.index   = list(korel_cols.keys())[:len(corr)]
corr.columns = list(korel_cols.keys())[:len(corr)]

fig, ax = plt.subplots(figsize=(11, 9))
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
plt.colorbar(im, ax=ax, shrink=0.8, label='Spearman r')
ax.set_xticks(range(len(corr)))
ax.set_yticks(range(len(corr)))
ax.set_xticklabels(corr.columns, fontsize=8)
ax.set_yticklabels(corr.index, fontsize=8)
for i in range(len(corr)):
    for j in range(len(corr)):
        v = corr.iloc[i, j]
        ax.text(j, i, f'{v:.2f}', ha='center', va='center',
                fontsize=7, color='white' if abs(v) > 0.6 else 'black')
ax.set_title('Morfoloji + Verim Spearman Korelasyon Matrisi', fontsize=12)
plt.tight_layout()
plt.savefig(f'{OUT}/korelasyon_matrisi.png', dpi=130, bbox_inches='tight')
plt.close()
print("4.1 korelasyon_matrisi.png kaydedildi")

# ── 4.2 Dane orani dagilimi ───────────────────────────────────────────────────
s = df['basak_dane_oran__D41'].dropna()
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(s, bins=50, color='steelblue', alpha=0.7, edgecolor='white', linewidth=0.4)
ax.axvline(s.median(), color='red', linestyle='--', linewidth=1.5, label=f'Medyan={s.median():.3f}')
ax.axvline(s.mean(),   color='green', linestyle=':', linewidth=1.5, label=f'Ortalama={s.mean():.3f}')
ax.axvline(1.0, color='black', linestyle='-', linewidth=1, alpha=0.5, label='D41=1 (biyolojik sinir)')
ax.set_xlabel('Dane Orani (D41 = E40/C40)', fontsize=10)
ax.set_ylabel('Frekans', fontsize=10)
ax.set_title(f'Dane Orani Dagilimi\nn={len(s)}, D41>1 sayisi: {(s>1).sum()}', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/dane_orani_dagilim.png', dpi=130, bbox_inches='tight')
plt.close()
print("4.2 dane_orani_dagilim.png kaydedildi")

# ── 4.3 Basak agirlik vs verim ────────────────────────────────────────────────
both = df[['ort_basak_agirlik_mg__C40','dane_m2_hesap_gram__C21','il_koordinat_final']].dropna()
iller = both['il_koordinat_final'].unique()
cmap  = plt.cm.tab20
renk_map = {il: cmap(i % 20) for i, il in enumerate(sorted(iller))}

fig, ax = plt.subplots(figsize=(9, 6))
for il, grp in both.groupby('il_koordinat_final'):
    ax.scatter(grp['ort_basak_agirlik_mg__C40'], grp['dane_m2_hesap_gram__C21'],
               s=20, alpha=0.55, color=renk_map[il], label=il if len(grp) >= 10 else None)

# Trend cizgisi
x, y = both['ort_basak_agirlik_mg__C40'], both['dane_m2_hesap_gram__C21']
slope, intercept, r, p, _ = stats.linregress(x, y)
xline = np.linspace(x.min(), x.max(), 200)
ax.plot(xline, slope*xline+intercept, 'k--', linewidth=1.5,
        label=f'Trend (r={r:.3f}, p={p:.2e})')

ax.set_xlabel('Ort. Basak Agirligi — C40 (mg)', fontsize=10)
ax.set_ylabel('C21 Verim (g/m²)', fontsize=10)
ax.set_title(f'Basak Agirligi vs Verim (n={len(both)})', fontsize=11)
handles, labels = ax.get_legend_handles_labels()
# Sadece n>=10 olan il etiketleri + trend
ax.legend(handles, labels, fontsize=7, ncol=3, loc='upper left',
          framealpha=0.7, markerscale=1.5)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/basak_agirlik_vs_verim.png', dpi=130, bbox_inches='tight')
plt.close()
print("4.3 basak_agirlik_vs_verim.png kaydedildi")

# ── 4.4 Sap boyu vs basak uzunlugu ───────────────────────────────────────────
both2 = df[['ort_sap_boy_cm__J39','ort_basak_uzunluk_cm__B40','dane_m2_hesap_gram__C21']].dropna()
x2, y2 = both2['ort_sap_boy_cm__J39'], both2['ort_basak_uzunluk_cm__B40']
r2, p2 = stats.pearsonr(x2, y2)

fig, ax = plt.subplots(figsize=(8, 6))
sc = ax.scatter(x2, y2, c=both2['dane_m2_hesap_gram__C21'],
                cmap='RdYlGn', s=25, alpha=0.65, edgecolors='white', linewidths=0.3,
                vmin=both2['dane_m2_hesap_gram__C21'].quantile(0.05),
                vmax=both2['dane_m2_hesap_gram__C21'].quantile(0.95))
cbar = plt.colorbar(sc, ax=ax, shrink=0.8)
cbar.set_label('C21 Verim (g/m²)', fontsize=9)

slope2, int2, *_ = stats.linregress(x2, y2)
xline2 = np.linspace(x2.min(), x2.max(), 200)
ax.plot(xline2, slope2*xline2+int2, 'k--', linewidth=1.5,
        label=f'Trend (r={r2:.3f}, p={p2:.2e})')

ax.set_xlabel('Ort. Toplam Sap Boyu — J39 (cm)', fontsize=10)
ax.set_ylabel('Ort. Basak Uzunlugu — B40 (cm)', fontsize=10)
ax.set_title(f'Sap Boyu vs Basak Uzunlugu\n(renk=C21 verimi, n={len(both2)})', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/sap_vs_basak_uzunluk.png', dpi=130, bbox_inches='tight')
plt.close()
print("4.4 sap_vs_basak_uzunluk.png kaydedildi")
print("Bolum 4 tamamlandi.")
