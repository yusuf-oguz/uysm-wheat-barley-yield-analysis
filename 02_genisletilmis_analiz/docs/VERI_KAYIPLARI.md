# Veri Kayıpları — HANSAY Buğday Verisi

> **Uyarı:** Bu belgede bazı bilgiler hatalı veya eksik olabilir — elle yazılmış bir özettir, otomatik üretilmemiştir. Kesin bilgi için `data/processed/README.md` dosyasındaki versiyon tablosunu oku veya ilgili versiyonu `data/processed/active/` altında doğrudan incele.

**Başlangıç:** 769 xlsx dosyası — ham veri, hiçbir değer değiştirilmemiş  
**Bitiş:** `vAnaliz1.0.csv` — 617 satır, 104 sütun  
**Net satır kaybı:** 769 → 617 = **152 satır (%19.8)**

Bu belge her önemli kaybın hikayesini, nedenini ve hangi versiyonda gerçekleştiğini açıklar.  
Geriye dönmek için ilgili versiyonu `data/processed/active/` veya `archive/` altında bulabilirsin.

---

## Özet Tablo

| # | Kayıp Türü | Satır | Hücre | Versiyon | Geri Dönülebilir? |
|---|---|---|---|---|---|
| 1 | Belirsiz bitki adı filtresi | −39 satır | — | v2.1 | ✓ ham_full.csv |
| 2 | Koordinat geçersiz | −1 satır | — | v2.10 | ✓ v2.9 |
| 3 | dane_agirlik eksik (3+) | −2 satır | — | v3.7 | ✓ v3.6 |
| 4 | dane_sayisi eksik (3+) | −1 satır | — | v3.8 | ✓ v3.7 |
| 5 | sap_boy tutarsız (10/10) | −3 satır | — | v3.10 | ✓ v3.9 |
| 6 | C41 lab tartımı girilmemiş | −1 satır | — | v4.7 | ✓ v4.6 |
| 7 | Kopya satır tespiti (tam kopya) | −5 satır | — | v5.2 | ✓ v5.1 |
| 8 | Kopya satır tespiti (b1-b10 kopya) | −8 satır | — | v5.3 | ✓ v5.2 |
| 9 | Arpa filtresi + vld_genel=False birikimi | −91 satır (−75 arpa, −16 False) | — | v6.0 | ✓ v5.3 |
| 10 | b1-b10 kopyalanmış sap ölçümleri | 0 satır (null) | ~28 hücre/satır × 10 satır | v5.1 | ✓ kismi_not |
| 11 | b1-b10 outlier — sap (seri+IQR) | 0 satır | ~25 hücre | v6.5 | ✓ v6.0 |
| 12 | b1-b10 outlier — uzunluk | 0 satır | 8 hücre | v6.6 | ✓ v6.5 |
| 13 | b1-b10 outlier — agirlik | 0 satır | 32 hücre | v6.7 | ✓ v6.6 |
| 14 | b1-b10 outlier — dane_sayisi | 0 satır | 23 hücre | v6.8 | ✓ v6.7 |
| 15 | b1-b10 outlier — dane_agirlik | 0 satır | 72 hücre | v6.9 | ✓ v6.8 |
| 16 | C41 alan tartımı outlier (v7.x) | 0 satır | 6 hücre | v7.1–7.3 | ✓ v7.0 |
| 17 | b1-b10 Global IQR 3x | 0 satır | 15 hücre | v7.4 | ✓ v7.3 |
| 18 | b1-b10 Global MAD 3.5 | 0 satır | 130 hücre | v7.5 | ✓ v7.4 |
| 19 | C11/C41 Global IQR 3x | 0 satır | 1 hücre | v7.6 | ✓ v7.5 |
| 20 | C11/C41 Global MAD 3.5 | 0 satır | 44 hücre | v7.7 | ✓ v7.6 |
| 21 | Türetilmiş sütunlar IQR 3x | 0 satır | 21 hücre | v7.8 | ✓ v7.7 |
| 22 | Türetilmiş sütunlar MAD 3.5 | 0 satır | 68 hücre | v7.9 | ✓ v7.8 |
| 23 | null_sayisi ≥ 25 (kopyalanmış) | −9 satır | — | v8.1 | ✓ v8.0 |
| 24 | C21+D21 ikisi null (verim yok) | −13 satır | — | v8.2 | ✓ v8.1 |

