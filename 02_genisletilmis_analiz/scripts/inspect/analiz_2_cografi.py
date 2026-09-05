"""
Bolum 2: Cografi / Il Bazli Analiz
- 2.1 Il bazinda verim bar chart
- 2.2 Il bazinda verim boxplot
- 2.3 Turkiye haritasi scatter
- 2.4 Il ozet CSV
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

CSV = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\vAnaliz1.0.csv'
OUT = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\output\cografi'

df = pd.read_csv(CSV, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir")

MIN_N = 5  # minimum kayit sayisi

# ── 2.4 Il ozet CSV (once hesapla, diger grafiklerde kullan) ─────────────────
il_ozet_rows = []
for il, grp in df.groupby('il_koordinat_final'):
    c21 = grp['dane_m2_hesap_gram__C21'].dropna()
    d21 = grp['dane_m2_gercek_gram__D21'].dropna()
    il_ozet_rows.append({
        'il': il,
        'n': len(grp),
        'n_c21': len(c21),
        'c21_median': round(c21.median(), 1) if len(c21) > 0 else np.nan,
        'c21_mean':   round(c21.mean(), 1)   if len(c21) > 0 else np.nan,
        'c21_std':    round(c21.std(), 1)     if len(c21) > 0 else np.nan,
        'c21_min':    round(c21.min(), 1)     if len(c21) > 0 else np.nan,
        'c21_max':    round(c21.max(), 1)     if len(c21) > 0 else np.nan,
        'n_d21': len(d21),
        'd21_median': round(d21.median(), 1) if len(d21) > 0 else np.nan,
        'd21_mean':   round(d21.mean(), 1)   if len(d21) > 0 else np.nan,
        'd21_std':    round(d21.std(), 1)     if len(d21) > 0 else np.nan,
        'enlem_ort':  round(grp['enlem_dd_final'].mean(), 4),
        'boylam_ort': round(grp['boylam_dd_final'].mean(), 4),
    })
il_ozet = pd.DataFrame(il_ozet_rows).sort_values('c21_median', ascending=False)
il_ozet.to_csv(f'{OUT}/il_ozet.csv', index=False, encoding='utf-8-sig')
print("2.4 il_ozet.csv kaydedildi")

# Minimum n filtresi
il_filtre = il_ozet[il_ozet['n'] >= MIN_N].copy()

# ── 2.1 Bar chart ─────────────────────────────────────────────────────────────
il_bar = il_filtre.sort_values('c21_median', ascending=True)
n_il = len(il_bar)
fig, ax = plt.subplots(figsize=(10, max(8, n_il * 0.28)))

colors_c21 = plt.cm.RdYlGn(np.linspace(0.15, 0.85, n_il))
bars = ax.barh(range(n_il), il_bar['c21_median'], color=colors_c21, alpha=0.85, height=0.6, label='C21 medyan')
ax.barh(range(n_il), il_bar['d21_median'], color='steelblue', alpha=0.4, height=0.6, label='D21 medyan', left=0)

ax.set_yticks(range(n_il))
ax.set_yticklabels([f"{r['il']} (n={r['n']})" for _, r in il_bar.iterrows()], fontsize=8)
ax.set_xlabel('Verim (g/m²)', fontsize=10)
ax.set_title(f'Il Bazinda Bugday Verimi — C21 Medyan\n(min n={MIN_N}, {n_il} il)', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, axis='x')
ax.axvline(il_bar['c21_median'].median(), color='red', linestyle='--', linewidth=1,
           label=f'Genel medyan={il_bar["c21_median"].median():.0f}')

for i, (_, r) in enumerate(il_bar.iterrows()):
    ax.text(r['c21_median'] + 10, i, f"{r['c21_median']:.0f}", va='center', fontsize=7)

plt.tight_layout()
plt.savefig(f'{OUT}/il_verim_bar.png', dpi=130, bbox_inches='tight')
plt.close()
print("2.1 il_verim_bar.png kaydedildi")

# ── 2.2 Boxplot ───────────────────────────────────────────────────────────────
il_box = il_filtre.sort_values('c21_median', ascending=False)
iller = il_box['il'].tolist()

box_data = []
for il in iller:
    s = df[df['il_koordinat_final'] == il]['dane_m2_hesap_gram__C21'].dropna()
    box_data.append(s.values)

fig, ax = plt.subplots(figsize=(max(14, len(iller) * 0.55), 6))
bp = ax.boxplot(box_data, patch_artist=True, vert=True,
                medianprops=dict(color='red', linewidth=2),
                flierprops=dict(marker='.', markersize=3, alpha=0.4))

cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(vmin=il_box['c21_median'].min(), vmax=il_box['c21_median'].max())
for patch, il in zip(bp['boxes'], iller):
    med = il_box[il_box['il'] == il]['c21_median'].values[0]
    patch.set_facecolor(cmap(norm(med)))
    patch.set_alpha(0.7)

ax.set_xticks(range(1, len(iller)+1))
ax.set_xticklabels([f"{il}\n(n={il_box[il_box['il']==il]['n'].values[0]})"
                    for il in iller], rotation=45, ha='right', fontsize=7.5)
ax.set_ylabel('C21 Verim (g/m²)', fontsize=10)
ax.set_title(f'Il Bazinda Verim Dagilimi — C21 Boxplot\n(min n={MIN_N}, {len(iller)} il)', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
ax.axhline(df['dane_m2_hesap_gram__C21'].median(), color='navy', linestyle='--',
           linewidth=1, alpha=0.6, label=f'Genel medyan={df["dane_m2_hesap_gram__C21"].median():.0f}')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(f'{OUT}/il_verim_boxplot.png', dpi=130, bbox_inches='tight')
plt.close()
print("2.2 il_verim_boxplot.png kaydedildi")

# ── 2.3 Harita scatter ────────────────────────────────────────────────────────
df_map = df[['enlem_dd_final','boylam_dd_final','dane_m2_hesap_gram__C21']].dropna()

fig, ax = plt.subplots(figsize=(13, 7))
sc = ax.scatter(df_map['boylam_dd_final'], df_map['enlem_dd_final'],
                c=df_map['dane_m2_hesap_gram__C21'],
                cmap='RdYlGn', s=40, alpha=0.75, edgecolors='white', linewidths=0.3,
                vmin=df_map['dane_m2_hesap_gram__C21'].quantile(0.05),
                vmax=df_map['dane_m2_hesap_gram__C21'].quantile(0.95))
cbar = plt.colorbar(sc, ax=ax, shrink=0.7)
cbar.set_label('C21 Verim (g/m²)', fontsize=9)

# Il etiketleri (min n=10)
for _, r in il_ozet[il_ozet['n'] >= 10].iterrows():
    ax.annotate(r['il'], (r['boylam_ort'], r['enlem_ort']),
                fontsize=6.5, ha='center', color='#333333',
                bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.5, linewidth=0))

ax.set_xlabel('Boylam', fontsize=9)
ax.set_ylabel('Enlem', fontsize=9)
ax.set_title(f'Turkiye Bugday Verimi Dagilimi (C21)\nn={len(df_map)} kayit', fontsize=12)
ax.set_xlim(25.5, 45.0)
ax.set_ylim(35.5, 42.5)
ax.grid(True, alpha=0.25, linewidth=0.5)
plt.tight_layout()
plt.savefig(f'{OUT}/harita_verim.png', dpi=130, bbox_inches='tight')
plt.close()
print("2.3 harita_verim.png kaydedildi")
print("Bolum 2 tamamlandi.")
