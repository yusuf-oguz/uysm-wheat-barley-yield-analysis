# UYSM Projesi — Excel Dosya Yapısı Rehberi

**Hazırlayan:** Yusuf Oguz  
**Analiz desteği:** Claude + Python  
**Güncelleme:** 2026-04-01

Bu belge, `UYSM-EXECELL HESAPLAMALARI 0-300 DOSYA` klasöründeki xlsx
dosyalarının iç yapısını, her hücrenin ne anlama geldiğini ve hücreler
arasındaki hesap ilişkilerini açıklar. Tüm satır numaraları Excel'in
kendi 1-tabanlı numaralandırmasıdır.

---

## 1. Genel Yapı

Her dosya tek bir istasyonun tek bir ölçüm gününe ait verilerini içerir.
Dosya adı genel olarak `[il_kodu][istasyon_no] [uzaklık] [rapor_no].xlsx`
formatındadır. Sayfa aktif (ilk) sayfadır.

---

## 2. Tanımlayıcı Bilgiler (Üst Bölüm)

| Hücre | İçerik | Not |
|-------|--------|-----|
| **E3** | Enlem (ham tam sayı) | Örnek: `3643467` → `36.43467°N` |
| **E4** | Boylam (ham tam sayı) | Örnek: `3515000` → `35.15000°E` |
| **D3** | "Enlem" etiketi | Hücrenin ne olduğunu doğrulamak için okunur |
| **J4** | Rapor no | Bazı dosyalarda J1'de olabilir |
| **C5** | Tarih | Ölçüm tarihi |
| **C6** | İstasyon no | Örnek: `16.03` → il kodu 16 (Bursa), istasyon 3 |
| **C9** | Bitki adı | `bugday`, `buğday`, `arpa` vb. |
| **C10** | Çeşit adı | Buğday/arpa çeşidi |

### Koordinat Dönüşümü

Ham değer `raw_int` iken ondalık dereceye çevrim:

```
decimal = raw_int / 10^(len(raw_int) - 2)
```

Örnekler:
- `3643467` → 7 basamak → `3643467 / 10^5` = `36.43467`
- `35150` → 5 basamak → `35150 / 10^3` = `35.150`
- `37435578` → 8 basamak → `37435578 / 10^6` = `37.435578`

---

## 3. Ölçüm Parametreleri

| Hücre | İçerik | Detay |
|-------|--------|-------|
| **C11** | 1/4 m² başak sayısı | Tarlada 1/4 m²'de sayılan başak adedi |
| **C12** | 1 m² başak sayısı | = C11 × ölçek faktörü (E13) |
| **E13** | Ölçek faktörü | `4` → 50×50 cm kare, `16` → 25×25 cm kare |

Çoğunlukla ölçek faktörü **4**'tür (50×50 cm). Örnek:
- C11 = 144, E13 = 16 → C12 = 144 × 16 = 2304 başak/m²

> **Uyarı:** C12'deki çarpım sonucu bazı dosyalarda tutarsız çıkmıştır.
> C11 ile E13'ten doğrudan hesaplamak daha güvenlidir.

---

## 4. Bireysel Başak Ölçümleri (Satırlar 29–38)

Her satır = 1 başak (toplam 10 başak protokolü, bazı dosyalarda 9 dolu)

| Sütun | İçerik | Birim | Kullanım |
|-------|--------|-------|----------|
| **A** | Başak etiketi | — | Tanımlayıcı, hesapta kullanılmaz |
| **B** | — | — | Çoğu dosyada boş veya formül |
| **C** | Kılçıklı ağırlık | mg | Başak + kavuz + kılçık dahil toplam ağırlık |
| **D** | — | — | Mevcut ama hiçbir hesapta kullanılmamış; içeriği belirlenemedi |
| **E** | Dane ağırlığı | mg | Sadece tane (kavuz ve kılçık çıkartılmış) ağırlık |

**Önemli:** Satır 38 (10. başak) bazen C ve D sütunları boş, yalnızca
E dolu olabilir (bkz. `01118 6 .xlsx`). Bu, kılçıklı tartımın yapılmadığı
ancak dane tartımının yapıldığı anlamına gelir.

---

## 5. Satır 39 — Toplamlar

| Hücre | İçerik | Olması gereken formül |
|-------|--------|-----------------------|
| **E39** | E29:E38 toplamı (dane mg toplamı) | `=SUM(E29:E38)` |
| **C39** | C29:C38 toplamı (kılçıklı mg toplamı) | `=SUM(C29:C38)` |

> **Bilinen hata:** 12 dosyada E39 hücresi `=SUM(...)` yerine sabit `948`
> değeri içerir. Bu değer `0103` şablonundan kopyalanırken oluşan bir hatadır.
> Bu dosyalar `duzeltilmis` statüsünde ham veriden yeniden hesaplanmıştır.
> Ayrıntılar: `HATALI_VERILER.txt` Bölüm 1A.

---

## 6. Tarla Tartımı

