import pandas as pd
import numpy as np

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v8.1.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v8.2.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir, {len(df.columns)} sutun")
print(f"Mevcut vld_genel: True={df['vld_genel'].sum()}, False={(df['vld_genel']==False).sum()}")

# vld_genel=True olan satirlarda C21 ve D21 ikisi birden null olanlar
true_mask = df['vld_genel'] == True
both_null = df['dane_m2_hesap_gram__C21'].isna() & df['dane_m2_gercek_gram__D21'].isna()
mask = true_mask & both_null

print(f"\nvld_genel=False yapilacak: {mask.sum()} satir")
print(df[mask]['dosya_adi__dosyaadi'].tolist())

df['vld_genel_neden'] = df['vld_genel_neden'].astype(str).replace('nan', '')
df.loc[mask, 'vld_genel'] = False
df.loc[mask, 'vld_genel_neden'] = (
    df.loc[mask, 'vld_genel_neden'].str.strip(' |') +
    ' | C21 ve D21 ikisi null (outlier analizi sonucu verim hesaplanamadi)'
)

print(f"\nGuncellendi: True={df['vld_genel'].sum()}, False={(df['vld_genel']==False).sum()}")

df.to_csv(DST, index=False, encoding='utf-8-sig')
print(f"Kaydedildi: {DST}")
