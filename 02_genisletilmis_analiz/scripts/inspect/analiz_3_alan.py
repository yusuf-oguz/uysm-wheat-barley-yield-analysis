"""
Bolum 3: Alan Carpani Bazli Analiz
- 3.1 E13 gruplarına gore verim boxplot + Kruskal-Wallis
- 3.2 C11 dagilimi E13 gruplarına gore scatter
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
OUT = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\output\alan'

df = pd.read_csv(CSV, encoding='utf-8-sig', low_memory=False)

gruplar = {4: '1/4 m² (E13=4)', 8: '1/8 m² (E13=8)', 16: '1/16 m² (E13=16)'}
renkler = {4: 'steelblue', 8: 'darkorange', 16: 'seagreen'}

# ── 3.1 Verim boxplot + Kruskal-Wallis ───────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 6))

for ax, (vcol, vlabel) in zip(axes, [
        ('dane_m2_hesap_gram__C21', 'C21 — Basak Sayisi Bazli Verim (g/m²)'),
        ('dane_m2_gercek_gram__D21', 'D21 — Tartim Bazli Verim (g/m²)')]):

    grp_data = []
    grp_labels = []
    grp_colors = []
    for e13_val in [4, 8, 16]:
        s = df[df['olcum_alani_carpani__E13'] == e13_val][vcol].dropna()
        grp_data.append(s.values)
        grp_labels.append(f"{gruplar[e13_val]}\nn={len(s)}")
        grp_colors.append(renkler[e13_val])

    bp = ax.boxplot(grp_data, patch_artist=True,
                    medianprops=dict(color='red', linewidth=2),
                    flierprops=dict(marker='.', markersize=4, alpha=0.4))
    for patch, color in zip(bp['boxes'], grp_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)

    # Kruskal-Wallis testi
    kw_stat, kw_p = stats.kruskal(*[d for d in grp_data if len(d) > 0])

    ax.set_xticks(range(1, 4))
    ax.set_xticklabels(grp_labels, fontsize=9)
    ax.set_ylabel('g/m²', fontsize=9)
    ax.set_title(f'{vlabel}\nKruskal-Wallis: H={kw_stat:.2f}, p={kw_p:.3f}', fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')

    # Grup medyanlarini yaz
    for i, (d, lbl) in enumerate(zip(grp_data, grp_labels), 1):
        if len(d) > 0:
            ax.text(i, np.median(d), f'{np.median(d):.0f}',
                    ha='center', va='bottom', fontsize=8, color='darkred', fontweight='bold')

plt.suptitle('Alan Carpanina (E13) Gore Verim Karsilastirmasi', fontsize=12)
plt.tight_layout()
plt.savefig(f'{OUT}/alan_carpani_verim.png', dpi=130, bbox_inches='tight')
plt.close()
print("3.1 alan_carpani_verim.png kaydedildi")

# ── 3.2 C11 dagilimi E13 gruplarına gore ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
for e13_val in [4, 8, 16]:
    sub = df[df['olcum_alani_carpani__E13'] == e13_val]['olcum_alani_basak__C11'].dropna()
    idx = df[df['olcum_alani_carpani__E13'] == e13_val].index
    ax.scatter(range(len(sub)), sub.values, s=12, alpha=0.5,
               color=renkler[e13_val], label=f'{gruplar[e13_val]} (n={len(sub)}, med={sub.median():.0f})')
    ax.axhline(sub.median(), color=renkler[e13_val], linestyle='--', linewidth=1, alpha=0.7)

ax.set_xlabel('Kayit Indeksi (grup icinde)', fontsize=9)
ax.set_ylabel('C11 — Olcum Alani Basak Sayisi (adet)', fontsize=9)
ax.set_title('C11 Basak Sayisi Dagilimi — E13 Alan Carpani Gruplarına Gore', fontsize=10)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/c11_dagilim.png', dpi=130, bbox_inches='tight')
plt.close()
print("3.2 c11_dagilim.png kaydedildi")
print("Bolum 3 tamamlandi.")