---

## 1. Belirsiz Bitki Adı Filtresi — −39 Satır

**Versiyon:** `v2.1`  
**Hikaye:** Ham 769 satırda `bitki_adi__C9` sütunu normalizasyondan geçirildi (v1): tüm varyantlar `bugday` veya `arpa` olarak birleştirildi. v2.1'de bu iki kategori dışında kalan — boş, belirsiz veya başka bitki adı taşıyan — 39 satır elendi. **Arpa bu aşamada hâlâ veride kaldı.**  
**Kalan:** 730 satır (655 buğday + 75 arpa)

---

## 2. Koordinat Geçersiz — −1 Satır

**Versiyon:** `v2.10`  
**Hikaye:** `v2.7`'de GADM spatial join ile koordinat-il uyuşması kontrol edildi. 6 satır "False" çıktı. Bunların 5'i `v2.8`'de KMZ noktalarıyla düzeltildi. Kalan 1 satırın koordinatı KMZ'de de bulunamadı ve düzeltilemedi — `koordinat_gecerli=False` olarak işaretlendi, analizden çıkarıldı.  
**Etkilenen dosya:** `vld_koordinat=False` olan tek satır.

---

## 3–5. Eksik/Tutarsız Ölçüm Nedeniyle False — −6 Satır

**Versiyon:** `v3.7`, `v3.8`, `v3.10`

### dane_agirlik eksik 3+ — −2 satır (v3.7)
`4216 10km 622` ve `4208 50m 594` dosyalarında 10 başaktan 3 veya daha fazlasında dane ağırlığı ölçümü yoktu. 1-2 eksik olan satırlarda ortalama ile doldurma yapıldı, ama 3+ eksik güvenilmez kabul edildi.

### dane_sayisi eksik 3+ — −1 satır (v3.8)
`7008 611` dosyasında dane sayısı 3+ hücrede eksikti. Aynı kural.

### sap_boy tutarsız 10/10 — −3 satır (v3.10)
`0201 3.xlsx`, `0203 4.xlsx`, `0205 5.xlsx` dosyalarında J=H+I denklem kontrolünde 10 başağın tamamı tutarsız çıktı — muhtemelen veri girişinde satır kayması yaşanmış. Düzeltme mümkün olmadığından `vld_sap_boy=False` yapıldı.

---

## 6. C41 Lab Tartımı Girilmemiş — −1 Satır

**Versiyon:** `v4.7`  
**Hikaye:** `6305 140.xlsx` dosyasında C41 (ölçüm alanındaki başakların laboratuvar tartımı) hiç girilmemişti. Bu sütun D21 verim hesabının kaynağı olduğundan D21 güvenilmez hale geldi. `vld_genel=False` yapıldı.

---

## 7–8. Kopya Satır Tespiti — −13 Satır

**Versiyon:** `v5.2` (−5) ve `v5.3` (−8)

### v5.2 — Tam kopya satırlar (−5 satır)
74 ham ölçüm sütunu üzerinden satır-satır karşılaştırma yapıldı. 5 kopya çifti tespit edildi; her çiftte orijinal dosya belirlendi (rapor numarası, tarih vb. ile), kopya olan False yapıldı:
- `0109 50m 352` → orijinal `5106`
- `0614 350 668` → orijinal `669`
- `3602 250m 796` → orijinal `736`
- `8001 13` → orijinal `6310`
- `6804 istasyon(a) 560` → orijinal `561`

