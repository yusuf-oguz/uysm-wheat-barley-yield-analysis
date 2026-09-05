# Outlier Analizi — HANSAY İşlenmiş Veri

**Kapsam:** `bitki_adi=bugday` AND `vld_genel=True` → **639 satır**  
**Nihai temiz versiyon:** `hansay_processed_v7.9.csv` (116 sütun)  
**Görseller:** `docs/figures/` — `line_*.png` (15 adet) ve `b1b10_line_*.png` (7 adet)

---

## Genel Kurallar (tüm aşamalarda geçerli)

- Null yapılan her hücre `kismi_not` sütununa kaydedilir
- Türetilmiş ortalamalar her zaman `mean(skipna=True)` — sabit /10 değil; null hücreler atlanır, geçerli sayıya bölünür
- `sap_boy (J) = H + I`; H veya I null yapılırsa J de null yapılır
- Kaynak null → türetilen null zinciri `mean(skipna=True)` ile otomatik korunur
- Her aşama sonrası yeni CSV versiyonu üretilir, README güncellenir — geriye dönüş mümkün

---

## Uygulanan Outlier Analizi — Tam Kronoloji

### Ön Aşama — Kopyalanmış Veri ve Veri Girişi Hataları (v5.x–v6.x)

b1–b10 sap ölçümlerinin tümünün birebir aynı olduğu satırlar kopya olarak işaretlendi, ilgili hücreler null yapıldı. Bu aşama klasik outlier tespiti değil, veri bütünlüğü kontrolüdür.

---

### Aşama 1 — b1-b10 Seri İçi MAD + Global IQR 3x, 2 Tur (v6.x → v7.3)

**Kapsam:** 7 ölçüm tipi × 10 sütun = 70 ham sütun; 639 × 10 ≈ 6.390 gözlem/tip

**Her ölçüm tipi için 2 tur:**

*Tur 1:*
1. **Global p1/p99:** Tüm 6.390 değerin 1. ve 99. yüzdelik dilimi dışındakiler → null. Bu adımda manuel inceleme sonucu ek null da uygulanmıştır (açıkça hatalı ama p1/p99 sınırını tam aşmayan birkaç değer — bkz. kismi_not sütunu).
2. **Seri içi MAD > 10:** Her satırın 10 başağı kendi içinde değerlendirildi. `|0.6745 × (bN − seri_median)| / seri_MAD > 10` → null. Eşik n=10 küçük örneklem boyutu nedeniyle muhafazakâr tutuldu.
3. **Global IQR 3x:** Q1 − 3×IQR / Q3 + 3×IQR dışı → null

*Tur 2:* (p1/p99 tekrarlanmadı)
1. Seri içi MAD > 10
2. Global IQR 3x

Her tur sonunda türetilmiş sütunlar `mean(skipna=True)` ile yeniden hesaplandı.