| Hücre | İçerik | Detay |
|-------|--------|-------|
| **C41** | Tarladan tartılan toplam ağırlık | Ölçüm karesinden toplanan tüm başakların kılçıklı ağırlığı (mg?) |

C41, GERÇEK dane ağırlığı hesabında kullanılır (bkz. Bölüm 7.2).

---

## 7. Sonuç Hücreleri — 1 m² Dane Ağırlığı (Satır 21)

CSV'de `xls_hesap_gram` ve `xls_gercek_gram` olarak tutulur.

| Hücre | CSV sütunu | Yöntem |
|-------|------------|--------|
| **C21** | `xls_hesap_gram` | HESAP yöntemi |
| **D21** | `xls_gercek_gram` | GERÇEK yöntemi |

Etiket: "1 m2 de toplanan" satırında aranır.

### 7.1 HESAP Yöntemi (C21)

Başak sayımına dayalı teorik hesap:

```
HESAP = (ort_dane_mg / 1000) × (1/4_m2_basak_sayisi) × olcek_faktoru

Açılımı:
  ort_dane_mg  = E29:E38 ortalaması  (mg/başak)
  / 1000       = mg → gram dönüşümü
  × C11        = 1/4 m²'deki başak adedini çarp
  × E13        = 1 m²'ye ölçekle (4 veya 16)
```

> Sonuç: gram / m²

### 7.2 GERÇEK Yöntemi (D21)

Tarladan tartılan ağırlığa dayalı ampirik hesap:

```
GERÇEK = C41 × (ort_dane_mg / ort_kilcikli_mg) × olcek_faktoru / 1000

Açılımı:
  C41                          = tarladan tartılan kılçıklı toplam ağırlık (mg)
  ort_dane_mg / ort_kilcikli_mg = dane / kılçıklı oranı  (E ort / C ort)
  × E13                         = 1 m²'ye ölçekle
  / 1000                        = mg → gram
```

> Sonuç: gram / m²

**Hangi değeri kullanmak?**  
HESAP yöntemi başak sayma hatasına duyarlıdır (C12 tutarsızlıkları).
GERÇEK yöntemi tartıma dayalıdır ve daha güvenilir kabul edilmektedir.
Bu nedenle analizde **`duzeltilmis_gercek_gram`** sütunu tercih edilir.

---

## 8. Ortalama Boy Ölçümleri

| Hücre | CSV sütunu | İçerik |
|-------|------------|--------|
| **C23** | `ortalama_bitki_boyu_cm` | Bitkinin (sap dahil) ortalama boyu, cm |
| **C24** | `ortalama_basak_boyu_cm` | Başağın ortalama uzunluğu, cm |

---

## 9. CSV Sütunları ile Excel Hücreleri Eşleştirmesi

| CSV Sütunu | Excel Hücresi | Açıklama |
|------------|---------------|----------|
| `enlem_raw` | E3 | Ham enlem (tam sayı) |
| `boylam_raw` | E4 | Ham boylam (tam sayı) |
| `enlem` | — | E3'ten dönüştürülmüş ondalık derece |
| `boylam` | — | E4'ten dönüştürülmüş ondalık derece |
| `rapor_no` | J4 (veya J1) | Dosya rapor numarası |
| `istasyon_no` | C6 | İstasyon kodu (il.istasyon) |
| `tarih` | C5 | Ölçüm tarihi |
| `bitki_adi` | C9 | Bitki türü |
| `cesit_adi` | C10 | Çeşit adı |
| `m2_basak_sayisi` | C12 | 1 m² başak sayısı |
| `xls_hesap_gram` | C21 | Spreadsheet'in hesapladığı dane ağırlığı (HESAP) |
| `xls_gercek_gram` | D21 | Spreadsheet'in hesapladığı dane ağırlığı (GERÇEK) |
| `duzeltilmis_hesap_gram` | — | Ham veriden (E29:E38) yeniden hesaplandı |
| `duzeltilmis_gercek_gram` | — | Ham veriden (C29:C38, E29:E38, C41) yeniden hesaplandı |
| `ortalama_bitki_boyu_cm` | C23 | Bitki boyu (cm) |
| `ortalama_basak_boyu_cm` | C24 | Başak boyu (cm) |

---

## 10. Hata ve Uyarı Notları

| Sorun | Etkilenen dosya sayısı | Referans |
|-------|----------------------|----------|
| E39 = 948 sabit (şablon hatası) | 12 (+3 koordinat dışı) | HATALI_VERILER Bölüm 1A |
| 9 başak verisi (10 yerine) | 8 | HATALI_VERILER Bölüm 1C |
| İstasyon kodu muhtemelen yanlış | 2 (`3507`, `0905`) | HATALI_VERILER Bölüm 5A |
| Koordinat/istasyon uyumsuz (uzak il) | 2 (`0104`, `6333`) | HATALI_VERILER Bölüm 5B |
| 10. başak C/D boş, E dolu | 1 (`01118 6`) | HATALI_VERILER Bölüm 1B |
