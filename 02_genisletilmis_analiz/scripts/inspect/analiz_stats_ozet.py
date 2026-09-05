import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv(r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\vAnaliz1.0.csv', encoding='utf-8-sig', low_memory=False)

c21 = df['dane_m2_hesap_gram__C21'].dropna()
d21 = df['dane_m2_gercek_gram__D21'].dropna()
both = df[['dane_m2_hesap_gram__C21','dane_m2_gercek_gram__D21']].dropna()
r_cd, p_cd = stats.pearsonr(both.iloc[:,0], both.iloc[:,1])

grps = {e: df[df['olcum_alani_carpani__E13']==e]['dane_m2_hesap_gram__C21'].dropna() for e in [4,8,16]}
kw_h, kw_p = stats.kruskal(*[g.values for g in grps.values()])

both2 = df[['ort_basak_agirlik_mg__C40','dane_m2_hesap_gram__C21']].dropna()
r_bag, p_bag = stats.pearsonr(both2.iloc[:,0], both2.iloc[:,1])

d41 = df['basak_dane_oran__D41'].dropna()

ort = (both.iloc[:,0] + both.iloc[:,1]) / 2
fark = (both.iloc[:,0] - both.iloc[:,1]) / ort * 100

il_agg = df.groupby('il_koordinat_final').agg(
    sap=('ort_sap_boy_cm__J39','median'),
    c21=('dane_m2_hesap_gram__C21','median'),
    n=('dosya_adi__dosyaadi','count')
).dropna()
il_agg = il_agg[il_agg['n']>=5]
r_sap, p_sap = stats.pearsonr(il_agg['sap'], il_agg['c21'])

both3 = df[['ort_basak_agirlik_mg__C40','dane_m2_hesap_gram__C21']].dropna()
r_dane, p_dane = stats.pearsonr(
    df[['ort_dane_sayisi__D40','dane_m2_hesap_gram__C21']].dropna().iloc[:,0],
    df[['ort_dane_sayisi__D40','dane_m2_hesap_gram__C21']].dropna().iloc[:,1])

print(f"C21_med={c21.median():.1f} C21_mean={c21.mean():.1f} C21_std={c21.std():.1f} C21_skew={c21.skew():.2f}")
print(f"D21_med={d21.median():.1f} D21_mean={d21.mean():.1f} D21_std={d21.std():.1f} D21_skew={d21.skew():.2f}")
print(f"C21_D21_r={r_cd:.3f} p={p_cd:.2e} n={len(both)}")
print(f"fark_bias={fark.mean():.1f} loa_lo={fark.mean()-1.96*fark.std():.1f} loa_hi={fark.mean()+1.96*fark.std():.1f}")
print(f"E13_KW_H={kw_h:.2f} p={kw_p:.4f}")
print(f"E13_4_med={grps[4].median():.0f} E13_8_med={grps[8].median():.0f} E13_16_med={grps[16].median():.0f}")
print(f"bag_vs_c21_r={r_bag:.3f} p={p_bag:.2e}")
print(f"d41_gt1={int((d41>1).sum())} pct={100*(d41>1).mean():.1f}")
print(f"sap_vs_verim_r={r_sap:.3f} p={p_sap:.3f} n_il={len(il_agg)}")
print(f"dane_sayisi_vs_c21_r={r_dane:.3f} p={p_dane:.2e}")