### v5.3 — b1-b10 düzeyinde kopya (−8 satır)
b1–b10 70 sütun üzerinden daha detaylı karşılaştırma. 5 yeni kopya çifti + 2 çift özel durum:
- `3103 741`, `4203 istasyon 588`, `7008 5km148` → orijinallerinden kopyalanmış, False
- `3503 2km 68` ve `3503 69`: C11/C41 farklı görünüyordu ama 10 başağın tüm ölçümleri birebir aynıydı — istatistiksel olarak imkânsız, **ikisi de** False yapıldı (2 satır)
- `6408 792`: kısmen kopya (uzunluk/ağırlık/dane kopyalanmış, sap farklı) → satır False yapılmadı, hücreler null, kismi_not ile işaretlendi. Bu satır ilerleyen aşamalarda null_sayisi ≥ 25 kuralıyla çıktı (bkz. #23).

---

## 9. Arpa Filtresi + Biriken False'lar — −91 Satır

**Versiyon:** `v6.0`  
**Hikaye:** `vld_genel=True` ve `bitki_adi=bugday` filtresi uygulandı. **Arpa bu versiyona kadar veride tutulmuştu** — v2.1'den bu yana koordinat, kopya, eksik ölçüm gibi kontroller hem buğday hem arpa satırları üzerinde yapıldı. v6.0'da arpa (75 satır) ve o ana kadar birikmiş vld_genel=False satırlar (yaklaşık 16 satır) birlikte düşürüldü. **Çalışma seti: 639 satır** (sadece buğday, vld_genel=True).

---

## 10. b1-b10 Kopyalanmış Sap Ölçümleri — Satır Kaybı Yok, Hücre Null

**Versiyon:** `v5.1`  
**Hikaye:** 10 satırda b1–b10 sap ölçümlerinin (sap_basak_boyu, sap_alt_cm, sap_boy_cm) tümü aynı değeri taşıyordu — bu biyolojik olarak imkânsız, kopyalama hatası. Satır dışarı atılmadı (`vld_genel=True` kaldı) ama ilgili 28 sütundaki ~280 hücre null yapıldı, `kismi_not` eklendi. Bu satırlar verim analizine girmeye devam etti; sadece sap ölçümleri güvenilmez.

---

## 11–15. b1-b10 Outlier Analizi (Seri İçi + Global IQR) — Satır Kaybı Yok

**Versiyon:** `v6.5` → `v6.9`

Her ölçüm tipi için 2 tur uygulandı: p1/p99 → seri içi MAD>10 → global IQR 3x. Satır dışarı atılmadı, yalnızca aykırı hücreler null yapıldı. Türetilmiş ortalamalar `mean(skipna=True)` ile güncellendi — null hücreler ortalamayı bozmaz, sadece böleni düşürür.

| Tip | Yöntem | Null hücre |
|---|---|---|
| sap (basak/alt/boy) | p1/p99 + MAD>10 + log-IQR 3x | ~25 |
| uzunluk | aynı | 8 |
| agirlik | aynı + ratio>5 | 32 |
| dane_sayisi | aynı + ratio>5 | 23 |
| dane_agirlik | aynı + ratio>5 | 72 |

**Not:** `ratio>5` kuralı — seri medyanının 5 katından küçük veya büyük değerler açıkça hata olarak kabul edildi.

---

## 16. C41 Alan Tartımı Outlier — 6 Hücre Null

**Versiyon:** `v7.1`, `v7.2`, `v7.3`

C41 (ölçüm alanındaki tüm başakların lab tartımı) farklı alan büyüklüklerinde (1/4, 1/8, 1/16 m²) toplanmıştı. Karşılaştırılabilirlik için `c41_m2_norm = C41 × E13` ile m² bazına normalize edildi.

- `v7.1`: `6309 23.xlsx` — C41=3.48M mg, log-IQR 3x ile null
- `v7.2`: 2 ek C41 null (C41 vs C11×C40 ilişki kontrolü)
- `v7.3`: `0902`, `3106`, `3102` — c41_m2_norm IQR 3x ile null (hepsi E13=16, norm değerleri 4.5–16.7M mg/m²)

C41 null olunca D21 zinciri (E41→E42→D21) de null oldu.

---

## 17–22. Global Outlier Analizi (IQR 3x + MAD 3.5) — Satır Kaybı Yok, Hücre Null

**Versiyon:** `v7.4` → `v7.9`

Önceki seri içi MAD'ın n=10 kısıtını telafi etmek için tüm popülasyon üzerinden iki aşamalı analiz:

**b1-b10 (70 ham sütun, ~6390 gözlem/tip):**
- IQR 3x (v7.4): 15 hücre null
- MAD 3.5 (v7.5): 130 hücre null — en büyük tek aşama kaybı

**C11 ve C41 (n=639):**
- IQR 3x (v7.6): 1 hücre null
- MAD 3.5 (v7.7): 44 hücre null (C11:31, C41:13)

**Türetilmiş sütunlar (n=639):**
- IQR 3x (v7.8): 21 hücre null
- MAD 3.5 (v7.9): 68 hücre null

**Toplam bu aşamada:** 279 hücre null.

**Not — Agresiflik riski:** MAD 3.5 eşiği standart olmakla birlikte, Tekirdağ gibi ulusal ortalamadan yüksek verimli bölgelerde gerçek ölçümleri de null yapmış olabilir. `5901 40km 568.xlsx` ve `5902 48km 562.xlsx` bu sebeple çok null aldı — ileriki çalışmalarda bölgesel MAD uygulaması değerlendirilebilir.

---

## 23. null_sayisi ≥ 25 — −9 Satır

**Versiyon:** `v8.1`

Tüm outlier analizleri tamamlandıktan sonra satır başına null sayısı hesaplandı. 25 veya daha fazla null taşıyan satırlar incelendi — tamamı zaten `kismi_not` içinde kopyalanmış veri olarak işaretliydi (b1-b10'un tümü aynı değer). Bunların analizde katkısı neredeyse sıfır, ancak null sayısı bu kadar yüksekken ortalama hesaplarına gürültü katar. `vld_genel=False` yapıldı.

Etkilenen dosyalar: `6408 792`, `2613 756`, `2601 787`, `2606 791`, `2603 789`, `6406 762`, `6403 786`, `6301 218`, `4303 754`

---

## 24. C21 ve D21 İkisi Birden Null — −13 Satır

**Versiyon:** `v8.2`

Outlier analizleri sonucunda hem C21 (başak sayısı bazlı verim) hem D21 (tartım bazlı verim) null olan 13 satır tespit edildi. Bu satırların temel kaybı:
- **C11 veya C41 null** olduğundan verim zinciri tamamen kopmuş
- veya **C21+D21 doğrudan MAD/IQR** ile popülasyondan çok yüksek bulunarak null yapılmış

İki verim sütununun da olmadığı satırlar analizin ana hedefine katkı yapamaz. `vld_genel=False` yapıldı.

Etkilenen dosyalar: `0101 2km 143`, `0103 3km 289`, `2715 366`, `3102 1.5km 194`, `3104 2km 173`, `3507 4.2km 105`, `4504 4.2km 73`, `4509 5 km 100`, `4703 800m 249`, `5901 40km 568`, `6309 23`, `6321 3km 134`, `6332 300m 141`

---

## Sonuç: Kalan Eksiklikler (vAnaliz1.0'da)

vAnaliz1.0'da 617 satır var, ancak bazı sütunlar kısmi null içeriyor:

| Sütun | Yaklaşık Null | Not |
|---|---|---|
| `dane_m2_hesap_gram__C21` | ~39 | C21 null ama D21 dolu satırlar — D21 ile analiz devam edebilir |
| `dane_m2_gercek_gram__D21` | ~9 | D21 null ama C21 dolu satırlar — C21 ile analiz devam edebilir |
| `olcum_basak_agirlik_ham__C41` | ~50+ | C41 null olan satırlarda D21 de null, zaten dışarıda |
| `ort_sap_basak_boyu__H39` vb. | ~10–30 | Sap ölçümleri bazı satırlarda kısmi — sap analizinde dikkat |
| `m2_sap_agirlik_kg__C17` | — | Kaynak C16/J41 v5.0'da çıkarıldığından güncelleme yapılamadı |

**Öneri:** Verim analizinde C21 ve D21'i ayrı ayrı değerlendirmek, her analiz için o sütunun dolu olduğu satırları kullanmak yeterli.

---

## Geri Dönüş Rehberi

| Nereye geri dönmek istiyorsun? | Kullanılacak versiyon |
|---|---|
| Tüm veriye dön (arpa + belirsiz bitki adları dahil) | `hansay_ham_full.csv` |
| Sadece buğday+arpa, belirsiz bitki adları çıkarılmış | `hansay_processed_v2.1.csv` |
| Outlier öncesi temiz başlangıç (sadece buğday, vld_genel=True) | `hansay_processed_v6.0.csv` |
| b1-b10 seri içi + IQR sonrası, global MAD öncesi | `hansay_processed_v7.3.csv` |
| Global outlier sonrası, satır eleme öncesi | `hansay_processed_v7.9.csv` |
| Sadece null_sayisi ≥ 25 elenmişler | `hansay_processed_v8.1.csv` |
| Her iki verim de null olanlar elenmişler | `hansay_processed_v8.2.csv` |
