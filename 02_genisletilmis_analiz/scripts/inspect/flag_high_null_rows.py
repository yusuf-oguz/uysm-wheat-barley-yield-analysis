import pandas as pd

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v8.0.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v8.1.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir, {len(df.columns)} sutun")

mask = df['null_sayisi'] >= 25
print(f"\nvld_genel=False yapilacak satirlar ({mask.sum()} adet):")
print(df[mask][['dosya_adi__dosyaadi', 'null_sayisi', 'kismi_not']].to_string())

df['vld_genel_neden'] = df['vld_genel_neden'].astype(str).replace('nan', '')
df.loc[mask, 'vld_genel'] = False
df.loc[mask, 'vld_genel_neden'] = df.loc[mask, 'vld_genel_neden'].str.strip(' |') + \
    ' | null_sayisi >= 25 (kopyalanmis/guvensiz veri)'

print(f"\nvld_genel dagilimi:")
print(df['vld_genel'].value_counts().to_string())

df.to_csv(DST, index=False, encoding='utf-8-sig')
print(f"\nKaydedildi: {DST}")
