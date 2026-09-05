import pandas as pd

df = pd.read_csv(
    r'D:\_Development\Projects\UYSM_Project_2\yusuf_oguz_calismalari\data\processed\active\hansay_processed_v8.1.csv',
    encoding='utf-8-sig', low_memory=False)

true_df = df[df['vld_genel'] == True]
both_null = true_df['dane_m2_hesap_gram__C21'].isna() & true_df['dane_m2_gercek_gram__D21'].isna()
sub = true_df[both_null][['dosya_adi__dosyaadi', 'null_sayisi', 'kismi_not']]

print(f"C21 ve D21 ikisi birden null olan satir: {len(sub)}\n")
print(f"{'Dosya':<30} {'null':>4}  Temel neden")
print("-" * 90)
for _, row in sub.iterrows():
    n = str(row['kismi_not'])
    c11 = 'C11' in n
    c41 = 'c41_m2_norm' in n or ('C41' in n and 'null' in n.lower())
    c21_direct = 'C21' in n
    d21_direct = 'D21' in n

    if c11 and c41:
        neden = 'C11 + C41 null -> her iki verim hesaplanamadi'
    elif c11:
        neden = 'C11 null -> C12 null -> C21 null; C41 ile D21 de etkilendi'
    elif c41:
        neden = 'C41 null -> D21 null; C21 ayrica MAD/IQR ile null'
    elif c21_direct and d21_direct:
        neden = 'C21 + D21 dogrudan MAD/IQR ile null (ham veri saglam)'
    else:
        neden = 'diger'

    dosya = str(row['dosya_adi__dosyaadi'])
    print(f"{dosya:<30} {row['null_sayisi']:>4}  {neden}")
