import pandas as pd

SRC = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v7.9.csv'
DST = r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v8.0.csv'

df = pd.read_csv(SRC, encoding='utf-8-sig', low_memory=False)
print(f"Yuklendi: {len(df)} satir, {len(df.columns)} sutun")

# Meta/kimlik sutunlari null sayimina dahil edilmez
meta_cols = {'dosya_adi__dosyaadi', 'kismi_not', 'bitki_adi__C9', 'sulama_tipi__G6',
             'fenolojik_evre__G9', 'rapor_no__C8'}
vld_cols   = {c for c in df.columns if c.startswith('vld_')}
koord_cols = {c for c in df.columns if any(c.startswith(p) for p in
              ('il_', 'koordinat', 'enlem', 'boylam', 'kmz_', 'istasyon'))}

skip = meta_cols | vld_cols | koord_cols
olcum_cols = [c for c in df.columns if c not in skip]
print(f"Null sayimina dahil edilen sutun sayisi: {len(olcum_cols)}")

df['null_sayisi'] = df[olcum_cols].isnull().sum(axis=1)

# kismi_not'tan hemen sonra yerlestir
cols = list(df.columns)
cols.remove('null_sayisi')
ins = cols.index('kismi_not') + 1
cols.insert(ins, 'null_sayisi')
df = df[cols]

print("null_sayisi dagilimi:")
print(df['null_sayisi'].value_counts().sort_index().head(25).to_string())

max_idx = df['null_sayisi'].idxmax()
print(f"\nEn cok null: {df['null_sayisi'].max()} — {df.at[max_idx, 'dosya_adi__dosyaadi']}")
print(f"Hic null olmayan satir: {(df['null_sayisi'] == 0).sum()}")
print(f"Median null: {df['null_sayisi'].median()}")

df.to_csv(DST, index=False, encoding='utf-8-sig')
print(f"\nKaydedildi: {DST}")
print(f"Sutun sayisi: {len(df.columns)}")