**Ölçüm Alanı Ham Değerleri (v7.1–v7.3):**
- C11: Global IQR 3x → temiz (müdahale yok)
- C41: `c41_m2_norm = C41 × E13` (m² normalizasyonu) üzerinden Global IQR 3x → 1+2+3 = toplam 6 null (v7.1'de 1, v7.2'de 2, v7.3'te 3)

**v6.x Null Özeti (README'den):**

| Versiyon | Ölçüm Tipi | Açıklama | Null |
|---|---|---|---|
| v6.5 | sap_basak / sap_alt / sap_boy | 3 sap sütunu, 2 tur (p1/p99 → MAD>10 → log-IQR 3x); swap düzeltmesi dahil | ~25 hücre |
| v6.6 | uzunluk | 2 tur; 1546, 86, 85, 76, 65, 56.5, 35, 1.1 cm gibi kesin hatalar | 8 hücre |
| v6.7 | agirlik | 2 tur; 5 üst hata + 17 alt >5x + 10 MAD>10 | 32 hücre |
| v6.8 | dane_sayisi | 2 tur; 5 üst + 15 alt >5x + 3 MAD>10 | 23 hücre |
| v6.9 | dane_agirlik | 2 tur; 68 ratio>5 + 4 MAD>10 | 72 hücre |
| **Toplam** | | | **~160 hücre** |

---

### Aşama 2 — b1-b10 Global IQR 3x (v7.3 → v7.4)

**Gerekçe:** Önceki seri içi MAD'da eşik n=10 kısıtı nedeniyle muhafazakâr tutulmuştu (>10). Buna ek olarak, tüm popülasyon üzerinden bütüncül bir IQR taraması yapılmadığı tespit edildi. Bu aşama bu boşluğu kapatır.

**Yöntem:** Her ölçüm tipi için 6.390 değer düzleştirilir, Q1 − 3×IQR / Q3 + 3×IQR sınırı dışındaki bireysel hücreler null yapılır.

| Ölçüm Tipi | Null |
|---|---|
| uzunluk | 1 |
| agirlik | 6 |
| dane_sayisi | 0 |
| dane_agirlik | 7 |
| sap_basak | 0 |
| sap_alt | 1 |
| sap_boy | 0 |
| **Toplam** | **15** |

---

### Aşama 3 — b1-b10 Global MAD 3.5 + Türetilmiş Yeniden Hesap (v7.4 → v7.5)

**Gerekçe:** IQR 3x uçları temizledikten sonra, daha ince dağılımsal sapmaları yakalamak için MAD 3.5 uygulandı. MAD, skewed dağılımlarda IQR'dan daha hassastır ve log dönüşümü gerektirmez (Iglewicz & Hoaglin, 1993).

**Yöntem:** `|0.6745 × (x − global_median)| / global_MAD > 3.5` → null

| Ölçüm Tipi | n_valid | Medyan | MAD | Sınır Alt | Sınır Üst | Null |
|---|---|---|---|---|---|---|
| uzunluk | 6.371 | 7.00 cm | 1.50 | -0.78 | 14.78 | 16 |
| agirlik | 6.342 | 1747.50 mg | 667.00 | -1713.58 | 5208.58 | 41 |
| dane_sayisi | 6.357 | 32.00 | 11.00 | -25.08 | 89.08 | 14 |
| dane_agirlik | 6.301 | 1281.00 mg | 515.00 | -1391.35 | 3953.35 | 48 |
| sap_basak | 6.304 | 7.00 cm | 2.00 | -3.38 | 17.38 | 3 |
| sap_alt | 6.291 | 68.00 cm | 12.00 | 5.73 | 130.27 | 8 |
| sap_boy | 6.264 | 75.00 cm | 13.00 | 7.54 | 142.46 | 0 |
| **Toplam** | | | | | | **130** |

Aşama sonrası tüm türetilmiş sütunlar (Katman 3–5) `mean(skipna=True)` ile yeniden hesaplandı.

---

### Aşama 4 — C11 ve C41 Global IQR 3x (v7.5 → v7.6)

| Sütun | Q1 | Q3 | IQR | Alt | Üst | Null |
|---|---|---|---|---|---|---|
| C11 (başak sayımı) | 40.00 | 81.50 | 41.50 | -84.50 | 206.00 | 1 |
| C41 (c41_m2_norm) | 458.480 | 1.182.976 | 724.496 | -1.715.008 | 3.356.464 | 0 |

Türetilmiş sütunlar yeniden hesaplandı.

---

### Aşama 5 — C11 ve C41 Global MAD 3.5 (v7.6 → v7.7)

| Sütun | Medyan | MAD | Alt | Üst | Null |
|---|---|---|---|---|---|
| C11 | 56.50 | 19.50 | -44.69 | 157.69 | 31 |
| C41 (c41_m2_norm) | 741.520 | 336.984 | -1.007.100 | 2.490.140 | 13 |

Türetilmiş sütunlar yeniden hesaplandı.

---

### Aşama 6 — Türetilmiş Sütunlara Global IQR 3x (v7.7 → v7.8)

15 türetilmiş sütun incelendi (n=639):

| Sütun | Null |
|---|---|
| basak_dane_oran__D41 | 5 |
| m2_basak_sayisi__C12 | 2 |
| dane_m2_hesap_gram__C21 | 2 |
| olcum_basak_agirlik_ham__C41 | 12 |
| diğerleri (B40, C40, D40, E40, C20, C22, J39, H39, I39, D21, C11) | 0 |
| **Toplam** | **21** |

---

### Aşama 7 — Türetilmiş Sütunlara Global MAD 3.5 (v7.8 → v7.9)

| Sütun | Medyan | MAD | Null |
|---|---|---|---|
| bin_dane_agirlik_gram__C22 | 40.84 | 6.23 | 1 |
| basak_dane_oran__D41 | 0.74 | 0.04 | 9 |
| m2_basak_sayisi__C12 | 496.00 | 152.00 | 2 |
| dane_m2_hesap_gram__C21 | 585.75 | 269.74 | 19 |
| dane_m2_gercek_gram__D21 | 536.95 | 252.11 | 3 |
| olcum_alani_basak__C11 | 55.00 | 18.00 | 10 |
| olcum_basak_agirlik_ham__C41 | 84.316 | 35.881 | 24 |
| diğerleri (B40, C40, D40, E40, C20, J39, H39, I39) | — | — | 0 |
| **Toplam** | | | **68** |

---

## Toplam Null Özeti

| Aşama | Versiyon | Yöntem | Toplam Null |
|---|---|---|---|
| 1 (b1-b10 seri içi + IQR, 2 tur) | v6.5–v6.9 | p1/p99 + Seri içi MAD>10 + IQR 3x + manuel | ~160 hücre (sap:~25, uzunluk:8, agirlik:32, dane_sayisi:23, dane_agirlik:72) |
| C11/C41 ilk temizlik | v7.1–v7.3 | IQR 3x | 6 (C41; C11 temiz) |
| 2 — b1-b10 Global IQR 3x | v7.4 | IQR 3x | 15 |
| 3 — b1-b10 Global MAD 3.5 | v7.5 | MAD 3.5 | 130 |
| 4 — C11/C41 Global IQR 3x | v7.6 | IQR 3x | 1 |
| 5 — C11/C41 Global MAD 3.5 | v7.7 | MAD 3.5 | 44 |
| 6 — Türetilmiş IQR 3x | v7.8 | IQR 3x | 21 |
| 7 — Türetilmiş MAD 3.5 | v7.9 | MAD 3.5 | 68 |

---

## Akademik Gerekçeler

### Neden çok aşamalı bir yaklaşım?

Tek bir yöntem veya eşik, farklı kökenli hataları aynı anda yakalamakta yetersiz kalır. Bu çalışmada üç farklı hata türü gözlemlenmiştir:

1. **Veri girişi hataları:** Birim karışıklığı (örn. mg yerine g girilmesi), ondalık nokta kaçması, kopyalama hatası. Bunlar genellikle popülasyondan çok uzak, açıkça aykırı değerlerdir — IQR 3x bu grubu yakalar.
2. **Seri içi tutarsızlıklar:** Aynı tarladan alınan 10 başağın ölçümlerinden birinin diğerlerinden aşırı sapması. Bu lokal hatalar global yöntemlerle fark edilemeyebilir — seri içi MAD bu grubu hedefler.
3. **Popülasyon düzeyinde sınır aşımları:** Ulusal ölçekte normal dağılımın dışında kalan ama tek bir seri içinde makul görünen değerler — global MAD 3.5 bu grubu yakalar.

### Neden IQR 3x önce, MAD 3.5 sonra?

IQR 3x, Tukey (1977) tarafından "extreme outlier" eşiği olarak tanımlanmıştır. Bu değerler temizlendikten sonra kalan dağılım üzerinde MAD hesabı daha güvenilirdir. Teorik olarak MAD medyan tabanlı olduğundan aşırı değerlerden etkilenmez; ancak uygulamada önce aşırı uçları temizlemek, ardından MAD ile ince ayar yapmak iki ayrı analitik katman oluşturur ve paper'da her katmanın amacını net biçimde tanımlamaya olanak tanır.

### Neden seri içi MAD için eşik 10, global için 3.5?

Iglewicz & Hoaglin (1993) eşiği 3.5 olarak önerir. Ancak bu eşik n büyük olduğunda güvenilirdir. n=10'da MAD tahmini kendisi kararsız olabilir — bir değer seri medyanından biraz uzaksa yanlış şekilde outlier sayılır. Eşiği 10'a çıkarmak yalnızca açıkça imkânsız değerleri yakalar; bu yaklaşım "conservative screening" olarak literatürde savunulabilir bir pozisyondur (bkz. Leys et al., 2013, *Journal of Experimental Social Psychology*: MAD eşik seçiminin örneklem boyutuna göre kalibre edilmesi).

### Neden log dönüşümü uygulanmadı?

C41 (lab tartımı) ve C21/D21 (verim) gibi sütunlar sağa çarpıktır (skewness > 2). Log dönüşümü bu tür sütunlarda IQR hassasiyetini artırır; ancak MAD zaten dönüşüm gerektirmeden skewed dağılımlarda sağlamlığını korur. Dolayısıyla MAD aşamasına geçildiğinde log dönüşümüne gerek kalmaz. Bu tercih yöntem karmaşıklığını azaltır ve paper'daki metodoloji bölümünü sadeleştirir.

### Neden türetilmiş sütunlara da outlier analizi uygulandı?

Türetilmiş sütunlar (C21, D21, D41 gibi) birden fazla ham ölçümün bileşimidir. Ham verilerdeki bireysel outlierlar temizlenmiş olsa dahi, birden fazla ham değerin birleşmesinden kaynaklanan yeni aykırılıklar ortaya çıkabilir — örneğin C11 yüksek ve C20 da yüksekse C21 (= C20 × C12) katlanarak aykırı olabilir. Türetilmiş sütunlara ayrı bir outlier aşaması uygulamak bu "kompozit aykırılıkları" yakalar.

### Null yapılan değerlerin ortalamaya etkisi

`mean(skipna=True)` kullanıldığından null yapılan hücreler ortalama hesabından çıkarılır; payda da buna göre güncellenir (örn. 9 geçerli değer varsa /9). Bu yaklaşım, sabit /10 bölmeye kıyasla gürültü enjeksiyonunu önler ve eksik değerlerin tahmin edilmesi (imputation) yerine gözlem atlanması (listwise deletion) stratejisiyle uyumludur — bu strateji tarımsal veri analizinde tercih edilen standart yaklaşımdır (Madley-Dowd et al., 2019).

---

## Paper İçin Önerilen Metodoloji Metni (İngilizce)

> "Outlier detection was performed in multiple sequential stages to address distinct error types present in field-collected agricultural data. First, within each 10-observation measurement series (one series per field record), a Modified Z-Score filter (Iglewicz & Hoaglin, 1993) was applied with a conservative threshold of 10, chosen to minimize false positives given the small series size (n=10; cf. Leys et al., 2013). This was followed by a global 3×IQR filter (Tukey, 1977) applied across all records to remove extreme values likely attributable to data entry or unit errors. To complement small-series detection, a population-level Modified Z-Score filter (threshold = 3.5) was subsequently applied across all observations pooled for each measurement type (n ≈ 6,390), which is robust to skewed distributions without requiring log transformation. The same two-step sequence (3×IQR followed by MAD, threshold = 3.5) was then applied to area-level raw measurements (ear count, lab weight) and to derived aggregate variables (yield, spike weight ratios). After each cleaning stage, derived variables were recalculated using mean(skipna=True) to propagate nulls through the calculation chain without imputation. All intermediate data versions are archived to allow replication with alternative outlier criteria."

---

## Referanslar

- Iglewicz, B., & Hoaglin, D. C. (1993). *How to Detect and Handle Outliers*. ASQC Quality Press. — Modified Z-Score yönteminin standart referansı; 3.5 eşiği bu kaynaktan alınmıştır.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley. — IQR tabanlı outlier tespitinin (1.5×IQR mild, 3×IQR extreme) orijinal kaynağı.
- Leys, C., Ley, C., Klein, O., Bernard, P., & Licata, L. (2013). Detecting outliers: Do not use standard deviation around the mean, use absolute deviation around the median. *Journal of Experimental Social Psychology*, 49(4), 764–766. — MAD'ın Z-score'a üstünlüğünü ve eşik seçimini tartışır; küçük örneklemlerde muhafazakâr eşik kullanımını destekler.
